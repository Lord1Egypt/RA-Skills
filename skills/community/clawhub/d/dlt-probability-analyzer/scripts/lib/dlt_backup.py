# -*- coding: utf-8 -*-
"""
大乐透系统 · 灾难恢复备份 (Disaster Recovery Backup)
=====================================================

把"四体系统"当前的**可恢复状态**一次性快照到 timestamped 目录,
换机 / WorkBuddy 重装 / 误删后, 用 dlt_restore.py 可在 ~10 分钟内复活:

  1. Windows 排程任务 DLT_V8_Smart 的 XML (schtasks /query /xml ONE, 可 /create 还原)
  2. 6 个离线兜底数据 JSON + 关键状态文件(预测产物/健康度历史/增强报告)
  3. 代码清单 + 版本标签 (模型版 V8.9.7 / 包版 2.1.x) 的 manifest

产物目录: backups/<YYYYMMDD_HHMMSS>/
           + 同目录 DLT_backup_<ts>.zip (整体压缩, 便于拷到新机)

用法
----
  python dlt_backup.py              # 执行备份 + 压缩 + 自动轮转(保留最近10份)
  python dlt_backup.py --dry       # 只报告会备份哪些, 不写盘
  python dlt_backup.py --max 20    # 保留最近 20 份(默认 10)

注意: 这是运维脚本, 不依赖网络, 不影响任何运行中的排程任务。
"""
import sys
import os
import io
import re
import json
import shutil
import subprocess
import datetime

# 强制 UTF-8 输出(Windows 默认 GBK, 打印中文/✅会崩溃)
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
# 顶层目录(lib/ 的父级): dlt_run_v8.bat / SKILL.md / README.md 等顶层文件所在处。
SCRIPTS_DIR = os.path.dirname(WORK_DIR)
BACKUP_ROOT = os.path.join(WORK_DIR, "backups")
TASK_NAME = "DLT_V8_Smart"
PYTHON = sys.executable

# 离线兜底数据(与 package_dlt_skill / build_dist 白名单同源)
DATA_FILES = [
    "dlt_history.json",
    "dlt_valid_combos.json",
    "dlt_expert_picks.json",
    "dlt_power_baseline.json",
    "dlt_winner_stats.json",
    "dlt_data_source.json",
]
# 关键状态文件(预测产物/健康度/报告)
STATE_FILES = [
    "dlt_recommended_periods.json",
    "dlt_power_report.json",
    "health_history.csv",
    "health_latest.json",
    "dlt_watchdog_status.txt",
]

KEEP_DEFAULT = 10


def _ts():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def _read_version():
    """读模型版(bat)与包版(SKILL.md)。

    路径修正(2026-08-07): dlt_run_v8.bat 位于 lib/ 的**父级**(Root 顶层 / SKILL 包 scripts/),
    旧代码只在 WORK_DIR(=lib/) 找 → 恒不存在, 被 except 吞掉后静默返回 None,
    备份元数据永久丢失模型版本号。现改为顶层优先、lib/ 兜底。
    """
    model_ver = None
    _bat = os.path.join(SCRIPTS_DIR, "dlt_run_v8.bat")
    if not os.path.exists(_bat):
        _bat = os.path.join(WORK_DIR, "dlt_run_v8.bat")
    try:
        for line in open(_bat, encoding="utf-8"):
            if line.strip().startswith("REM") and "V8." in line:
                # 用正则精确截取版本号。旧写法 split()[0].rstrip(".123456789") 在
                # "大乐透V8.9.7智能预测" 这类**中文紧邻版本号**时会停在中文边界,
                # 解析出 "V8.9.7智能预测"(脏值)。该缺陷此前被上游路径错误(文件读不到)
                # 长期掩盖, 修好路径后才暴露。
                m = re.search(r"V(\d+(?:\.\d+)+)", line)
                model_ver = "V" + m.group(1) if m else None
                break
    except Exception:
        pass
    pkg_ver = None
    try:
        # SKILL.md 候选: lib/ → 顶层(scripts/) → 其父(SKILL 包根) → 用户级 skills 目录
        sk = None
        for _c in (os.path.join(WORK_DIR, "SKILL.md"),
                   os.path.join(SCRIPTS_DIR, "SKILL.md"),
                   os.path.join(os.path.dirname(SCRIPTS_DIR), "SKILL.md"),
                   # Root 部署下 SKILL.md 不在工程内, 位于用户级 skills 目录:
                   os.path.join(os.path.expanduser("~"), ".workbuddy", "skills",
                                "dlt-probability-analyzer", "SKILL.md")):
            if os.path.exists(_c):
                sk = _c
                break
        if sk is None:
            raise FileNotFoundError("SKILL.md not found in any candidate path")
        txt = open(sk, encoding="utf-8").read()
        m = re.search(r"(?:version|版本)[^\d]{0,12}(\d+\.\d+\.\d+)", txt, re.I)
        if m:
            pkg_ver = m.group(1)
    except Exception:
        pass
    return model_ver, pkg_ver


def export_task(dest):
    """导出 DLT_V8_Smart 排程 XML。返回 (ok, detail)。"""
    if os.name != "nt":
        return False, "非 Windows 平台, 跳过排程导出(schtasks 不可用)"
    try:
        xml_path = os.path.join(dest, f"{TASK_NAME}.xml")
        # 注意: 本机 schtasks 无 /export 参数, 用 /query /xml ONE 导出
        r = subprocess.run(
            ["schtasks", "/query", "/tn", TASK_NAME, "/xml", "ONE"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30,
        )
        raw = r.stdout or b""
        if r.returncode != 0 or len(raw) < 50:
            err = (r.stderr or b"").decode("gbk", errors="replace")
            return False, f"schtasks 导出失败(rc={r.returncode}): {err[:120]}"
        # 输出可能是 UTF-16(带 BOM), 统一转 UTF-8 落盘, 便于 /create 还原
        if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
            text = raw.decode("utf-16", errors="replace")
        else:
            text = raw.decode("gbk", errors="replace")
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(text)
        return True, f"排程任务 {TASK_NAME}.xml 已导出 ({len(text)} 字符)"
    except Exception as e:
        return False, f"排程导出异常: {type(e).__name__}: {e}"


def snapshot_files(dest, dry):
    """快照数据 + 状态文件。返回 (copied_list, missing_list)。"""
    copied, missing = [], []
    combined = [(f, "data") for f in DATA_FILES] + [(f, "state") for f in STATE_FILES]
    for fname, kind in combined:
        src = os.path.join(WORK_DIR, fname)
        if os.path.exists(src):
            copied.append(fname)
            if not dry:
                shutil.copy2(src, os.path.join(dest, fname))
        else:
            missing.append(fname)
    return copied, missing


def rotate(keep):
    """删除 backups/ 下最旧的, 仅保留最近 keep 份(含目录与对应 zip)。"""
    if not os.path.isdir(BACKUP_ROOT):
        return []
    entries = sorted(
        [d for d in os.listdir(BACKUP_ROOT) if d[:8].isdigit()],
        reverse=True,
    )
    removed = []
    for old in entries[keep:]:
        p = os.path.join(BACKUP_ROOT, old)
        try:
            if os.path.isdir(p):
                shutil.rmtree(p)
            else:
                os.remove(p)
            removed.append(old)
        except Exception:
            pass
    return removed


def main():
    args = sys.argv[1:]
    dry = "--dry" in args
    keep = KEEP_DEFAULT
    for i, a in enumerate(args):
        if a == "--max" and i + 1 < len(args):
            try:
                keep = int(args[i + 1])
            except Exception:
                pass

    print("=" * 64)
    print("  大乐透系统 · 灾难恢复备份")
    print(f"  时间: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
    print("=" * 64)
    if dry:
        print("  [DRY-RUN] 仅报告, 不写盘")

    ts = _ts()
    dest = os.path.join(BACKUP_ROOT, ts)
    zip_path = os.path.join(BACKUP_ROOT, f"DLT_backup_{ts}.zip")

    model_ver, pkg_ver = _read_version()
    print(f"\n  版本: 模型={model_ver or '未知'}  包={pkg_ver or '未知'}")

    # 1) 导出排程
    print("\n[1/3] 导出 Windows 排程任务")
    if not dry:
        os.makedirs(dest, exist_ok=True)
    ok, detail = export_task(dest)
    print(f"    {'✅' if ok else '⚠️'} {detail}")

    # 2) 快照文件
    print("\n[2/3] 快照数据与状态文件")
    copied, missing = snapshot_files(dest, dry)
    print(f"    ✅ 已备份 {len(copied)} 个文件:")
    for f in copied:
        print(f"       - {f}")
    if missing:
        print(f"    ⚠️ 不存在(跳过) {len(missing)} 个:")
        for f in missing:
            print(f"       - {f}")

    # 3) manifest + zip + 轮转
    print("\n[3/3] 写 manifest + 压缩 + 轮转")
    manifest = {
        "created": datetime.datetime.now().isoformat(timespec="seconds"),
        "model_version": model_ver,
        "package_version": pkg_ver,
        "task_name": TASK_NAME,
        "task_exported": ok,
        "data_files": copied,
        "missing_files": missing,
        "restore_cmd": "python dlt_restore.py " + ts,
    }
    if not dry:
        with open(os.path.join(dest, "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        # 压缩(目录 -> zip), 便于拷到新机
        import zipfile
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(dest):
                for fn in files:
                    fp = os.path.join(root, fn)
                    z.write(fp, os.path.relpath(fp, BACKUP_ROOT))
        removed = rotate(keep)
        print(f"    ✅ 备份目录: {dest}")
        print(f"    ✅ 压缩包:   {zip_path}")
        if removed:
            print(f"    ✅ 已轮转清理最旧 {len(removed)} 份")
    else:
        print(f"    (dry) 将创建: {dest}")
        print(f"    (dry) 将压缩: {zip_path}")

    print("\n" + "=" * 64)
    if dry:
        print("  DRY-RUN 完成, 未做任何改动")
    else:
        print(f"  备份完成 ✅  还原命令: python dlt_restore.py {ts}")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
