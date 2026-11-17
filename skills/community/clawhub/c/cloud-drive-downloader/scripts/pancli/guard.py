"""网盘通 · 后台守护 / 限速识别 / ETA 预估（v0.16.0）

本模块把 2026-10-15 两次实测的教训固化成可执行规则：

1. 后台常驻必须"双 fork + setsid"，不能用 `nohup ... &`：
   实测 nohup+disown 起的下载进程会在调用方退出时被回收，任务静默死掉。
2. 限速要能识别并如实汇报：
   同一批文件实测 30–120 KB/s，而本机 OVH/Cloudflare 单连接 1.9–5.2 MB/s，
   出口 IP 是用户真实公网 IP → 瓶颈在网盘侧账号限速，不是本机/沙箱。
3. 失败要分类，不能把"限速/风控/未登录"混为一谈：
   login_required / throttle / dlink_missing / captcha / not_found / disk_full。
"""

from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_here = _boot_os.path.dirname(_boot_os.path.abspath(__file__))
    _boot_parent = _boot_os.path.dirname(_boot_here)
    for _boot_dir in (_boot_here, _boot_parent):
        if _boot_dir not in _boot_sys.path:
            _boot_sys.path.insert(0, _boot_dir)
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from pancli import tasklock as _tl


def human_size(n: float) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    v = float(n or 0)
    for u in units:
        if abs(v) < 1024 or u == units[-1]:
            return "%.2f%s" % (v, u)
        v /= 1024.0
    return "%.2fTB" % (v,)


def human_speed(bps: float) -> str:
    return human_size(bps) + "/s"


def human_eta(seconds: Optional[float]) -> str:
    if seconds is None or seconds <= 0:
        return "未知"
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h >= 24:
        return "%d天%02d小时" % (h // 24, h % 24)
    if h:
        return "%d小时%02d分" % (h, m)
    if m:
        return "%d分%02d秒" % (m, s)
    return "%d秒" % s


# --------------------------------------------------------------- 守护化
def daemonize(nochdir: bool = False) -> None:
    """双 fork + setsid 守护化；必须在真正干活前调用。"""
    if os.fork() > 0:
        os._exit(0)
    os.setsid()
    if os.fork() > 0:
        os._exit(0)
    if not nochdir:
        try:
            os.chdir("/")
        except Exception:
            pass
    devnull = os.open(os.devnull, os.O_RDWR)
    os.dup2(devnull, 0)
    os.dup2(devnull, 1)
    os.dup2(devnull, 2)
    try:
        os.close(devnull)
    except Exception:
        pass


def spawn_daemon(argv: List[str], *, log_path: str = "") -> int:
    """守护化启动 argv；返回父进程看到的中间 pid（真正 pid 写入 log）。"""
    if not argv:
        raise ValueError("spawn_daemon 需要 argv")
    pid = os.fork()
    if pid > 0:
        os.waitpid(pid, 0)
        return pid
    daemonize()
    if log_path:
        try:
            Path(log_path).parent.mkdir(parents=True, exist_ok=True)
            fd = os.open(log_path, os.O_CREAT | os.O_WRONLY | os.O_APPEND)
            os.dup2(fd, 1)
            os.dup2(fd, 2)
        except Exception:
            pass
    os.execv(argv[0], argv)
    os._exit(127)


# --------------------------------------------------------------- 限速/ETA
def measure_throughput(target: str, seconds: int = 20) -> Dict[str, Any]:
    """采样 target 目录的真实占用增量，估算吞吐与 ETA。"""
    root = Path(target)
    if not root.exists():
        return {"ok": False, "error": "目标目录不存在：%s" % target}
    def size_of() -> int:
        total = 0
        for p in root.rglob("*"):
            try:
                if p.is_file() and not p.name.endswith(".BaiduPCS-Go-downloading"):
                    st = p.stat()
                    total += st.st_blocks * 512 if hasattr(st, "st_blocks") else st.st_size
            except Exception:
                continue
        return total
    start = size_of()
    time.sleep(max(1, int(seconds)))
    end = size_of()
    delta = max(0, end - start)
    bps = delta / float(max(1, int(seconds)))
    return {"ok": True, "seconds": int(seconds), "start_bytes": start, "end_bytes": end,
            "delta_bytes": delta, "bytes_per_sec": bps, "speed": human_speed(bps)}


def eta_for(total_bytes: float, bytes_per_sec: float) -> Optional[float]:
    if not bytes_per_sec or bytes_per_sec <= 0:
        return None
    return float(total_bytes) / float(bytes_per_sec)


THROTTLE_KBPS = 200.0  # 低于该吞吐一律按"网盘侧限速/免费账号"如实提示


def throttle_hint(bps: float, drive: str = "") -> str:
    kb = bps / 1024.0
    if bps <= 0:
        return "当前无进展：可能被网盘限速到 0、登录态失效或连接被中断；先跑 `pan guard status` 看锁与进程。"
    if kb < THROTTLE_KBPS:
        name = {"baidu": "百度网盘", "quark": "夸克", "aliyun": "阿里云盘"}.get(drive, drive or "该网盘")
        return ("实测 %.0f KB/s，低于 %d KB/s 阈值：%s免费账号限速的典型特征（本机网络本身通常有 MB/s 级）。"
                "不破解限速；如可接受，开会员是唯一合法提速途径。" % (kb, int(THROTTLE_KBPS), name))
    return "实测 %.0f KB/s，未触发限速判定。" % kb


# --------------------------------------------------------------- 错误分类
ERROR_RULES: List[Tuple[str, str, str]] = [
    ("login_required", "未登录", "未登录或登录态失效：跑 `pan login <网盘> --qr` 走统一扫码入口，不要用临时脚本直连登录接口。"),
    ("login_required", "登录", "未登录或登录态失效：跑 `pan login <网盘> --qr` 走统一扫码入口，不要用临时脚本直连登录接口。"),
    ("login_required", "BDUSS", "登录态失效：重新 `pan login <网盘> --qr`。"),
    ("dlink_missing", "未返回下载直链", "官方接口未给直链：先把分享转存到自己网盘，再走 baidupcs 引擎下载。"),
    ("dlink_missing", "dlink_missing", "未拿到官方直链：确认已登录且分享未过期，必要时先转存到自己网盘。"),
    ("captcha", "验证码", "官方要求验证码：请人工在官方网页完成验证，工具不破解验证码。"),
    ("risk_control", "风控", "触发官方风控：等一段时间再用官方网页会话重试，不要高频重试。"),
    ("not_found", "不存在", "文件或分享不存在/已失效，请核对链接与提取码。"),
    ("disk_full", "空间不足", "本地磁盘空间不足，清理后重试；断点会保留。"),
    ("throttle", "限速", "网盘侧限速：如实报告，不绕过；可选会员提速或耐心等待。"),
    ("http_403", "403", "服务器返回 403：多为登录态过期/无权限/直链失效；重新登录后重跑，断点会续传。"),
]


def classify_error(text: str) -> Dict[str, str]:
    """把原始错误文本归类成统一错误码 + 处置建议。"""
    raw = str(text or "")
    for code, needle, fix in ERROR_RULES:
        if needle in raw:
            return {"code": code, "raw": raw[:200], "remediation": fix}
    if "超时" in raw or "timeout" in raw.lower():
        return {"code": "timeout", "raw": raw[:200], "remediation": "超时：网络慢或文件大；重跑会断点续传，不要加 --ow。"}
    return {"code": "unknown", "raw": raw[:200], "remediation": "按原始错误排查；重跑会断点续传。"}


# --------------------------------------------------------------- CLI
def _print(obj: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(obj, ensure_ascii=False, indent=2))
    else:
        if isinstance(obj, str):
            print(obj)
        else:
            for k, v in obj.items():
                print("%s: %s" % (k, v))


def cmd_guard(args) -> int:
    action = getattr(args, "action", None) or "status"
    as_json = bool(getattr(args, "json", False))

    if action in ("locks", "status"):
        locks = _tl.active_locks()
        if as_json:
            print(json.dumps({"locks": locks, "lock_dir": str(_tl.lock_dir())}, ensure_ascii=False, indent=2))
            return 0
        if not locks:
            print("没有活动的下载锁（单实例空闲）")
            print("锁目录：%s" % _tl.lock_dir())
            return 0
        print("当前下载锁（同一来源只允许一个进程）：")
        for rec in locks:
            print("  %s  drive=%s  运行中=%s  pid=%s  开始=%s" % (
                rec.get("key"), rec.get("drive"), (not rec.get("stale")), rec.get("pid"), rec.get("started")))
            print("     来源：%s" % rec.get("source"))
            print("     目标：%s" % rec.get("target"))
        return 0

    if action == "clean":
        removed = _tl.cleanup_stale()
        if as_json:
            print(json.dumps({"removed": removed}, ensure_ascii=False, indent=2))
        else:
            print("已清理陈旧锁 %d 个：%s" % (len(removed), ", ".join(removed) or "无"))
        return 0

    if action == "speed":
        target = getattr(args, "target", "") or ""
        if not target:
            print("需要 --target <下载目录>")
            return 2
        res = measure_throughput(target, int(getattr(args, "seconds", 20) or 20))
        if not res.get("ok"):
            print("❌ %s" % res.get("error"))
            return 1
        hint = throttle_hint(res["bytes_per_sec"], getattr(args, "drive", "") or "")
        res["hint"] = hint
        if as_json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print("采样 %ss：%s → %s，增量 %s" % (res["seconds"], human_size(res["start_bytes"]),
                                                 human_size(res["end_bytes"]), human_size(res["delta_bytes"])))
            print("实测速度：%s" % res["speed"])
            print("提示：%s" % hint)
        return 0

    if action == "eta":
        total = float(getattr(args, "total", 0) or 0)
        bps = float(getattr(args, "bps", 0) or 0)
        eta = eta_for(total, bps)
        obj = {"total_bytes": total, "bytes_per_sec": bps, "eta_seconds": eta, "eta": human_eta(eta)}
        _print(obj, as_json)
        return 0

    if action == "daemon":
        cmd = getattr(args, "cmd", "") or ""
        if not cmd:
            print("需要 --cmd '<要后台执行的命令>'")
            return 2
        log_path = getattr(args, "log", "") or ""
        argv = ["/bin/zsh", "-lc", cmd]
        pid = spawn_daemon(argv, log_path=log_path)
        obj = {"daemon_started": True, "launcher_pid": pid, "cmd": cmd, "log": log_path,
               "note": "双 fork + setsid 守护化；不会随调用方退出被回收"}
        _print(obj, as_json)
        return 0

    if action == "error":
        obj = classify_error(getattr(args, "text", "") or "")
        _print(obj, as_json)
        return 0

    print("未知动作：%s（可选 locks/status/clean/speed/eta/daemon/error）" % action)
    return 2
