"""飞书 Base 任务追踪后端。本地 task_tracker.json 为统一真相，飞书为云端镜像/附件层。"""
import json, os, time
from typing import Any


# ── 本地 JSON 与飞书记录的双向转换 ──────────────────────────────
# 状态优先级（数值越大越靠后）。双向同步时不降级已更靠后的状态。
_STATUS_RANK = {"queued": 0, "submitted": 1, "processing": 2, "failed": 2, "completed": 3}


def _records_to_local(records, existing=None):
    """把飞书/合并后的记录列表（含 _seq / 状态(list) / API任务ID / 备注(JSON)）
    转成本地 schema dict（key=str(_seq)）。

    existing 为本地已有 dict 时做合并：保留更靠后的状态、非空 task_id，
    以及本地已有的 video_url / ref_urls。
    """
    out = {}
    for r in records:
        seq = r.get("_seq")
        if seq is None:
            continue
        sid = str(seq)
        note = {}
        rem = r.get("备注")
        if isinstance(rem, str):
            try:
                note = json.loads(rem)
            except Exception:
                note = {}
        status = r.get("状态")
        if isinstance(status, list):
            status = status[0] if status else ""
        out[sid] = {
            "tool": "Agnes AI",
            "task_id": r.get("API任务ID", "") or "",
            "status": status or "",
            "created_at": note.get("submitted_at", "") or "",
            "updated_at": note.get("submitted_at", "") or "",
            "video_url": None,
            "ref_urls": [],
            "submitted_at": note.get("submitted_at"),
            "retry": note.get("retry", 0),
        }
    if existing:
        for sid, old in existing.items():
            if sid not in out:
                out[sid] = old
            else:
                cur = out[sid]
                if _STATUS_RANK.get(old.get("status", ""), 0) > _STATUS_RANK.get(cur.get("status", ""), 0):
                    cur["status"] = old["status"]
                if not cur.get("task_id") and old.get("task_id"):
                    cur["task_id"] = old["task_id"]
                if old.get("video_url"):
                    cur["video_url"] = old["video_url"]
                if old.get("ref_urls"):
                    cur["ref_urls"] = old["ref_urls"]
    return out


def _load_feishu_config() -> dict[str, str]:
    """从 config 读取飞书配置（通过 _shared_tools 走 Layer 2 优先级链）。"""
    result = {"base_token": "", "table_id": "", "workflow_table_id": ""}
    try:
        from _shared_tools import get as _cfg_get
        from modules.config import get_feishu_base_token
    except ImportError:
        return result
    # base_token 已从 config.toml 迁出，缺失时回退 ~/.feishu-base-token（见 get_feishu_base_token）
    result["base_token"] = get_feishu_base_token() or ""
    result["table_id"] = _cfg_get("feishu", "table_id") or ""
    result["workflow_table_id"] = _cfg_get("feishu", "workflow_table_id") or ""
    return result


class FeishuTracker:
    """通过飞书 Base 读写任务状态。token/table_id 通过 _paths.py 三层路径模型自动解析。"""

    def __init__(self, doc_id: str = "",
                 feishu_mod: Any = None,
                 base_token: str | None = None,
                 table_id: str | None = None,
                 workflow_table_id: str | None = None):
        # 读取飞书模块
        if feishu_mod is None:
            import feishu
            feishu_mod = feishu
        self._feishu = feishu_mod
        # 本地状态统一走 LocalJsonTracker（写同一个 task_tracker.json），
        # 这样 feishu 模式与 local 模式共用一份本地真相，切换 tracker 无需迁移。
        from task_tracker_local import LocalJsonTracker
        self._local = LocalJsonTracker()

        # 从配置读取缺失项
        cfg = _load_feishu_config()
        self._base_token = base_token if base_token is not None else cfg["base_token"]
        self._table_id = table_id if table_id is not None else cfg["table_id"]
        self._workflow_table_id = workflow_table_id if workflow_table_id is not None else cfg["workflow_table_id"]
        self._doc_id = doc_id

    def save(self, project: str, shot_id: int, task_id: str) -> None:
        feishu = self._feishu
        rid = feishu.get_record_id(project, self._base_token, self._table_id, self._doc_id, shot_id)
        if rid:
            feishu.update_record(self._base_token, self._table_id, rid, {
                "task_id": task_id, "状态": ["submitted"],
            })
        else:
            rid = feishu.upsert_record(self._base_token, self._table_id, {
                "镜头序号": shot_id, "task_id": task_id, "状态": ["submitted"],
            })
        try:
            from modules.api import get_last_submit_result
        except ImportError:
            get_last_submit_result = lambda: None
        result = get_last_submit_result()
        if result and result.get("image_urls"):
            feishu.save_keyframe_urls(self._base_token, self._table_id, rid, result["image_urls"])

    def update(self, project: str, shot_id: int, status: str, video_url: str | None = None) -> None:
        feishu = self._feishu
        rid = feishu.get_record_id(project, self._base_token, self._table_id, self._doc_id, shot_id)
        if not rid:
            return
        feishu.update_record(self._base_token, self._table_id, rid, {"状态": [status]})
        if video_url and status == "completed":
            vpath = os.path.join(project, "videos", f"shot_{shot_id:02d}.mp4")
            if os.path.isfile(vpath):
                feishu.upload_attachment(self._base_token, self._table_id, rid, vpath)

    def load(self, project: str) -> dict[str, dict]:
        feishu = self._feishu
        shots = feishu.list_shots(project, self._base_token, self._table_id, self._doc_id)
        result: dict[str, dict] = {}
        for s in shots:
            sid = str(s.get("镜头序号", ""))
            if not sid:
                continue
            raw_status = s.get("状态", [""])
            status = raw_status[0] if isinstance(raw_status, list) else str(raw_status)
            result[sid] = {
                "task_id": s.get("task_id", ""),
                "status": status,
                "video_url": None,
            }
        return result

    # ── 新增通用接口方法 ──

    def get_record_id(self, project, shot_id):
        return self._feishu.get_record_id(project, self._base_token, self._table_id, self._doc_id, shot_id)

    KNOWN_BASE_FIELDS = {"状态", "备注", "API任务ID", "镜头ID", "生成工具", "对应视频任务ID"}

    def upsert_task(self, project, shot_id, task_id, status, **fields):
        """写入飞书 Base（含本地缓存兜底）。返回 True 表示飞书写入成功，False 表示仅写入本地缓存。"""
        feishu = self._feishu
        sid_str = str(shot_id)
        now_iso = time.strftime("%Y-%m-%dT%H:%M:%S")
        # 备注同时携带 retry，使飞书云端成为权威源（不再仅靠本地缓存兜底）
        note = {"submitted_at": now_iso}
        if "retry" in fields:
            note["retry"] = fields["retry"]
        base_fields = {"状态": [status], "备注": json.dumps(note, ensure_ascii=False)}
        if task_id:
            base_fields["API任务ID"] = task_id
        # 只将 Base 表已有的字段写入飞书，其余字段（submitted_at/retry 等）仅供本地缓存
        for k, v in fields.items():
            if k in self.KNOWN_BASE_FIELDS:
                base_fields[k] = v

        # 1) 始终写入统一本地真相（task_tracker.json）
        self._local.upsert_task(project, shot_id, task_id, status, **fields)

        # 2) 尝试写入飞书
        rid = feishu.get_record_id(project, self._base_token, self._table_id,
                                    self._doc_id, shot_id)
        feishu_ok = False
        if rid:
            feishu_ok = feishu.update_record(self._base_token, self._table_id, rid, base_fields)
        else:
            display_id = f"shot_{shot_id:02d}" if isinstance(shot_id, int) else shot_id
            new_rid = feishu.upsert_record(self._base_token, self._table_id, {
                "镜头ID": display_id,
                "生成工具": ["Agnes AI"],
                "对应视频任务ID": self._doc_id,
                **base_fields,
            })
            if new_rid:
                feishu_ok = True

        if not feishu_ok:
            print(f"  [tracker] ⚠️ 飞书写入失败，已写入本地缓存（shot_id={shot_id}）", flush=True)
        return feishu_ok

    def set_status(self, project, shot_id, status):
        feishu = self._feishu
        rid = feishu.get_record_id(project, self._base_token, self._table_id, self._doc_id, shot_id)
        if rid:
            feishu.update_record(self._base_token, self._table_id, rid, {"状态": [status]})

    def upload_attachment(self, project, shot_id, filepath):
        feishu = self._feishu
        rid = feishu.get_record_id(project, self._base_token, self._table_id, self._doc_id, shot_id)
        if rid and os.path.isfile(filepath):
            return feishu.upload_attachment(self._base_token, self._table_id, rid, filepath)
        return False

    def save_ref_urls(self, project, shot_id, urls):
        feishu = self._feishu
        rid = feishu.get_record_id(project, self._base_token, self._table_id, self._doc_id, shot_id)
        if rid:
            feishu.save_keyframe_urls(self._base_token, self._table_id, rid, urls)

    def list_tasks(self, project):
        """列出任务，本地缓存覆盖飞书数据（兜底重试不丢数据）。"""
        feishu_tasks = self._feishu.list_shots(project, self._base_token,
                                                self._table_id, self._doc_id)
        local_data = self._local.load(project)
        if not local_data:
            return feishu_tasks

        # 用本地缓存覆盖：本地有且 task_id 非空时，覆盖对应 shot 的 task_id 和 status
        local_by_sid: dict[int, dict] = {}
        for sid_str, info in local_data.items():
            try:
                local_by_sid[int(sid_str)] = info
            except (ValueError, TypeError):
                pass

        if not local_by_sid:
            return feishu_tasks

        merged = []
        for s in feishu_tasks:
            seq = s.get("_seq", 0)
            if seq in local_by_sid:
                local_info = local_by_sid[seq]
                local_tid = local_info.get("task_id", "")
                local_st = local_info.get("status", "")
                local_retry = local_info.get("retry")
                # 本地 task_id 非空 → 覆盖飞书
                if local_tid:
                    s["API任务ID"] = local_tid
                # 本地状态非空 → 覆盖飞书（存为字符串，不包列表）
                if local_st:
                    s["状态"] = local_st
                # 本地 retry 有值 → 写入备注（供 poll_shots 读取）
                if local_retry is not None:
                    try:
                        note = json.loads(s.get("备注", "{}")) if isinstance(s.get("备注"), str) else {}
                    except Exception:
                        note = {}
                    note["retry"] = local_retry
                    s["备注"] = json.dumps(note, ensure_ascii=False)
            merged.append(s)

        # 补充本地有但飞书没有的任务（通常不会，因为飞书是主存储）
        feishu_seqs = {s.get("_seq", 0) for s in feishu_tasks}
        for seq, info in local_by_sid.items():
            if seq not in feishu_seqs and info.get("task_id"):
                merged.append({
                    "_seq": seq,
                    "镜头ID": f"shot_{seq:02d}",
                    "API任务ID": info["task_id"],
                    "状态": info.get("status", "queued"),
                    "对应视频任务ID": self._doc_id,
                    "备注": json.dumps({"retry": info.get("retry", 0)}, ensure_ascii=False),
                })
        # 自动镜像：把（飞书 ∪ 本地覆盖）的合并结果写回统一的本地
        # task_tracker.json，使本地文件始终等于权威状态。这样在另一台机器上跑
        # 一次 feishu 模式即可把飞书进度落到本地，无需手动复制。
        # 注意：本地为 canonical —— 必须传入 existing 做兜底合并，否则若某条
        # 飞书记录 API任务ID 为空（如飞书写入瞬时异常），会把本地已保存的有效
        # task_id 覆盖清空，导致 poll 误判「无 task_id」而重复提交、浪费配额。
        self._local.dump(project, _records_to_local(merged, self._local.load(project)), merge=False)
        return merged

    def sync_to_local(self, project) -> int:
        """反向同步：把飞书 Base 进度拉到本地 task_tracker.json。返回同步条数。

        供 `tracker sync` 命令与跨机接力：在另一台机跑此命令即把云端进度
        复制到本地，之后可切 --tracker local 续跑。
        """
        feishu_tasks = self._feishu.list_shots(project, self._base_token,
                                               self._table_id, self._doc_id)
        existing = self._local.load(project)
        local_dict = _records_to_local(feishu_tasks, existing)
        self._local.dump(project, local_dict, merge=False)
        return len(local_dict)

    # ── 工作流操作 ──────────────────────────────────

    def find_workflow(self) -> str | None:
        """在工作流表中查找当前项目的记录 ID。"""
        return self._feishu.find_workflow_rec(self._base_token, self._workflow_table_id, self._doc_id)

    def update_workflow(self, rec_id: str, phase: str, extra: dict | None = None) -> None:
        """更新工作流阶段。"""
        self._feishu.update_workflow_phase(self._base_token, self._workflow_table_id, rec_id, phase, extra)

    def get_workflow_phase(self, rec_id: str) -> str:
        """查询当前工作流阶段。"""
        return self._feishu.get_workflow_phase(self._base_token, self._workflow_table_id, rec_id)
