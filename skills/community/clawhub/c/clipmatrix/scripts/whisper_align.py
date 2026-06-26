"""
Whisper时间轴对齐 — 用字幕原文生成时间戳
- 使用faster-whisper
- prev_end防重叠
- 字幕用原文，不转录
"""
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def align_subtitles(audio_path: str, text: str, model_size: str = "base") -> list:
    """
    对齐语音文本，生成带时间戳的字幕
    返回: [{"start": float, "end": float, "text": str}, ...]
    """
    if not audio_path or not Path(audio_path).exists():
        logger.warning(f"Audio file not found: {audio_path}")
        return _fallback_segments(text)

    try:
        from faster_whisper import WhisperModel

        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        segments, _ = model.transcribe(audio_path, language="en", word_timestamps=True)

        # 词级时间轴 → 按3-4词分组为短语行
        result = []
        words_buffer = []
        for seg in segments:
            if hasattr(seg, 'words') and seg.words:
                for w in seg.words:
                    words_buffer.append({"word": w.word.strip(), "start": w.start, "end": w.end})
            else:
                # 降级：整个segment作为一个短语
                result.append({"start": round(seg.start, 2), "end": round(seg.end, 2), "text": seg.text.strip()})
        
        # 每3-5个词组成一个短语行
        i = 0
        while i < len(words_buffer):
            # 🔧 合并被拆分的数字（Whisper把"2,000"拆成"2"和"000"）
            chunk = []
            while i < len(words_buffer):
                w = words_buffer[i]
                # 如果当前词是纯数字或空格/符号且很短，和前后合并
                if chunk and len(w["word"]) <= 2 and (w["word"].isdigit() or w["word"] in [",", "-", "."]):
                    chunk.append(w); i += 1
                elif len(chunk) >= 4 and len(w["word"]) > 1:
                    break  # 已经4个词了，下一行
                else:
                    if len(chunk) >= 4:
                        break
                    chunk.append(w); i += 1
            text = " ".join([w["word"] for w in chunk])
            # 清理多余空格（合并数字时可能留下空格）
            import re
            text = re.sub(r'(\d)\s+(\d)', r'\1\2', text)  # "2 000" → "2000"
            text = re.sub(r'\s+,', ',', text)  # "2 ,000" → "2,000"
            start = chunk[0]["start"]
            end = chunk[-1]["end"]
            result.append({"start": round(start, 2), "end": round(end, 2), "text": text})
        
        return result
    except Exception as e:
        logger.error(f"Whisper alignment failed: {e}")
        return _fallback_segments(text)


def get_word_timeline(audio_path: str, text: str, model_size: str = "base") -> list:
    """
    返回原始词级时间轴（不分组），供M4逐词clip渲染使用。
    返回: [{"word": str, "start": float, "end": float}, ...]
    """
    if not audio_path or not Path(audio_path).exists():
        return _fallback_words(text)

    try:
        from faster_whisper import WhisperModel
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        segments, _ = model.transcribe(audio_path, language="en", word_timestamps=True)

        words = []
        for seg in segments:
            if hasattr(seg, 'words') and seg.words:
                for w in seg.words:
                    word = w.word.strip()
                    if word:
                        words.append({"word": word, "start": round(w.start, 2), "end": round(w.end, 2)})
        if words:
            return words
        return _fallback_words(text)
    except Exception as e:
        logger.error(f"Word timeline failed: {e}")
        return _fallback_words(text)


def _fallback_words(text: str, avg_speed: float = 3.0) -> list:
    """降级：按单词数和总时长均匀分配词级时间戳"""
    raw_words = text.split()
    if not raw_words:
        return []
    total_dur = max(3, len(raw_words) / (avg_speed * 1.5))
    word_dur = total_dur / len(raw_words)
    words = []
    t = 0.0
    for w in raw_words:
        words.append({"word": w, "start": round(t, 2), "end": round(t + word_dur, 2)})
        t += word_dur
    return words


def _fallback_segments(text: str, avg_speed: float = 3.0) -> list:
    """降级：按单词数估算时间轴"""
    words = text.split()
    total_dur = len(words) / (avg_speed * 1.5)  # 约4.5词/秒
    if total_dur < 3:
        total_dur = 3

    # 均匀分割
    chunk_size = max(1, len(words) // 8)
    chunks = [words[i:i+chunk_size] for i in range(0, len(words), chunk_size)]

    result = []
    chunk_dur = total_dur / len(chunks) if chunks else total_dur
    current = 0.0

    for chunk in chunks:
        result.append({
            "start": round(current, 2),
            "end": round(current + chunk_dur, 2),
            "text": " ".join(chunk),
        })
        current += chunk_dur

    return result


def format_srt(segments: list) -> str:
    """字幕段 → SRT格式"""
    lines = []
    for i, seg in enumerate(segments, 1):
        start = _srt_time(seg["start"])
        end = _srt_time(seg["end"])
        lines.append(str(i))
        lines.append(f"{start} --> {end}")
        lines.append(seg["text"])
        lines.append("")
    return "\n".join(lines)


def _srt_time(seconds: float) -> str:
    """秒 → SRT时间格式 HH:MM:SS,mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_text = "Welcome to Chengdu. This is Wenshu Monastery, built in the Tang Dynasty."
    segs = _fallback_segments(test_text)
    print(format_srt(segs))
