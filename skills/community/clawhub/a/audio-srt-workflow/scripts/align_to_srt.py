#!/usr/bin/env python3
"""
Generate an SRT file by aligning a reference transcript text to an audio file.

This script uses faster-whisper for token-level timestamps, then aligns those
tokens with the user-provided reference text and interpolates missing timings.
"""

from __future__ import annotations

import argparse
import bisect
import difflib
import os
import re
import statistics
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple

try:
    from faster_whisper import WhisperModel
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: faster-whisper.\n"
        "Install with: pip install -r requirements.txt"
    ) from exc

try:
    import av
except ImportError:  # pragma: no cover
    av = None

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None


CJK_OR_WORD_PATTERN = re.compile(
    r"[\u4e00-\u9fff]|[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?", re.UNICODE
)
PUNCT_BOUNDARY_PATTERN = re.compile(r"[。！？!?；;，,、：:]")
REMOVE_COMMA_PERIOD_TABLE = str.maketrans("", "", ",.，。")
CHINESE_LANGUAGE_CODES = {"yue", "cmn", "wuu", "gan", "hak", "nan", "hsn"}


@dataclass
class TimedToken:
    text: str
    start: float
    end: float


@dataclass
class SubtitleUnit:
    text: str
    start_idx: int
    end_idx: int


@dataclass
class SrtEntryDraft:
    seq: int
    start: float
    end: float
    text: str
    token_count: int
    matched_count: int


@dataclass
class AlignmentConfig:
    model_name: str
    device: str
    compute_type: str
    language: Optional[str]
    beam_size: int
    start_lag: float
    end_hold: float
    min_gap: float
    snap_window: float
    no_waveform_snap: bool
    max_unit_duration: float
    split_pause_gap: float
    max_split_depth: int
    max_early_lead: float
    anchor_min_voice: float
    onset_lookahead: float
    tail_end_guard: float


@dataclass
class AlignmentRunResult:
    output_path: Path
    detected_language: str
    reference_token_count: int
    aligned_token_count: int
    coverage: float
    raw_unit_count: int
    refined_unit_count: int
    waveform_interval_count: int
    srt_entry_count: int


@dataclass
class TimedSubtitleEntry:
    text: str
    start: float
    end: float


@dataclass
class AutoSubtitleRunResult:
    output_path: Path
    detected_language: str
    raw_segment_count: int
    raw_entry_count: int
    refined_entry_count: int
    waveform_interval_count: int


def tokenize(text: str) -> List[str]:
    tokens: List[str] = []
    for match in CJK_OR_WORD_PATTERN.finditer(text):
        token = match.group(0)
        if token and token[0].isascii():
            token = token.lower()
        tokens.append(token)
    return tokens


def remove_commas_and_periods(text: str) -> str:
    return text.translate(REMOVE_COMMA_PERIOD_TABLE)


def should_strip_commas_periods(language: Optional[str]) -> bool:
    if not language:
        return False
    normalized = language.strip().lower().replace("_", "-")
    if not normalized:
        return False
    if normalized.startswith("zh"):
        return True
    return normalized in CHINESE_LANGUAGE_CODES


def format_subtitle_text(text: str, output_language: Optional[str]) -> str:
    cleaned = text.strip()
    if should_strip_commas_periods(output_language):
        cleaned = remove_commas_and_periods(cleaned)
    return cleaned


def merge_short_units(units: Sequence[str], min_chars: int = 8) -> List[str]:
    if not units:
        return []

    merged: List[str] = []
    for unit in units:
        cur = unit.strip()
        if not cur:
            continue
        prev_has_strong_break = bool(merged and re.search(r"[。！？!?；;]$", merged[-1]))
        cur_has_strong_break = bool(re.search(r"[。！？!?；;]$", cur))
        if len(cur) < min_chars and merged and not prev_has_strong_break and not cur_has_strong_break:
            merged[-1] = f"{merged[-1]}{cur}"
        else:
            merged.append(cur)
    return merged


def split_unit_text(text: str) -> List[str]:
    normalized = re.sub(r"\s+", " ", text.strip())
    if not normalized:
        return []

    # Prefer sentence punctuation for timing boundaries.
    sentences = [
        p.strip()
        for p in re.split(r"(?<=[。！？!?；;])\s*", normalized)
        if p.strip()
    ]
    if not sentences:
        sentences = [normalized]

    out: List[str] = []
    for sentence in sentences:
        # If a sentence is long, split by clause punctuation.
        if len(sentence) > 34:
            clauses = [
                c.strip()
                for c in re.split(r"(?<=[，,、：:])\s*", sentence)
                if c.strip()
            ]
            if len(clauses) > 1:
                out.extend(clauses)
            else:
                out.append(sentence)
        else:
            out.append(sentence)
    return merge_short_units(out, min_chars=8)


def split_to_units(text: str) -> List[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) >= 1:
        units: List[str] = []
        for line in lines:
            units.extend(split_unit_text(line))
        return units

    merged = re.sub(r"\s+", " ", text.strip())
    if not merged:
        return []

    return split_unit_text(merged)


def build_reference(units_text: Sequence[str]) -> Tuple[List[SubtitleUnit], List[str]]:
    units: List[SubtitleUnit] = []
    all_tokens: List[str] = []
    cursor = 0
    for raw in units_text:
        unit_tokens = tokenize(raw)
        start = cursor
        cursor += len(unit_tokens)
        units.append(SubtitleUnit(text=raw, start_idx=start, end_idx=cursor))
        all_tokens.extend(unit_tokens)
    return units, all_tokens


def resolve_model_source(model_name: str) -> str:
    raw = (model_name or "").strip() or "small"

    direct_path = Path(raw).expanduser()
    if direct_path.exists():
        return str(direct_path.resolve())

    model_root = (os.getenv("FASTER_WHISPER_MODEL_DIR") or "").strip()
    if model_root:
        root_path = Path(model_root).expanduser()
        candidate = (root_path / raw).resolve()
        if candidate.exists():
            return str(candidate)

    return raw


def transcribe_to_tokens(
    audio_path: Path,
    model_name: str,
    device: str,
    compute_type: str,
    language: Optional[str],
    beam_size: int,
    progress: Optional[Callable[[str], None]] = None,
) -> Tuple[List[TimedToken], float, Optional[str]]:
    model_source = resolve_model_source(model_name)
    if progress:
        progress(f"Loading Whisper model: {model_source} ({device}/{compute_type})")
    model = WhisperModel(model_source, device=device, compute_type=compute_type)

    if progress:
        progress("Transcribing audio to token timestamps (first run may download model).")
    segments, info = model.transcribe(
        str(audio_path),
        language=language,
        beam_size=beam_size,
        word_timestamps=True,
        vad_filter=True,
    )

    timed_tokens: List[TimedToken] = []
    audio_end = 0.0
    seg_count = 0

    for segment in segments:
        seg_count += 1
        if progress and (seg_count == 1 or seg_count % 40 == 0):
            progress(f"ASR progress: processed segments = {seg_count}")
        seg_start = float(segment.start or audio_end)
        seg_end = float(segment.end or seg_start)
        audio_end = max(audio_end, seg_end)

        if segment.words:
            for word in segment.words:
                raw_word = (word.word or "").strip()
                if not raw_word:
                    continue
                token_texts = tokenize(raw_word)
                if not token_texts:
                    continue

                word_start = float(word.start if word.start is not None else seg_start)
                word_end = float(word.end if word.end is not None else seg_end)
                if word_end <= word_start:
                    word_end = word_start + 0.05

                step = (word_end - word_start) / len(token_texts)
                for idx, token in enumerate(token_texts):
                    tok_start = word_start + idx * step
                    tok_end = tok_start + step
                    timed_tokens.append(TimedToken(token, tok_start, tok_end))
        else:
            fallback_tokens = tokenize(segment.text or "")
            if not fallback_tokens:
                continue
            seg_dur = max(seg_end - seg_start, 0.1)
            step = seg_dur / len(fallback_tokens)
            for idx, token in enumerate(fallback_tokens):
                tok_start = seg_start + idx * step
                tok_end = tok_start + step
                timed_tokens.append(TimedToken(token, tok_start, tok_end))

    if timed_tokens:
        audio_end = max(audio_end, timed_tokens[-1].end)

    detected_language = getattr(info, "language", None)
    if progress:
        progress(
            f"ASR done: segments={seg_count}, tokens={len(timed_tokens)}, "
            f"detected_language={detected_language or 'unknown'}"
        )
    return timed_tokens, audio_end, detected_language


def split_segment_to_timed_entries(
    text: str,
    start: float,
    end: float,
) -> List[TimedSubtitleEntry]:
    cleaned = text.strip()
    if not cleaned:
        return []

    parts = split_unit_text(cleaned)
    if not parts:
        return []

    if end <= start:
        end = start + 0.30

    if len(parts) == 1:
        return [TimedSubtitleEntry(text=parts[0], start=start, end=end)]

    weights = [max(1, len(tokenize(part))) for part in parts]
    total_weight = sum(weights)
    if total_weight <= 0:
        total_weight = len(parts)

    seg_duration = max(end - start, 0.30)
    cursor = start
    entries: List[TimedSubtitleEntry] = []
    for idx, (part, weight) in enumerate(zip(parts, weights)):
        part_start = cursor
        if idx == len(parts) - 1:
            part_end = end
        else:
            part_end = cursor + seg_duration * (weight / total_weight)
        if part_end <= part_start:
            part_end = part_start + 0.20
        entries.append(TimedSubtitleEntry(text=part, start=part_start, end=part_end))
        cursor = part_end
    return entries


def transcribe_to_timed_subtitles(
    audio_path: Path,
    model_name: str,
    device: str,
    compute_type: str,
    language: Optional[str],
    beam_size: int,
    progress: Optional[Callable[[str], None]] = None,
) -> Tuple[List[TimedSubtitleEntry], float, Optional[str], int]:
    model_source = resolve_model_source(model_name)
    if progress:
        progress(f"Loading Whisper model: {model_source} ({device}/{compute_type})")
    model = WhisperModel(model_source, device=device, compute_type=compute_type)

    if progress:
        progress("Transcribing audio to subtitle segments (first run may download model).")
    segments, info = model.transcribe(
        str(audio_path),
        language=language,
        beam_size=beam_size,
        word_timestamps=True,
        vad_filter=True,
    )

    entries: List[TimedSubtitleEntry] = []
    audio_end = 0.0
    segment_count = 0
    iter_count = 0
    for segment in segments:
        iter_count += 1
        if progress and (iter_count == 1 or iter_count % 40 == 0):
            progress(f"ASR progress: processed segments = {iter_count}")
        text = (segment.text or "").strip()
        if not text:
            continue
        segment_count += 1
        seg_start = float(segment.start if segment.start is not None else audio_end)
        seg_end = float(segment.end if segment.end is not None else seg_start + 0.30)
        if seg_end <= seg_start:
            seg_end = seg_start + 0.30
        audio_end = max(audio_end, seg_end)
        entries.extend(
            split_segment_to_timed_entries(
                text=text,
                start=seg_start,
                end=seg_end,
            )
        )

    detected_language = getattr(info, "language", None)
    if progress:
        progress(
            f"ASR done: segments={segment_count}, entries={len(entries)}, "
            f"detected_language={detected_language or 'unknown'}"
        )
    return entries, audio_end, detected_language, segment_count


def fill_short_false(mask: "np.ndarray", max_gap_frames: int) -> "np.ndarray":
    out = mask.copy()
    n = out.shape[0]
    i = 0
    while i < n:
        if out[i]:
            i += 1
            continue
        j = i
        while j < n and not out[j]:
            j += 1
        if i > 0 and j < n and (j - i) <= max_gap_frames:
            out[i:j] = True
        i = j
    return out


def drop_short_true(mask: "np.ndarray", min_true_frames: int) -> "np.ndarray":
    out = mask.copy()
    n = out.shape[0]
    i = 0
    while i < n:
        if not out[i]:
            i += 1
            continue
        j = i
        while j < n and out[j]:
            j += 1
        if (j - i) < min_true_frames:
            out[i:j] = False
        i = j
    return out


def extract_voice_intervals(
    audio_path: Path,
    sample_rate: int = 16_000,
    frame_ms: int = 10,
) -> List[Tuple[float, float]]:
    if av is None or np is None:
        return []

    try:
        container = av.open(str(audio_path))
    except Exception:
        return []

    stream = next((s for s in container.streams if s.type == "audio"), None)
    if stream is None:
        container.close()
        return []

    resampler = av.audio.resampler.AudioResampler(
        format="s16",
        layout="mono",
        rate=sample_rate,
    )

    chunks: List["np.ndarray"] = []
    try:
        for frame in container.decode(audio=stream.index):
            converted = resampler.resample(frame)
            if converted is None:
                continue
            frames = converted if isinstance(converted, list) else [converted]
            for frm in frames:
                arr = frm.to_ndarray()
                if arr.size == 0:
                    continue
                chunks.append(arr.reshape(-1).astype(np.float32) / 32768.0)

        flushed = resampler.resample(None)
        if flushed is not None:
            frames = flushed if isinstance(flushed, list) else [flushed]
            for frm in frames:
                arr = frm.to_ndarray()
                if arr.size == 0:
                    continue
                chunks.append(arr.reshape(-1).astype(np.float32) / 32768.0)
    except Exception:
        container.close()
        return []
    finally:
        container.close()

    if not chunks:
        return []

    audio = np.concatenate(chunks)
    frame_len = max(1, int(sample_rate * frame_ms / 1000))
    n_frames = audio.shape[0] // frame_len
    if n_frames <= 1:
        return []

    trimmed = audio[: n_frames * frame_len].reshape(n_frames, frame_len)
    rms = np.sqrt(np.mean(trimmed * trimmed, axis=1))

    low = float(np.percentile(rms, 25))
    high = float(np.percentile(rms, 90))
    # Conservative threshold: avoid missing low-energy speech.
    threshold = max(low * 1.2, low + (high - low) * 0.16, 5e-5)
    mask = rms >= threshold

    # Bridge short dips in speech energy and remove very short bursts.
    mask = fill_short_false(mask, max_gap_frames=max(1, int(0.22 / (frame_ms / 1000))))
    mask = drop_short_true(mask, min_true_frames=max(1, int(0.05 / (frame_ms / 1000))))

    hop = frame_ms / 1000.0
    intervals: List[Tuple[float, float]] = []
    i = 0
    while i < n_frames:
        if not mask[i]:
            i += 1
            continue
        j = i + 1
        while j < n_frames and mask[j]:
            j += 1
        start = i * hop
        end = j * hop
        if end - start >= 0.06:
            intervals.append((start, end))
        i = j

    return intervals


def lis_on_pairs(pairs: Sequence[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if not pairs:
        return []

    tails: List[int] = []
    tails_idx: List[int] = []
    prev_idx: List[int] = [-1] * len(pairs)

    for idx, (_, asr_idx) in enumerate(pairs):
        pos = bisect.bisect_left(tails, asr_idx)
        if pos == len(tails):
            tails.append(asr_idx)
            tails_idx.append(idx)
        else:
            tails[pos] = asr_idx
            tails_idx[pos] = idx
        if pos > 0:
            prev_idx[idx] = tails_idx[pos - 1]

    chain: List[Tuple[int, int]] = []
    cur = tails_idx[-1] if tails_idx else -1
    while cur != -1:
        chain.append(pairs[cur])
        cur = prev_idx[cur]
    chain.reverse()
    return chain


def fill_with_sequence_matcher(
    mapping: List[Optional[int]],
    ref_tokens: Sequence[str],
    asr_tokens: Sequence[str],
    ref_offset: int,
    asr_offset: int,
) -> None:
    matcher = difflib.SequenceMatcher(a=ref_tokens, b=asr_tokens, autojunk=False)
    for block in matcher.get_matching_blocks():
        if block.size <= 0:
            continue
        for i in range(block.size):
            mapping[ref_offset + block.a + i] = asr_offset + block.b + i


def build_ref_to_asr_index(ref_tokens: Sequence[str], asr_tokens: Sequence[str]) -> List[Optional[int]]:
    mapping: List[Optional[int]] = [None] * len(ref_tokens)
    if not ref_tokens or not asr_tokens:
        return mapping

    ref_counter = Counter(ref_tokens)
    asr_counter = Counter(asr_tokens)
    asr_unique_pos = {
        token: idx for idx, token in enumerate(asr_tokens) if asr_counter[token] == 1
    }

    unique_pairs = [
        (idx, asr_unique_pos[token])
        for idx, token in enumerate(ref_tokens)
        if ref_counter[token] == 1 and token in asr_unique_pos
    ]
    anchors = lis_on_pairs(unique_pairs)

    # Fallback to plain matcher when too few reliable anchors are available.
    min_anchor_count = max(12, int(min(len(ref_tokens), len(asr_tokens)) * 0.008))
    if len(anchors) < min_anchor_count:
        fill_with_sequence_matcher(mapping, ref_tokens, asr_tokens, 0, 0)
        return mapping

    for ref_idx, asr_idx in anchors:
        mapping[ref_idx] = asr_idx

    boundaries: List[Tuple[int, int]] = [(-1, -1)]
    boundaries.extend(anchors)
    boundaries.append((len(ref_tokens), len(asr_tokens)))

    for (ref_left, asr_left), (ref_right, asr_right) in zip(boundaries, boundaries[1:]):
        ref_start = ref_left + 1
        ref_end = ref_right
        asr_start = asr_left + 1
        asr_end = asr_right
        if ref_start >= ref_end or asr_start >= asr_end:
            continue
        fill_with_sequence_matcher(
            mapping=mapping,
            ref_tokens=ref_tokens[ref_start:ref_end],
            asr_tokens=asr_tokens[asr_start:asr_end],
            ref_offset=ref_start,
            asr_offset=asr_start,
        )

    return mapping


def infer_token_times(
    ref_to_asr: Sequence[Optional[int]],
    asr_tokens: Sequence[TimedToken],
    audio_duration: float,
) -> List[Tuple[float, float]]:
    n = len(ref_to_asr)
    if n == 0:
        return []

    times: List[Optional[Tuple[float, float]]] = [None] * n
    for idx, asr_idx in enumerate(ref_to_asr):
        if asr_idx is None:
            continue
        if 0 <= asr_idx < len(asr_tokens):
            tok = asr_tokens[asr_idx]
            times[idx] = (tok.start, tok.end)

    known = [i for i, item in enumerate(times) if item is not None]

    durations = [max(t.end - t.start, 0.05) for t in asr_tokens]
    avg_duration = statistics.median(durations) if durations else 0.12
    avg_duration = max(avg_duration, 0.05)

    if not known:
        total = max(audio_duration, n * avg_duration)
        step = total / n
        filled = [(i * step, (i + 1) * step) for i in range(n)]
        return filled

    first = known[0]
    for i in range(first - 1, -1, -1):
        nxt_start = times[i + 1][0] if times[i + 1] else 0.0
        start = max(0.0, nxt_start - avg_duration)
        times[i] = (start, nxt_start)

    last = known[-1]
    for i in range(last + 1, n):
        prev_end = times[i - 1][1] if times[i - 1] else 0.0
        times[i] = (prev_end, prev_end + avg_duration)

    i = first + 1
    while i <= last:
        if times[i] is not None:
            i += 1
            continue
        span_start = i
        while i <= last and times[i] is None:
            i += 1
        span_end = i - 1

        left_end = times[span_start - 1][1] if times[span_start - 1] else 0.0
        right_start = times[i][0] if i < n and times[i] else left_end

        count = span_end - span_start + 1
        if right_start <= left_end:
            right_start = left_end + count * avg_duration
        step = (right_start - left_end) / count

        for j in range(count):
            start = left_end + j * step
            end = start + step
            times[span_start + j] = (start, end)

    filled_times: List[Tuple[float, float]] = []
    prev_end = 0.0
    for item in times:
        assert item is not None
        start, end = item
        start = max(start, prev_end)
        end = max(end, start + 0.05)
        filled_times.append((start, end))
        prev_end = end

    return filled_times


def split_text_on_punctuation_near_token(
    text: str,
    target_token_offset: int,
    min_side_tokens: int,
) -> Optional[Tuple[str, str, int]]:
    total_tokens = tokenize(text)
    total_count = len(total_tokens)
    if total_count < min_side_tokens * 2:
        return None

    candidates: List[Tuple[int, int, int, str, str]] = []
    for match in PUNCT_BOUNDARY_PATTERN.finditer(text):
        left_text = text[: match.end()].strip()
        right_text = text[match.end() :].strip()
        if not left_text or not right_text:
            continue
        left_tokens = tokenize(left_text)
        right_tokens = tokenize(right_text)
        left_count = len(left_tokens)
        right_count = len(right_tokens)
        if left_count < min_side_tokens or right_count < min_side_tokens:
            continue
        if left_count + right_count != total_count:
            continue
        distance = abs(left_count - target_token_offset)
        center_bias = abs(left_count - total_count // 2)
        candidates.append((distance, center_bias, left_count, left_text, right_text))

    if not candidates:
        return None

    candidates.sort(key=lambda item: (item[0], item[1], item[2]))
    _, _, left_count, left_text, right_text = candidates[0]
    return left_text, right_text, left_count


def refine_units_by_timing(
    units: Sequence[SubtitleUnit],
    token_times: Sequence[Tuple[float, float]],
    max_unit_duration: float,
    split_pause_gap: float,
    max_split_depth: int,
    min_tokens_for_split: int = 12,
) -> List[SubtitleUnit]:
    if not units:
        return []

    refined: List[SubtitleUnit] = []
    for unit in units:
        pending: List[Tuple[SubtitleUnit, int]] = [(unit, 0)]
        while pending:
            cur, depth = pending.pop(0)
            token_count = cur.end_idx - cur.start_idx
            if token_count <= 0:
                continue
            if cur.start_idx >= len(token_times) or cur.end_idx - 1 >= len(token_times):
                refined.append(cur)
                continue
            if depth >= max_split_depth or token_count < min_tokens_for_split:
                refined.append(cur)
                continue

            start = token_times[cur.start_idx][0]
            end = token_times[cur.end_idx - 1][1]
            duration = end - start

            max_gap = 0.0
            split_target: Optional[int] = None
            for idx in range(cur.start_idx, cur.end_idx - 1):
                gap = token_times[idx + 1][0] - token_times[idx][1]
                if gap > max_gap:
                    max_gap = gap
                    split_target = (idx + 1) - cur.start_idx

            should_split = duration > max_unit_duration or max_gap >= split_pause_gap
            if not should_split or split_target is None:
                refined.append(cur)
                continue

            split_result = split_text_on_punctuation_near_token(
                text=cur.text,
                target_token_offset=split_target,
                min_side_tokens=max(4, min_tokens_for_split // 3),
            )
            if split_result is None:
                refined.append(cur)
                continue
            left_text, right_text, left_count = split_result
            if left_count <= 0 or left_count >= token_count:
                refined.append(cur)
                continue

            left = SubtitleUnit(
                text=left_text,
                start_idx=cur.start_idx,
                end_idx=cur.start_idx + left_count,
            )
            right = SubtitleUnit(
                text=right_text,
                start_idx=cur.start_idx + left_count,
                end_idx=cur.end_idx,
            )
            next_depth = depth + 1
            pending.insert(0, (right, next_depth))
            pending.insert(0, (left, next_depth))

    return refined


def sec_to_srt_time(sec: float) -> str:
    ms = int(round(max(sec, 0.0) * 1000.0))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def locate_voice_neighbors(
    intervals: Sequence[Tuple[float, float]],
    time_point: float,
) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    prev_idx: Optional[int] = None
    for idx, (start, end) in enumerate(intervals):
        if start <= time_point <= end:
            next_idx = idx + 1 if idx + 1 < len(intervals) else None
            return idx, prev_idx, next_idx
        if time_point < start:
            return None, prev_idx, idx
        prev_idx = idx
    return None, prev_idx, None


def snap_start_to_waveform(
    start: float,
    intervals: Sequence[Tuple[float, float]],
    start_lag: float,
    snap_window: float,
    early_trigger: float = 0.10,
) -> float:
    inside_idx, _, next_idx = locate_voice_neighbors(intervals, start)
    if inside_idx is not None:
        interval_start, _ = intervals[inside_idx]
        if start - interval_start <= 0.35:
            return interval_start + start_lag
        return start

    if next_idx is not None:
        next_start, _ = intervals[next_idx]
        lead = next_start - start
        if early_trigger <= lead <= snap_window:
            return next_start + start_lag
    return start


def snap_end_to_waveform(
    end: float,
    intervals: Sequence[Tuple[float, float]],
    end_hold: float,
    snap_window: float,
) -> float:
    inside_idx, prev_idx, _ = locate_voice_neighbors(intervals, end)
    if inside_idx is not None:
        _, interval_end = intervals[inside_idx]
        if interval_end - end <= 0.30:
            return interval_end + end_hold
        return end

    if prev_idx is not None:
        _, prev_end = intervals[prev_idx]
        if 0.0 <= (end - prev_end) <= snap_window:
            return prev_end + end_hold
    return end


def clamp_start_to_effective_onset(
    start: float,
    anchor_intervals: Sequence[Tuple[float, float]],
    max_early_lead: float,
    onset_lookahead: float,
    tail_end_guard: float,
) -> float:
    if not anchor_intervals:
        return start

    inside_idx, _, next_idx = locate_voice_neighbors(anchor_intervals, start)
    if inside_idx is not None:
        _, inside_end = anchor_intervals[inside_idx]
        if next_idx is not None and (inside_end - start) <= tail_end_guard:
            next_start, _ = anchor_intervals[next_idx]
            lead = next_start - start
            if 0.0 < lead <= onset_lookahead:
                earliest_allowed = next_start - max_early_lead
                if start < earliest_allowed:
                    return earliest_allowed
        return start
    if next_idx is None:
        return start

    next_start, _ = anchor_intervals[next_idx]
    lead = next_start - start
    if lead <= 0.0 or lead > onset_lookahead:
        return start

    earliest_allowed = next_start - max_early_lead
    if start < earliest_allowed:
        return earliest_allowed
    return start


def normalize_timed_entries(
    entries: Sequence[TimedSubtitleEntry],
    voice_intervals: Sequence[Tuple[float, float]],
    start_lag: float,
    end_hold: float,
    min_gap: float,
    snap_window: float,
    max_early_lead: float,
    anchor_min_voice: float,
    onset_lookahead: float,
    tail_end_guard: float,
) -> List[TimedSubtitleEntry]:
    if not entries:
        return []

    min_duration = 0.20
    max_start_shift = 0.45
    max_end_shift = 0.40
    anchor_intervals = [
        item for item in voice_intervals if (item[1] - item[0]) >= anchor_min_voice
    ]
    if not anchor_intervals:
        anchor_intervals = list(voice_intervals)

    staged: List[TimedSubtitleEntry] = []
    for entry in entries:
        text = entry.text.strip()
        if not text:
            continue
        start = max(0.0, entry.start)
        end = max(start + 0.05, entry.end)

        if voice_intervals:
            snapped_start = snap_start_to_waveform(
                start=start,
                intervals=voice_intervals,
                start_lag=start_lag,
                snap_window=snap_window,
            )
            if abs(snapped_start - start) <= max_start_shift:
                start = snapped_start

            start = clamp_start_to_effective_onset(
                start=start,
                anchor_intervals=anchor_intervals,
                max_early_lead=max_early_lead,
                onset_lookahead=onset_lookahead,
                tail_end_guard=tail_end_guard,
            )

            snapped_end = snap_end_to_waveform(
                end=end,
                intervals=voice_intervals,
                end_hold=end_hold,
                snap_window=snap_window,
            )
            if abs(snapped_end - end) <= max_end_shift:
                end = snapped_end

        if end <= start:
            end = start + min_duration
        staged.append(TimedSubtitleEntry(text=text, start=start, end=end))

    if not staged:
        return []

    staged.sort(key=lambda x: (x.start, x.end))
    normalized: List[TimedSubtitleEntry] = []
    prev_end = 0.0
    for idx, entry in enumerate(staged):
        start = max(entry.start, prev_end + min_gap)
        end = max(entry.end, start + min_duration)

        if idx + 1 < len(staged):
            next_start = max(staged[idx + 1].start, start + min_duration)
            cap_end = next_start - min_gap
            if cap_end >= start + min_duration:
                end = min(end, cap_end)

        end = max(end, start + min_duration)
        normalized.append(TimedSubtitleEntry(text=entry.text, start=start, end=end))
        prev_end = end

    return normalized


def write_srt(
    units: Sequence[SubtitleUnit],
    token_times: Sequence[Tuple[float, float]],
    ref_to_asr: Sequence[Optional[int]],
    voice_intervals: Sequence[Tuple[float, float]],
    start_lag: float,
    end_hold: float,
    min_gap: float,
    snap_window: float,
    max_early_lead: float,
    anchor_min_voice: float,
    onset_lookahead: float,
    tail_end_guard: float,
    output_path: Path,
    output_language: Optional[str] = None,
) -> int:
    # Stricter defaults: reduce subtitle display in silent edges.
    min_duration = 0.20
    matched_tail_trim = 0.02
    unmatched_tail_trim = 0.06
    max_unmatched_duration = 2.80
    sec_per_unmatched_token = 0.18
    low_confidence_ratio = 0.72
    max_start_shift = 0.45
    max_end_shift = 0.40
    anchor_intervals = [
        item for item in voice_intervals if (item[1] - item[0]) >= anchor_min_voice
    ]
    if not anchor_intervals:
        anchor_intervals = list(voice_intervals)

    drafts: List[SrtEntryDraft] = []
    idx = 1
    for unit in units:
        if unit.end_idx <= unit.start_idx:
            continue
        if unit.start_idx >= len(token_times) or unit.end_idx - 1 >= len(token_times):
            continue
        matched = [
            i
            for i in range(unit.start_idx, unit.end_idx)
            if i < len(ref_to_asr) and ref_to_asr[i] is not None
        ]
        token_count = unit.end_idx - unit.start_idx
        matched_count = len(matched)
        full_start = token_times[unit.start_idx][0]
        full_end = token_times[unit.end_idx - 1][1] - unmatched_tail_trim
        if matched:
            match_ratio = matched_count / token_count if token_count > 0 else 0.0
            if match_ratio >= low_confidence_ratio:
                start = token_times[matched[0]][0]
                end = token_times[matched[-1]][1] - matched_tail_trim
            else:
                start = full_start
                end = full_end
        else:
            start = full_start
            end = full_end
            est = min(max_unmatched_duration, max(min_duration, token_count * sec_per_unmatched_token))
            end = min(end, start + est)

        if voice_intervals:
            snapped_start = snap_start_to_waveform(
                start=start,
                intervals=voice_intervals,
                start_lag=start_lag,
                snap_window=snap_window,
            )
            if abs(snapped_start - start) <= max_start_shift:
                start = snapped_start

            start = clamp_start_to_effective_onset(
                start=start,
                anchor_intervals=anchor_intervals,
                max_early_lead=max_early_lead,
                onset_lookahead=onset_lookahead,
                tail_end_guard=tail_end_guard,
            )

            snapped_end = snap_end_to_waveform(
                end=end,
                intervals=voice_intervals,
                end_hold=end_hold,
                snap_window=snap_window,
            )
            if abs(snapped_end - end) <= max_end_shift:
                end = snapped_end

        if end <= start:
            end = start + min_duration
        text = format_subtitle_text(unit.text, output_language=output_language)
        if not text:
            continue
        drafts.append(
            SrtEntryDraft(
                seq=idx,
                start=max(0.0, start),
                end=max(0.0, end),
                text=text,
                token_count=token_count,
                matched_count=matched_count,
            )
        )
        idx += 1

    if not drafts:
        output_path.write_text("", encoding="utf-8")
        return 0

    drafts.sort(key=lambda x: (x.start, x.end, x.seq))
    entries: List[Tuple[int, float, float, str]] = []
    prev_end = 0.0
    for i, entry in enumerate(drafts):
        start = max(entry.start, prev_end + min_gap)
        end = max(entry.end, start + min_duration)

        if i + 1 < len(drafts):
            next_start = max(drafts[i + 1].start, start + min_duration)
            cap_end = next_start - min_gap
            if cap_end >= start + min_duration:
                end = min(end, cap_end)

        end = max(end, start + min_duration)
        entries.append((len(entries) + 1, start, end, entry.text))
        prev_end = end

    with output_path.open("w", encoding="utf-8") as f:
        for seq, start, end, text in entries:
            f.write(f"{seq}\n")
            f.write(f"{sec_to_srt_time(start)} --> {sec_to_srt_time(end)}\n")
            f.write(f"{text}\n\n")

    return len(entries)


def write_timed_entries_srt(
    entries: Sequence[TimedSubtitleEntry],
    output_path: Path,
    output_language: Optional[str] = None,
) -> int:
    if not entries:
        output_path.write_text("", encoding="utf-8")
        return 0

    written = 0
    with output_path.open("w", encoding="utf-8") as f:
        for entry in entries:
            text = format_subtitle_text(entry.text, output_language=output_language)
            if not text:
                continue
            written += 1
            f.write(f"{written}\n")
            f.write(f"{sec_to_srt_time(entry.start)} --> {sec_to_srt_time(entry.end)}\n")
            f.write(f"{text}\n\n")

    return written


def build_alignment_config(args: argparse.Namespace) -> AlignmentConfig:
    return AlignmentConfig(
        model_name=args.model,
        device=args.device,
        compute_type=args.compute_type,
        language=args.language,
        beam_size=args.beam_size,
        start_lag=max(0.0, args.start_lag),
        end_hold=max(0.0, args.end_hold),
        min_gap=max(0.0, args.min_gap),
        snap_window=max(0.05, args.snap_window),
        no_waveform_snap=bool(args.no_waveform_snap),
        max_unit_duration=max(2.0, args.max_unit_duration),
        split_pause_gap=max(0.15, args.split_pause_gap),
        max_split_depth=max(0, args.max_split_depth),
        max_early_lead=max(0.0, args.max_early_lead),
        anchor_min_voice=max(0.06, args.anchor_min_voice),
        onset_lookahead=max(0.10, args.onset_lookahead),
        tail_end_guard=max(0.0, args.tail_end_guard),
    )


def resolve_output_path(
    audio_path: Path,
    output_arg: Optional[str],
    with_date_suffix: bool,
) -> Path:
    output_path = (
        Path(output_arg).expanduser().resolve()
        if output_arg
        else (Path.cwd() / f"{audio_path.stem}.srt")
    )
    if with_date_suffix:
        date_tag = datetime.now().strftime("%Y%m%d")
        if not output_path.stem.endswith(f"_{date_tag}"):
            output_path = output_path.with_name(f"{output_path.stem}_{date_tag}{output_path.suffix}")
    return output_path


def run_alignment_pipeline(
    audio_path: Path,
    text_path: Path,
    output_path: Path,
    config: AlignmentConfig,
    progress: Optional[Callable[[str], None]] = None,
) -> AlignmentRunResult:
    if progress:
        progress("Validating input files...")
    if not audio_path.exists():
        raise SystemExit(f"Audio file not found: {audio_path}")
    if not text_path.exists():
        raise SystemExit(f"Text file not found: {text_path}")

    if progress:
        progress("Loading and splitting transcript...")
    reference_text = text_path.read_text(encoding="utf-8")
    units_text = split_to_units(reference_text)
    if not units_text:
        raise SystemExit("Transcript text is empty after preprocessing.")

    units, ref_tokens = build_reference(units_text)
    if not ref_tokens:
        raise SystemExit("No valid tokens found in transcript text.")

    asr_tokens, audio_duration, detected_language = transcribe_to_tokens(
        audio_path=audio_path,
        model_name=config.model_name,
        device=config.device,
        compute_type=config.compute_type,
        language=config.language,
        beam_size=config.beam_size,
        progress=progress,
    )
    if not asr_tokens:
        raise SystemExit("Failed to obtain timed tokens from audio.")

    if progress:
        progress("Running token alignment...")
    ref_to_asr = build_ref_to_asr_index(
        ref_tokens=ref_tokens,
        asr_tokens=[t.text for t in asr_tokens],
    )
    if progress:
        progress("Inferring timing for transcript tokens...")
    token_times = infer_token_times(
        ref_to_asr=ref_to_asr,
        asr_tokens=asr_tokens,
        audio_duration=audio_duration,
    )
    if progress:
        progress("Refining subtitle units by timing and pauses...")
    refined_units = refine_units_by_timing(
        units=units,
        token_times=token_times,
        max_unit_duration=config.max_unit_duration,
        split_pause_gap=config.split_pause_gap,
        max_split_depth=config.max_split_depth,
    )
    voice_intervals: List[Tuple[float, float]] = []
    if not config.no_waveform_snap:
        if progress:
            progress("Extracting waveform voice intervals...")
        voice_intervals = extract_voice_intervals(audio_path=audio_path)

    if progress:
        progress("Writing SRT...")
    output_language = detected_language or config.language
    written = write_srt(
        units=refined_units,
        token_times=token_times,
        ref_to_asr=ref_to_asr,
        voice_intervals=voice_intervals,
        start_lag=config.start_lag,
        end_hold=config.end_hold,
        min_gap=config.min_gap,
        snap_window=config.snap_window,
        max_early_lead=config.max_early_lead,
        anchor_min_voice=config.anchor_min_voice,
        onset_lookahead=config.onset_lookahead,
        tail_end_guard=config.tail_end_guard,
        output_path=output_path,
        output_language=output_language,
    )

    aligned = sum(1 for item in ref_to_asr if item is not None)
    coverage = 100.0 * aligned / len(ref_to_asr)
    detected = detected_language or "unknown"
    if progress:
        progress(
            f"Alignment done: coverage={coverage:.1f}%, entries={written}, "
            f"language={detected}"
        )
    return AlignmentRunResult(
        output_path=output_path,
        detected_language=detected,
        reference_token_count=len(ref_tokens),
        aligned_token_count=aligned,
        coverage=coverage,
        raw_unit_count=len(units),
        refined_unit_count=len(refined_units),
        waveform_interval_count=len(voice_intervals),
        srt_entry_count=written,
    )


def run_auto_subtitle_pipeline(
    audio_path: Path,
    output_path: Path,
    config: AlignmentConfig,
    progress: Optional[Callable[[str], None]] = None,
) -> AutoSubtitleRunResult:
    if progress:
        progress("Validating input files...")
    if not audio_path.exists():
        raise SystemExit(f"Audio file not found: {audio_path}")

    raw_entries, _audio_duration, detected_language, raw_segment_count = transcribe_to_timed_subtitles(
        audio_path=audio_path,
        model_name=config.model_name,
        device=config.device,
        compute_type=config.compute_type,
        language=config.language,
        beam_size=config.beam_size,
        progress=progress,
    )
    if not raw_entries:
        raise SystemExit("Failed to produce subtitles from audio.")

    voice_intervals: List[Tuple[float, float]] = []
    if not config.no_waveform_snap:
        if progress:
            progress("Extracting waveform voice intervals...")
        voice_intervals = extract_voice_intervals(audio_path=audio_path)

    if progress:
        progress("Applying waveform snap and anti-early policy...")
    refined_entries = normalize_timed_entries(
        entries=raw_entries,
        voice_intervals=voice_intervals,
        start_lag=config.start_lag,
        end_hold=config.end_hold,
        min_gap=config.min_gap,
        snap_window=config.snap_window,
        max_early_lead=config.max_early_lead,
        anchor_min_voice=config.anchor_min_voice,
        onset_lookahead=config.onset_lookahead,
        tail_end_guard=config.tail_end_guard,
    )
    written = write_timed_entries_srt(
        entries=refined_entries,
        output_path=output_path,
        output_language=(detected_language or config.language),
    )
    detected = detected_language or "unknown"
    if progress:
        progress(
            f"Auto subtitle done: segments={raw_segment_count}, "
            f"entries={written}, language={detected}"
        )
    return AutoSubtitleRunResult(
        output_path=output_path,
        detected_language=detected,
        raw_segment_count=raw_segment_count,
        raw_entry_count=len(raw_entries),
        refined_entry_count=written,
        waveform_interval_count=len(voice_intervals),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Align reference text to audio and output an SRT subtitle file."
    )
    parser.add_argument("--audio", required=True, help="Path to input audio file.")
    parser.add_argument("--text", required=True, help="Path to transcript text file.")
    parser.add_argument(
        "--output",
        help="Path to output .srt file. Defaults to <audio_stem>.srt in current directory.",
    )
    parser.add_argument("--model", default="small", help="faster-whisper model name.")
    parser.add_argument(
        "--device", default="auto", help="Computation device: auto/cpu/cuda."
    )
    parser.add_argument(
        "--compute-type",
        default="int8",
        help="Computation type, e.g. int8, int8_float16, float16, float32.",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Optional language code, e.g. zh, en. If omitted, auto-detect.",
    )
    parser.add_argument("--beam-size", type=int, default=5, help="Beam search size.")
    parser.add_argument(
        "--start-lag",
        type=float,
        default=0.03,
        help="Subtitle start lag after detected voice onset, in seconds.",
    )
    parser.add_argument(
        "--end-hold",
        type=float,
        default=0.12,
        help="Subtitle end hold after detected voice offset, in seconds.",
    )
    parser.add_argument(
        "--min-gap",
        type=float,
        default=0.03,
        help="Minimum gap between adjacent subtitle items, in seconds.",
    )
    parser.add_argument(
        "--snap-window",
        type=float,
        default=0.30,
        help="Max waveform snapping distance for start/end adjustment, in seconds.",
    )
    parser.add_argument(
        "--no-waveform-snap",
        action="store_true",
        help="Disable waveform-based boundary snapping and use token timing only.",
    )
    parser.add_argument(
        "--max-unit-duration",
        type=float,
        default=5.80,
        help="Auto-split subtitle units longer than this duration (seconds) when punctuation allows.",
    )
    parser.add_argument(
        "--split-pause-gap",
        type=float,
        default=0.55,
        help="Auto-split subtitle units when internal token gap exceeds this threshold (seconds).",
    )
    parser.add_argument(
        "--max-split-depth",
        type=int,
        default=2,
        help="Maximum recursive split depth for one subtitle unit.",
    )
    parser.add_argument(
        "--max-early-lead",
        type=float,
        default=0.04,
        help="Clamp subtitle start to at most this many seconds before effective voice onset.",
    )
    parser.add_argument(
        "--anchor-min-voice",
        type=float,
        default=0.28,
        help="Minimum voice interval duration (seconds) to be considered a valid onset anchor.",
    )
    parser.add_argument(
        "--onset-lookahead",
        type=float,
        default=1.20,
        help="Apply early-start clamp only when next effective onset is within this lookahead window.",
    )
    parser.add_argument(
        "--tail-end-guard",
        type=float,
        default=0.08,
        help="If start falls in the last thin tail of an anchor interval, treat it as next-onset candidate.",
    )
    parser.add_argument(
        "--date-suffix",
        action="store_true",
        help="Append current date (YYYYMMDD) to output filename for versioned comparison.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    audio_path = Path(args.audio).expanduser().resolve()
    text_path = Path(args.text).expanduser().resolve()
    output_path = resolve_output_path(
        audio_path=audio_path,
        output_arg=args.output,
        with_date_suffix=bool(args.date_suffix),
    )
    config = build_alignment_config(args)
    result = run_alignment_pipeline(
        audio_path=audio_path,
        text_path=text_path,
        output_path=output_path,
        config=config,
    )

    print(f"Output: {result.output_path}")
    print(f"Detected language: {result.detected_language}")
    print(f"Reference tokens: {result.reference_token_count}")
    print(f"Aligned tokens: {result.aligned_token_count} ({result.coverage:.1f}%)")
    print(f"Units (raw -> refined): {result.raw_unit_count} -> {result.refined_unit_count}")
    print(f"Waveform intervals: {result.waveform_interval_count}")
    print(f"SRT entries: {result.srt_entry_count}")


if __name__ == "__main__":
    main()
