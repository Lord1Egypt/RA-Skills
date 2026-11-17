"""
项目结构化状态 — 聚合多源状态，输出 JSON。

数据来源：
  - script.json         → shot 总数、角色/场景卡数
  - .auto_state.json    → 流水线阶段进度
  - tasks/task_tracker.json → shot 级任务状态
  - 文件系统检查        → 视频/资产文件存在性

用法:
    from project_status import gather_status
    status = gather_status(project)
    print(json.dumps(status, indent=2, ensure_ascii=False))
"""

import json, os, time, glob
from typing import Any, Optional
from datetime import datetime, timezone

from modules.config import _script_path


# ── 阶段定义 ─────────────────────────────────────────────

STAGES = [
    ("0", "script_optimization",       "脚本优化"),
    ("1", "build_prompts",             "构建 prompt 文件"),
    ("2", "character_assets",          "角色资产"),
    ("3", "troop_assets",              "辅助资产"),
    ("4", "scene_assets",              "场景资产"),
    ("5", "init_first_frames",         "初始化 first_frame"),
    ("6", "first_frame_generation",    "首帧图生成"),
    ("7", "video_submission",          "提交视频"),
    ("8", "video_polling",             "轮询+拼接"),
]

TOTAL_STAGES = len(STAGES)  # 9

# 阶段基础耗时（分钟），用于 ETA 粗略估计
# 数值偏保守，避免给用户不切实际的期望
_STAGE_ETA_BASE = {
    "0": 0.5,   # 脚本优化：秒级
    "1": 0.5,   # 构建 prompt：秒级
    "2": 3.0,   # 角色资产：每角色 ~3min
    "3": 1.0,   # 辅助资产：每 troop ~1min
    "4": 2.0,   # 场景资产：每场景 ~2min
    "5": 0.3,   # 初始化 first_frame：秒级
    "6": 1.5,   # 首帧图生成：每 shot ~1.5min
    "7": 0.2,   # 提交视频：秒级
    "8": 5.0,   # 视频轮询：每 shot ~5min（并行但保守估计）
}


# ── 状态收集 ─────────────────────────────────────────────

def _load_json(path: str) -> dict:
    """安全加载 JSON，失败返回空 dict。"""
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _count_files(directory: str, pattern: str) -> int:
    """统计目录中匹配 glob 模式的文件数。"""
    if not os.path.isdir(directory):
        return 0
    return len(glob.glob(os.path.join(directory, pattern)))


def _now_iso() -> str:
    """当前时间的 ISO 8601 字符串。"""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _gather_shot_status(project: str, script: dict, tracker: dict) -> dict:
    """收集 shot 级状态。"""
    from video_utils import is_video_done

    shots = script.get("shots", [])
    total = len(shots)

    by_id: dict[str, dict] = {}
    completed_ids: list[str] = []
    processing_ids: list[str] = []
    pending_ids: list[str] = []
    failed_ids: list[str] = []
    queued_ids: list[str] = []

    for s in shots:
        sid = s["id"]
        key = f"shot_{sid:02d}"
        t = tracker.get(str(sid), {})

        video_done = is_video_done(project, sid)
        task_status = t.get("status", "")

        # 确定最终状态
        if video_done:
            status = "completed"
        elif task_status in ("failed",):
            status = "failed"
        elif task_status in ("processing", "submitted"):
            status = "processing"
        elif task_status == "queued":
            status = "queued"
        else:
            status = "pending"

        entry: dict[str, Any] = {
            "status": status,
        }
        if t.get("task_id"):
            entry["task_id"] = t["task_id"]
        if t.get("video_url"):
            entry["video_url"] = t["video_url"]

        by_id[key] = entry

        # 分类
        if status == "completed":
            completed_ids.append(key)
        elif status == "processing":
            processing_ids.append(key)
        elif status == "failed":
            failed_ids.append(key)
        elif status == "queued":
            queued_ids.append(key)
        else:
            pending_ids.append(key)

    return {
        "total": total,
        "completed": len(completed_ids),
        "processing": len(processing_ids),
        "pending": len(pending_ids),
        "queued": len(queued_ids),
        "failed": failed_ids,
        "by_id": by_id,
    }


def _gather_asset_status(project: str, script: dict) -> dict:
    """收集资产生成状态。"""
    # 角色
    char_cards = script.get("character_cards", [])
    char_total = len(char_cards)
    char_done = 0
    for c in char_cards:
        name = c.get("name", "").replace(" ", "_")
        if name and _count_files(
            os.path.join(project, "images", "characters"),
            f"{name}_*.png",
        ) > 0:
            char_done += 1

    # 场景
    scene_cards = script.get("scene_cards", [])
    scene_total = len(scene_cards)
    scene_done = 0
    for s in scene_cards:
        name = s.get("name", "").replace(" ", "_").replace("/", "_")
        if name and _count_files(
            os.path.join(project, "images", "scenes"),
            f"{name}_*.png",
        ) > 0:
            scene_done += 1

    # 首帧图
    shots = script.get("shots", [])
    ff_total = len(shots)
    ff_done = _count_files(
        os.path.join(project, "images", "storyboard"),
        "*_first_frame*.png",
    )

    # 视频
    video_total = len(shots)
    video_done = sum(
        1 for s in shots
        if os.path.isfile(os.path.join(project, "videos", f"shot_{s['id']:02d}.mp4"))
    )

    return {
        "characters": {"completed": char_done, "total": max(char_total, 1)},
        "scenes": {"completed": scene_done, "total": max(scene_total, 1)},
        "first_frames": {"completed": ff_done, "total": max(ff_total, 1)},
        "videos": {"completed": video_done, "total": max(video_total, 1)},
    }


def _compute_stage(auto_state: dict, shot_status: dict, asset_status: dict) -> dict:
    """计算当前流水线阶段和进度百分比。"""
    done = set(auto_state.get("done", []))

    # 找到第一个未完成的阶段
    current_stage = TOTAL_STAGES  # 已完成全部阶段
    current_stage_name = "completed"
    for num, eng_name, _ in STAGES:
        if num not in done:
            current_stage = int(num)
            current_stage_name = eng_name
            break

    # 进度百分比：已完成的阶段数 / 总阶段数
    progress_pct = round(len(done) / TOTAL_STAGES * 100, 1) if TOTAL_STAGES > 0 else 100

    return {
        "stage": current_stage if current_stage < TOTAL_STAGES else TOTAL_STAGES,
        "stage_name": current_stage_name,
        "total_stages": TOTAL_STAGES,
        "completed_stages": sorted(done, key=int),
        "progress_pct": progress_pct,
    }


def _estimate_eta(project: str, script: dict, pipeline: dict, shot_status: dict) -> int:
    """粗略估算剩余时间（分钟）。

    基于各阶段基础耗时和 asset/shot 数量。
    实际时间会因 API 响应速度、重试次数等波动。
    """
    done = set(pipeline["completed_stages"])
    remaining_minutes = 0.0

    num_shots = len(script.get("shots", []))
    num_chars = len(script.get("character_cards", []))
    num_scenes = len(script.get("scene_cards", []))
    num_troops = len(script.get("troop_cards", []))

    vdots = shot_status.get("completed", 0)

    for num, eng_name, _ in STAGES:
        if num in done:
            continue

        base = _STAGE_ETA_BASE.get(num, 1.0)

        # 根据实际内容量调整
        if num == "2":   # 角色
            base *= max(num_chars, 1)
        elif num == "3":  # 辅助资产
            base *= max(num_troops, 1)
        elif num == "4":  # 场景
            base *= max(num_scenes, 1)
        elif num == "6":  # 首帧图
            base *= max(num_shots, 1)
        elif num == "8":  # 视频轮询：只算未完成的 shot
            remaining = max(num_shots - vdots, 0)
            base *= max(remaining, 1)

        remaining_minutes += base

    return max(round(remaining_minutes), 1)


def _gather_errors(project: str, tracker: dict, shot_status: dict) -> list[str]:
    """收集需要关注的问题。"""
    errors: list[str] = []

    # shot 失败
    for shot_key in shot_status.get("failed", []):
        sid = shot_key.split("_")[1].lstrip("0") or "0"
        t = tracker.get(sid, {})
        status = t.get("status", "unknown")
        errors.append(f"{shot_key}: 状态={status}")

    # 视频不全
    vs = shot_status
    if vs["total"] > 0 and vs["completed"] < vs["total"] and not vs["failed"]:
        pending = vs["total"] - vs["completed"] - len(vs["failed"])
        if pending > 0:
            errors.append(f"还有 {pending}/{vs['total']} 个视频正在处理中")

    return errors


def gather_status(project: str) -> dict:
    """聚合所有状态，返回结构化 JSON 兼容 dict。"""
    script = _load_json(_script_path(project))
    auto_state = _load_json(os.path.join(project, ".auto_state.json"))
    tracker = _load_json(os.path.join(project, "tasks", "task_tracker.json"))

    shot_status = _gather_shot_status(project, script, tracker)
    asset_status = _gather_asset_status(project, script)
    pipeline_info = _compute_stage(auto_state, shot_status, asset_status)

    # 时间信息
    start_time = auto_state.get("started_at")
    poll_state = _load_json(os.path.join(project, ".poll_state.json"))

    eta_minutes = _estimate_eta(project, script, pipeline_info, shot_status)

    result = {
        "project": os.path.basename(os.path.abspath(project)),
        "pipeline": pipeline_info,
        "shots": shot_status,
        "assets": asset_status,
        "timing": {
            "started_at": start_time,
            "last_updated": poll_state.get("last_poll_at", _now_iso()),
            "eta_minutes": eta_minutes,
        },
        "errors": _gather_errors(project, tracker, shot_status),
    }

    return result


def print_status(project: str, json_output: bool = False) -> None:
    """打印状态到 stdout。"""
    from modules.config import _log, LOG_LEVEL as _ll

    status = gather_status(project)

    if json_output:
        # JSON 模式：静默输出，只打印 JSON
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return

    # 人类可读模式
    if _ll < 1:
        return

    p = status["pipeline"]
    s = status["shots"]
    a = status["assets"]

    _log(f"\n{'='*50}")
    _log(f"  项目: {status['project']}")
    _log(f"  流水线: 阶段 {p['stage']}/{p['total_stages']} ({p['stage_name']}) {p['progress_pct']:.0f}%")
    _log(f"{'='*50}")

    _log(f"\n  📹 视频: {s['completed']}/{s['total']}")
    if s["failed"]:
        _log(f"     ❌ 失败: {', '.join(s['failed'])}")
    if s["processing"]:
        _log(f"     ⏳ 处理中: {s['processing']}")

    _log(f"\n  🖼️  资产:")
    _log(f"     角色: {a['characters']['completed']}/{a['characters']['total']}")
    _log(f"     场景: {a['scenes']['completed']}/{a['scenes']['total']}")
    _log(f"     首帧图: {a['first_frames']['completed']}/{a['first_frames']['total']}")

    eta = status["timing"]["eta_minutes"]
    _log(f"\n  ⏱️  ETA: 约 {eta} 分钟")

    errs = status.get("errors", [])
    if errs:
        _log(f"\n  ⚠️  需要注意:")
        for e in errs:
            _log(f"    • {e}")

    _log("")
