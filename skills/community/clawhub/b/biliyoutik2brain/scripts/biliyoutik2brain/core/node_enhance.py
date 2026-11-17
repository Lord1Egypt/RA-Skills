"""
BiliYouTik2Brain — 增强节点

职责：
  1. 编排 enhance_and_analyze 调用（组装各并行节点结果）
  2. P2正反验证（六维动态阈值决策 → 局部重转录 → 双模型交叉验证）
  3. 不触碰 prompt 工程（在 enhance_engine.py）
"""

import os, sys, json, time, re, tempfile, subprocess
from typing import Dict, List, Tuple, Optional

from .schemas import CollectResult
from .slots import acquire_heavy_slot, release_heavy_slot
from .enhance_engine import enhance_and_analyze
from .retry_orchestrator import (
    orchestrate_retry, tri_source_confidence,
)
from .system_monitor import check_system_status


def enhance(text: str, domain: str = "", speaker: Optional[str] = None,
            video_title: str = "", uploader: str = "") -> Dict:
    """旧版修复（保留作为回退）"""
    from biliyoutik2brain.extra.transcription_enhancer import (
        apply_all_corrections, llm_enhance_text,
        _guess_domain, _match_speaker
    )
    from .node_transcribe import _smart_correct
    
    if not domain:
        domain = _guess_domain(video_title, uploader)
    if not speaker:
        speaker = _match_speaker(uploader)
    
    corrected = _smart_correct(text)
    enhanced = llm_enhance_text(corrected, domain=domain, speaker=speaker)
    
    return {"corrected_text": enhanced, "domain": domain, "speaker": speaker}


def analyze(full_text: str) -> Dict:
    """旧版分析（保留作为回退）"""
    from biliyoutik2brain.extra.transcription_enhancer import structured_analysis
    return structured_analysis(full_text)


def _node_enhance(**kw) -> Dict:
    """节点：LLM修复+分析"""
    collect_result = kw.get("collect")
    transcribe_result = kw.get("transcribe", {})
    
    if isinstance(transcribe_result, dict):
        raw_text = transcribe_result.get("text", "")
        low_conf_words = transcribe_result.get("low_conf_words", [])
    else:
        raw_text = str(kw.get("raw_text", ""))
        low_conf_words = kw.get("low_conf_words", [])
    
    if collect_result:
        video_title = collect_result.video.title or ""
        uploader = collect_result.video.uploader or ""
        bvid = collect_result.video.video_id or ""
        video_path = getattr(collect_result, "video_file", "")
    else:
        video_title = str(kw.get("video_title", ""))
        uploader = str(kw.get("uploader", ""))
        bvid = str(kw.get("bvid", ""))
        video_path = str(kw.get("video_path", ""))
    
    raw_segments = transcribe_result.get("segments", []) if isinstance(transcribe_result, dict) else []
    
    # 字幕数据
    subtitle_text = ""
    subtitle_segments = []
    if collect_result and collect_result.subtitle.success:
        subtitle_text = collect_result.subtitle.text
        subtitle_segments = collect_result.subtitle.segments or []
    
    # 并行OCR结果
    ocr_result = kw.get("ocr", {})
    if not isinstance(ocr_result, dict):
        ocr_result = {}
    
    # 音频消音检测
    bleep_text = kw.get("bleep_detect", "")
    if not bleep_text:
        assess_result = kw.get("assess", {})
        if isinstance(assess_result, dict):
            audio_file = assess_result.get("audio_file", "")
            if audio_file and os.path.exists(audio_file):
                try:
                    from biliyoutik2brain.extra.audio_detector import mark_bleeps_in_text
                    bleep_text = mark_bleeps_in_text(audio_file, [])
                except Exception as e:
                    print(f"  [BLEEP] ⚠️ 标注失败: {e}")
    if bleep_text:
        print(f"  [BLEEP] 🔇 {bleep_text.count('[BLEEP]')}个消音段")
    
    print(f"  [LLM] 修复+分析...")
    if not raw_text.strip():
        print("  ⚠️ 文本为空，跳过LLM")
        return {"corrected_text": raw_text, "analysis": {}}
    
    # P1: 内容预览 → 知识检索
    existing_knowledge = ""
    assess_result = kw.get("assess", {})
    if isinstance(assess_result, dict):
        domain_hint = assess_result.get("domain_hint", "")
    else:
        domain_hint = ""
    
    if domain_hint or uploader:
        from .paths import KNOWLEDGE_DIR
        know_dir = KNOWLEDGE_DIR
        if os.path.exists(know_dir):
            u_lower = uploader.lower().replace(" ", "_") if uploader else ""
            for kf in os.listdir(know_dir):
                if u_lower and u_lower in kf.lower():
                    try:
                        with open(os.path.join(know_dir, kf), "r") as f:
                            kcontent = f.read(800)
                            existing_knowledge = kcontent.strip()
                            print(f"  [知识库] 📖 找到已有知识: {kf} ({len(existing_knowledge)}字)")
                    except Exception:
                        pass
                    break
    
    # 获取重活槽位
    acquire_heavy_slot("base")
    try:
        ea = enhance_and_analyze(
            raw_text,
            video_title=video_title,
            uploader=uploader,
            bvid=bvid,
            low_conf_words=low_conf_words or [],
            video_path=video_path,
            raw_segments=raw_segments,
            subtitle_text=subtitle_text,
            subtitle_segments=subtitle_segments,
            ocr_data=ocr_result if ocr_result else None,
            bleep_text=bleep_text,
            existing_knowledge=existing_knowledge,
        )
    finally:
        release_heavy_slot()
    
    # ── Phase 4.2: 概率修正（L5 残留词二次修正，多源投票） ──
    unresolved = ea.get("_unresolved", [])
    if unresolved and uploader:
        try:
            from .probabilistic_correction import probabilistic_correct
            from .speaker_knowledge import get_profile
            
            speaker_profile = get_profile(uploader)
            ocr_persistent = ""
            if isinstance(ocr_result, dict):
                ocr_persistent = ocr_result.get("persistent_text", "")
            if not ocr_persistent and isinstance(ocr_result, dict):
                persistent_list = ocr_result.get("persistent", [])
                if isinstance(persistent_list, list):
                    ocr_persistent = "\n".join(persistent_list)
            
            prob_corrected, prob_corrections = probabilistic_correct(
                text=ea.get("corrected_text", "") or ea.get("_raw_text", ""),
                low_conf_words=unresolved,
                speaker_profile=speaker_profile,
                domain=domain_hint,
                subtitle_text=subtitle_text,
                subtitle_segments=subtitle_segments,
                ocr_persistent=ocr_persistent,
            )
            
            if prob_corrections:
                ea["corrected_text"] = prob_corrected
                # 从 unresolved 中移除已修正的词
                corrected_originals = {c["original"] for c in prob_corrections}
                unresolved = [(w, p) for w, p in unresolved if w not in corrected_originals]
                ea["_unresolved"] = unresolved
                print(f"  [概率修正] ✅ 修正了 {len(prob_corrections)}/{len(corrected_originals)} 处残留")
        except Exception as e:
            print(f"  [概率修正] ⚠️ 跳过: {e}")
    
    # P2: 正反验证 — 六维动态阈值决策
    # 注意：unresolved 已被概率修正更新
    if unresolved and bvid:
        print(f"  [正反验证] 🔄 {len(unresolved)}词残留仍未修复")
        
        from .p2_decision import should_retranscribe
        total_chars = len(ea.get("corrected_text", "") or ea.get("_raw_text", ""))
        avg_quality = assess_result.get("avg_quality", 0.0) if isinstance(assess_result, dict) else 0.0
        chapters = ea.get("analysis", {}).get("chapters", [])
        
        p2_trigger, p2_debug = should_retranscribe(
            unresolved_words=unresolved,
            total_chars=total_chars,
            speech_segments=assess_result.get("speech_segments", []) if isinstance(assess_result, dict) else [],
            avg_quality=avg_quality,
            domain_hint=domain_hint,
            uploader=uploader,
            chapters=chapters,
        )
        
        print(f"  [P2决策] 有效值={p2_debug['effective']:.4f}%, "
              f"阈值={p2_debug['threshold']}%, "
              f"触发={'✅' if p2_trigger else '❌'}")
        if p2_debug.get("domain_coeff", 1) != 1 or p2_debug.get("speaker_coeff", 1) != 1:
            print(f"  [P2决策] 领域系数={p2_debug['domain_coeff']}, "
                  f"说话人系数={p2_debug['speaker_coeff']}")
        
        if p2_trigger:
            audio_file = ""
            if isinstance(assess_result, dict):
                audio_file = assess_result.get("audio_file", "")
            if audio_file and os.path.exists(audio_file):
                # ── Phase 1/2: 三级回退链调度层 ──
                system_status = check_system_status()
                
                retry_result = orchestrate_retry(
                    url=bvid,  # 用video_id代替url
                    video_title=video_title,
                    video_path=video_path,
                    duration_s=assess_result.get("duration_s", 0) if isinstance(assess_result, dict) else 0,
                    collect_result=collect_result if collect_result else kw.get("collect"),
                    assess_result=assess_result if isinstance(assess_result, dict) else {},
                    transcribe_result={"text": raw_text, "segments": raw_segments, "low_conf_words": low_conf_words},
                    enhance_result=ea,
                    system_status=system_status,
                )
                
                if retry_result.get("upgraded_text") and retry_result["upgraded_text"] != ea.get("corrected_text", ""):
                    ea["corrected_text"] = retry_result["upgraded_text"]
                    print(f"  [回退链] ✅ 三级回退链生效: Tier1={retry_result['tier_1_applied']}, Tier2={retry_result['tier_2_applied']}, Tier3={retry_result['tier_3_applied']}")
                
                if retry_result.get("tier_3_applied"):
                    # Tier 3 只是生成账单，具体执行需要用户确认
                    # 这里标记到 ea 中供外部处理
                    ea["_tier_3_bill"] = retry_result.get("cost_bill", {})
    
    # ── 三源融合置信度估算 (Phase 1.3) ──
    subtitle_quality = 0.0
    subtitle_text = ""
    collect_obj = collect_result if collect_result else kw.get("collect")
    if collect_obj:
        subtitle_quality = getattr(getattr(collect_obj, "subtitle", None), "quality", 0.0) or 0.0
        subtitle_text = getattr(getattr(collect_obj, "subtitle", None), "text", "") or ""
    
    ocr_result = kw.get("ocr", {})
    ocr_persistent = ocr_result.get("persistent_text", "") if isinstance(ocr_result, dict) else ""
    
    # 从 assess 获取 whisper 原始置信度
    raw_confidence = 0.5
    if isinstance(assess_result, dict):
        raw_confidence = assess_result.get("avg_quality", 0.5)
    
    confidence = tri_source_confidence(
        raw_confidence=raw_confidence,
        subtitle_quality=subtitle_quality,
        subtitle_text=subtitle_text,
        corrected_text=ea.get("corrected_text", ""),
        ocr_text=ocr_persistent,
        speaker_knowledge=existing_knowledge,
        domain=domain_hint,
    )
    ea["_tri_source_confidence"] = confidence
    ea["overall_confidence"] = confidence["overall_confidence"]
    
    print(f"  [完成] 修复={len(ea.get('corrected_text', ''))}字, "
          f"三源置信度={confidence['overall_confidence']:.2f}, "
          f"明细: {confidence['source_breakdown']}, "
          f"重转录={'有' if ea.get('retranscribed') else '无'}")
    return ea
