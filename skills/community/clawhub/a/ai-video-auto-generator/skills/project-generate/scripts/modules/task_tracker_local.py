"""本地 JSON 文件任务追踪后端（canonical 真相，两种 tracker 模式共用）。"""
import json, os, threading, time
from datetime import datetime


def _get_tp(project):
    return os.path.join(project, "tasks", "task_tracker.json")


def _atomic_write(tp, data):
    td = os.path.dirname(tp)
    os.makedirs(td, exist_ok=True)
    tmp = tp + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, tp)


# 并发提交（ThreadPoolExecutor）时多个线程会同时做 read-modify-write 同一文件。
# 无锁会导致 TOCTOU：后写线程覆盖先写线程的结果，任务记录被静默丢弃。
# FeishuTracker 的本地缓存也复用本锁，保证两种模式下并发写都安全。
_lock = threading.Lock()


class LocalJsonTracker:
    """本地 JSON 文件任务追踪（默认后端）。"""

    def save(self, project, shot_id, task_id):
        with _lock:
            data = self.load(project)
            sid = str(shot_id)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if sid in data:
                data[sid]["task_id"] = task_id
                data[sid]["status"] = "submitted"
                data[sid]["updated_at"] = now
            else:
                data[sid] = {
                    "tool": "Agnes AI", "task_id": task_id,
                    "status": "submitted", "created_at": now,
                    "updated_at": now, "video_url": None, "ref_urls": [],
                }
            _atomic_write(_get_tp(project), data)

    def update(self, project, shot_id, status, video_url=None):
        with _lock:
            data = self.load(project)
            sid = str(shot_id)
            if sid not in data:
                return
            data[sid]["status"] = status
            data[sid]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if video_url:
                data[sid]["video_url"] = video_url
            _atomic_write(_get_tp(project), data)

    def load(self, project):
        tp = _get_tp(project)
        if not os.path.isfile(tp):
            return {}
        with open(tp, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_record_id(self, project, shot_id):
        data = self.load(project)
        sid = str(shot_id)
        return sid if sid in data else None

    def upsert_task(self, project, shot_id, task_id, status, **fields):
        with _lock:
            data = self.load(project)
            sid = str(shot_id)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            now_iso = time.strftime("%Y-%m-%dT%H:%M:%S")
            if sid in data:
                data[sid]["task_id"] = task_id
                data[sid]["status"] = status
                data[sid]["updated_at"] = now
                data[sid].update(fields)
            else:
                data[sid] = {
                    "tool": "Agnes AI", "task_id": task_id,
                    "status": status, "created_at": now,
                    "updated_at": now, "video_url": None, "ref_urls": [],
                    "submitted_at": now_iso,
                }
                data[sid].update(fields)
            _atomic_write(_get_tp(project), data)

    def set_status(self, project, shot_id, status):
        with _lock:
            data = self.load(project)
            sid = str(shot_id)
            if sid in data:
                data[sid]["status"] = status
                data[sid]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                _atomic_write(_get_tp(project), data)

    def upload_attachment(self, project, shot_id, filepath):
        pass

    def save_ref_urls(self, project, shot_id, urls):
        with _lock:
            data = self.load(project)
            sid = str(shot_id)
            if sid in data:
                data[sid]["ref_urls"] = urls
                _atomic_write(_get_tp(project), data)

    def dump(self, project, data, merge=False):
        """原子全量写入（供飞书镜像 / 反向同步回写本地）。

        merge=True 时与现有内容合并（dict.update，不删除已有 key）；
        merge=False 时整体替换。两种模式下 task_tracker.json 为唯一本地真相文件。
        """
        tp = _get_tp(project)
        with _lock:
            if merge and os.path.isfile(tp):
                try:
                    with open(tp, "r", encoding="utf-8") as f:
                        existing = json.load(f)
                    existing.update(data)
                    data = existing
                except Exception:
                    pass
            _atomic_write(tp, data)

    def list_tasks(self, project):
        data = self.load(project)
        result = []
        for sid, info in sorted(data.items()):
            try:
                seq = int(sid)
            except ValueError:
                continue  # 非数字 shot_id（如 seg_02）跳过
            result.append({"_seq": seq, **info})
        return result

    # ── 工作流操作（本地模式无工作流，全部空实现） ──

    def find_workflow(self) -> str | None:
        return None

    def update_workflow(self, rec_id: str, phase: str, extra: dict | None = None) -> None:
        pass

    def get_workflow_phase(self, rec_id: str) -> str:
        return ""
