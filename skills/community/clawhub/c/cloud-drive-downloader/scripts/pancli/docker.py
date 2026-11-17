#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pan-downloader — Docker/NAS 安装文件、连通性检查、Range 分片下载子模块。"""
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


import shutil
import signal
import subprocess
import time
from datetime import datetime
from pathlib import Path

# 所有共享工具函数从 engine 懒加载（engine 在文件末尾 import 本模块，避免循环引用）。
from pancli.engine import *  # noqa: F401,F403
from pancli.report import _signal_group, _terminate_group  # noqa: F401

DOCKER_FILES = {
    "Dockerfile": (
        "FROM python:3.11-slim\n"
        "RUN apt-get update && apt-get install -y --no-install-recommends \\\n"
        "      curl aria2 ca-certificates openssh-client ffmpeg tini \\\n"
        "      && pip install --no-cache-dir yt-dlp \\\n"
        "      && apt-get clean && rm -rf /var/lib/apt/lists/*\n"
        "WORKDIR /app\n"
        "COPY scripts/ scripts/\n"
        "COPY config.example.json .\n"
        "RUN useradd -m -r -s /usr/sbin/nologin pan && mkdir -p /data/download /data/state && \\\n"
        "      chown -R pan:pan /app /data\n"
        "USER pan\n"
        "ENV PAN_CONFIG=/data/state/config.json PAN_STATE_DIR=/data/state \\\n"
        "    PAN_LOG=/data/state/pan.log\n"
        "EXPOSE 17890\n"
        "ENTRYPOINT [\"tini\", \"--\", \"python3\", \"scripts/pan.py\"]\n"
        "CMD [\"serve\", \"--host\", \"0.0.0.0\", \"--port\", \"17890\"]\n"
    ),
    "docker-compose.yml": (
        "services:\n"
        "  pandownloader:\n"
        "    image: lis/cloud-drive-downloader:0.14.1\n"
        "    container_name: pan-downloader\n"
        "    restart: unless-stopped\n"
        "    ports:\n"
        "      - \"${PAN_WEB_PORT:-17890}:17890\"\n"
        "    volumes:\n"
        "      - ${PAN_STATE_DIR:-./state}:/data/state\n"
        "      - ${PAN_DOWNLOAD_DIR:-./download}:/data/download\n"
        "    # 需要时在新设备上执行：PAN_WEB_PORT=8901 bash install.sh\n"
    ),
    "install.sh": (
        "#!/bin/sh\n"
        "# pan-downloader skill Docker 安装脚本（NAS/服务器/本机通用）\n"
        "set -e\n"
        "DIR=\"$(CDPATH= cd -- \"$(dirname -- \"$0\")\" && pwd)\"\n"
        "cd \"$DIR\"\n"
        "PAN_WEB_PORT=\"${PAN_WEB_PORT:-17890}\"\n"
        "port_free() { ! (command -v nc >/dev/null 2>&1 && nc -z 127.0.0.1 \"$1\" >/dev/null 2>&1); }\n"
        "while ! port_free \"$PAN_WEB_PORT\"; do PAN_WEB_PORT=$((PAN_WEB_PORT + 1)); done\n"
        "export PAN_WEB_PORT\n"
        "if ! command -v docker >/dev/null 2>&1; then\n"
        "  echo '❌ 未安装 Docker，请先安装 Docker/Container Manager' >&2\n"
        "  exit 1\n"
        "fi\n"
        "mkdir -p \"${PAN_STATE_DIR:-$DIR/state}\" \"${PAN_DOWNLOAD_DIR:-$DIR/download}\"\n"
        "docker compose up -d --build\n"
        "IP=\"${PAN_PUBLIC_HOST:-$(ip route get 1 2>/dev/null | awk '{print $7; exit}' || true)}\"\n"
        "[ -z \"$IP\" ] && IP=\"127.0.0.1\"\n"
        "echo \"✅ Web UI: http://$IP:$PAN_WEB_PORT/\"\n"
        "echo \"✅ API: http://$IP:$PAN_WEB_PORT/api/status\"\n"
        "echo '浏览器插件请填写上面的 Web/API 地址。'\n"
    ),
    "README-Docker.md": (
        "# 网盘通 Skill · Docker/NAS 部署\n\n"
        "- 镜像基于 python:3.11-slim，内置 curl、aria2、yt-dlp、ffmpeg、ssh 客户端。\n"
        "- 暴露 17890 端口（serve Web UI / 下载接口），配置与任务状态存 ./state，下载文件落 ./download。\n"
        "- 本容器不包含、不上传本机 config.json / Cookie / Token；请在容器内重新配置登录态。\n"
        "- 群晖：套件中心装 Container Manager → 本目录 `docker compose up -d`；威联通/飞牛/TrueNAS 同理。\n\n"
        "```bash\n"
        "bash install.sh\n"
        "```\n"
    ),
}


def docker_assets_dir():
    d = SKILL_DIR / "docker"
    return d


def cmd_search_check(cfg=None, kind="auto", timeout=20, json_flag=False):
    """检查各搜索源连通性（真实尝试抓取最小探测页），供本机回归确认。"""
    cfg = cfg or load_config()
    results = []
    probes = [
        ("archive", "https://archive.org/advancedsearch.php?q=test&rows=1&fl[]=identifier&output=json", lambda: None),
        ("duckduckgo", "https://html.duckduckgo.com/html/?q=test", lambda: None),
        ("ytdlp", "", lambda: find_engine_binary("ytdlp", cfg)),
    ]
    for key, url, ready in probes:
        try:
            if key == "ytdlp":
                ok = bool(ready())
                note = "yt-dlp 已找到" if ok else "未安装 yt-dlp"
                results.append({"provider": key, "ok": ok, "note": note})
                continue
            if not url:
                results.append({"provider": key, "ok": False, "note": "无探测地址"})
                continue
            from pancli import search_movie as _sm
            data = _sm.fetch_url(url, timeout=timeout, cfg=cfg)
            ok = bool(data)
            results.append({"provider": key, "ok": ok, "note": "抓取 %d 字节" % len(data)})
        except Exception as exc:
            results.append({"provider": key, "ok": False, "note": str(exc)[:160]})
    all_ok = all(r["ok"] for r in results)
    if json_flag:
        print(json.dumps({"ok": all_ok, "kind": kind, "results": results}, ensure_ascii=False, indent=2))
    else:
        print("搜索源连通性检查（kind=%s）：" % kind)
        for r in results:
            mark = "✓" if r["ok"] else "✗"
            print("  %s %-12s %s" % (mark, r["provider"], r["note"]))
        if not all_ok:
            print()
            print("提示：部分源未连通。archive/duckduckgo 需能访问外网；ytdlp 需已安装 yt-dlp。")
            print("本机回归：pan search \"关键词\" --check")
    return 0 if all_ok else 2


def docker_runtime_available():
    for name in ("docker", "podman"):
        found = shutil.which(name)
        if found:
            return name, found
    return None, ""


def cmd_docker_check(json_flag=False):
    """离线检查 docker 可用性与生成文件是否完整（不要求实际启动容器）。"""
    out = {"ok": True, "docker": None, "bin": "", "files": [], "issues": []}
    name, found = docker_runtime_available()
    out["docker"], out["bin"] = name, found
    if not found:
        out["ok"] = False
        out["issues"].append("本机未检测到 docker/podman；容器安装需在 NAS/装有 Docker 的主机上执行 bash install.sh")
    d = Path(getattr(cmd_docker, "_last_out", None) or SKILL_DIR / "docker")
    expected = {k: (["FROM python:3.11-slim", "aria2", "yt-dlp"] if k == "Dockerfile" else
                    (["docker", "compose", "up"] if k == "install.sh" else
                     (["services", "17890"] if k == "docker-compose.yml" else []))) for k in DOCKER_FILES}
    for name, tokens in expected.items():
        fp = d / name
        if not fp.exists():
            out["ok"] = False
            out["issues"].append("缺少文件 %s" % name)
            continue
        out["files"].append(str(fp))
        text = fp.read_text(encoding="utf-8")
        for tok in tokens:
            if tok not in text:
                out["ok"] = False
                out["issues"].append("%s 缺少关键内容 %r" % (name, tok))
    if json_flag:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("Docker/NAS 检查：")
        print("  docker 运行时：%s" % (out["bin"] or "未找到 docker/podman"))
        print("  文件数：%d" % len(out["files"]))
        for issue in out["issues"]:
            print("  - %s" % issue)
        if out["ok"]:
            print("  ✅ 本机可用的 Docker 文件完整；实际容器启动请在装有 Docker 的 NAS 执行 bash install.sh")
        else:
            print("  ⚠️ 存在待处理项：%d 项" % len(out["issues"]))
    return 0 if out["ok"] else 2


def cmd_docker(args):
    """生成/检查 Docker(NAS) 运行文件；不执行系统级安装，只落地脚本与说明。"""
    scope = getattr(args, "docker_cmd", "files") or "files"
    out_dir = Path(getattr(args, "out", None) or SKILL_DIR / "docker")
    if scope in ("check", "doctor", "verify"):
        import types as _t
        cmd_docker._last_out = str(out_dir)
        return cmd_docker_check(json_flag=bool(getattr(args, "json", False)))
    if scope == "files":
        out_dir.mkdir(parents=True, exist_ok=True)
        for name, text in DOCKER_FILES.items():
            (out_dir / name).write_text(text, encoding="utf-8")
        if getattr(args, "json", False):
            print(json.dumps({"ok": True, "scope": scope, "dir": str(out_dir),
                              "files": [str(f) for f in sorted(out_dir.iterdir())] if out_dir.exists() else []},
                             ensure_ascii=False, indent=2))
        else:
            print("已生成 Docker/NAS 安装文件：%s" % out_dir)
            for f in sorted(out_dir.iterdir()):
                print("  - %s" % f)
        return 0
    print("docker 子命令：files（生成 Docker 文件到 --out 目录）| check（检测本机 docker 可用性与生成文件完整性）。部署走 pan remote deploy。")
    return 1


def cmd_probe(args):
    """测速候选直链并排序（不下载到目标目录）。"""
    cfg = load_config()
    timeout = int(getattr(args, "timeout", 6) or 6)
    samples = int(getattr(args, "samples", 200000) or 200000)
    urls = [getattr(args, "url", None)] or []
    if getattr(args, "candidates", None):
        urls += [c.strip() for c in args.candidates.split(",") if c.strip()]
    if isinstance(urls, str):
        urls = [urls]
    urls = [u for u in urls if u]
    if not urls:
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": "缺少候选链接"}, ensure_ascii=False, indent=2))
        else:
            print("❌ 缺少候选链接：pan probe <url1> [--candidates url2,url3]")
        return 1
    ranked = rank_fastest_urls(urls, cfg=cfg, timeout=timeout, samples=samples)
    if getattr(args, "json", False):
        print(json.dumps({"ok": True, "samples": samples, "timeout": timeout, "results": ranked},
                          ensure_ascii=False, indent=2))
        return 0
    print("候选链接测速（按从快到慢，样本 %d 字节）：" % samples)
    for i, r in enumerate(ranked, start=1):
        if r.get("ok"):
            print("  %d. %8.1f KB/s  %s" % (i, r.get("kbps", 0), r.get("url", "")))
        else:
            print("  %d. 失败 %s  %s" % (i, r.get("error", ""), r.get("url", "")))
    fast = next((r for r in ranked if r.get("ok")), None)
    if fast:
        print("最快：%s（%.1f KB/s）" % (fast.get("url", ""), fast.get("kbps", 0)))
    return 0


def run_curl_split(url, target_path, split, cfg, emit_events=False, live=None, task_control=None):
    """http 直链单文件 Range 分片下载；服务端不支持时返回 (None, [], 说明) 回退整文件。

    v0.20.0（F1）三项增强：
      - 并发池：同时在跑的分片数受 http.split_max_concurrency（默认 4）约束，
        跑完一段补一段，不再 N 段一次性全起（避免触发服务端连接数风控）；
      - 分片级复用：.partNN 已存在且字节数等于该段应有大小 → 直接跳过（segment_reuse）；
        不完整则整段重下（curl 拒绝把 -C - 与 -r 组合，半成品续传不可行，故整段重下）；
      - 单段重试：某段失败时单独重试 1 次（--retry 只管连接级错误）。
    http.split_limit_rate 非空时透传 curl --limit-rate。
    """
    length, accept_ranges = probe_http_range(url)
    if not length or not accept_ranges or length < 2:
        return None, [], "服务端不支持可探测的 Range/Content-Length，回退整文件下载"
    n = min(int(split), length)
    if n < 2:
        return None, [], "分片数不足，回退整文件下载"
    http = cfg.get("http", {})
    timeout = int(http.get("connect_timeout", 30) or 30)
    retries = str(http.get("retries", 3))
    delay = str(http.get("retry_delay", 5))
    try:
        pool_size = max(1, int(http.get("split_max_concurrency", 4) or 4))
    except (TypeError, ValueError):
        pool_size = 4
    limit_rate = str(http.get("split_limit_rate") or "").strip()
    base = length // n

    # 计算各段区间与期望大小
    segments = []  # (index, start, end, part_path, expected_size)
    for i in range(n):
        start = base * i
        end = (base * (i + 1) - 1) if i < n - 1 else (length - 1)
        part = Path(str(target_path) + ".part%02d" % i)
        segments.append((i, start, end, part, end - start + 1))

    def _emit(event):
        if emit_events:
            print(json.dumps(event, ensure_ascii=False), flush=True)

    def _note_step(text):
        if live is not None:
            live.set_step(text)
        if task_control is not None:
            task_control.set_step(text)

    def _argv(start, end, part):
        argv = ["curl", "-L", "--fail", "--retry", retries, "--retry-delay", delay,
                "--connect-timeout", str(timeout), "-r", "%d-%d" % (start, end),
                "-o", str(part), url]
        if limit_rate:
            argv[1:1] = ["--limit-rate", limit_rate]
        return argv

    results = {}
    for i, start, end, part, expected in segments:
        results[i] = {"index": i + 1, "engine": "curl-split", "note": "Range %d-%d" % (start, end),
                      "argv": mask_argv(_argv(start, end, part)), "uses_stdin_credential": False,
                      "started": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
                      "rc": -1, "elapsed": 0.0, "error": "", "reused": False}

    started = time.time()
    pending = list(segments)
    running = []   # (i, start, end, part, proc)
    cancelled = False
    paused = False
    retried = set()
    spawn_error = None

    while (pending or running) and not cancelled:
        # 任务级暂停：SIGSTOP 全部在跑段，恢复时 SIGCONT（不往池里补新段）
        if task_control is not None:
            state = task_control.read_state()
            if state == "paused" and not paused:
                paused = True
                for _i, _s, _e, _p, _pr in running:
                    if _pr.poll() is None:
                        _signal_group(_pr, signal.SIGSTOP)
            elif state != "paused" and paused:
                paused = False
                for _i, _s, _e, _p, _pr in running:
                    if _pr.poll() is None:
                        _signal_group(_pr, signal.SIGCONT)
            if state == "cancelled":
                cancelled = True
                for _i, _s, _e, _p, _pr in running:
                    if _pr.poll() is None:
                        _terminate_group(_pr)
                break

        # 填满并发池（复用检查在启动前：完整 .part 直接跳过）
        if not paused:
            while pending and len(running) < pool_size:
                i, start, end, part, expected = pending.pop(0)
                if part.exists() and part.stat().st_size == expected:
                    results[i]["rc"] = 0
                    results[i]["reused"] = True
                    _emit({"event": "segment_reuse", "index": i + 1, "range": "%d-%d" % (start, end)})
                    continue
                if part.exists():
                    # 半成品：curl 拒绝 -C - 与 -r 组合，无法段内续传，整段重下
                    try:
                        part.unlink()
                    except OSError:
                        pass
                try:
                    _note_step(results[i]["note"])
                    _emit({"event": "segment_start", "index": i + 1, "range": "%d-%d" % (start, end)})
                    proc = subprocess.Popen(_argv(start, end, part), stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL,
                                            start_new_session=bool(task_control is not None))
                except OSError as exc:
                    results[i]["rc"] = 127
                    results[i]["error"] = str(exc)
                    spawn_error = "无法启动 curl：%s" % exc
                    break
                running.append((i, start, end, part, proc))
            if spawn_error:
                break

        # 非阻塞轮询在跑的进程
        still = []
        for (i, start, end, part, proc) in running:
            rc = proc.poll()
            if rc is None:
                still.append((i, start, end, part, proc))
                continue
            results[i]["rc"] = rc
            results[i]["elapsed"] = round(time.time() - started, 2)
            _emit({"event": "segment_done", "index": i + 1, "range": "%d-%d" % (start, end), "rc": rc})
            size = part.stat().st_size if part.exists() else 0
            if rc == 0 and size == end - start + 1:
                continue  # 本段成功
            # 失败段：单独重试一次
            if i not in retried:
                retried.add(i)
                results[i]["error"] = "segment exit=%s size=%s，重试" % (rc, size)
                pending.append((i, start, end, part, end - start + 1))
            else:
                results[i]["error"] = "segment exit=%s size=%s（重试后仍失败）" % (rc, size)
        running = still
        if not running and not pending:
            break
        time.sleep(0.2)

    if cancelled:
        return 130, [results[i] for i in sorted(results)], "任务已取消"
    if spawn_error:
        return 127, [results[i] for i in sorted(results)], spawn_error

    # 段完整性终检（复用段 rc 已置 0）
    failed = None
    for i, start, end, part, expected in segments:
        size = part.stat().st_size if part.exists() else 0
        if results[i]["rc"] != 0 or size != expected:
            if failed is None:
                failed = (i, results[i]["rc"], size, expected)
    if failed is not None:
        i, rc, size, expected = failed
        return rc or 127, [results[i] for i in sorted(results)], \
            "分片下载失败（第 %s 段 exit=%s size=%s expected=%s）" % (i + 1, rc, size, expected)

    try:
        with Path(target_path).open("wb") as out:
            for i, start, end, part, expected in segments:
                with part.open("rb") as pin:
                    shutil.copyfileobj(pin, out)
                try:
                    part.unlink()
                except OSError:
                    pass
    except OSError as exc:
        return 127, [results[i] for i in sorted(results)], "合并写文件失败：%s" % exc
    size = Path(target_path).stat().st_size if Path(target_path).exists() else 0
    if size != length:
        return 127, [results[i] for i in sorted(results)], "合并字节数校验失败 expected=%s actual=%s" % (length, size)
    reused_n = sum(1 for i in results if results[i].get("reused"))
    note = "Range 分片下载完成（%sB，%s 段" % (length, n)
    if reused_n:
        note += "，复用 %d 段" % reused_n
    note += "）"
    return 0, [results[i] for i in sorted(results)], note




