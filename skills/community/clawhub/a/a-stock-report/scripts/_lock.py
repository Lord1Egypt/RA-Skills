"""
智能锁模块：PID + TTL + stale 检测

解决原版锁的 3 个痛点：
1. 无 PID：无法判断锁的"主人"是否还活着
2. 无 TTL：进程死了锁永远留着
3. 无 stale 检测：手动 rm 是唯一清理手段

行为：
- 无锁 → 创建并占用
- 有锁 + 持有者存活 + 未超 TTL → 报错退出（避免并发）
- 有锁 + 持有者死亡 → 自动清理并占用
- 有锁 + 锁超时（>ttl）→ 视为 stale，清理并占用
"""

import os
import sys
import time


def _pid_alive(pid: int) -> bool:
    """检测 PID 是否存活。返回 True=存活, False=已死。"""
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        # 进程存在但当前用户无权限杀，仍视为存活
        return True


def _read_lock(path: str):
    """读取锁文件，返回 (pid, owner, created_at) 或 None。"""
    try:
        with open(path) as f:
            lines = f.read().splitlines()
        if len(lines) < 3:
            return None
        return int(lines[0]), lines[1], float(lines[2])
    except (OSError, ValueError):
        return None


def lock(path: str, owner: str = None, ttl: int = 3600) -> bool:
    """
    智能锁获取。

    Args:
        path: 锁文件路径
        owner: 持有者标识（通常传 __file__）
        ttl: 锁过期秒数（默认 1 小时）

    Returns:
        True = 获取成功
        False = 已有活跃实例占用，未获取
    """
    if os.path.exists(path):
        info = _read_lock(path)
        if info is not None:
            pid, prev_owner, created = info
            age = time.time() - created
            if _pid_alive(pid) and age < ttl:
                print(
                    f"[LOCK] 已有实例在运行 (pid={pid} {prev_owner})，退出。",
                    file=sys.stderr,
                )
                return False
            # 死锁 或 超时 → 清理
            if not _pid_alive(pid):
                reason = f"持有者已退出 (pid={pid})"
            else:
                reason = f"锁超 {ttl}s (pid={pid} 已活 {int(age)}s)"
            print(f"[LOCK] {reason}，自动清理并抢占。")
        try:
            os.remove(path)
        except OSError:
            pass
    # 创建新锁
    with open(path, "w") as f:
        f.write(f"{os.getpid()}\n{owner or 'unknown'}\n{time.time()}\n")
    return True


def unlock(path: str):
    """释放锁（幂等：锁不存在不报错）。"""
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass
