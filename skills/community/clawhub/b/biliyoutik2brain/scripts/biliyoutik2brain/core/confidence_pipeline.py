"""
置信度驱动管线 (v3.0)

串联 env + asr + llm 三个模块，实现置信度驱动的智能处理管线。

流程:
  ASRResult(token级置信度)
    → 低置信区域扫描
    → 中文句边界智能切分
    → 高置信块跳过LLM(省成本) / 低置信块送LLM修正
    → 重组完整文本 + 分析
    → PipelineResult

核心价值:
  - 只修正真正有问题的部分 (降LLM成本 60-80%)
  - 分块边界对齐中文句子结尾 (不硬切句中词)
  - 说话人知识库注入修正上下文
"""

import time, re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field

from .asr import (
    ASRResult, ASRSegment, ConfidenceRegion,
    smart_chunk, scan_low_confidence_regions, confidence_summary,
)
from .llm import correct, analyze, CorrectResult, AnalysisResult
from .env import detect, EnvProfile


@dataclass
class ChunkResult:
    """单个分块的处理结果"""
    char_start: int
    char_end: int
    original_text: str
    corrected_text: str
    confidence: float
    was_corrected: bool         # 是否经过了 LLM 修正
    tokens_used: int = 0
    elapsed_ms: int = 0


@dataclass
class PipelineResult:
    """管线处理完整结果"""
    full_text: str              # 最终修正文本
    original_text: str          # 原始转录文本
    chunks: List[ChunkResult] = field(default_factory=list)
    analysis: AnalysisResult = field(default_factory=AnalysisResult)
    stats: Dict = field(default_factory=dict)
    elapsed_s: float = 0.0


# ═══════════════════════════════════════════════════════════════
#  核心管线
# ═══════════════════════════════════════════════════════════════

def process(
    asr_result: ASRResult,
    video_title: str = "",
    uploader: str = "",
    domain: str = "",
    speaker_context: str = "",
    confidence_threshold: float = 0.6,
    target_chunk_chars: int = 3000,
    backend: str = "auto",
    correction_hints: str = "",
    ocr_timeline: list = None,
    env: Optional[EnvProfile] = None,
) -> PipelineResult:
    """置信度驱动的完整处理管线

    这是整个 v3.0 的核心入口函数。一次性完成:
      置信度分析 → 智能切分 → 靶向修正 → 重组 → 分析

    Args:
        asr_result: ASR 转录结果（含 token 置信度）
        video_title: 视频标题
        uploader: UP主名
        domain: 领域
        speaker_context: 说话人知识库上下文
        confidence_threshold: 低置信阈值（0.6 = 只修正置信度<0.6的片段）
        target_chunk_chars: 分块目标大小
        backend: LLM 后端
        correction_hints: 额外的修正提示词
        ocr_timeline: OCR 画面文字时间线 [{time_s, text}] — 第二条信息通道
        env: 环境画像（自动检测）

    Returns:
        PipelineResult(full_text, chunks, analysis, stats)
    """
    if env is None:
        env = detect()
    if ocr_timeline is None:
        ocr_timeline = []

    # ── 第二条信息通道: OCR 画面文字 → 补充到修正提示中 ──
    if ocr_timeline:
        ocr_text_parts = []
        for item in ocr_timeline[:20]:  # 取前20条，避免提示词过长
            t = item.get('time', item.get('t', 0))
            txt = item.get('text', item.get('ocr_text', ''))
            if txt:
                ocr_text_parts.append(f"[{t:.0f}s] {txt}")
        if ocr_text_parts:
            ocr_bonus = "【画面文字(OCR) — 第二条信息通道，用于交叉验证音频转录】\n" + "\n".join(ocr_text_parts)
            correction_hints = f"{correction_hints}\n\n{ocr_bonus}" if correction_hints else ocr_bonus
            print(f"  [OCR] 🧠 注入 {len(ocr_text_parts)} 条画面文字到LLM修正提示")

    t0 = time.time()
    text = asr_result.full_text

    if not text:
        return PipelineResult(full_text="", original_text="")

    print(f"\n{'='*50}")
    print(f"  置信度管线启动 | 环境: {env.profile_summary}")
    print(f"{'='*50}")

    # ── 步骤1: 置信度分析 ──
    if not asr_result.low_confidence_regions:
        if asr_result.has_token_confidence:
            # 有真实 token 置信度 → 重新扫描
            asr_result.low_confidence_regions = scan_low_confidence_regions(
                asr_result, threshold=confidence_threshold
            )
        else:
            # B方案: 无token置信度 → 已在 asr.transcribe() 中估算
            print(f"  [步骤1] ⚠️ ASR无token置信度({asr_result.engine}), 使用估算置信度")

    total_tokens = sum(len(s.tokens) for s in asr_result.segments if s.tokens)
    low_tokens = sum(len(r.token_indices) for r in asr_result.low_confidence_regions)
    low_ratio = low_tokens / max(total_tokens, 1)
    print(f"  [步骤1] {confidence_summary(asr_result)}")

    # ── 步骤2: 智能切分 ──
    chunks = smart_chunk(asr_result, target_chars=target_chunk_chars)
    print(f"  [步骤2] 智能切分: {len(text)}字 → {len(chunks)}块")

    # 构建低置信区间映射
    low_conf_map = _build_low_conf_map(text, asr_result.low_confidence_regions)

    # ── 步骤3: 逐块处理 ──
    chunk_results = []
    llm_calls = 0
    llm_tokens = 0
    llm_ms = 0

    for i, (cs, ce) in enumerate(chunks):
        chunk_text = text[cs:ce]
        chunk_conf = _chunk_avg_confidence(text, cs, ce, asr_result.low_confidence_regions)

        needs_correction = chunk_conf < confidence_threshold

        print(f"  [块{i+1}/{len(chunks)}] [{cs}:{ce}] {len(chunk_text)}字, "
              f"置信度={chunk_conf:.3f} → {'🤖 LLM修正' if needs_correction else '✅ 信任原文'}")

        if needs_correction:
            # 该块内的低置信片段（用于传递提示给 LLM）
            span_hints = _extract_low_conf_hints(
                asr_result.low_confidence_regions, cs, ce
            )

            result = correct(
                text=chunk_text,
                video_title=video_title,
                uploader=uploader,
                domain=domain,
                speaker_context=speaker_context,
                low_conf_spans=span_hints,
                correction_hints=correction_hints,
                backend=backend,
            )
            chunk_results.append(ChunkResult(
                char_start=cs, char_end=ce,
                original_text=chunk_text,
                corrected_text=result.corrected_text,
                confidence=chunk_conf,
                was_corrected=True,
                tokens_used=result.tokens_used,
                elapsed_ms=result.elapsed_ms,
            ))
            llm_calls += 1
            llm_tokens += result.tokens_used
            llm_ms += result.elapsed_ms
        else:
            # 高置信块：跳过 LLM（省成本），用纯规则排版兜底（零 API）
            chunk_results.append(ChunkResult(
                char_start=cs, char_end=ce,
                original_text=chunk_text,
                corrected_text=paragraphize(chunk_text),
                confidence=chunk_conf,
                was_corrected=False,
            ))

    # ── 步骤4: 重组 ──
    corrected_full = _reassemble(text, chunk_results)

    # ── 步骤5: 结构化分析 ──
    print(f"\n  [步骤5] 结构化分析...")
    analysis_result = analyze(
        text=corrected_full,
        video_title=video_title,
        uploader=uploader,
        domain=domain,
        backend=backend,
    )

    elapsed = time.time() - t0
    corrected_ratio = sum(len(cr.corrected_text) for cr in chunk_results if cr.was_corrected)
    total_chars = max(len(text), 1)

    result = PipelineResult(
        full_text=corrected_full,
        original_text=text,
        chunks=chunk_results,
        analysis=analysis_result,
        stats={
            "total_chars": len(text),
            "chunks": len(chunks),
            "llm_calls": llm_calls,
            "llm_skipped": len(chunks) - llm_calls,
            "llm_tokens": llm_tokens,
            "llm_ms": llm_ms,
            "low_conf_ratio": round(low_ratio, 3),
            "corrected_ratio": round(corrected_ratio / total_chars, 3),
            "elapsed_s": round(elapsed, 1),
            "cost_saved": f"{(1 - llm_calls/max(len(chunks),1))*100:.0f}%",
        },
        elapsed_s=round(elapsed, 1),
    )

    print(f"\n  ✅ 管线完成 ({elapsed:.1f}s)")
    print(f"     总字符: {len(text)} → 修正后: {len(corrected_full)}")
    print(f"     LLM调用: {llm_calls}/{len(chunks)} 次 (跳过 {len(chunks)-llm_calls} 块)")
    print(f"     成本节省: {result.stats['cost_saved']}")
    print(f"     分析: {len(analysis_result.keywords)}关键词, {len(analysis_result.topics)}主题")
    print(f"{'='*50}\n")

    # ── v3.2: 自进化记录 ──
    try:
        from .self_evolve import log_run
        log_run(
            video_id=asr_result.engine if not video_title else video_title[:30],
            uploader=uploader,
            duration_s=int(asr_result.duration),
            asr_engine=asr_result.engine,
            asr_model=asr_result.model,
            chars=len(text),
            confidence=asr_result.overall_confidence,
            low_conf_ratio=low_ratio,
            llm_backend=analysis_result.backend,
            llm_calls=llm_calls,
            llm_tokens=llm_tokens,
            chunks=len(chunks),
            elapsed_s=elapsed,
        )
    except Exception:
        pass  # 自进化不是关键路径

    return result


# ═══════════════════════════════════════════════════════════════
#  辅助函数
# ═══════════════════════════════════════════════════════════════

# ── 纯规则排版：把 ASR 碎行整理成带标点的自然段落（零 API 成本）──
# 用于高置信块（被"信任原文"跳过 LLM 的块）的排版兜底，
# 保证无论高低置信，最终文本都有标点和段落。
_PARA_TRIGGERS = (
    "那么", "所以", "因此", "接下来", "下面", "总结", "总的来说", "综上",
    "首先", "其次", "再次", "另外", "此外", "最后", "话又说回来", "话说回来",
    "比如", "举个例子", "举例", "第二", "第三", "第四", "其实说", "不过呢",
)
# 只认强疑问信号"吗/吧"——"呢/么/嘛"歧义大（什么/这么/那么），
# 保守补句号比误补问号安全。
_Q_TAILS = ("吗", "吧")
_END_PUNCT = "。！？!?…"
_PAUSE_PUNCT = "，,、；;："


def paragraphize(text: str, sentences_per_para: int = 4) -> str:
    """纯规则：把 ASR 碎行整理成带标点的自然段落（零 API 调用）。

    利用 ASR "每段一行"的韵律：一行≈一句，行尾补句末标点（疑问语气词→？，
    否则→。），再按段落触发词或句数阈值聚成自然段，段间空行。

    仅用于高置信块的兜底排版——这些块识别准确、相对规整，规则排版副作用小。
    低置信块由 LLM 排版（见 llm.correct），不经过此函数。
    """
    if not text or not text.strip():
        return text

    # 1) 切句：优先用 ASR 的换行（行≈句）；无换行则退化为按已有句末标点切
    lines = [ln.strip() for ln in re.split(r"[\r\n]+", text) if ln.strip()]
    if len(lines) <= 1:
        single = lines[0] if lines else text.strip()
        parts = re.split(r"(?<=[。！？!?…])", single)
        lines = [p.strip() for p in parts if p.strip()]
        if len(lines) <= 1:
            s = single
            if s and s[-1] not in _END_PUNCT:
                s += "？" if s.endswith(_Q_TAILS) else "。"
            return s

    # 2) 每行补句末标点
    sentences = []
    for ln in lines:
        last = ln[-1]
        if last in _END_PUNCT:
            sentences.append(ln)
        elif last in _PAUSE_PUNCT:
            core = ln[:-1]
            sentences.append(core + ("？" if core.endswith(_Q_TAILS) else "。"))
        else:
            sentences.append(ln + ("？" if ln.endswith(_Q_TAILS) else "。"))

    # 3) 聚段：段落触发词另起一段，或累计句数到阈值另起一段
    paras, cur = [], []
    for s in sentences:
        if cur and (s.startswith(_PARA_TRIGGERS) or len(cur) >= sentences_per_para):
            paras.append("".join(cur))
            cur = []
        cur.append(s)
    if cur:
        paras.append("".join(cur))

    return "\n\n".join(paras)


def _build_low_conf_map(
    full_text: str,
    regions: List[ConfidenceRegion],
) -> Dict[int, float]:
    """构建字符位置 → 置信度映射（用于快速查询）"""
    if not regions:
        return {}
    char_map = {}
    for region in regions:
        for i in range(region.char_start, min(region.char_end, len(full_text))):
            char_map[i] = region.avg_confidence
    return char_map


def _chunk_avg_confidence(
    full_text: str,
    chunk_start: int,
    chunk_end: int,
    regions: List[ConfidenceRegion],
) -> float:
    """计算一个分块的平均置信度

    如果 chunks 内没有低置信区域 → 返回 1.0 (完全信任)
    有低置信区域 → 返回该区域的平均置信度
    """
    relevant = []
    for region in regions:
        # 区域与 chunk 有交集
        if region.char_end > chunk_start and region.char_start < chunk_end:
            overlap_start = max(region.char_start, chunk_start)
            overlap_end = min(region.char_end, chunk_end)
            overlap_len = overlap_end - overlap_start
            relevant.append((region.avg_confidence, overlap_len))

    if not relevant:
        return 1.0

    total_weight = sum(w for _, w in relevant)
    if total_weight == 0:
        return 1.0

    weighted_conf = sum(c * w for c, w in relevant) / total_weight
    return round(weighted_conf, 3)


def _extract_low_conf_hints(
    regions: List[ConfidenceRegion],
    chunk_start: int,
    chunk_end: int,
    max_hints: int = 8,
) -> List[str]:
    """提取落在指定分块内的低置信片段（用于 LLM 提示）"""
    hints = []
    for region in regions:
        if region.char_start >= chunk_start and region.char_end <= chunk_end:
            hints.append(f"「{region.text}」(置信度 {region.avg_confidence:.2f})")
    return hints[:max_hints]


def _reassemble(
    original_text: str,
    chunks: List[ChunkResult],
) -> str:
    """重组修正后的文本

    策略:
    - 修正过的块: 使用 LLM 修正文本
    - 未修正的块: 使用原文（信任）
    - 按原始顺序拼接
    """
    chunks = sorted(chunks, key=lambda c: c.char_start)

    # 验证连续性
    parts = []
    prev_end = 0

    def _append_piece(piece: str):
        """拼接时保证块间段落分隔，避免相邻块文字黏连成一行"""
        if not piece:
            return
        if parts and not parts[-1].endswith("\n") and not piece.startswith("\n"):
            parts.append("\n\n")
        parts.append(piece)

    for cr in chunks:
        if cr.char_start > prev_end:
            # 中间有间隙（不应该发生，但兜底）— 也做规则排版
            gap_text = original_text[prev_end:cr.char_start]
            if gap_text.strip():
                _append_piece(paragraphize(gap_text))

        _append_piece(cr.corrected_text)
        prev_end = cr.char_end

    # 末尾残余 — 同样排版兜底
    if prev_end < len(original_text):
        tail = original_text[prev_end:]
        if tail.strip():
            _append_piece(paragraphize(tail))

    return "".join(parts)


# ═══════════════════════════════════════════════════════════════
#  快捷函数: 一把梭
# ═══════════════════════════════════════════════════════════════

def enhance_audio(
    audio_path: str,
    video_title: str = "",
    uploader: str = "",
    domain: str = "",
    speaker_context: str = "",
    asr_engine: str = "auto",
    asr_model: str = "base",
    llm_backend: str = "auto",
    confidence_threshold: float = 0.6,
) -> PipelineResult:
    """从音频文件一步到位: ASR → 置信度管线 → 修正 → 分析

    使用示例:
      result = enhance_audio(
          "video_audio.wav",
          video_title="FVG交易策略详解",
          uploader="张聚贤",
          speaker_context=format_context("张聚贤"),
      )
      print(result.full_text)  # 修正后的文本
      print(result.analysis)   # 结构化分析
    """
    from .asr import transcribe

    print(f"[管线] 🎤 转录中...")
    asr_result = transcribe(audio_path, engine=asr_engine, model_size=asr_model)

    return process(
        asr_result=asr_result,
        video_title=video_title,
        uploader=uploader,
        domain=domain,
        speaker_context=speaker_context,
        confidence_threshold=confidence_threshold,
        backend=llm_backend,
    )


def diagnose_confidence(asr_result: ASRResult) -> str:
    """输出置信度诊断报告（调试用）"""
    lines = ["置信度诊断报告", "=" * 40]

    lines.append(f"整体置信度: {asr_result.overall_confidence:.3f}")
    lines.append(f"段落数: {len(asr_result.segments)}")
    lines.append(f"低置信区域: {len(asr_result.low_confidence_regions)}")

    if asr_result.low_confidence_regions:
        lines.append("\n低置信片段:")
        for i, region in enumerate(asr_result.low_confidence_regions[:10]):
            lines.append(
                f"  {i+1}. [{region.avg_confidence:.2f}] "
                f"'{region.text[:40]}' "
                f"(位置 {region.char_start}-{region.char_end})"
            )

    if asr_result.segments:
        confs = [s.avg_confidence for s in asr_result.segments if s.avg_confidence > 0]
        if confs:
            lines.append(f"\n段落置信度: min={min(confs):.3f} max={max(confs):.3f} avg={sum(confs)/len(confs):.3f}")

    return "\n".join(lines)
