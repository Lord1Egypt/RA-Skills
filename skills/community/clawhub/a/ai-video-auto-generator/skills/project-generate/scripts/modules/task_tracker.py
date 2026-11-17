"""可插拔任务追踪后端 — 门面模块。默认 LocalJsonTracker。"""
from task_tracker_local import LocalJsonTracker

_backend = None


def _backend_or_default():
    return _backend if _backend is not None else LocalJsonTracker()


def set_tracker(backend):
    global _backend
    _backend = backend


def init_tracker(project: str, mode: str = "feishu") -> None:
    """初始化追踪后端。mode='feishu' 时使用 FeishuTracker，否则默认 LocalJsonTracker。"""
    global _backend
    if mode == "feishu":
        try:
            from task_tracker_feishu import FeishuTracker
            _backend = FeishuTracker(project)
            print(f"  [tracker] FeishuTracker 已初始化（{project}）", flush=True)
        except Exception as e:
            print(f"  [tracker] ⚠️ FeishuTracker init 失败: {e}，回退 LocalJsonTracker", flush=True)
            _backend = LocalJsonTracker()
    else:
        _backend = LocalJsonTracker()


def get_current_backend():
    """返回当前追踪后端实例。"""
    return _backend_or_default()


def save_task(project, shot_id, task_id):
    _backend_or_default().save(project, shot_id, task_id)


def update_task(project, shot_id, status, video_url=None):
    _backend_or_default().update(project, shot_id, status, video_url)


def load_tasks(project):
    return _backend_or_default().load(project)


def get_record_id(project, shot_id):
    return _backend_or_default().get_record_id(project, shot_id)


def upsert_task(project, shot_id, task_id, status, **fields):
    _backend_or_default().upsert_task(project, shot_id, task_id, status, **fields)


def set_status(project, shot_id, status):
    _backend_or_default().set_status(project, shot_id, status)


def upload_attachment(project, shot_id, filepath):
    _backend_or_default().upload_attachment(project, shot_id, filepath)


def save_ref_urls(project, shot_id, urls):
    _backend_or_default().save_ref_urls(project, shot_id, urls)


def list_tasks(project):
    """列出所有任务（自动 CI 验证数据格式）。"""
    raw = _backend_or_default().list_tasks(project)
    try:
        from data_validator import validate_task_list
        return validate_task_list(raw)
    except Exception:
        import traceback
        print(f"  [tracker] ⚠️ CI 验证异常: {traceback.format_exc()}", flush=True)
        return raw


def find_workflow():
    return _backend_or_default().find_workflow()


def update_workflow(rec_id, phase, extra=None):
    _backend_or_default().update_workflow(rec_id, phase, extra)


def get_workflow_phase(rec_id):
    return _backend_or_default().get_workflow_phase(rec_id)
