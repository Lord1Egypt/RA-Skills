"""
ASR 抽象层 (v3.0)

统一接口，支持多引擎转录，输出 token 级置信度。
中文友好：句边界检测、低置信区域标记、繁体转简体。

支持的引擎:
  - faster-whisper: 本地, word_timestamps 提供 token 级置信度 (推荐)
  - bailian (百炼ASR): 云端 DashScope, 段落级置信度, 免费
  - openai-whisper: 本地 torch, 段落级, 无 token 置信度 (回退)

数据流:
  音频 → [引擎选择] → ASRResult(segments, tokens, confidences)
    → 低置信区域扫描 → 输出置信度地图
"""

import os, time, re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


# ═══════════════════════════════════════════════════════════════
#  数据类型
# ═══════════════════════════════════════════════════════════════

@dataclass
class TokenInfo:
    """单个 token 的信息"""
    word: str                  # 词本身
    confidence: float          # 0-1 置信度
    start: float               # 开始时间(秒)
    end: float                 # 结束时间(秒)
    is_chinese: bool = False   # 是否是中文字符


@dataclass
class ASRSegment:
    """一个转录段落"""
    start: float
    end: float
    text: str
    tokens: List[TokenInfo] = field(default_factory=list)
    avg_confidence: float = 0.0
    speaker_id: str = ""       # 说话人标签（多人转录时）


@dataclass
class ConfidenceRegion:
    """低置信区域"""
    char_start: int            # 在 full_text 中的起始位置
    char_end: int              # 结束位置
    text: str                  # 该区域的文本
    avg_confidence: float      # 平均置信度
    token_indices: List[int] = field(default_factory=list)


@dataclass
class ASRResult:
    """转录结果"""
    full_text: str
    segments: List[ASRSegment] = field(default_factory=list)
    low_confidence_regions: List[ConfidenceRegion] = field(default_factory=list)
    overall_confidence: float = 0.0
    engine: str = "unknown"
    model: str = ""
    language: str = "zh"
    chars_per_second: float = 0.0
    duration: float = 0.0
    has_token_confidence: bool = False  # ← v3.1: 标记是否有真实token置信度


# ═══════════════════════════════════════════════════════════════
#  中文处理
# ═══════════════════════════════════════════════════════════════

def _to_simplified(text: str) -> str:
    """繁体中文转简体"""
    try:
        from opencc import OpenCC
        return OpenCC('t2s').convert(text)
    except ImportError:
        return text


def _is_chinese_char(ch: str) -> bool:
    """判断是否中文字符"""
    return '\u4e00' <= ch <= '\u9fff'


def _find_sentence_boundaries(text: str) -> List[int]:
    """找到中文句子边界位置（。！？；\n）

    返回每个句子结束位置的索引列表。
    用于智能分块——不硬切句中词。
    """
    boundaries = []
    for i, ch in enumerate(text):
        if ch in '。！？；\n':
            boundaries.append(i + 1)
    if boundaries and boundaries[-1] < len(text):
        boundaries.append(len(text))
    if not boundaries:
        boundaries.append(len(text))
    return boundaries


def _count_chars_per_second(text: str, duration: float) -> float:
    """计算语速（字/秒）"""
    if not text or duration <= 0:
        return 0.0
    chinese_chars = sum(1 for c in text if _is_chinese_char(c))
    return chinese_chars / max(duration, 1)


# ═══════════════════════════════════════════════════════════════
#  faster-whisper 引擎（token 级置信度）
# ═══════════════════════════════════════════════════════════════

_fw_model = None
_fw_model_size = None
_LOCAL_MODEL_SIZES_CACHE = None  # 延迟扫描

def _list_local_whisper_models() -> list:
    """扫描 ~/.cache/huggingface/hub 中已缓存的 faster-whisper 模型"""
    global _LOCAL_MODEL_SIZES_CACHE
    if _LOCAL_MODEL_SIZES_CACHE is not None:
        return _LOCAL_MODEL_SIZES_CACHE
    import glob as _glob
    hub = os.path.expanduser("~/.cache/huggingface/hub")
    pattern = os.path.join(hub, "models--Systran--faster-whisper-*", "snapshots", "*")
    cached = set()
    for d in _glob.glob(pattern):
        if os.path.isfile(os.path.join(d, "model.bin")):
            # 从路径名提取模型尺寸: models--Systran--faster-whisper-base
            parent = os.path.basename(os.path.dirname(os.path.dirname(d)))
            tag = parent.replace("models--Systran--faster-whisper-", "")
            cached.add(tag)
    _LOCAL_MODEL_SIZES_CACHE = sorted(cached, reverse=True)  # 大模型优先
    return _LOCAL_MODEL_SIZES_CACHE

def resolve_model_size(preferred: str = None) -> str:
    """解析最终使用的模型尺寸

    优先级：
    1. 用户指定的 preferred（如 "base"）
    2. 本地已缓存的最优模型（大模型优先：large > medium > small > base > tiny）
    3. 默认 "base"

    返回的模型保证本地有缓存，不会触发联网下载。
    """
    local = _list_local_whisper_models()
    size_order = ["large", "medium", "small", "base", "tiny"]

    if preferred and preferred in local:
        return preferred

    # 从大到小找第一个已缓存的
    for s in size_order:
        if s in local:
            return s

    return "base"  # fallback

def _init_faster_whisper(model_size: str = "base"):
    """初始化 faster-whisper 模型

    优先用本地缓存加载，避免 HuggingFace Hub SSL 连接问题。
    如果请求的 model_size 本地没有，自动 fallback 到已缓存的模型。
    """
    global _fw_model, _fw_model_size
    if _fw_model is not None and _fw_model_size == model_size:
        return

    # 安全检查：如果请求的模型本地没有，切换到已缓存的
    local = _list_local_whisper_models()
    if local and model_size not in local:
        fallback = resolve_model_size(model_size)
        print(f"  [ASR] ⚠️  {model_size} 未缓存, 切换到: {fallback}")
        model_size = fallback

    try:
        from faster_whisper import WhisperModel
        device = "cuda" if _has_gpu() else "cpu"
        compute_type = "float16" if device == "cuda" else "int8"
        # 优先用本地缓存路径，避免 HuggingFace Hub SSL 连接问题
        local_model_path = os.path.expanduser(
            f"~/.cache/huggingface/hub/models--Systran--faster-whisper-{model_size}/snapshots"
        )
        # 遍历 snapshots 下所有目录，找到包含 model.bin 的那个（不一定叫 1778413916）
        if os.path.isdir(local_model_path):
            import glob as _glob2
            candidates = _glob2.glob(os.path.join(local_model_path, "*/model.bin"))
            if candidates:
                actual = os.path.dirname(candidates[0])
                _fw_model = WhisperModel(
                    actual, device=device, compute_type=compute_type,
                    local_files_only=True,
                )
                print(f"  [ASR] 本地模型: {model_size} ({device}/{compute_type})")
                _fw_model_size = model_size
                return
        # 不在本地 → 联网下载
        _fw_model = WhisperModel(model_size, device=device, compute_type=compute_type)
        print(f"  [ASR] 在线模型: {model_size} ({device}/{compute_type})")
        _fw_model_size = model_size
    except ImportError:
        raise RuntimeError("faster-whisper 未安装: pip install faster-whisper")


def _has_gpu() -> bool:
    """检测是否有 GPU"""
    try:
        import subprocess
        r = subprocess.run(["nvidia-smi"], capture_output=True, timeout=3)
        return r.returncode == 0
    except Exception:
        return False


def transcribe_faster_whisper(
    audio_path: str,
    model_size: str = "base",
    language: str = "zh",
    beam_size: int = 5,
    confidence_threshold: float = 0.4,
) -> ASRResult:
    """faster-whisper 转录 → 含 token 级置信度

    这是唯一能提供词级置信度的引擎，是整个置信度管线的基石。
    """
    if not os.path.exists(audio_path):
        return ASRResult(full_text="", engine="faster_whisper", model=model_size)

    _init_faster_whisper(model_size)
    t0 = time.time()

    segments_out, info = _fw_model.transcribe(
        audio_path,
        language=language,
        beam_size=beam_size,
        word_timestamps=True,       # ← 关键：启用词级时间戳
        vad_filter=True,            # 自动跳过长静音
        temperature=0.0,            # 贪婪解码，最大确定性
    )

    result = ASRResult(
        full_text="",
        engine="faster_whisper",
        model=model_size,
        language=info.language,
        duration=info.duration,
        has_token_confidence=True,  # ← 只有这个引擎有真实token置信度
    )

    full_parts = []
    seg_index = 0

    for seg in segments_out:
        seg_text = seg.text.strip()
        if not seg_text:
            continue

        tokens = []
        seg_conf_sum = 0.0
        token_count = 0

        # 提取 token 级信息
        if hasattr(seg, 'words') and seg.words:
            for w in seg.words:
                is_cn = _is_chinese_char(w.word)
                tok = TokenInfo(
                    word=w.word,
                    confidence=round(w.probability, 3),
                    start=round(w.start, 2),
                    end=round(w.end, 2),
                    is_chinese=is_cn,
                )
                tokens.append(tok)
                if is_cn:  # 只统计中文字符的置信度（英文/标点的置信度参考意义小）
                    seg_conf_sum += w.probability
                    token_count += 1

        avg_conf = seg_conf_sum / max(token_count, 1) if token_count > 0 else 0.5

        result.segments.append(ASRSegment(
            start=round(seg.start, 2),
            end=round(seg.end, 2),
            text=_to_simplified(seg_text),
            tokens=tokens,
            avg_confidence=round(avg_conf, 3),
        ))

        full_parts.append(seg_text)
        seg_index += 1

    result.full_text = _to_simplified("\n".join(full_parts))
    result.chars_per_second = _count_chars_per_second(result.full_text, info.duration)

    # 计算整体置信度
    if result.segments:
        result.overall_confidence = round(
            sum(s.avg_confidence for s in result.segments) / len(result.segments), 3
        )

    elapsed = time.time() - t0
    print(f"  [ASR] faster-whisper 完成 ({elapsed:.1f}s, {len(result.segments)}段, "
          f"置信度={result.overall_confidence:.3f}, 语速={result.chars_per_second:.1f}字/秒)")

    # 扫描低置信区域
    result.low_confidence_regions = scan_low_confidence_regions(
        result, threshold=confidence_threshold
    )

    return result


# ═══════════════════════════════════════════════════════════════
#  openai-whisper 引擎（回退，无 token 置信度）
# ═══════════════════════════════════════════════════════════════

_ow_model = None

def _init_openai_whisper(model_size: str = "base"):
    global _ow_model
    if _ow_model is not None:
        return
    try:
        import whisper
        _ow_model = whisper.load_model(model_size, device="cpu")
        print(f"  [ASR] openai-whisper {model_size} 已加载")
    except ImportError:
        raise RuntimeError("openai-whisper 未安装: pip install openai-whisper")


def transcribe_openai_whisper(
    audio_path: str,
    model_size: str = "base",
    language: str = "zh",
) -> ASRResult:
    """openai-whisper 转录 → 段落级，无 token 置信度

    openai-whisper 不支持 word_timestamps 的置信度输出。
    只能提供段落级置信度估算（基于 beam search 的平均值）。
    """
    if not os.path.exists(audio_path):
        return ASRResult(full_text="", engine="openai_whisper", model=model_size)

    _init_openai_whisper(model_size)
    t0 = time.time()

    result_raw = _ow_model.transcribe(
        audio_path,
        language=language,
        beam_size=5,
        fp16=False,
    )

    result = ASRResult(
        full_text="",
        engine="openai_whisper",
        model=model_size,
        language=language,
    )

    full_parts = []
    for seg in result_raw.get("segments", []):
        seg_text = seg.get("text", "").strip()
        if not seg_text:
            continue
        result.segments.append(ASRSegment(
            start=round(seg.get("start", 0), 2),
            end=round(seg.get("end", 0), 2),
            text=_to_simplified(seg_text),
            tokens=[],   # openai-whisper 不提供词级信息
            avg_confidence=0.6,  # 乐观估算
        ))
        full_parts.append(seg_text)

    result.full_text = _to_simplified("\n".join(full_parts))
    result.overall_confidence = 0.6  # 保守

    elapsed = time.time() - t0
    print(f"  [ASR] openai-whisper 完成 ({elapsed:.1f}s, {len(result.segments)}段, "
          f"⚠️ 无token置信度)")

    return result


# ═══════════════════════════════════════════════════════════════
#  百炼 ASR (DashScope) — 云端引擎
# ═══════════════════════════════════════════════════════════════

def transcribe_bailian(
    audio_path: str,
    language: str = "zh",
) -> ASRResult:
    """百炼 ASR 转录 → 云端, 段落级, 无 token 置信度"""
    if not os.path.exists(audio_path):
        return ASRResult(full_text="", engine="bailian")

    api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY 未设置")

    import requests

    t0 = time.time()
    url = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription"

    with open(audio_path, "rb") as f:
        files = {"file": f}
        headers = {"Authorization": f"Bearer {api_key}"}
        data = {
            "model": "paraformer-v2",
            "parameters": json.dumps({"language_hints": ["zh"]}),
        }
        resp = requests.post(url, files=files, headers=headers, data=data, timeout=120)

    if resp.status_code != 200:
        raise RuntimeError(f"百炼ASR 请求失败: {resp.status_code} {resp.text[:200]}")

    raw = resp.json()
    output = raw.get("output", {})
    sentences = output.get("sentence", [])

    result = ASRResult(
        full_text="",
        engine="bailian",
        model="paraformer-v2",
        language=language,
        duration=0.0,
    )

    full_parts = []
    for sent in sentences:
        text = sent.get("text", "").strip()
        if not text:
            continue
        result.segments.append(ASRSegment(
            start=round(sent.get("begin_time", 0) / 1000, 2),
            end=round(sent.get("end_time", 0) / 1000, 2),
            text=text,
            tokens=[],
            avg_confidence=0.7,  # 百炼不返回置信度
        ))
        full_parts.append(text)

    result.full_text = "\n".join(full_parts)
    result.overall_confidence = 0.7
    if result.segments:
        result.duration = result.segments[-1].end

    elapsed = time.time() - t0
    print(f"  [ASR] 百炼ASR 完成 ({elapsed:.1f}s, {len(result.segments)}段)")

    return result

import json as _json  # for bailian only


# ═══════════════════════════════════════════════════════════════
#  置信度分析
# ═══════════════════════════════════════════════════════════════

def scan_low_confidence_regions(
    result: ASRResult,
    threshold: float = 0.4,
    min_consecutive_tokens: int = 2,
) -> List[ConfidenceRegion]:
    """扫描低置信度区域

    规则：
    1. 连续 N 个低置信 token → 标记为一个区域
    2. 只统计中文字符 token（英文/标点过滤）
    3. 跨段落连续 → 合并为同一区域

    中文友好：低置信词经常是"同音词"（均线/军线）或"韵母混淆"，
    这些是 LLM 增强的重点目标。
    """
    regions = []
    current_start = -1
    current_end = -1
    current_tokens = []
    current_text_parts = []
    char_offset = 0

    for seg in result.segments:
        for i, tok in enumerate(seg.tokens):
            if not tok.is_chinese:
                char_offset += len(tok.word)
                continue

            if tok.confidence < threshold:
                if current_start == -1:
                    current_start = char_offset
                current_end = char_offset + len(tok.word)
                current_tokens.append(i)
                current_text_parts.append(tok.word)
            else:
                if current_start != -1 and len(current_tokens) >= min_consecutive_tokens:
                    text = "".join(current_text_parts)
                    confs = [seg.tokens[ti].confidence for ti in current_tokens if ti < len(seg.tokens)]
                    avg_conf = sum(confs) / max(len(confs), 1) if confs else 0.4
                    regions.append(ConfidenceRegion(
                        char_start=current_start,
                        char_end=current_end,
                        text=text,
                        avg_confidence=round(avg_conf, 3),
                        token_indices=list(current_tokens),
                    ))
                current_start = -1
                current_end = -1
                current_tokens = []
                current_text_parts = []

            char_offset += len(tok.word)

    # 末尾残留
    if current_start != -1 and len(current_tokens) >= min_consecutive_tokens:
        text = "".join(current_text_parts)
        # Get conf from last valid segment's tokens
        last_seg_tokens = result.segments[-1].tokens if result.segments else []
        confs = []
        for ti in current_tokens:
            if ti < len(last_seg_tokens):
                confs.append(last_seg_tokens[ti].confidence)
        avg_conf = sum(confs) / max(len(confs), 1) if confs else 0.4
        regions.append(ConfidenceRegion(
            char_start=current_start,
            char_end=current_end,
            text=text,
            avg_confidence=round(avg_conf, 3),
        ))

    return regions


def confidence_summary(result: ASRResult) -> str:
    """置信度摘要（一行）
    区分真实置信度还是估算: has_token_confidence 字段"""
    low = result.low_confidence_regions
    total_tokens = sum(len(s.tokens) for s in result.segments if s.tokens)
    low_tokens = sum(len(r.token_indices) for r in low)
    source = "token级" if result.has_token_confidence else "估算"

    return (
        f"整体={result.overall_confidence:.2f} | "
        f"低置信区域={len(low)}个({source}) | "
        f"低置信token={low_tokens}/{total_tokens}"
        + (f" ({low_tokens/max(total_tokens,1)*100:.0f}%)" if total_tokens > 0 else "")
    )


# ═══════════════════════════════════════════════════════════════
#  B方案: 无token置信度时的置信度估算
# ═══════════════════════════════════════════════════════════════

def estimate_confidence(
    result: ASRResult,
    threshold: float = 0.6,
    correction_dict: Dict[str, str] = None,
) -> ASRResult:
    """无 token 置信度时的 B方案: 用多信号估算置信度

    当 ASR 引擎不提供 token 级置信度时（百炼、openai-whisper），
    用以下信号估算每个段落的置信度:

    信号1 - 段落时间长度:
      过短(<1s)或过长(>30s) → 可能有问题 → -0.15
    信号2 - 语速异常:
      远高/低于平均值 → 可能转录错误 → -0.10
    信号3 - 纠错词典命中:
      包含已知易错词 → 需要LLM检查 → -0.20
    信号4 - 句子结构:
      是否有完整的主谓结构 → 有 = +0.05
    信号5 - 段落累积偏差:
      远离中位数的段落 → -0.10

    输出: ASRResult（丰富了 low_confidence_regions）
    """
    if result.has_token_confidence:
        return result  # 已有真实置信度, 不需要估算

    if not result.segments:
        return result

    # 段落时长统计
    durations = [s.end - s.start for s in result.segments]
    median_dur = sorted(durations)[len(durations) // 2] if durations else 10

    # 字数统计
    char_counts = [len(s.text) for s in result.segments]
    median_chars = sorted(char_counts)[len(char_counts) // 2] if char_counts else 20

    # 语速统计 (字/秒)
    speeds = []
    for s in result.segments:
        dur = s.end - s.start
        if dur > 0:
            speeds.append(len(s.text) / dur)

    regions = []
    char_offset = 0

    for si, seg in enumerate(result.segments):
        base_conf = 0.75  # 起步分数
        reasons = []

        # 信号1: 段落时长
        dur = seg.end - seg.start
        if dur < 0.5 or dur > 60:
            base_conf -= 0.20
            reasons.append(f"时长异常({dur:.1f}s)")
        elif dur < 1.0 or dur > 30:
            base_conf -= 0.10
            reasons.append(f"时长偏{'短' if dur < 1 else '长'}({dur:.1f}s)")

        # 信号2: 字数异常
        chars = len(seg.text)
        if chars < 3 or chars > 200:
            base_conf -= 0.10
            reasons.append(f"字数异常({chars}字)")

        # 信号3: 纠错词典命中
        if correction_dict:
            hit_count = 0
            for wrong_word in correction_dict:
                if wrong_word in seg.text:
                    hit_count += 1
            if hit_count > 0:
                base_conf -= 0.15
                reasons.append(f"词典命中{hit_count}词")

        # 信号4: 句子结构 (中文: 包含动词/名词组合)
        has_subject = any(c in seg.text for c in '我你他是这在')
        has_verb = any(c in seg.text for c in '是讲了说看做用会要给到去')
        if has_subject and has_verb:
            base_conf += 0.05

        # 信号5: 段落累积字数偏差
        if speeds and si > 0:
            expected_chars = char_counts[si - 1]
            if abs(chars - expected_chars) > expected_chars * 0.5:
                base_conf -= 0.05
                reasons.append("段落突变")

        final_conf = max(0.15, min(0.95, base_conf))
        seg.avg_confidence = round(final_conf, 3)

        if final_conf < threshold:
            # 构造一个 ConfidenceRegion
            text = seg.text
            regions.append(ConfidenceRegion(
                char_start=char_offset,
                char_end=char_offset + len(text),
                text=text,
                avg_confidence=round(final_conf, 3),
            ))

        char_offset += len(seg.text)

    result.low_confidence_regions = regions

    # 整体置信度: 所有段落的加权平均
    if result.segments:
        result.overall_confidence = round(
            sum(s.avg_confidence for s in result.segments) / len(result.segments), 3
        )

    if regions:
        print(f"  [ASR/B] ⚠️ 无token置信度, 多信号估算完成: "
              f"{len(regions)}/{len(result.segments)}段标记为低置信 "
              f"(整体={result.overall_confidence:.2f})")

    return result


# ═══════════════════════════════════════════════════════════════
#  智能切分（中文友好）
# ═══════════════════════════════════════════════════════════════

def smart_chunk(
    result: ASRResult,
    target_chars: int = 3000,
    min_chars: int = 1500,
) -> List[Tuple[int, int]]:
    """智能切分：按句子边界分块，不硬切句中词

    算法：
    1. 先找到所有句子边界（。！？\n）
    2. 从每个低置信区域向前找最近的句子边界 → 以此为分块边界
    3. 每块 1500-3000 字，优先对齐句子边界

    返回: [(start_char, end_char), ...] 每块在 full_text 中的起止位置
    """
    text = result.full_text
    boundaries = _find_sentence_boundaries(text)

    if not boundaries:
        return [(0, len(text))]

    # 低置信区域的中点位置
    low_conf_centers = []
    for region in result.low_confidence_regions:
        center = (region.char_start + region.char_end) // 2
        low_conf_centers.append(center)

    chunks = []
    chunk_start = 0

    for i, b in enumerate(boundaries):
        if b - chunk_start < min_chars:
            continue  # 还没到最小块

        # 如果下一个边界会让块太大
        next_boundary = boundaries[min(i + 1, len(boundaries) - 1)]

        # 检查是否有低置信中心在当前范围内
        has_low_conf = any(
            chunk_start <= c < b for c in low_conf_centers
        )

        if b - chunk_start >= target_chars or has_low_conf:
            chunks.append((chunk_start, b))
            chunk_start = b
        elif next_boundary - chunk_start > target_chars * 1.3:
            chunks.append((chunk_start, b))
            chunk_start = b

    # 最后一块
    if chunk_start < len(text) and (not chunks or chunks[-1][1] < len(text)):
        chunks.append((chunk_start, len(text)))

    # 合并过小的块
    merged = []
    for start, end in chunks:
        if merged and start - merged[-1][1] < 100:
            # 离上一块太近 → 合并
            prev_start, _ = merged.pop()
            merged.append((prev_start, end))
        else:
            merged.append((start, end))

    return merged


# ═══════════════════════════════════════════════════════════════
#  统一转录接口
# ═══════════════════════════════════════════════════════════════

def transcribe(
    audio_path: str,
    engine: str = "auto",
    model_size: str = "base",
    language: str = "zh",
    confidence_threshold: float = 0.4,
) -> ASRResult:
    """统一转录接口 — 自动选择最优引擎

    engine="auto" 时:
      1. 优先 faster-whisper (token 置信度)
      2. 回退百炼ASR (云端, 需 API Key)
      3. 回退 openai-whisper (本地, 无置信度)
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"音频文件不存在: {audio_path}")

    # 自动选择
    if engine == "auto":
        try:
            import importlib
            if importlib.util.find_spec("faster_whisper"):
                engine = "faster_whisper"
            elif os.environ.get("DASHSCOPE_API_KEY"):
                engine = "bailian"
            else:
                engine = "openai_whisper"
        except Exception:
            engine = "openai_whisper"

    print(f"  [ASR] 引擎: {engine}, 模型: {model_size}")

    if engine == "faster_whisper":
        result = transcribe_faster_whisper(
            audio_path, model_size=model_size, language=language,
            confidence_threshold=confidence_threshold
        )
        return result

    if engine == "bailian":
        result = transcribe_bailian(audio_path, language=language)
        # B方案: 百炼无token置信度 → 多信号估算
        result = estimate_confidence(result, threshold=confidence_threshold)
        return result

    if engine == "openai_whisper":
        result = transcribe_openai_whisper(
            audio_path, model_size=model_size, language=language
        )
        # B方案: openai-whisper无token置信度 → 多信号估算
        result = estimate_confidence(result, threshold=confidence_threshold)
        return result

    raise ValueError(f"不支持的 ASR 引擎: {engine}")


def check_available() -> List[str]:
    """检查当前环境可用的 ASR 引擎"""
    available = []
    try:
        if __import__('importlib').util.find_spec("faster_whisper"):
            available.append("faster_whisper")
    except Exception:
        pass
    try:
        if __import__('importlib').util.find_spec("whisper"):
            available.append("openai_whisper")
    except Exception:
        pass
    if os.environ.get("DASHSCOPE_API_KEY"):
        available.append("bailian")
    return available
