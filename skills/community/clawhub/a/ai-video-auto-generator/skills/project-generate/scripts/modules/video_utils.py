# -*- coding: utf-8 -*-
"""视频轮询/提交/下载/验证工具函数。"""
import json, os, re, subprocess, sys, time
from datetime import datetime
from typing import Any, Optional

from project_verify import _verify_shot_video
from error_utils import classify as _classify_failure, soften_prompt
from config import _log as _log_raw
try:
    _log = _log_raw
except Exception:
    _log = print


def _p(project: str) -> dict:
    return {
        "videos": os.path.join(project, "videos"),
        "output": os.path.join(project, "output"),
        "sounds": os.path.join(project, "sounds"),
        "images": os.path.join(project, "images"),
    }


def _paths(project: str) -> dict:
    return _p(project)


def _shot_count(project: str) -> int:
    sp = os.path.join(project, "script.json")
    with open(sp, encoding="utf-8") as f:
        d = json.load(f)
    return len(d.get("shots", []))


def load_script(project: str) -> dict:
    sp = os.path.join(project, "script.json")
    with open(sp, encoding="utf-8") as f:
        return json.load(f)


def is_video_done(project: str, shot_id: int) -> bool:
    return os.path.isfile(os.path.join(_p(project)["videos"], f"shot_{shot_id:02d}.mp4"))


def _uploaded_marker(project: str, sid: int) -> str:
    return os.path.join(_p(project)["videos"], f".uploaded_shot_{sid:02d}")


def _is_uploaded(project: str, sid: int, vpath: str) -> bool:
    m = _uploaded_marker(project, sid)
    if not os.path.isfile(m) or not os.path.isfile(vpath):
        return False
    try:
        with open(m, encoding="utf-8") as f:
            return os.path.getmtime(vpath) == float(f.read().strip())
    except Exception:
        return False


def _mark_uploaded(project: str, sid: int, vpath: str) -> None:
    try:
        with open(_uploaded_marker(project, sid), "w", encoding="utf-8") as f:
            f.write(str(os.path.getmtime(vpath)))
    except Exception:
        pass


def is_segment_done(project: str, seg_id: int) -> bool:
    return os.path.isfile(os.path.join(_p(project)["videos"], f"seg_{seg_id:02d}.mp4"))


def set_status(project: str, sid: int, status: str) -> None:
    try:
        from task_tracker import upsert_task
        upsert_task(project, sid, "", status, error="", error_cat="status_update")
    except Exception:
        pass


def upload_attachment(project: str, sid: int, vpath: str) -> bool:
    try:
        from feishu import upload_video_attachment
        return upload_video_attachment(project, sid, vpath)
    except Exception:
        return False


_patch_lock = set()


def _patch_video_prompt(project: str, sid: int, category: str, detail: str) -> None:
    prompt_path = os.path.join(project, "prompts", f"video_shot{sid:02d}.md")
    if not os.path.isfile(prompt_path):
        return
    if sid in _patch_lock:
        return
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "[video_fix]" in content:
            return
        fixes = []
        if category in ("static_or_black", "frozen", "no_motion"):
            fixes.append("大幅运镜，镜头缓慢推进，画面动态变化，非静止")
        if category in ("camera_mismatch",):
            if "dolly" in detail.lower() or "推" in detail:
                fixes.append("镜头缓慢推进")
            elif "pan" in detail.lower() or "横移" in detail:
                fixes.append("镜头平稳横移")
            elif "tilt" in detail.lower() or "摇" in detail:
                fixes.append("镜头上下摇摄")
            else:
                fixes.append("镜头平稳运动")
        if category in ("mood_mismatch", "mood"):
            fixes.append("高动态，富有表现力")
        if category == "content_moderation":
            fixes.append("safe, family-friendly, no violence, no blood, no gore, no weapons, no injury, peaceful")
        if fixes:
            with open(prompt_path, "a", encoding="utf-8") as f:
                f.write(f"\n[video_fix] {'，'.join(fixes)}")
        _patch_lock.add(sid)
    except Exception:
        pass


def _ensure_tracker(project: str, tracker: str) -> None:
    pass


def _resubmit_shot(project: str, sid: int, script: dict, provider: Any,
                   retry_count: int = 0, regen_first_frame: bool = False) -> bool:
    try:
        from task_tracker import upsert_task
        if regen_first_frame:
            _log(f"  🔄 shot_{sid:02d}: 重建首帧后重提 (retry={retry_count})")
        from provider_factory import create_provider
        return _do_resubmit(project, sid, script, provider, retry_count, regen_first_frame)
    except Exception as e:
        _log(f"  ❌ shot_{sid:02d} 重提失败: {e}")
        return False


def _do_resubmit(project: str, sid: int, script: dict, provider: Any,
                 retry_count: int = 0, regen_first_frame: bool = False) -> bool:
    try:
        from task_tracker import upsert_task
        shot = next((s for s in script.get("shots", []) if s["id"] == sid), None)
        if not shot:
            return False
        prompt = shot.get("description", "")
        duration = shot.get("duration", 5)
        aspect = script.get("aspect_ratio", "9:16")
        ff_path = os.path.join(project, "images", "storyboard", f"shot_{sid:02d}_first_frame.png")
        ref_img = ff_path if os.path.isfile(ff_path) else None
        result = provider.submit_video(
            project=project, shot_id=sid, prompt=prompt,
            ref_img=ref_img, duration=duration, aspect=aspect,
        )
        if result:
            upsert_task(project, sid, result.get("task_id", ""), "queued",
                        error="", error_cat="", retry=retry_count,
                        meta=json.dumps({"retry": retry_count, "submitted_at": datetime.now().isoformat()}))
            return True
        return False
    except Exception as e:
        _log(f"  ⚠️ shot_{sid:02d} 重提异常: {e}")
        return False


def _poll_shots(project: str) -> tuple[list, bool]:
    from task_tracker import list_tasks, upsert_task
    from provider_factory import create_provider
    
    script = load_script(project)
    shots = script.get("shots", [])
    shot_ids = [s["id"] for s in shots]
    all_completed = True
    results = []
    tasks_cache = list_tasks(project)
    if not tasks_cache:
        return results, False
    project_paths = _paths(project)
    
    for sid in shot_ids:
        if is_video_done(project, sid):
            vpath = os.path.join(project_paths["videos"], f"shot_{sid:02d}.mp4")
            if _is_uploaded(project, sid, vpath):
                results.append((sid, "completed"))
                continue
            if upload_attachment(project, sid, vpath):
                _mark_uploaded(project, sid, vpath)
            results.append((sid, "completed"))
            continue
        
        task_id = ""; retry = 0
        for t in tasks_cache:
            if str(t.get("_seq", "")) == str(sid):
                task_id = t.get("task_id", "") or t.get("API任务ID", "")
                try:
                    note = t.get("备注", "") or ""
                    meta = json.loads(note) if note else {}
                    retry = int(meta.get("retry", 0))
                except Exception:
                    retry = 0
                break
        
        if not task_id:
            results.append((sid, "no_task"))
            all_completed = False
            continue
        
        try:
            provider = create_provider(project)
            qr = provider.quick_query(task_id)
        except Exception as e:
            results.append((sid, "pending"))
            all_completed = False
            continue
        
        if not qr:
            results.append((sid, "pending"))
            all_completed = False
            continue
        
        qs = qr.get("status", "unknown")
        if qs in ("completed", "succeeded"):
            video_url = qr.get("video_url")
            if video_url:
                vpath = os.path.join(project_paths["videos"], f"shot_{sid:02d}.mp4")
                os.makedirs(os.path.dirname(vpath), exist_ok=True)
                try:
                    provider.download_video(video_url, vpath)
                    if os.path.isfile(vpath) and os.path.getsize(vpath) >= 1024:
                        _log(f"  shot_{sid:02d} ✅ 完成 (已下载)")
                        results.append((sid, "completed"))
                    else:
                        results.append((sid, "failed"))
                        all_completed = False
                except Exception:
                    results.append((sid, "failed"))
                    all_completed = False
            else:
                raw = qr.get("raw", {}) or {}
                category, reason = _classify_failure(raw, qs)
                _patch_video_prompt(project, sid, "content_moderation", reason)
                _log(f"  shot_{sid:02d} ⏳ 完成但无视频 URL（{reason}），修补视频 prompt 后重提...")
                if retry < 5:
                    _resubmit_shot(project, sid, script, provider, retry + 1, regen_first_frame=False)
                    all_completed = False
                    results.append((sid, "retrying"))
                else:
                    set_status(project, sid, "failed")
                    _log(f"  shot_{sid:02d} ❌ 完成无 URL，已重试 5 次仍失败")
                    all_completed = False
                    results.append((sid, "failed_exhausted"))
            continue
        
        if qs in ("failed", "error"):
            raw = qr.get("raw", {}) or {}
            category, reason = _classify_failure(raw, qs)
            _log(f"  ⚠️ shot_{sid:02d} 失败分类={category} 原因={reason}")
            if category == "rate_limit":
                all_completed = False
                results.append((sid, "rate_limited"))
                continue
            if any(kw in reason.lower() for kw in ("timed out", "timeout", "read timed")):
                results.append((sid, "pending"))
                all_completed = False
                continue
            if retry < 5:
                regen = category in ("invalid_image", "bad_request")
                _resubmit_shot(project, sid, script, provider, retry + 1, regen_first_frame=regen)
                all_completed = False
                results.append((sid, "retrying"))
            else:
                set_status(project, sid, "failed")
                all_completed = False
                results.append((sid, "failed_exhausted"))
            continue
        
        results.append((sid, "pending"))
        all_completed = False
    
    return results, all_completed


def _cmd_poll(project: str, tracker: str = "feishu") -> bool:
    import time as _time
    from task_tracker import init_tracker
    init_tracker(project, tracker)
    
    state_path = os.path.join(project, ".poll_state.json")
    now = _time.time()
    if os.path.isfile(state_path):
        try:
            with open(state_path, "r", encoding="utf-8") as f:
                state = json.load(f)
            next_poll = state.get("next_poll_at", 0)
            if next_poll > now:
                remaining = int(next_poll - now)
                _log(f"  ⏳ 轮询间隔未到（{remaining}秒后），跳过本次")
                return False
        except Exception:
            pass
    
    sc = _shot_count(project)
    from provider_factory import create_provider as _cp
    
    _log(f"\n  [轮询] 检查 {sc} 个镜头状态...")
    from task_tracker import list_tasks
    tasks_cache = list_tasks(project)
    shot_ids = list(range(1, sc + 1))
    shots_to_resubmit = []
    past_error_cats = {}
    for sid in shot_ids:
        if is_video_done(project, sid):
            continue
        has_task = False
        past_error = ""
        if tasks_cache:
            for t in tasks_cache:
                if str(t.get("_seq", "")) == str(sid):
                    if t.get("task_id", ""):
                        has_task = True
                        break
                    past_error = t.get("error_cat") or ""
        if not has_task:
            shots_to_resubmit.append(sid)
            past_error_cats[sid] = past_error
    
    if shots_to_resubmit:
        _log(f"  ⚠️ {len(shots_to_resubmit)} 个 shot 无 task_id，策略性重提: {shots_to_resubmit}")
        script = load_script(project)
        for sid in shots_to_resubmit:
            error_cat = past_error_cats.get(sid, "")
            regen = error_cat in ("invalid_image", "bad_request")
            _resubmit_shot(project, sid, script, _cp(project), 0, regen_first_frame=regen)
    
    _, all_completed = _poll_shots(project)
    
    state = {"last_poll_at": now, "next_poll_at": now + 600}
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f)
    
    if all_completed:
        _log("\n  🎬 所有镜头完成，即时拼接...")
        script = load_script(project)
        output_dir = _p(project)["output"]
        os.makedirs(output_dir, exist_ok=True)
        final_path = os.path.join(output_dir, "final.mp4")
        try:
            from stitch import StitcherRegistry
            StitcherRegistry.run_first(project, shot_count=sc)
            _log(f"  ✅ 拼接完成: {final_path}")
        except Exception as e:
            _log(f"  ⚠️ 拼接失败: {e}")
    
    return all_completed


def _cmd_stitch(project: str, tracker: str = "feishu") -> Optional[str]:
    """独立拼接：直接调用 StitcherRegistry.run_first，不重新提交/轮询。
    流程：HF 渲染无字幕版 → ffmpeg 烧录分段字幕 + 混音 → CRF18 final.mp4
    """
    from task_tracker import init_tracker
    init_tracker(project, tracker)
    sc = _shot_count(project)
    missing = [i for i in range(1, sc + 1) if not is_video_done(project, i)]
    if missing:
        _log(f"⚠️ 以下镜头视频缺失，无法拼接: {missing}")
        return None
    _log(f"🎬 开始独立拼接（共 {sc} 个镜头）...")
    try:
        from stitch import StitcherRegistry
        out = StitcherRegistry.run_first(project, shot_count=sc)
        if out:
            _log(f"✅ 拼接完成: {out}")
        else:
            _log("⚠️ 拼接失败（无可用 Provider 或渲染失败）")
        return out
    except Exception as e:
        _log(f"⚠️ 拼接异常: {e}")
        return None


# ═══════════════════════════════════════════════════════════════
# shot 信息查询 / 参考图解析（供 BaseProvider 委托调用）
# ═══════════════════════════════════════════════════════════════

def get_shot_mode(script: dict, shot_id: int) -> str:
    """获取 shot 的生成模式。"""
    for s in script.get("shots", []):
        if s.get("id") == shot_id:
            return s.get("generation", {}).get("mode", "standard")
    return "standard"


def get_shot_info(script: dict, shot_id: int, mode: str = "standard",
                  project: str = "") -> dict:
    """提取 shot 的视频生成参数（prompt/duration/mode）。"""
    for s in script.get("shots", []):
        if s.get("id") == shot_id:
            gen = s.get("generation", {})
            return {
                "prompt": gen.get("prompt_meta", s.get("description", "")),
                "duration": s.get("duration", 5),
                "mode": gen.get("mode", mode),
            }
    return {"prompt": "", "duration": 5, "mode": mode}


def ref_image(project: str, shot_id: int) -> str | None:
    """获取 shot 的视频参考图路径（首帧图）。"""
    path = os.path.join(project, "images", "storyboard",
                        f"shot_{shot_id:02d}_first_frame.png")
    if os.path.isfile(path):
        return path
    return None


def resolve_ref_images(project: str, script: dict, shot_id: int) -> list[str]:
    """解析 shot 的所有参考图路径（dict 格式 key→path / list 格式 path 列表）。"""
    for s in script.get("shots", []):
        if s.get("id") != shot_id:
            continue
        refs = s.get("generation", {}).get("reference_images", {})

        # dict 格式：{"kf1": "images/xxx.png", "kf2": [...], ...}
        if isinstance(refs, dict):
            resolved = []
            for key, val in refs.items():
                if isinstance(val, str):
                    apath = val if os.path.isabs(val) else os.path.join(project, val)
                    if os.path.isfile(apath):
                        resolved.append(apath)
                elif isinstance(val, list):
                    for item in val:
                        p = item.get("path", item) if isinstance(item, dict) else item
                        apath = p if os.path.isabs(p) else os.path.join(project, p)
                        if os.path.isfile(apath):
                            resolved.append(apath)
            return resolved

        # list 格式：[{"path": "images/xxx.png", ...}, ...]
        if isinstance(refs, list):
            resolved = []
            for ref in refs:
                p = ref.get("path", ref) if isinstance(ref, dict) else ref
                apath = p if os.path.isabs(p) else os.path.join(project, p)
                if os.path.isfile(apath):
                    resolved.append(apath)
            return resolved
    return []
