"""
BiliYouTik2Brain — 评估节点

职责：
  1. 资源评估（本地算力检查 → 路由决策）
  2. 音频预览（采样检测 + 领域猜测 + VAD分段）
  3. 算力不足 → 排队
"""

import os
from typing import Dict


def _node_assess(**kw) -> Dict:
    """节点：资源评估"""
    collect_result = kw.get("collect")
    if collect_result:
        duration_s = collect_result.video.duration
        audio_file = collect_result.audio.file_path or ""
        url = collect_result.video.url or kw.get("url", "")
    else:
        duration_s = int(kw.get("duration_s", 0))
        audio_file = str(kw.get("audio_file", ""))
        url = str(kw.get("url", ""))
    
    print(f"  [评估] 时长={duration_s}s")
    from .config import assess_and_route
    from .system_monitor import check_system_status
    system_status = check_system_status()
    route = assess_and_route(duration_s, local_available=False, system_status=system_status)
    if route.target == "pending":
        print(f"  ⚠️ 算力不足: {route.reason}")
        from .config import add_pending
        wf_id = add_pending(url, duration_s, route.estimated_workload,
                          notes=f"需要{route.required_cores}核/{route.required_ram_gb}GB")
        return {"pending": True, "wf_id": wf_id, "route": route}
    
    sample_texts = []
    domain_hint = ""
    speech_segments = []
    avg_quality = 0.0
    if audio_file:
        from .assessor import assess_audio
        assmnt = assess_audio(audio_file, duration_s)
        route.model = assmnt["model"]
        sample_texts = assmnt.get("sample_texts", [])
        speech_segments = assmnt.get("speech_segments", [])
        avg_quality = assmnt.get("avg_quality", 0.0)
        if sample_texts:
            from biliyoutik2brain.extra.transcription_enhancer import _guess_domain
            collect_result = kw.get("collect")
            uploader_str = collect_result.video.uploader if collect_result else ""
            domain_hint = _guess_domain(uploader=uploader_str)
            print(f"  [预览] {len(sample_texts)}个采样点, 领域={domain_hint or '未知'}")
    
    print(f"  [路由] {route.target} | 模型: {route.model}")
    if route.use_vad:
        print(f"  [VAD] ✅ 智能分段已启用")
    
    return {
        "pending": False, "route": route,
        "duration_s": duration_s, "audio_file": audio_file,
        "sample_texts": sample_texts, "domain_hint": domain_hint,
        "speech_segments": speech_segments,
        "avg_quality": avg_quality,
        "system_status": system_status,  # Phase 2.1: 供下游2.4决策
    }
