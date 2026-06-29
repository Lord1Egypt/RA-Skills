"""
vault_watcher.py — Vault 文件变化监听器
实时监控 vault 目录文件变化，立即触发同步。

工作原理：
1. 每 2 秒扫描 vault 目录，检查文件的 mtime
2. 检测到变化后，立即调用 vault_to_qdrant.py 同步变更文件
3. 无依赖，纯 Python os.stat() 实现

用法: python scripts/vault_watcher.py
      python scripts/vault_watcher.py --interval 5  (自定义轮询间隔)
      python scripts/vault_watcher.py --once         (单次扫描)
"""
import _suppress_windows

import os
import sys
import time
import subprocess
import atexit
from pathlib import Path


# PID 锁：防重复启动
PID_FILE = Path.home() / ".openclaw" / ".vault_watcher.pid"


def acquire_lock():
    """获取 PID 锁，已有实例则退出。"""
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    if PID_FILE.exists():
        try:
            old_pid = int(PID_FILE.read_text().strip())
            # 检查进程是否存活
            if os.name == "nt":
                import ctypes
                kernel32 = ctypes.windll.kernel32
                h = kernel32.OpenProcess(0x400, False, old_pid)
                if h:
                    kernel32.CloseHandle(h)
                    print(f"[vault_watcher] 已有实例在运行 (PID {old_pid})，退出")
                    sys.exit(0)
            else:
                try:
                    os.kill(old_pid, 0)
                    print(f"[vault_watcher] 已有实例在运行 (PID {old_pid})，退出")
                    sys.exit(0)
                except OSError:
                    pass  # 进程已死，锁是陈旧的
        except (ValueError, OSError):
            pass  # 锁文件损坏或无法访问

    # 写入当前 PID
    PID_FILE.write_text(str(os.getpid()))
    atexit.register(lambda: PID_FILE.unlink(missing_ok=True))

# Vault 配置
from shared_config import VAULT_DIR
SYNC_SUBDIRS = ["01-日记", "02-知识", "04-教训", "07-项目"]

# 脚本路径
SCRIPTS_DIR = Path(__file__).parent
VAULT_SYNC_SCRIPT = SCRIPTS_DIR / "vault_to_qdrant.py"
PROFILE_SCRIPT = SCRIPTS_DIR / "build_project_profile.py"

# 状态记录
STATE_FILE = Path.home() / ".openclaw" / ".vault_watcher_state.json"


def get_vault_files() -> dict:
    """扫描 vault 目录，返回 {relative_path: mtime}"""
    files = {}
    for subdir in SYNC_SUBDIRS:
        target = VAULT_DIR / subdir
        if not target.exists():
            continue
        for f in target.rglob("*.md"):
            try:
                stat = f.stat()
                files[str(f.relative_to(VAULT_DIR))] = stat.st_mtime
            except (OSError, ValueError):
                continue
    return files


def load_state() -> dict:
    """加载上次的扫描状态"""
    if STATE_FILE.exists():
        try:
            import json
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"files": {}, "last_scan": None}


def save_state(state: dict):
    """保存扫描状态"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    import json
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def detect_changes(current: dict, previous: dict) -> tuple:
    """检测变化，返回 (新增, 修改, 删除)"""
    prev_files = previous.get("files", {})
    added = []
    modified = []
    deleted = []

    for path, mtime in current.items():
        if path not in prev_files:
            added.append(path)
        elif prev_files[path] != mtime:
            modified.append(path)

    for path in prev_files:
        if path not in current:
            deleted.append(path)

    return added, modified, deleted


def trigger_sync(change_type: str, files: list):
    """触发 vault 同步"""
    if not files:
        return

    summary = ", ".join(f[:40] for f in files[:5])
    if len(files) > 5:
        summary += f" ... (共 {len(files)} 个)"

    print(f"[{change_type}] {summary}")

    # 调用 vault_to_qdrant.py 全量同步
    try:
        result = subprocess.run(
            ["python", str(VAULT_SYNC_SCRIPT)],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0:
            print(f"  同步完成")
        else:
            print(f"  同步出错: {result.stderr.strip()[:200]}")
    except subprocess.TimeoutExpired:
        print(f"  同步超时")
    except Exception as e:
        print(f"  同步失败: {e}")


def scan_once():
    """单次扫描"""
    print("扫描 vault 目录...")
    current = get_vault_files()
    state = load_state()
    added, modified, deleted = detect_changes(current, state)

    if not added and not modified and not deleted:
        print("无变化")
        return

    if added:
        print(f"  新增: {len(added)} 个文件")
        trigger_sync("新增", added)
    if modified:
        print(f"  修改: {len(modified)} 个文件")
        trigger_sync("修改", modified)
    if deleted:
        print(f"  删除: {len(deleted)} 个文件")
        trigger_sync("删除", deleted)

    # 更新状态
    state["files"] = current
    state["last_scan"] = time.time()
    save_state(state)


def watch_loop(interval: int = 2):
    """持续监听循环"""
    state = load_state()
    previous = state.get("files", {})

    print(f"Vault 监听器启动，轮询间隔 {interval}s")
    print(f"  监控: {VAULT_DIR}")
    print(f"  子目录: {', '.join(SYNC_SUBDIRS)}")
    print("  按 Ctrl+C 停止\n")

    while True:
        try:
            current = get_vault_files()
            added, modified, deleted = detect_changes(current, {"files": previous})

            if added or modified or deleted:
                all_changed = added + modified
                if all_changed:
                    print(f"\n[{time.strftime('%H:%M:%S')}] 检测到 {len(all_changed)} 个文件变化")
                    trigger_sync("变化", all_changed)

                if deleted:
                    trigger_sync("删除", deleted)

                # 更新缓存
                previous = current
                state["files"] = current
                state["last_scan"] = time.time()
                save_state(state)

            time.sleep(interval)

        except KeyboardInterrupt:
            print("\n监听器停止")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(interval * 5)  # 出错后延长等待


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", "-i", type=int, default=600, help="轮询间隔（秒）")
    parser.add_argument("--once", action="store_true", help="单次扫描后退出")
    parser.add_argument("--force", action="store_true", help="强制启动（忽略 PID 锁）")
    opts = parser.parse_args()

    if not opts.force and not opts.once:
        acquire_lock()

    if opts.once:
        scan_once()
    else:
        watch_loop(opts.interval)


if __name__ == "__main__":
    main()


