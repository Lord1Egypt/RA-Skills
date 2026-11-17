"""
BiliYouTik2Brain — 转录节点

职责：
  1. 原始缓存命中检查 → 跳过whisper
  2. 字幕优先检测（高质量API字幕 → 跳过whisper）
  3. VAD智能分段 / 直接whisper转录
  4. 结果写入原始缓存
  5. 获取/释放重活槽位
"""

import os, sys, json, time, re, tempfile
from typing import Dict, List, Tuple, Optional

from .schemas import CollectResult
from .cache import get_raw_cached, set_raw_cached
from .slots import acquire_heavy_slot, release_heavy_slot


# ── 确定性纠错 ──

def _smart_correct(text: str) -> str:
    """确定性纠错：100%不会错的替换，无需语境判断"""
    text = text.replace("一贴", "一单")
    return text


def _mark_low_confidence(text: str, low_conf_words: List[Tuple[str, float]]) -> str:
    """在文本中对低置信度的词添加【？】标记"""
    if not low_conf_words:
        return text
    
    marked = text
    for word, prob in sorted(low_conf_words, key=lambda x: x[1]):
        if len(word.strip()) <= 1:
            continue
        marked_word = f"【？{word}】"
        if marked_word not in marked:
            marked = marked.replace(word, marked_word, 1)
    
    return marked


def _format_confidence_notes(low_conf_words: List[Tuple[str, float]]) -> str:
    """生成置信度说明，供LLM参考"""
    if not low_conf_words:
        return "所有词置信度正常。"
    
    notes = ["以下词汇whisper识别置信度偏低（<0.5），请重点检查语义合理性："]
    for word, prob in sorted(low_conf_words, key=lambda x: x[1])[:15]:
        notes.append(f"  - 「{word}」置信度={prob}")
    if len(low_conf_words) > 15:
        notes.append(f"  ...还有{len(low_conf_words)-15}个低置信词")
    return "\n".join(notes)


# ── 转录函数 ──

def _vad_transcribe(audio_path: str, duration_s: int, target_batch_dur: int = 600) -> Dict:
    """VAD 智能分段转录：按自然停顿切分 → 逐段 whisper → 合并结果"""
    try:
        from biliyoutik2brain.extra.vad_preprocessor import vad_process, merge_neighbor_segments
    except ImportError:
        from biliyoutik2brain.extra.vad_preprocessor import vad_process, merge_neighbor_segments
    
    from biliyoutik2brain.extra.faster_transcriber import transcribe_full_audio_detailed
    
    print(f"  [VAD] 按自然停顿分段 (batch={target_batch_dur}s说话量)...", flush=True)
    t0 = time.time()
    
    with tempfile.TemporaryDirectory(prefix="vad_") as tmpdir:
        batches = vad_process(audio_path, tmpdir, target_batch_dur=target_batch_dur)
        
        text_parts = []
        all_low_conf = []
        for i, b in enumerate(batches):
            batch_path = b["path"]
            print(f"  [VAD·转录] batch{i+1}/{len(batches)} ({b['speech_dur']:.0f}s说话)...", flush=True)
            seg_text, seg_low_conf, _ = transcribe_full_audio_detailed(
                batch_path, language="zh", confidence_threshold=0.5
            )
            if seg_text.strip():
                text_parts.append(seg_text.strip())
                all_low_conf.extend(seg_low_conf)
        
        merged_text = "\n".join(text_parts)
        vad_time = time.time() - t0
        print(f"  [VAD] 完成: {len(text_parts)}段→{len(merged_text)}字, "
              f"{len(all_low_conf)}个低置信词 ({vad_time:.0f}s)", flush=True)
    
    return {"text": merged_text, "segments": [], "method": "vad", "low_conf_words": all_low_conf}


def transcribe(audio_path: str, duration_s: int = 0, model: str = "base",
                use_vad: bool = False) -> Dict:
    """转录阶段：用faster-whisper转录音频，返回词级置信度"""
    from biliyoutik2brain.extra.faster_transcriber import transcribe_full_audio_detailed
    
    if use_vad:
        return _vad_transcribe(audio_path, duration_s)
    
    text, low_conf_words, raw_segments = transcribe_full_audio_detailed(
        audio_path, language="zh", confidence_threshold=0.5
    )
    return {"text": text, "segments": raw_segments, "method": "full", "low_conf_words": low_conf_words}


def _node_transcribe(**kw) -> Dict:
    """节点：转录"""
    assess_result = kw.get("assess", {})
    collect_result = kw.get("collect")
    bvid = collect_result.video.video_id if collect_result else kw.get("bvid", "")
    
    if isinstance(assess_result, dict):
        audio_file = assess_result.get("audio_file", "") or kw.get("audio_file", "")
        duration_s = assess_result.get("duration_s", 0) or int(kw.get("duration_s", 0))
        route = assess_result.get("route")
        model = route.model if route else kw.get("model", "base")
        use_vad = route.use_vad if route else False
    else:
        audio_file = str(kw.get("audio_file", ""))
        duration_s = int(kw.get("duration_s", 0))
        model = str(kw.get("model", "base"))
        use_vad = False
    
    # 缓存命中 → 跳过转录
    if bvid:
        cached_raw = get_raw_cached(bvid)
        if cached_raw and cached_raw.get("text", ""):
            print(f"  [转录] 📦 命中原始缓存 (bvid={bvid}, {len(cached_raw['text'])}字)")
            return {
                "text": cached_raw["text"],
                "segments": cached_raw.get("segments", []),
                "low_conf_words": cached_raw.get("low_conf_words", []),
                "cached": True,
            }
    
    # 字幕优先检测
    if collect_result and collect_result.subtitle.success:
        st = collect_result.subtitle
        quality = getattr(st, "quality", 0.0) or 0.0
        if quality >= 0.7 and st.text.strip():
            print(f"  [转录] 📝 字幕优先: 质量={quality:.2f} ({len(st.text)}字)")
            return {
                "text": st.text,
                "segments": getattr(st, "segments", []),
                "low_conf_words": [],
                "subtitle_first": True,
            }
        if st.text.strip():
            print(f"  [转录] ⚠️ 字幕质量{quality:.2f}<0.7，降级whisper")
    
    # 获取重活槽位
    acquire_heavy_slot(model)
    try:
        method_str = "VAD智能分段" if use_vad else "直接转录"
        print(f"  [转录] faster-whisper {model} ({duration_s}s) — {method_str}", flush=True)
        tr = transcribe(audio_file, duration_s, model, use_vad=use_vad)
        raw_text = tr.get("text", "")
        if not raw_text.strip():
            print("  ⚠️ 转录结果为空（可能是纯音乐/环境音视频）")
        print(f"  [完成] {len(raw_text)}字, {len(tr.get('low_conf_words', []))}个低置信词")
        
        if bvid and raw_text:
            set_raw_cached(bvid, tr)
        
        return tr
    finally:
        release_heavy_slot()


# ================================================================
# 移植自 ZIP v1.x: node_transcribe.py 扩展内容
# ================================================================

def _merge_with_overlap_dedup(ordered_results: list, overlaps: list) -> str:
    """
    将有序转录结果按overlap对齐拼接，去除重叠部分的重复文本
    
    策略：
    1. 对每对 (batch_i, batch_{i+1})，取前后文本末尾/开头的 overlap_s 秒的转录
    2. 用最长公共序列（LCS）找重复部分
    3. 公共部分只保留一次
    """
    if len(ordered_results) <= 1:
        return ordered_results[0]["text"] if ordered_results else ""
    
    # 构建重叠映射：{batch_idx: overlap_duration_with_next}
    overlap_map = {}
    for ov in overlaps:
        overlap_map[ov["prev_batch"]] = ov["duration"]
    
    parts = []
    for i, result in enumerate(ordered_results):
        text = result["text"]
        if not text:
            continue
        
        if i > 0 and (i - 1) in overlap_map:
            # 当前batch开头与前一个batch末尾有overlap
            ov_dur = overlap_map[i - 1]
            prev_text = ordered_results[i - 1]["text"]
            
            # 取前一个文本末尾 ~200 字符，当前文本开头 ~200 字符
            prev_tail = prev_text[-200:] if len(prev_text) > 200 else prev_text
            curr_head = text[:200] if len(text) > 200 else text
            
            # 找最长公共后缀/前缀（简单滑窗比对）
            overlap_trim = 0
            for win in range(min(50, len(prev_tail), len(curr_head)), 5, -1):
                if prev_tail[-win:] == curr_head[:win]:
                    overlap_trim = win
                    break
            
            if overlap_trim > 0:
                text = text[overlap_trim:]
                print(f"    overlap batch{i-1}→batch{i}: 去除{overlap_trim}字重复")
        
        if text.strip():
            parts.append(text.strip())
    
    return "\n".join(parts)



def _check_noise_before_transcribe(wav_path: str):
    """转录前噪声预检。
    
    接 auto_fixer.noise_precheck()：
    - 高噪声（>-30dB）→ 预计转录时间翻倍，打印预警
    - 不阻断，仅通知
    """
    try:
        from .auto_fixer import noise_precheck
        result = noise_precheck(wav_path)
    except ImportError:
        return  # auto_fixer 不可用，跳过
    
    if result.get("error"):
        print(f"  [噪声预检] ⚠️ 检测失败: {result['error']}")
        return
    
    level = result.get("level", "unknown")
    db = result.get("db", 0)
    est_rft = result.get("estimated_rft", 1.0)
    
    if level == "high":
        print(f"  [噪声预检] 🔴 高噪声 ({db}dB) — 预计RFT×{est_rft:.1f}，转录时间翻倍")
        if result.get("warning"):
            print(f"  [噪声预检] {result['warning']}")
    elif level == "normal":
        print(f"  [噪声预检] 🟡 正常噪声 ({db}dB) — 预计RFT×{est_rft:.1f}")
    else:
        print(f"  [噪声预检] 🟢 低噪声 ({db}dB)")


