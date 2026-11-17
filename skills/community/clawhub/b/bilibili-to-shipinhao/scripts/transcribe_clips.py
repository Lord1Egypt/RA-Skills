"""只精转选中的 5 段(而非全片), small 模型 + 简体引导, 输出每段独立 SRT

内存紧张时(本机 16GB, WorkBuddy+Chrome+VSCode 常占 85%+)small 模型可能抛
`RuntimeError: mkl_malloc: failed to allocate memory`。因此:
  1) **HF_HUB_OFFLINE=1 强制离线只读本地缓存** —— 这是最关键的修复。本机有系统代理
     (http://127.0.0.1:12902), 不设离线时 huggingface_hub 会走代理去校验/拉模型,
     表现为 `ProxyError: 502 Bad Gateway` 或加载到一半的 mkl_malloc 分配失败;
     离线后 small 加载 5s、97s 音频转写 44s, 稳定可复现。
  2) 用满 4 线程(cpu_threads=4); 若仍失败再降 beam_size / 换 tiny;
  3) 逐级降级 small -> tiny, 任一能跑通即可。
"""
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_OFFLINE"] = "1"          # 只读本地缓存, 绕开系统代理
os.environ["HF_HUB_DISABLE_XET"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

import json, subprocess
from faster_whisper import WhisperModel

FFMPEG = "bin/ffmpeg.exe"
SRC_WAV = "download/src.wav"
OUT = "output"

CLIPS = [
    (1, 1080.4, 1177.4, "01数据会撒谎"),
]

# 引导 whisper 输出简体中文(否则易出繁体)
PROMPT = "以下是普通话的句子，请使用简体中文输出。"
# 内存友好度阶梯: 优先 small+beam1(实测 97s 音频 44s 跑完, 质量已足够), 越往下越省内存
ATTEMPTS = [("small", 1), ("small", 5), ("tiny", 5)]


def fmt(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def run_one(model, wav, beam):
    """转写单段; 生成器在这里才真正执行, 内存错误会在遍历时抛出"""
    segs, _ = model.transcribe(wav, language="zh", beam_size=beam,
                               vad_filter=True, initial_prompt=PROMPT,
                               condition_on_previous_text=False)
    out = []
    for sg in segs:
        txt = sg.text.strip()
        if txt:
            out.append({"start": round(sg.start, 2), "end": round(sg.end, 2), "text": txt})
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    for clip in CLIPS:
        idx, start, end, title = clip
        wav = f"download/clip{idx}.wav"
        dur = end - start
        if not os.path.exists(wav):
            subprocess.run([FFMPEG, "-y", "-ss", str(start), "-t", str(dur),
                            "-i", SRC_WAV, "-ac", "1", "-ar", "16000",
                            "-c:a", "pcm_s16le", wav], capture_output=True)
        print(f"[{idx}] {title} {start}-{end}s ({dur}s) -> {wav}", flush=True)
        done = False
        for name, beam in ATTEMPTS:
            try:
                print(f"  try {name} beam={beam} ...", flush=True)
                model = WhisperModel(name, device="cpu", compute_type="int8",
                                     cpu_threads=4, num_workers=1)
                js = run_one(model, wav, beam)
                del model
                if not js:
                    raise RuntimeError("empty transcript")
                lines, i = [], 1
                for sg in js:
                    lines += [str(i), f"{fmt(sg['start'])} --> {fmt(sg['end'])}", sg["text"], ""]
                    i += 1
                with open(f"{OUT}/clip{idx}.srt", "w", encoding="utf-8") as f:
                    f.write("\n".join(lines))
                with open(f"{OUT}/clip{idx}.json", "w", encoding="utf-8") as f:
                    json.dump(js, f, ensure_ascii=False, indent=2)
                print(f"  OK -> {OUT}/clip{idx}.srt ({len(js)} segs, "
                      f"model={name}, beam={beam})", flush=True)
                done = True
                break
            except Exception as ex:
                print(f"  !! {name} beam={beam} failed: "
                      f"{type(ex).__name__}: {str(ex)[:160]}", flush=True)
        if not done:
            print(f"[{idx}] ALL ATTEMPTS FAILED — 需先释放内存(关掉 Chrome/VSCode)再跑", flush=True)
    print("DONE")


if __name__ == "__main__":
    main()
