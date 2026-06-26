import os
import hashlib
import json
import shutil
import time
import sys
import datetime

STATE_FILE = ".sync_state.json"
IGNORE_DIRS = {".conflict", ".trash", ".sync_logs"}
HISTORY_LIMIT = 10

## 行为说明
# 在两个目录之间执行双向同步（通常为 PC ↔ USB）
# 自动递归遍历子目录（忽略 .conflict/、.trash/、.sync_logs/）
# 基于文件内容（hash）与版本历史（history）进行同步决策
## 同步规则
# 单边修改：将变更复制到另一端
# 并发修改（冲突）：保存到 .conflict/，不覆盖原文件
# 删除操作：移动到 .trash/，不会直接删除
# 新文件：自动复制到另一端
## History（版本历史）规则
# 每个文件维护一个 history 列表，记录其历史版本（hash）
# 当文件内容发生变化时：
#    新 hash 会追加到 history 尾部
#    history 长度限制为 HISTORY_LIMIT（默认 10）
# 当文件被复制到另一端时：
#    会同步并合并双方的 history（避免历史断裂）
#    合并规则为去重后按时间顺序保留最近版本
# 冲突检测基于 history：
#    若存在共同祖先且双方均偏离该祖先 → 判定为冲突
#    若仅一方偏离祖先 → 判定为单边更新
## 日志
# 同步日志保存在：.sync_logs/
# 包含：复制、删除、冲突、错误及统计信息
# ========= 日志 =========


def init_logger(root):
    log_dir = os.path.join(root, ".sync_logs")
    os.makedirs(log_dir, exist_ok=True)

    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(log_dir, f"sync_{ts}.log")

    return open(log_path, "w", encoding="utf-8")


def log(log_file, level, msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {level} {msg}"
    print(line)
    log_file.write(line + "\n")
    log_file.flush()


# ========= 工具 =========


def ensure_dirs(root):
    os.makedirs(os.path.join(root, ".conflict"), exist_ok=True)
    os.makedirs(os.path.join(root, ".trash"), exist_ok=True)


def file_hash(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def load_state(path):
    try:
        with open(path, "r") as f:
            return json.load(f)["files"]
    except:
        return {}


def save_state(path, data):
    with open(path, "w") as f:
        json.dump({"files": data}, f, indent=2)


# ========= 扫描 =========
# 负责生成当前文件状态，并维护 version history


def scan_folder(root, old_state):
    state = {}

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

        for f in filenames:
            if f == STATE_FILE:
                continue

            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, root)

            stat = os.stat(full)
            size = stat.st_size
            mtime = int(stat.st_mtime)

            old = old_state.get(rel)

            # ===== 判断是否需要重新计算 hash =====
            if old and old["size"] == size and old["mtime"] == mtime:
                state[rel] = old
                continue

            h = file_hash(full)

            # ===== 维护 history（版本链）=====
            history = old.get("history", [])[:] if old else []

            if not history or history[-1] != h:
                history.append(h)
                history = history[-HISTORY_LIMIT:]

            state[rel] = {
                "size": size,
                "mtime": mtime,
                "hash": h,
                "history": history,
                "deleted": False,
            }

    return state


# ========= 找共同祖先 =========


def find_common_ancestor(h1, h2):
    s2 = set(h2)
    for v in reversed(h1):
        if v in s2:
            return v
    return None


# ========= 删除 =========


def move_to_trash(root, rel_path, log_file):
    src = os.path.join(root, rel_path)
    if not os.path.exists(src):
        return

    dst = os.path.join(root, ".trash", rel_path + f".{int(time.time())}")
    os.makedirs(os.path.dirname(dst), exist_ok=True)

    shutil.move(src, dst)
    log(log_file, "TRASH", rel_path)


# ========= 冲突 =========


def handle_conflict(local_root, remote_root, rel_path, device, log_file):
    timestamp = int(time.time())

    for root, tag in [(local_root, "LOCAL"), (remote_root, "REMOTE")]:
        src = os.path.join(root, rel_path)
        if not os.path.exists(src):
            continue

        dst = os.path.join(
            local_root,
            ".conflict",
            f"{rel_path.replace(os.sep,'_')}_{tag}_{device}_{timestamp}",
        )

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

    log(log_file, "CONFLICT", f"{rel_path} → see .conflict/")


# ========= history 合并 =========


def merge_history(src, dst, f):
    src_hist = src.get(f, {}).get("history", [])
    dst_hist = dst.get(f, {}).get("history", [])
    merged = list(dict.fromkeys(dst_hist + src_hist))
    return merged[-HISTORY_LIMIT:]


# ========= 同步 =========


def sync(local_root, remote_root, device_name):
    ensure_dirs(local_root)
    ensure_dirs(remote_root)

    log_file = init_logger(local_root)
    log(log_file, "INFO", f"Start sync {local_root} <-> {remote_root}")

    stats = {"copy": 0, "conflict": 0, "trash": 0}

    local_state_path = os.path.join(local_root, STATE_FILE)
    remote_state_path = os.path.join(remote_root, STATE_FILE)

    local_old = load_state(local_state_path)
    remote_old = load_state(remote_state_path)

    local_now = scan_folder(local_root, local_old)
    remote_now = scan_folder(remote_root, remote_old)

    all_files = set(local_now) | set(remote_now) | set(local_old) | set(remote_old)

    for f in all_files:
        try:
            l = local_now.get(f)
            r = remote_now.get(f)
            lo = local_old.get(f)
            ro = remote_old.get(f)

            local_path = os.path.join(local_root, f)
            remote_path = os.path.join(remote_root, f)

            l_deleted = (not l) and lo
            r_deleted = (not r) and ro

            # ========= 双方存在 =========
            if l and r:
                lh = l["hash"]
                rh = r["hash"]

                if lh == rh:
                    continue

                base = find_common_ancestor(l["history"], r["history"])

                # 冲突：无共同祖先 或 双向分叉
                if base is None or (lh != base and rh != base):
                    handle_conflict(local_root, remote_root, f, device_name, log_file)
                    stats["conflict"] += 1
                    continue

                # remote 更新
                if lh == base:
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    shutil.copy2(remote_path, local_path)
                    local_now[f]["history"] = merge_history(remote_now, local_now, f)
                    log(log_file, "INFO", f"COPY remote→local {f}")
                    stats["copy"] += 1
                    continue

                # local 更新
                if rh == base:
                    os.makedirs(os.path.dirname(remote_path), exist_ok=True)
                    shutil.copy2(local_path, remote_path)
                    remote_now[f]["history"] = merge_history(local_now, remote_now, f)
                    log(log_file, "INFO", f"COPY local→remote {f}")
                    stats["copy"] += 1
                    continue

            # ========= 删除 vs 修改 =========
            if l_deleted and r:
                handle_conflict(local_root, remote_root, f, device_name, log_file)
                stats["conflict"] += 1
                continue

            if r_deleted and l:
                handle_conflict(local_root, remote_root, f, device_name, log_file)
                stats["conflict"] += 1
                continue

            # ========= 删除 =========
            if l_deleted:
                move_to_trash(remote_root, f, log_file)
                stats["trash"] += 1
                continue

            if r_deleted:
                move_to_trash(local_root, f, log_file)
                stats["trash"] += 1
                continue

            # ========= 新文件 =========
            if l and not r:
                os.makedirs(os.path.dirname(remote_path), exist_ok=True)
                shutil.copy2(local_path, remote_path)
                remote_now[f] = l.copy()
                log(log_file, "INFO", f"COPY NEW → remote {f}")
                stats["copy"] += 1
                continue

            if r and not l:
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                shutil.copy2(remote_path, local_path)
                local_now[f] = r.copy()
                log(log_file, "INFO", f"COPY NEW → local {f}")
                stats["copy"] += 1
                continue

        except Exception as e:
            log(log_file, "ERROR", f"{f} {str(e)}")

    save_state(local_state_path, local_now)
    save_state(remote_state_path, remote_now)

    log(log_file, "SUMMARY", str(stats))
    log(log_file, "INFO", "Sync complete")
    log_file.close()


# ========= 入口 =========

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python sync.py <local_folder> <remote_folder> <device_name>")
        sys.exit(1)

    sync(sys.argv[1], sys.argv[2], sys.argv[3])
