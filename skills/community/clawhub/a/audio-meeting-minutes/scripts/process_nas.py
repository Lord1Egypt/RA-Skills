# -*- coding: utf-8 -*-
"""熠小听 · 语音转文字（阿里云NLS云端识别）
输出 transcript.txt 后由 WorkBuddy AI 完成总结 + HTML 生成
"""
import sys, os, io, shutil, subprocess, json, time, requests, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') if hasattr(sys.stdout, 'buffer') else sys.stdout
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8') if hasattr(sys.stderr, 'buffer') else sys.stderr

HERE = os.path.dirname(os.path.abspath(__file__))

# ── 用户配置 ──────────────────────────────────────────────────
NAS_DIR  = os.environ.get("LYD_NAS_DIR",  r"\\192.168.1.219\品牌视觉部-新\图片\2024.8-2025.7箱包\1-产品作图\自动化裁剪\录音文件智能总结")

NLS_TOKEN  = os.environ.get("NLS_TOKEN",  "你的AccessToken")
NLS_APPKEY = os.environ.get("NLS_APPKEY", "你的AppKey")
NLS_URL    = "https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/asr"
CHUNK_BYTES = 1_800_000

LOCAL_TMP = os.path.join(HERE, "nas_tmp")
TMPDIR    = os.path.join(LOCAL_TMP, ".chunks")
os.makedirs(LOCAL_TMP, exist_ok=True)
os.makedirs(TMPDIR, exist_ok=True)

from pathlib import Path

def fmt_time(s):
    h, r = divmod(int(s), 3600)
    m, sec = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{sec:02d}"

def nls_transcribe_chunk(wav_path, chunk_index):
    with open(wav_path, "rb") as f:
        data = f.read()
    headers = {"X-NLS-Token": NLS_TOKEN, "Content-Type": "application/octet-stream"}
    params = {
        "appkey": NLS_APPKEY, "format": "pcm", "sample_rate": 16000,
        "enable_punctuation_prediction": "true",
        "enable_inverse_text_normalization": "true",
        "enable_voice_detection": "false",
    }
    resp = requests.post(NLS_URL, headers=headers, params=params, data=data, timeout=120)
    resp.raise_for_status()
    body = resp.json()
    if body.get("status") == 20000000:
        return body.get("result", "")
    else:
        print(f"  [WARN] chunk_{chunk_index} NLS status={body.get('status')} msg={body.get('message','')}")
        return ""

# ===== 主流程 =====
print("=" * 60)
print("熠小听 · 阿里云NLS云端识别")
print(f"NAS目录: {NAS_DIR}")
print("=" * 60)

import glob as _g
audio_files = []
for ext in ["m4a","M4A","mp3","MP3","wav","WAV","ogg","OGG","flac","FLAC","aac","AAC"]:
    audio_files += _g.glob(os.path.join(NAS_DIR, f"*.{ext}"))
audio_files = [f for f in audio_files if "会议纪要输出" not in f]
seen = {}
for f in audio_files:
    fn = os.path.basename(f)
    if fn not in seen: seen[fn] = f
audio_files = list(seen.values())

print(f"\n发现 {len(audio_files)} 个音频文件:")
for af in audio_files:
    print(f"  {Path(af).name}")

if not audio_files:
    print("没有音频文件，退出。")
    sys.exit(0)

results = []

for AUDIO in audio_files:
    name = Path(AUDIO).stem
    print(f"\n{'='*60}")
    print(f"处理: {Path(AUDIO).name}")
    print(f"{'='*60}")

    dur = float(subprocess.check_output(
        ["ffprobe","-i",AUDIO,"-show_entries","format=duration","-v","quiet","-of","csv=p=0"],
        stderr=subprocess.DEVNULL
    ).decode().strip())
    print(f"时长: {dur:.0f}s ({dur/60:.1f} 分钟)")

    print(f"\n[1/2] 音频转换 + 切块（每块≤1.8MB）...")
    t0 = time.time()
    pcm_path = os.path.join(TMPDIR, f"{name}_full.pcm")
    subprocess.run([
        "ffmpeg", "-y", "-i", AUDIO,
        "-ac","1","-ar","16000","-f","s16le", pcm_path
    ], capture_output=True)

    pcm_size = os.path.getsize(pcm_path)
    num_chunks = math.ceil(pcm_size / CHUNK_BYTES)
    bytes_per_sec = 16000 * 2
    chunk_sec = CHUNK_BYTES / bytes_per_sec
    print(f"  PCM大小: {pcm_size/1024/1024:.1f}MB → {num_chunks}块，每块约{chunk_sec:.0f}秒")

    chunks = []
    with open(pcm_path, "rb") as f:
        idx = 0
        while True:
            buf = f.read(CHUNK_BYTES)
            if not buf: break
            cp = os.path.join(TMPDIR, f"c{idx}.pcm")
            with open(cp, "wb") as out: out.write(buf)
            start_sec = idx * chunk_sec
            chunks.append((cp, start_sec, len(buf)))
            idx += 1
    print(f"  已生成 {len(chunks)} 块")

    print(f"\n[2/2] 阿里云NLS云端识别（{len(chunks)}块串行）...")
    all_texts, all_segs = [], []
    for i, (cp, start_sec, chunk_len) in enumerate(chunks):
        print(f"  [{i+1}/{len(chunks)}] {fmt_time(start_sec)} ...", end=" ", flush=True)
        t_c = time.time()
        try:
            result_text = nls_transcribe_chunk(cp, i)
            cost = time.time() - t_c
            print(f"{len(result_text)}字 ({cost:.1f}s)")
            all_texts.append(result_text)
            if result_text.strip():
                all_segs.append({
                    "start": start_sec, "end": start_sec + chunk_len / bytes_per_sec,
                    "text": result_text.strip(),
                    "start_fmt": fmt_time(start_sec),
                    "end_fmt": fmt_time(start_sec + chunk_len / bytes_per_sec),
                })
        except Exception as e:
            print(f"失败: {e}")
            all_texts.append("")
        time.sleep(0.3)

    full_text = "".join(all_texts)
    print(f"\n  转写完成: {len(full_text)} 字，耗时 {time.time()-t0:.1f}s")

    # 保存转写结果
    transcript_path = os.path.join(LOCAL_TMP, f"{name}_transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"  已保存: {transcript_path}")

    results.append({
        "filename": Path(AUDIO).name,
        "stem": name,
        "duration_seconds": dur,
        "duration_fmt": fmt_time(dur),
        "text_length": len(full_text),
        "transcript_path": transcript_path,
    })

    shutil.rmtree(TMPDIR, ignore_errors=True)
    os.makedirs(TMPDIR, exist_ok=True)

# 输出 JSON 给 WorkBuddy Agent 读取
print("\n" + "=" * 60)
print("TRANSCRIPT_RESULTS_JSON:")
print(json.dumps(results, ensure_ascii=False, indent=2))
