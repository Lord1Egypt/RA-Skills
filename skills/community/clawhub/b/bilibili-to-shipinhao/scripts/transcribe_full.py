"""第①步: tiny 模型快速转写全片(只为选段), 输出 JSON 转写 + 30 秒分块预览供 LLM 通读"""
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_DISABLE_XET"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

import json, sys, time
from faster_whisper import WhisperModel

WAV = sys.argv[1] if len(sys.argv) > 1 else "download/src.wav"
OUT_JSON = sys.argv[2] if len(sys.argv) > 2 else "download/src_transcript.json"
OUT_PREVIEW = sys.argv[3] if len(sys.argv) > 3 else "download/preview_30s.txt"
BLOCK = 30  # 秒


def fmt(t):
    m, s = divmod(int(t), 60)
    return f"{m:02d}:{s:02d}"


def main():
    t0 = time.time()
    print("loading tiny model...", flush=True)
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    print("model ready", flush=True)
    segs, info = model.transcribe(WAV, language="zh", beam_size=5, vad_filter=True)
    dur = getattr(info, "duration", 0)
    print(f"audio duration {dur:.1f}s", flush=True)

    js, blocks = [], {}
    for sg in segs:
        txt = sg.text.strip()
        if not txt:
            continue
        js.append({"start": round(sg.start, 2), "end": round(sg.end, 2), "text": txt})
        b = int(sg.start // BLOCK)
        blocks.setdefault(b, []).append(txt)

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(js, f, ensure_ascii=False, indent=2)

    lines = []
    for b in sorted(blocks):
        lines.append(f"[{fmt(b * BLOCK)}-{fmt((b + 1) * BLOCK)}] {' '.join(blocks[b])}")
    with open(OUT_PREVIEW, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"segments={len(js)} blocks={len(blocks)}")
    print(f"-> {OUT_JSON}\n-> {OUT_PREVIEW}")
    print(f"elapsed {time.time() - t0:.0f}s (audio {dur:.0f}s, speed {dur / max(time.time() - t0, 1):.2f}x)")


if __name__ == "__main__":
    main()
