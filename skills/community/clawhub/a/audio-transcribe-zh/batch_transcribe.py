import os, subprocess, time, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"E:\BaiduNetdiskDownload\浙房理\post"
FFMPEG = r"C:\Users\PC\.openclaw\workspace\ffmpeg-bin\ffmpeg.exe"
WORKSPACE = r"C:\Users\PC\.openclaw\workspace"

def extract_audio(mp4_path, wav_path):
    """用 ffmpeg 提取音频为 WAV 16kHz mono"""
    subprocess.run(
        [FFMPEG, "-i", mp4_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", wav_path, "-y"],
        capture_output=True, timeout=120
    )

# 收集所有需要处理的视频
videos = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    mp4s = [f for f in filenames if f.lower().endswith('.mp4')]
    for mp4 in mp4s:
        base = os.path.splitext(mp4)[0]
        txt_path = os.path.join(dirpath, base + '.txt')
        if not os.path.exists(txt_path):
            videos.append((dirpath, mp4, base))

print(f"需处理视频: {len(videos)} 个")
if not videos:
    print("全部已完成！")
    exit(0)

# 加载 FunASR 模型（只加载一次）
from funasr import AutoModel
print("加载 FunASR Paraformer 模型...")
t0 = time.time()
model = AutoModel(
    model='iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
    device='cuda:0',
    disable_update=True,
)
print(f"模型加载完成: {time.time()-t0:.1f}s")

total = len(videos)
for i, (dirpath, mp4, base) in enumerate(videos):
    mp4_path = os.path.join(dirpath, mp4)
    wav_path = os.path.join(WORKSPACE, f'_batch_temp_{i}.wav')
    txt_path = os.path.join(dirpath, base + '.txt')
    
    try:
        # 提取音频
        t1 = time.time()
        extract_audio(mp4_path, wav_path)
        extract_time = time.time() - t1
        
        # 转录
        t2 = time.time()
        result = model.generate(input=wav_path)
        trans_time = time.time() - t2
        
        text = result[0]['text']
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # 清理临时wav
        try: os.remove(wav_path)
        except: pass
        
        print(f"[{i+1}/{total}] ✅ {base[:30]}... | 提取:{extract_time:.1f}s 转录:{trans_time:.1f}s")
        
    except Exception as e:
        print(f"[{i+1}/{total}] ❌ {mp4}: {e}")
        try: os.remove(wav_path)
        except: pass

print(f"\n全部完成！总共转录 {total} 个视频")
