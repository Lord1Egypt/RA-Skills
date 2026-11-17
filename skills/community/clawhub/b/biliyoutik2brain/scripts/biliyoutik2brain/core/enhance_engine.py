"""
BiliYouTik2Brain — 增强引擎

职责单一：接收原始转录文本，输出修正文本+结构化分析。
不做编排（由 node_enhance.py 负责编排）。

v3 改造关键原则：
  ✓ 代码做确定的事 → 确定性词典修复、置信度计算、回归检查、Gotcha过滤
  ✓ 提示词做不确定的事 → 语义修复（LLM）、结构化分析（LLM）
  ✓ 所有LLM产出必须经exit.py验证后才能应用
"""

import os, json, time, re, math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field  # 移植自 ZIP v1.9.1

from .schemas import TranscriptionResult
from .secrets import get_llm_config
from .cache import get_llm_cached, set_llm_cached, get_raw_cached
from .node_transcribe import _smart_correct, _mark_low_confidence, _format_confidence_notes


# ═══════════════════════════════════════════════════════════════
# 增强引擎（enhance_and_analyze）
# ═══════════════════════════════════════════════════════════════

_LLM_CONFIG_LOADED = False
DEEPSEEK_API_KEY = None
DEEPSEEK_BASE = None
LLM_MODEL = None


def _ensure_llm_config():
    global _LLM_CONFIG_LOADED, DEEPSEEK_API_KEY, DEEPSEEK_BASE, LLM_MODEL
    if _LLM_CONFIG_LOADED:
        return
    key, base, model = get_llm_config()
    DEEPSEEK_API_KEY = key
    DEEPSEEK_BASE = base
    LLM_MODEL = model
    _LLM_CONFIG_LOADED = True


def _condense_for_analysis(full_text: str, max_chars: int = 1500) -> str:
    """摘录式输入，避免注意力衰减"""
    if not full_text:
        return ""
    head = full_text[:600]
    tail = full_text[-300:] if len(full_text) > 600 else ""
    lines = full_text.split("\n")
    markers = [l for l in lines if any(m in l for m in ["【", "|", "关键词", "核心", "总结"])]
    markers_text = "\n".join(markers[:3])
    parts = [head]
    if markers_text and len(markers_text) < max_chars // 2:
        parts.append(f"\n--- 重点标记 ---\n{markers_text}")
    if tail:
        parts.append(f"\n--- 结尾 ---\n{tail}")
    return "\n".join(parts)[:max_chars]


def enhance_and_analyze(
    text: str,
    video_title: str = "",
    uploader: str = "",
    bvid: str = "",
    domain: str = "",
    speaker: str = "",
    low_conf_words: Optional[List[Tuple[str, float]]] = None,
    video_path: str = "",
    raw_segments: Optional[List[Dict]] = None,
    subtitle_text: str = "",
    subtitle_segments: Optional[List[Dict]] = None,
    ocr_data: Optional[Dict] = None,
    bleep_text: str = "",
    existing_knowledge: str = "",
) -> Dict:
    """合并修复+分析：1次LLM调用（v3重构版）
    
    代码做确定性纠错 + 上下文组装 → 1次LLM调用输出修正文本+分析。
    """
    _ensure_llm_config()
    
    from biliyoutik2brain.extra.transcription_enhancer import (
        _guess_domain, _match_speaker
    )
    
    # 1) 纠错词典优先
    if not domain:
        domain = _guess_domain(video_title, uploader)
    if not speaker:
        speaker = _match_speaker(uploader)
    corrected = _smart_correct(text)
    title_salt = video_title
    
    # 2) 查缓存
    if bvid:
        cached = get_llm_cached(bvid, domain, speaker, title_salt)
        if cached:
            raw_valid = True
            if bvid:
                raw_ck = get_raw_cached(bvid)
                if not raw_ck or not raw_ck.get("text", ""):
                    raw_valid = False
            if raw_valid:
                print(f"  [缓存] 命中! 跳过LLM调用")
                return {
                    "corrected_text": cached["corrected_text"],
                    "analysis": cached["analysis"],
                    "domain": domain,
                    "speaker": speaker,
                }
    
    # 3) 说话人专属纠错备注
    speaker_note = ""
    from biliyoutik2brain.extra.transcription_enhancer import _speaker_corrections_text
    speaker_note = _speaker_corrections_text(text, speaker)
    
    # 4) 说话人知识库注入（含wiki同领域关联知识）
    from .speaker_knowledge import format_context
    speaker_context = format_context(speaker, video_title, domain)
    
    # 5) 标记低置信度词
    confidence_notes = _format_confidence_notes(low_conf_words or [])
    marked_text = _mark_low_confidence(corrected, low_conf_words or [])
    
    # 5.5) P0 质量门
    skip_ocr = not (low_conf_words and video_path and os.path.exists(video_path) and raw_segments)
    if skip_ocr and video_path:
        print(f"  [质量门] 无低置信词，跳过OCR")
    
    ocr_persistent = ""
    ocr_timeline = []
    
    if ocr_data:
        ocr_timeline = ocr_data.get("timeline", [])
        ocr_persistent = ocr_data.get("persistent_text", "")
        if ocr_timeline or ocr_persistent:
            print(f"  [OCR] 📦 使用预计算结果: {len(ocr_timeline)}帧, {len(ocr_persistent)}条持久文字")
        skip_ocr = True
    
    if not skip_ocr:
        try:
            from biliyoutik2brain.extra.ocr_video import ocr_video_targeted, cleanup
            from biliyoutik2brain.extra.transcription_enhancer import get_persistent_text
            
            problem_timestamps = []
            for word, prob in (low_conf_words or []):
                for seg in (raw_segments or []):
                    if word in seg.get("text", ""):
                        midpoint = (seg.get("start", 0) + seg.get("end", 0)) / 2
                        problem_timestamps.append(midpoint)
                        break
            
            if problem_timestamps:
                problem_timestamps = sorted(set(round(ts, 1) for ts in problem_timestamps))
                print(f"  [OCR] 低置信词时间戳: {len(problem_timestamps)}个 → 精准抽帧")
                ocr_data = ocr_video_targeted(video_path, timestamps=problem_timestamps, window_pad=1.0)
                ocr_timeline = ocr_data.get("timeline", [])
                ocr_persistent = get_persistent_text(ocr_data)
                if ocr_timeline or ocr_persistent:
                    print(f"  [OCR] ✅ {len(ocr_timeline)}帧画面, {len(ocr_persistent)}条固定文字")
                cleanup()
            else:
                print(f"  [OCR] 无法对齐时间戳，跳过")
        except Exception as e:
            print(f"  [OCR] ⚠️ 失败: {e}")
    
    # 5.75) 时间线对齐融合 (Phase 3.4)
    align_result = None
    if raw_segments and (subtitle_segments or ocr_timeline):
        try:
            from .timeline_aligner import align_for_enhancement
            align_result = align_for_enhancement(
                raw_segments=raw_segments,
                subtitle_segments=subtitle_segments or [],
                ocr_timeline=ocr_timeline or [],
            )
            if align_result and align_result.get("alignment_report"):
                print(f"  [对齐] 📐 {align_result['alignment_report']}")
                if align_result.get("conflict_texts"):
                    print(f"  [对齐] ⚠️ {len(align_result['conflict_texts'])}段内容冲突")
        except Exception as e:
            print(f"  [对齐] ⚠️ 对齐失败: {e}")
            align_result = None
    
    # 6) 构建LLM prompt
    user_prompt_parts = [f"""请修复以下转录文本并进行结构化分析。

## 视频上下文
标题：{video_title}
UP主：{uploader or "未知"}

{speaker_note}"""]

    if align_result and align_result.get("alignment_report"):
        report = align_result["alignment_report"]
        user_prompt_parts.append(f"""
## 多源时间线对齐报告
以下是对 Whisper/字幕/OCR 三个转录源的时间轴对齐结果摘要：
{report}
""")
        # 如果有跨源冲突段，通知LLM
        conflict_texts = align_result.get("conflict_texts", [])
        if conflict_texts:
            lines = [f"⚠️ 以下 {len(conflict_texts)} 段存在跨源内容冲突："]
            for i, ct in enumerate(conflict_texts[:5]):
                lines.append(f"  [{i+1}] {ct[:80]}")
            lines.append("（冲突段需判断哪个源更可信）")
            user_prompt_parts.append("\n".join(lines))

    if speaker_context:
        user_prompt_parts.append(speaker_context)
    
    # ── Phase 4.1: 模糊音混淆矩阵注入（记题型不记题目） ──
    fuzzy_rules_text = ""
    try:
        from .fuzzy_confusion import format_rules_for_prompt
        fuzzy_rules_text = format_rules_for_prompt(domain=domain, speaker=speaker)
        if fuzzy_rules_text:
            user_prompt_parts.append(fuzzy_rules_text)
    except Exception as e:
        pass  # 混淆矩阵不是关键路径，静默跳过
    
    if ocr_persistent:
        user_prompt_parts.append(f"""
## 视频画面固定文字（贯穿全视频，非逐字口语内容）
以下文字全程显示在画面上（如视频标题、说话人身份），属于视频元信息而非说话人的口语内容。
它们仅用于理解视频场景背景，**不用于逐词对照**。

{ocr_persistent}""")
    
    if ocr_timeline and low_conf_words and raw_segments:
        from biliyoutik2brain.extra.transcription_enhancer import build_ocr_aligned_section
        aligned_section = build_ocr_aligned_section(
            low_conf_words, raw_segments, ocr_timeline, ocr_persistent, full_text=corrected,
        )
        if aligned_section:
            user_prompt_parts.append(aligned_section)
    elif ocr_persistent:
        user_prompt_parts.append("""
注意：上述视频画面固定文字是从视频帧中提取的。如果转录文本中的人名、术语与画面不符，以画面文字为准。""")
    
    if subtitle_text or subtitle_segments:
        sub_lines = ["## 同期官方字幕参考（有时间戳）"]
        if subtitle_segments:
            for seg in subtitle_segments[:100]:
                start_s = float(seg.get("start", 0))
                end_s = float(seg.get("end", 0))
                sub_lines.append(f"[{int(start_s//60):02d}:{int(start_s%60):02d}-{int(end_s//60):02d}:{int(end_s%60):02d}] {seg.get('text','')}")
        elif subtitle_text:
            sub_lines.append(f"完整字幕：\n{subtitle_text[:2000]}")
        sub_lines.append("")
        user_prompt_parts.append("\n".join(sub_lines))
    
    if bleep_text:
        user_prompt_parts.append(bleep_text + "\n")
    
    # 7) 层次化修正（v1.8.2+）
    result = {
        "original_text": text,
        "corrected_text": corrected,
        "analysis": {"summary": "", "keywords": [], "chapters": [], "topics": []},
        "domain": domain,
        "speaker": speaker,
    }
    
    from .corrector_engine import correct_transcription as engine_correct
    from .corrector_dictionary import fast_domain_correct
    from biliyoutik2brain.extra.transcription_enhancer import structured_analysis
    
    lcw_list = list(low_conf_words) if low_conf_words else []
    
    import concurrent.futures as cf
    
    quick_corrected = _smart_correct(text)
    condensed_input = _condense_for_analysis(quick_corrected)
    
    ocr_context_str = ""
    if ocr_persistent:
        ocr_context_str = f"视频画面固定文字:\n{ocr_persistent[:600]}"
        if ocr_timeline:
            ocr_lines = []
            for frame in ocr_timeline[:30]:
                ts = frame.get("timestamp", 0)
                ft = frame.get("text", "")
                if ft:
                    ocr_lines.append(f"[{int(ts//60):02d}:{int(ts%60):02d}] {ft}")
            ocr_context_str += "\n画面帧文字:\n" + "\n".join(ocr_lines[:10])
    
    with cf.ThreadPoolExecutor(max_workers=2) as pool:
        corr_future = pool.submit(
            engine_correct,
            text=text,
            segments=raw_segments or [],
            low_conf_words=lcw_list,
            bvid=bvid,
            enable_ocr=False,
            l2_max_words=10,
            speaker_knowledge=existing_knowledge,
            ocr_context=ocr_context_str,
        )
        
        analysis_future = pool.submit(structured_analysis, quick_corrected[:8000])
        
        corr_result = corr_future.result()
        
        if corr_result.get("corrected_text") and corr_result["corrected_text"] != text:
            result["corrected_text"] = corr_result["corrected_text"]
            result["corrections"] = corr_result.get("corrections", [])
            app_count = len([c for c in corr_result.get("corrections", [])
                           if c.get("original") != c.get("corrected")])
            print(f"  [层次修正] ✅ {app_count}修正, "
                  f"置信度={corr_result.get('final_confidence', 0):.2f}, "
                  f"回归={'✅' if corr_result.get('regression_passed', True) else '❌'}")
        else:
            result["corrected_text"] = fast_domain_correct(text)
            result["corrections"] = corr_result.get("corrections", [])
            print(f"  [层次修正] 管线无修正, 确定性词典兜底")
        
        # P2追踪
        l5_words = corr_result.get("l5_unresolved_words", [])
        if l5_words:
            result["_unresolved"] = list(set(l5_words))
        
        try:
            analysis_result = analysis_future.result(timeout=90)
            if analysis_result:
                result["analysis"] = analysis_result
        except Exception:
            pass
    
    # ── 8) 代码收口层（v3新增）：代码做最终裁决 ──
    # LLM产出的修正结果已由 __init__.py 的 exit.py 验证
    # 这里再加一层跨源一致性评分（由代码计算，不依赖LLM）
    _final_code_check(result, lcw_list)
    
    # 写缓存
    if bvid:
        set_llm_cached(bvid, domain, speaker, result, title_salt)
    
    return result


def _final_code_check(result: Dict, low_conf_words: List[Tuple[str, float]]) -> None:
    """代码收口层：做代码确定的事，不做LLM不确定的事
    
    1. 高置信词保护：原始置信度≥0.9的词不应该被修正
    2. 修正前后长度变化合理性
    3. 置信度评分由代码根据修正比例和原始置信度计算
    """
    corrections = result.get("corrections", [])
    if not corrections or not low_conf_words:
        return
    
    corrected_text = result.get("corrected_text", "")
    
    # 子检查1: 高置信词保护
    high_conf_words = {w for w, c in low_conf_words if c >= 0.9}
    protected_violations = []
    for corr in corrections:
        if corr.get("original") in high_conf_words and corr.get("corrected") != corr.get("original"):
            protected_violations.append(corr.get("original"))
    
    if protected_violations:
        print(f"  [代码收口] ⚠️ {len(protected_violations)}个高置信词被修正: {protected_violations[:3]}")
    
    # 子检查2: 修正前后的长度变化合理性（跟原始文本对比）
    original_for_compare = result.get("original_text", "")
    if original_for_compare and corrected_text:
        len_ratio = len(corrected_text) / max(len(original_for_compare), 1)
        if len_ratio < 0.8 or len_ratio > 1.2:
            print(f"  [代码收口] ⚠️ 文本长度变化异常: {len(original_for_compare)}→{len(corrected_text)} ({len_ratio:.2f}x)")
    
    # 子检查3: 代码计算置信度
    avg_raw_conf = sum(c for _, c in low_conf_words) / max(len(low_conf_words), 1)
    app_count = len([c for c in corrections if c.get("original") != c.get("corrected")])
    fix_ratio = app_count / max(len(low_conf_words), 1)
    
    # 原始平均置信度作为锚点，修正越多下调越多
    code_computed_conf = avg_raw_conf - (fix_ratio * 0.1)
    code_computed_conf = max(0.3, min(0.99, code_computed_conf))
    
    result["_code_computed_confidence"] = round(code_computed_conf, 3)
    print(f"  [代码收口] 代码置信度={code_computed_conf:.3f} (avg_raw={avg_raw_conf:.3f}, fix_ratio={fix_ratio:.3f})")
# ================================================================# 移植自 ZIP v1.9.1: 三分级分类 + 格式修复 + 语义风险检测# ================================================================@dataclass
class SegmentClass:
    """文本段落分类结果"""
    text: str
    grade: str  # "A"高置信 "B"中置信 "C"低置信
    avg_confidence: float
    min_confidence: float
    word_count: int
    raw_text: str = ""  # 原始转录文本（在分级后填充）
    start_pos: int = 0  # 在全文中的起始位置


def _classify_segments(
    text: str,
    token_confidences: List[Tuple[str, float, int]],
    raw_segments: List[Dict],
) -> Tuple[List[SegmentClass], float]:
    """按 token 置信度将全文切为 A(高)/B(中)/C(低) 三级段落

    置信度来源优先级（自动检测）：
      1. token_confidences — faster-whisper 原生词级置信度
      2. raw_segments[].pseudo_confidence — whisper.cpp adapter 伪置信度
      3. 回退(B级全量) — 无任何置信度可用

    阈值（基于豆包AI建议）：
      - A级：avg_conf > 0.95 —— 高置信，仅需格式修复
      - B级：avg_conf 0.80-0.95 —— 中置信，L1+L2 纠正
      - C级：avg_conf < 0.80 —— 低置信，完整五层

    Returns:
        (segments, overall_quality) — 分类结果和全局质量分
    """

    def _fallback_single_segment(txt: str, grade: str = "B", conf: float = 0.90) -> Tuple[List, float]:
        wc = len(txt.replace("\n", "")) if txt else 1
        return [SegmentClass(
            text=txt, grade=grade, avg_confidence=conf,
            min_confidence=conf, word_count=wc, raw_text=txt
        )], conf

    # ═══ 来源2: whisper.cpp pseudo_confidence（优先，不依赖token位置匹配） ═══
    # 注意：来源2必须在来源1之前！规则引擎前置修正会篡改 text 内容，
    # 导致 token_confidences 里的词和修正后的 text 对不上。
    # pseudo_confidence 是段级信号，不依赖具体词位置 → 规则修正后依然有效。
    if raw_segments:
        has_pseudo = any(
            s.get("pseudo_confidence") is not None
            for s in raw_segments[:5]
        )
        if has_pseudo:
            segments = []
            for seg in raw_segments:
                seg_text = seg.get("text", "")
                conf = seg.get("pseudo_confidence", 0.90)
                wc = len(seg_text.replace("\n", ""))

                if conf > 0.95:
                    grade = "A"
                elif conf >= 0.80:
                    grade = "B"
                else:
                    grade = "C"

                segments.append(SegmentClass(
                    text=seg_text, grade=grade,
                    avg_confidence=conf, min_confidence=conf,
                    word_count=wc, raw_text=seg_text
                ))

            a_count = sum(1 for s in segments if s.grade == "A")
            c_count = sum(1 for s in segments if s.grade == "C")
            total = len(segments) if segments else 1
            overall = (a_count / total) * 0.5 + (1 - c_count / total) * 0.5
            overall = round(overall, 3)

            print(f"  [分级] pseudo_confidence 来源: A={a_count} B={total-a_count-c_count} C={c_count}")
            return segments, overall

    # ═══ 来源1: 原生 token_confidences（faster-whisper 词级置信度） ═══
    if token_confidences and raw_segments:
        has_real_conf = any(
            isinstance(tc, tuple) and len(tc) >= 2 and
            isinstance(tc[1], (int, float)) and not (isinstance(tc[1], float) and math.isnan(tc[1]))
            for tc in token_confidences[:10]
        )
        if has_real_conf:
            seg_words = {}
            for word, prob, seg_idx in token_confidences:
                if seg_idx not in seg_words:
                    seg_words[seg_idx] = []
                seg_words[seg_idx].append((word, prob))

            segments = []
            for seg in raw_segments:
                seg_text = seg.get("text", "")
                seg_idx_raw = raw_segments.index(seg)
                words = seg_words.get(seg_idx_raw, [])
                if not words:
                    avg_conf = 0.90; min_conf = 0.90
                    wc = len(seg_text.replace("\n", ""))
                else:
                    probs = [p for _, p in words]
                    avg_conf = sum(probs) / len(probs)
                    min_conf = min(probs)
                    wc = len(words)
                grade = "A" if avg_conf > 0.95 else ("B" if avg_conf >= 0.80 else "C")
                segments.append(SegmentClass(
                    text=seg_text, grade=grade, avg_confidence=round(avg_conf, 3),
                    min_confidence=round(min_conf, 3), word_count=wc,
                    raw_text=seg_text
                ))
            a_count = sum(1 for s in segments if s.grade == "A")
            c_count = sum(1 for s in segments if s.grade == "C")
            total = len(segments) if segments else 1
            overall = (a_count / total) * 0.5 + (1 - c_count / total) * 0.5
            return segments, round(overall, 3)

    # ═══ 来源3: 回退 ═══
    if not raw_segments:
        return _fallback_single_segment(text)

    segments = []
    for seg in raw_segments:
        seg_text = seg.get("text", "")
        wc = len(seg_text.replace("\n", ""))
        segments.append(SegmentClass(
            text=seg_text, grade="B", avg_confidence=0.90,
            min_confidence=0.90, word_count=wc, raw_text=seg_text
        ))
    a_count = sum(1 for s in segments if s.grade == "A")
    c_count = sum(1 for s in segments if s.grade == "C")
    total = len(segments) if segments else 1
    overall = (a_count / total) * 0.5 + (1 - c_count / total) * 0.5
    return segments, round(overall, 3)


def _refresh_token_confidences(
    original_text: str,
    corrected_text: str,
    token_confidences: List[Tuple[str, float, int]],
) -> List[Tuple[str, float, int]]:
    """规则引擎预修正后刷新 token 置信度

    对 fast_domain_correct 修正命中的字词，将其 token 置信度抬高至 ≥0.95，
    使其在后续分级中自动升入 A 级，避免已修正内容重复进入 LLM 矫正。

    Returns:
        新的 token_confidences 列表
    """
    if not token_confidences or original_text == corrected_text:
        return token_confidences

    new_confs = []
    corrected_chars = set()
    for (wrong, correct) in _get_domain_corrections().items():
        if wrong in original_text and wrong not in corrected_text:
            corrected_chars.update(wrong)

    for word, prob, seg_idx in token_confidences:
        # 如果该词被规则修改过，抬高置信度
        if word in corrected_chars or any(c in word for c in corrected_chars if len(c) >= 2):
            new_confs.append((word, max(prob, 0.95), seg_idx))
        else:
            new_confs.append((word, prob, seg_idx))

    return new_confs


def _get_domain_corrections() -> Dict[str, str]:
    """返回 DOMAIN_CORRECTIONS 字典（延迟导入避免循环依赖）"""
    from .corrector_dictionary import DOMAIN_CORRECTIONS
    return DOMAIN_CORRECTIONS


def _format_fix(text: str) -> str:
    """纯规则格式修复：标点归一化、段落合并（不调LLM）

    用于 A 级高置信段落——文本内容已经正确，只需格式美化。
    """
    if not text.strip():
        return text

    # 0. 繁体→简体转换（v2.1.0）
    try:
        from opencc import OpenCC
        text = OpenCC('t2s').convert(text)
    except ImportError:
        pass

    # 1. 中英文标点归一化
    text = re.sub(r'[，,]', '，', text)
    text = re.sub(r'[。.]', '。', text)
    text = re.sub(r'[！!]', '！', text)
    text = re.sub(r'[？?]', '？', text)
    text = re.sub(r'[：:]', '：', text)

    # 2. 标点重复清理
    text = re.sub(r'([，。！？：]){2,}', r'\1', text)

    # 3. 句首去空格
    text = re.sub(r'^\s+', '', text)

    # 4. 段落合并（连续无标点短句拼接）
    lines = text.split('\n')
    merged = []
    buf = ""
    for line in lines:
        line = line.strip()
        if not line:
            if buf:
                merged.append(buf)
                buf = ""
            continue
        # 以句号/问号/感叹号结尾 → 自然断句
        if buf and (buf.endswith(('。', '！', '？', '：')) or len(buf) > 80):
            merged.append(buf)
            buf = line
        else:
            buf = (buf + line) if buf else line
    if buf:
        merged.append(buf)

    return '\n'.join(merged)


def _detect_semantic_risks(text: str) -> List[Dict]:
    """P1: 语义风险检测——识别需要定向校验的高风险片段

    检测四类高风险模式：
      1. 否定词（不/没/无/别/从未） —— 可能被whisper漏掉或误加
      2. 同音异义词（的/得/地、在/再、他/她/它） —— 易混
      3. 数字+单位（百分比/金额/时间） —— 错一位就变意思
      4. 人名/地名/专有名词 —— 高频同音错误

    Returns: [{"type": "negation", "text": "...", "position": 120}, ...]
    """
    risks = []

    # 1. 否定词检测 — 句中出现否定词的句子
    negation_words = r'(不|没|无|别|从未|绝不|毫不|毫无|并非)'
    for m in re.finditer(r'[^。！？\n]*?' + negation_words + r'[^。！？\n]*[。！？]', text):
        risks.append({
            "type": "negation",
            "text": m.group().strip(),
            "position": m.start(),
        })

    # 2. 同音异义词检测
    homophone_patterns = [
        (r'(?<=[^的])的(?=[^确话])', '的/得/地'),
        (r'\b在\b', '在/再'),
        (r'\b他\b', '他/她/它'),
    ]
    for pattern, desc in homophone_patterns:
        for m in re.finditer(pattern, text):
            risks.append({
                "type": "homophone",
                "text": m.group(),
                "position": m.start(),
                "note": desc,
            })

    # 3. 数字+单位组合
    num_unit = re.finditer(r'\d+\.?\d*\s*[万亿千百%％点倍秒分时日年月元刀美元港币块]', text)
    for m in num_unit:
        risks.append({
            "type": "number_unit",
            "text": m.group(),
            "position": m.start(),
        })

    # 4. 大写+组合（可能是专有名词/人名）
    proper_noun = re.finditer(r'[A-Z\u4e00-\u9fff]{2,}(?:[·\-][A-Z\u4e00-\u9fff]+)+', text)
    for m in proper_noun:
        risks.append({
            "type": "proper_noun",
            "text": m.group(),
            "position": m.start(),
        })

    return risks


# == 移植自 ZIP v1.9.1: LLM System Prompt ==
COMBINED_SYSTEM_PROMPT = """你是一个专业的【转录分析师】，需要同时完成两项任务：

## 任务A：修复转录文本
原始文本来自语音识别（whisper），存在同音错字、断句错误。
请复原为通顺的中文文本。

### 🎯 置信度标注说明
文本中用【？】标记了whisper识别置信度较低的词，例如：
  「【？阻力】结构没有办法通过」→ 正确应为「阻力结构」

这些【？】标记只是提示，请结合上下文语义判断最终用词。

### ⚠️ 常识检查（重要！）
修复时同步检查以下内容，发现明显错误直接修正：
- **时间顺序**：不会出现"1月3号之后又出现1月2号"这种倒流
- **数字合理性**："3274点"合理，"3724点"可能就是顺序错了
- **因果关系**："因为A所以B"逻辑要通，不通可能是whisper听错
- **专业名词**：以交易领域实际术语为准
- **whisper重复卡词**：同一词组连续出现3次以上（如"通过法"×11），是whisper卡环问题，应精简为1~2次

### 🧬 三源交叉验证（v1.8.1 多模态融合）
你有三个信源来确认转录是否正确：
1. **whisper 词级置信度** — 低置信词标记为【？】，优先查看
2. **官方字幕参考** — 如有字幕段（带时间戳），字幕是第三方确认的文本，可信度较高
3. **画面 OCR 文字** — 视频帧中的固定文字（标题、图表标签、ppt文字），最可靠但只覆盖部分内容

**融合原则**：
- 字幕和OCR都确认的词 → 即使whisper低置信，也可放心修正
- 字幕确认但OCR无结果 → 以字幕为准（字幕来源独立于语音）
- OCR有但字幕无 → OCR画面文字确认的词优先
- 三个信源都不一致 → 保留whisper原始文本标记【？】
- 最终 confidence_score 应综合三个信源的一致性来评定

### 🔧 交易领域常见纠错（按类别，结合上下文判断）
**同音字群（总是替换）**：
  拼罢/拼盼→Pinbar、运线/晕线→孕线（or均线看语境）
  脏色→止损、阴力→盈利、扛单→扛单

**语境敏感（需要判断上下文）**：
  1. 主力结构/位/区/过→阻力结构/位/区/过（技术术语语境）
     主力吸筹/买入/出货/抢货→保留"主力"（大资金方语境）
  2. 尺寸→止损（在讲**止损金额/位置**的语境下）
  3. 排单→卖单（在讲**阻力区/供给区**的语境下）
  4. 深证→恒生（在讲**香港/国际指数**的语境下）
  5. 二看→你看（在**对话开头**的语境下）
  6. 牛逼手→牛逼之处（在**评价能力/特性**的语境下）

**说话人专属纠错（张聚贤视频中常见）**：
  图行之死扛→图形止损法、十之间之神→时间止损法
  三榜/三绑→三宝（胖杰克的三宝体系）
  模绩→逻辑（"底层的模绩"→"底层的逻辑"）
  攻击需求→供给需求、描组→描述、回事性→滞后性

### 行话保留
- 交易单位"刀"不修改（如"500刀"）
- "需求区""供给区""机构订单原理"等交易术语保留原词

### 🚫 边界规则（v1.12.0 新增 — 果叔模式）

**严格禁止**：
- ❌ **禁止编造内容** — 只修复语音识别错误，不添加原文中没有的信息
- ❌ **禁止补充信息** — 不用你"知道"的背景知识去补充原文
- ❌ **禁止修改数据** — 原文中的数字、百分比、价格等一律保留原值
- ❌ **禁止改变语气** — 保留说话人的口语风格和语气词

**明确允许**：
- ✅ 删除口头禅和填充词（"嗯"、"那个"、"就是说"等连续重复）
- ✅ 合并重复表达（同一意思说了多遍，精简为一遍）
- ✅ 修正语音识别错误（同音字、断句、卡词）
- ✅ 增加标题层级（在结构化分析中合理分章分节）
- ✅ 修正 whisper 重复卡词（同一词连续出现 3 次以上精简为 1~2 次）

**核心原则**：修复的是"语音→文字"的转换误差，不是"内容→内容"的改写。

## 任务B：结构化分析 + 知识复用提取
分析修复后的文本内容，提取关键信息。
额外注意：识别视频中讨论或引用的人物/博主/导师（如"吴江老师说的"、"张三的策略"）。
不是UP主自己，而是内容里**提到的人**。如果没提到任何人就返回空数组。

## 任务C：知识复用标记（重要！）
分析这段内容：
1. **essence**（是什么）— 最浓缩的核心知识点，一段话说清楚
2. **usages**（能干什么）— 这个知识具体能用在什么地方（如：EA风控设计、手动交易规则、系统架构设计等）
3. **relations**（跟什么有关）— 关联知识库中已知的概念/人物/体系（如：张聚贤、吴江方法论、供需区策略等）

注意：usages 和 relations 都可能是空的（新知识没找到关联），如实返回即可。

## 输出格式
必须是合法的JSON，只有JSON没有其他内容：
{
  "corrected": "修复后完整文本（保持原意，不改说话人语气）",
  "summary": "一句话总结核心内容（不超过50字）",
  "keywords": ["关键词1", "关键词2", "关键词3"],
  "chapters": [{"title": "章节名", "line_start": 1, "line_end": 5}],
  "topics": ["主题1", "主题2"],
  "key_persons": ["关键人物1", "关键人物2"],
  "essence": "核心知识点一句话",
  "usages": ["可用在XX场景", "可用于YY"],
  "relations": ["关联吴江方法论", "关联张聚贤体系"],
  "corrections": {"错误的词": "正确的词", "另一个错词": "正确词"},
  "confidence_score": 0.95
}

**corrections（v1.11.0 新增）**：
  - 记录你在修复过程中实际修正的错误词映射，格式 {"原文错词":"修正后正确词"}
  - 只记录你**确定**的修正（>80%确信度的地方才写入）
  - 每条只保留中文词（2-6字），不填句子级的改动
  - 示例：{"主力位":"阻力位", "拼罢":"Pinbar", "阴力":"盈利"}
  - 如果本次没有确定修正的词，返回空对象 {}

**confidence_score（0~1）**：
  - 三源融合评定：综合考虑 whisper 词级置信度 + 官方字幕一致性 + 画面 OCR 文字一致性
  - 0.9~1.0：对修复结果非常有信心，所有歧义都已解决
  - 0.7~0.9：大部分正确，可能有1~2处不太确定
  - 0.5~0.7：有较多不确定的地方，建议人工复查
  - <0.5：整体不自信，原始质量太差

要求：
- 不改原意，不编造，不添加额外解释
- 保留说话人的口语风格
- 无法理解的乱码标记为 [unclear]
- 交易单位"刀"保留
- confidence_score 如实反映修复质量，不要虚高"""


# == 移植自 ZIP v1.9.1: 否定词校验 + Jaccard回归 + B级窗口修正 + 空分析 ==

def _validate_negation_segment(segment: str, api_key, api_base, model) -> Optional[str]:
    """定向校验否定词句子的语义正确性

    用极简 prompt 让 LLM 判断"这段话是否否定义被whisper搞反了"，
    只让LLM回答原文或修正文本，不要求完整分析。
    """
    import urllib.request, urllib.error
    prompt = f"""检查以下中文句子，判断否定义是否被语音识别搞反了。

常见模式：
- "不去" → 可能被识别为"去除" → 否定义丢失
- "没有" → 可能被识别为"也没" → 否定义模糊
- "不打球" → 可能被识别为"打球" → 否定义消失
- 反过来：如果句子明显不该有否定但识别时误加了"不/没"，也可能

句子：{segment}

规则：只考虑同音导致的否定义错误，不考虑语法错误。
如果否定义正确就输出原句，如果有问题就输出修正后的句子。
只输出最终句子，不要解释。"""

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是中文语音识别校正专家。只输出校正后的文本，不作解释。"},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 200,
        "temperature": 0.1,
    }

    from .anti_crawl import robust_llm_call
    result_dict, warnings = robust_llm_call(data, api_key, api_base, timeout=15, max_retries=1)
    if result_dict is None:
        return None  # API 降级，规则引擎回退

    try:
        result = result_dict["choices"][0]["message"]["content"].strip()
        return result if result else None
    except (KeyError, IndexError):
        return None
def _jaccard_similarity(text_a: str, text_b: str, n: int = 3) -> float:
    """基于 char n-gram 的 Jaccard 相似度

    用于修正后回归检查：修正结果与原文差距过大时有可能是过度矫正。
    """
    if not text_a or not text_b:
        return 0.0

    def ngrams(t, k):
        s = set()
        t = t.replace('\n', ' ').replace('\r', ' ')
        t = ' '.join(t.split())
        for i in range(len(t) - k + 1):
            s.add(t[i:i + k])
        return s

    a_set = ngrams(text_a, n)
    b_set = ngrams(text_b, n)

    if not a_set or not b_set:
        return 0.0

    intersection = len(a_set & b_set)
    union = len(a_set | b_set)
    return intersection / union if union > 0 else 0.0
def _windowed_b_level_correct(
    b_segment_text: str,
    low_conf_words: List[Tuple[str, float]],
    speaker_knowledge: str = "",
) -> str:
    """B 级段落窗口式修正 — 只送低置信词+前后1句上下文给 LLM

    豆包链接2/3核心要求：B级段不是整段送 LLM，而是逐个低置信词 + 局部上下文。
    每次调用 ~200 tokens prompt + max_tokens=80，远小于完整正确器。
    """
    if not b_segment_text or not low_conf_words:
        return b_segment_text

    from .secrets import get_llm_config
    key, base, model = get_llm_config()
    if not key:
        return b_segment_text

    # v1.10.0: 规则引擎已前置执行，B分支内不做重复 fast_domain_correct
    text = b_segment_text

    # 对每个低置信词，提取前后1句窗口
    import urllib.request, urllib.error, json as _json
    sentences = re.split(r'([。！？\n])', text)
    sentences_full = ['']  # odd=分隔符, even=句子内容 — 重组后

    # 取每个低置信词所在句子+前后句
    for word, _conf in low_conf_words[:5]:  # B级最多5个低置信词
        if word not in text:
            continue
        # 找 word 所在位置，取周围文字（前后 ~50 字窗口）
        pos = text.find(word)
        left = max(0, pos - 60)
        right = min(len(text), pos + len(word) + 60)
        window = text[left:right]

        prompt = f"""修复以下中文转录片段中的一个低置信词。

片段：{window}
低置信词：{word}

这个词是whisper语音识别置信度较低的词，请结合上下文判断它应该是什么。
如果该词在当前上下文中是合理的就保留原词，否则给出正确的修正。
只输出修正后的**完整窗口文本**，不要解释。"""

        try:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "你是中文语音识别校正专家。只输出校正后的窗口文本，不作解释。"},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 120,
                "temperature": 0.1,
            }

            from .anti_crawl import robust_llm_call
            body, warns = robust_llm_call(payload, key, base, timeout=12, max_retries=1)
            if body is None:
                # API 降级：规则引擎回退（不做任何修改）
                continue

            result = body["choices"][0]["message"]["content"].strip()
            if result and result != window:
                # 安全替换：只替换窗口出现的第一个位置
                text = text.replace(window, result, 1)
                print(f"    [B级窗口] '{word}' → '{result[:30]}...'")
        except Exception as e:
            print(f"    [B级窗口] ⚠️ 校验失败({word}): {e}")
            continue

    return text
def _empty_analysis(text: str = "") -> Dict:
    """空分析结果，用于 raw_only / 纯格式修复场景"""
    return {
        "summary": text[:50] if text else "",
        "keywords": [],
        "chapters": [],
        "topics": [],
        "key_persons": [],
        "essence": "",
        "usages": [],
        "relations": [],
        "confidence_score": 0.95,
    }
