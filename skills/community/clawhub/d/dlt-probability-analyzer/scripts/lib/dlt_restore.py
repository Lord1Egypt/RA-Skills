# -*- coding: utf-8 -*-
"""
大乐透系统 · 灾难恢复还原 (Disaster Recovery Restore)
======================================================

从 dlt_backup.py 生成的备份中复活"四体系统":

  1. 还原 Windows 排程任务 DLT_V8_Smart (schtasks /create /xml, 需管理员)
  2. 还原 6 个离线兜底数据 + 关键状态文件 到工作区
  3. 调 build_dist.py 重新同步四体(Root->SKILL副本->dist zip)

典型场景: 换机 / WorkBuddy 重装 / 误删数据后, 把 DLT_backup_<ts>.zip
解压到工作区, 跑本脚本即可 ~10 分钟复活。

用法
----
  python dlt_restore.py                 # 还原最新一份备份(默认 dry-run)
  python dlt_restore.py 20260805_162800# 还原指定时间戳目录
  python dlt_restore.py --force        # 真正写盘(默认只报告)
  python dlt_restore.py <ts> --force

安全: 默认 dry-run(只报告会做什么), 必须 --force 才真正改动文件/排程。
排程还原因涉及系统, 即便 --force 也只发命令并打印结果, 失败需人工处理。
"""
import sys
import os
import io
import json
import shutil
import subprocess

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_ROOT = os.path.join(WORK_DIR, "backups")
TASK_NAME = "DLT_V8_Smart"
PYTHON = sys.executable


def _latest_backup():
    if not os.path.isdir(BACKUP_ROOT):
        return None
    entries = sorted(
        [d for d in os.listdir(BACKUP_ROOT) if d[:8].isdigit()
         and os.path.isdir(os.path.join(BACKUP_ROOT, d))],
        reverse=True,
    )
    return entries[0] if entries else None


def _resolve(ts):
    if ts and os.path.isdir(os.path.join(BACKUP_ROOT, ts)):
        return ts
    # 也接受目录名直接给
    if ts and os.path.isdir(ts):
        return ts
    return _latest_backup()


def restore_task(dest, force):
    """还原排程任务。返回 (action_taken, detail)。"""
    xml = os.path.join(dest, f"{TASK_NAME}.xml")
    if not os.path.exists(xml):
        return False, f"备份中无 {TASK_NAME}.xml, 跳过排程还原"
    print(f"\n[1/3] 还原 Windows 排程任务 {TASK_NAME}")
    if not force:
        print(f"    (dry) 将执行: schtasks /create /tn {TASK_NAME} /xml {xml} /f")
        return True, "dry-run: 未执行"
    try:
        r = subprocess.run(
            ["schtasks", "/create", "/tn", TASK_NAME, "/xml", xml, "/f"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30,
        )
        out = (r.stdout or b"").decode("gbk", errors="replace")
        err = (r.stderr or b"").decode("gbk", errors="replace")
        if r.returncode == 0:
            return True, f"排程任务已还原 ✅ ({out[:80]}".strip() + ")"
        # 常见: 权限不足 -> 需要管理员
        if "拒绝访问" in err or "access" in err.lower():
            return False, "还原被拒绝: 需以管理员身份运行本脚本(右键->管理员)"
        return False, f"还原失败(rc={r.returncode}): {err[:160]}"
    except Exception as e:
        return False, f"还原异常: {type(e).__name__}: {e}"


def restore_files(dest, force):
    print("\n[2/3] 还原数据 / 状态文件")
    restored, skipped = [], []
    for fn in os.listdir(dest):
        if fn in ("manifest.json", f"{TASK_NAME}.xml"):
            continue
        src = os.path.join(dest, fn)
        if not os.path.isfile(src):
            continue
        dst = os.path.join(WORK_DIR, fn)
        if os.path.exists(dst):
            skipped.append(fn)
        else:
            restored.append(fn)
        if force:
            shutil.copy2(src, dst)
    if restored:
        print(f"    ✅ 将还原 {len(restored)} 个文件: {', '.join(restored)}")
    if skipped:
        print(f"    ⚠️ 已存在, 跳过(不覆盖): {len(skipped)} 个: {', '.join(skipped)}")
    if not restored and not skipped:
        print("    (无文件可还原)")
    return len(restored) > 0


def resync_four(force):
    print("\n[3/3] 调 build_dist.py 重新同步四体")
    bd = os.path.join(WORK_DIR, "build_dist.py")
    if not os.path.exists(bd):
        print("    ⚠️ 未找到 build_dist.py, 跳过四体同步(请手动同步)")
        return
    if not force:
        print("    (dry) 将执行: python build_dist.py")
        return
    try:
        r = subprocess.run(
            [PYTHON, bd], cwd=WORK_DIR, capture_output=True, text=True,
            timeout=900, encoding="utf-8", errors="replace",
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
        )
        if r.returncode == 0:
            print("    ✅ 四体同步完成 (build_dist.py EXIT=0)")
        else:
            print(f"    ❌ 四体同步失败(rc={r.returncode}), 请查看 build_dist 输出")
            if r.stderr:
                print("    " + r.stderr[:300].replace("\n", "\n    "))
    except Exception as e:
        print(f"    ❌ 同步异常: {type(e).__name__}: {e}")


def main():
    args = sys.argv[1:]
    force = "--force" in args
    ts = None
    for a in args:
        if a != "--force" and not a.startswith("-"):
            ts = a
            break

    dest_ts = _resolve(ts)
    if not dest_ts:
        print("❌ 未找到任何备份 (backups/ 为空)。请先运行 dlt_backup.py")
        return 1
    dest = os.path.join(BACKUP_ROOT, dest_ts)
    if not os.path.isdir(dest):
        # ts 可能是绝对路径
        dest = dest_ts if os.path.isdir(dest_ts) else dest

    print("=" * 64)
    print("  大乐透系统 · 灾难恢复还原")
    print(f"  备份: {dest}")
    print("=" * 64)
    if not force:
        print("  [DRY-RUN] 仅报告, 不写盘。加 --force 才真正还原。\n")

    mani = {}
    mp = os.path.join(dest, "manifest.json")
    if os.path.exists(mp):
        try:
            mani = json.load(open(mp, encoding="utf-8"))
            print(f"  备份版本: 模型={mani.get('model_version')} 包={mani.get('package_version')}")
            print(f"  备份时间: {mani.get('created')}")
        except Exception:
            pass

    ok, detail = restore_task(dest, force)
    print(f"    {'✅' if ok else '❌'} {detail}")
    restore_files(dest, force)
    resync_four(force)

    print("\n" + "=" * 64)
    if not force:
        print("  DRY-RUN 完成。确认无误后加 --force 真正还原:")
        print(f"    python dlt_restore.py {dest_ts} --force")
    else:
        print("  还原流程执行完毕, 请检查上方结果(排程若失败需管理员重跑)")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
