"""Speech-to-text with word timestamps.

Apple Silicon: mlx-whisper (whisper-large-v3-turbo). Elsewhere: faster-whisper (large-v3-turbo, CPU int8).
The first run downloads the model (~1.6 GB) from Hugging Face into the local cache.
Returns a list of segments: {start, end, text, words: [{start, end, word}]}.
"""
import numpy as np


def transcribe(audio_16k_f32, words=True):
    try:
        import mlx_whisper
        r = mlx_whisper.transcribe(audio_16k_f32, path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
                                   word_timestamps=words, condition_on_previous_text=False)
        return r["segments"]
    except ImportError:
        from faster_whisper import WhisperModel
        m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
        segs, _ = m.transcribe(np.asarray(audio_16k_f32, np.float32), word_timestamps=words, condition_on_previous_text=False)
        out = []
        for s in segs:
            out.append({"start": s.start, "end": s.end, "text": s.text,
                        "words": [{"start": w.start, "end": w.end, "word": w.word} for w in (s.words or [])]})
        return out
