#!/usr/bin/env python3
"""
FunASR 语音转录脚本（内存优化版 v2）

核心优化：
- 单进程分段：模型只加载一次，逐段转录，避免重复加载
- SenseVoiceSmall 默认模型：~500MB，支持中英日韩粤多语言
- VAD + 标点恢复：自动断句 + 加标点
- 段间 gc：及时释放临时张量内存
- 任务锁：防止同一音频被并行处理

用法：
  python3 transcribe.py audio.wav                    # 默认 small 模式
  python3 transcribe.py audio.wav --mode large       # 大模型
  python3 transcribe.py audio.wav --format json      # JSON 输出
  python3 transcribe.py audio.wav --segment 600      # 自定义分段时长（秒）
"""

import sys
import os
import json
import argparse
import gc
import subprocess
import tempfile
import fcntl
from pathlib import Path
from datetime import datetime

try:
    from funasr import AutoModel
except ImportError:
    print("❌ 未安装 FunASR，请运行: pip install funasr onnxruntime", file=sys.stderr)
    sys.exit(1)

try:
    import psutil
except ImportError:
    psutil = None

# ==================== 配置 ====================
LOCK_DIR = Path("/tmp/funasr_locks")
LOCK_DIR.mkdir(exist_ok=True)

MODEL_CONFIG = {
    "small": {
        "model": "iic/SenseVoiceSmall",
        "vad_model": "iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
        "punc_model": "iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
        "memory_mb": 500,
        "description": "SenseVoiceSmall (~500MB, 中英日韩粤)",
    },
    "large": {
        "model": "iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
        "vad_model": "iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
        "punc_model": "iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
        "memory_mb": 2000,
        "description": "Paraformer-Large (~2GB, 中文极高精度)",
    }
}

# ==================== 工具函数 ====================
def get_available_memory_mb():
    """获取可用内存 MB"""
    if psutil:
        return psutil.virtual_memory().available / 1024 / 1024
    try:
        with open('/proc/meminfo') as f:
            for line in f:
                if line.startswith('MemAvailable:'):
                    return int(line.split()[1]) / 1024
    except:
        pass
    return 500

def get_duration(audio_path):
    """获取音频时长"""
    try:
        r = subprocess.run(
            ['ffprobe', '-i', audio_path, '-show_entries', 'format=duration',
             '-v', 'quiet', '-of', 'csv=p=0'],
            capture_output=True, text=True, timeout=10
        )
        return float(r.stdout.strip())
    except:
        return 1800.0

def acquire_lock(audio_path):
    """获取任务锁，防止同一音频被并行处理"""
    audio_name = Path(audio_path).stem
    lock_file = LOCK_DIR / f"{audio_name}.lock"

    if lock_file.exists():
        try:
            with open(lock_file, 'r') as f:
                pid = int(f.read().strip())
            if psutil and not psutil.pid_exists(pid):
                os.unlink(lock_file)
        except (ValueError, OSError):
            pass

    try:
        fd = os.open(lock_file, os.O_CREAT | os.O_WRONLY)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        os.write(fd, str(os.getpid()).encode())
        return fd, True
    except IOError:
        return None, False

def release_lock(lock_fd):
    """释放任务锁"""
    if lock_fd:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            os.close(lock_fd)
        except:
            pass

# ==================== 转录核心 ====================
def split_and_transcribe(audio_path, mode="small", segment_seconds=600, output_format="text"):
    """单进程分段转录：模型加载一次，逐段处理"""

    config = MODEL_CONFIG[mode]
    available_mem = get_available_memory_mb()

    print(f"🔧 模式: {mode} ({config['description']})", file=sys.stderr)
    print(f"💾 可用内存: {available_mem:.0f} MB", file=sys.stderr)

    if available_mem < config["memory_mb"]:
        print(f"❌ 内存不足: 需要 {config['memory_mb']}MB，可用 {available_mem:.0f}MB", file=sys.stderr)
        sys.exit(1)

    # 加载模型（只一次）
    print("📦 加载模型...", file=sys.stderr)
    start_time = datetime.now()

    model = AutoModel(
        model=config["model"],
        vad_model=config["vad_model"],
        punc_model=config["punc_model"],
        disable_update=True,
    )

    load_time = (datetime.now() - start_time).total_seconds()
    print(f"✅ 模型加载完成 ({load_time:.1f}s)", file=sys.stderr)

    # 获取音频时长并计算分段
    total_duration = get_duration(audio_path)
    num_segments = max(1, int(total_duration / segment_seconds) + 
                       (1 if total_duration % segment_seconds > 30 else 0))

    print(f"⏱️ 音频时长: {total_duration:.0f}s ({total_duration/60:.1f}min)", file=sys.stderr)
    print(f"📊 分段: {num_segments} 段，每段 {segment_seconds}s", file=sys.stderr)

    # 逐段转录
    results = []
    tmpdir = tempfile.mkdtemp(prefix='funasr_seg_')

    for i in range(num_segments):
        start = i * segment_seconds
        end = min((i + 1) * segment_seconds, total_duration)

        if end - start < 30:
            continue

        seg_path = os.path.join(tmpdir, f'seg_{i:03d}.wav')

        # ffmpeg 提取片段（16kHz mono PCM）
        subprocess.run([
            'ffmpeg', '-y', '-i', audio_path,
            '-ss', str(start), '-to', str(end),
            '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
            seg_path
        ], capture_output=True, timeout=120)

        # 转录
        seg_start = datetime.now()
        result = model.generate(input=seg_path, batch_size_s=300)
        text = result[0]['text'] if result and result[0] else ''
        results.append(text)

        seg_time = (datetime.now() - seg_start).total_seconds()
        print(f"✅ [{i+1}/{num_segments}] {seg_time:.0f}s, {len(text)} 字", file=sys.stderr)

        # 清理 + gc
        try: os.unlink(seg_path)
        except: pass
        gc.collect()

    # 清理临时目录
    try: os.rmdir(tmpdir)
    except: pass

    # 输出结果
    full_text = '\n\n'.join(results)
    
    # 清理 SenseVoice 特殊标记
    clean_text = full_text.replace('<|en|>', '').replace('<|zh|>', '') \
                          .replace('<|NEUTRAL|>', '').replace('<|emo_unknown|>', '') \
                          .replace('<|bgm|>', '').replace('<|woitn|>', '') \
                          .replace('<|SPOKEN|>', '').replace('<|nospeech|>', '')

    total_time = (datetime.now() - start_time).total_seconds()

    if output_format == "json":
        output = {
            "text": clean_text.strip(),
            "chars": len(clean_text.strip()),
            "segments": num_segments,
            "duration_seconds": total_duration,
            "elapsed_seconds": total_time,
            "mode": mode,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*60}")
        print("转录结果：")
        print(f"{'='*60}")
        print(clean_text.strip())
        print(f"{'='*60}")
        print(f"📝 {len(clean_text.strip())} 字 | ⏱️ {total_time:.0f}s | 🔧 {mode}", file=sys.stderr)

    return clean_text.strip()

# ==================== 主函数 ====================
def main():
    parser = argparse.ArgumentParser(description="FunASR 语音转录（内存优化版 v2）")
    parser.add_argument("audio", nargs="?", help="音频文件路径")
    parser.add_argument("--mode", "-m", default="small", choices=["small", "large"],
                       help="模型模式: small(500MB) / large(2GB)")
    parser.add_argument("--format", "-f", default="text", choices=["text", "json"],
                       help="输出格式")
    parser.add_argument("--segment", "-s", type=int, default=600,
                       help="分段时长（秒），默认 600=10分钟")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    parser.add_argument("--no-wait", action="store_true",
                       help="不等待其他任务完成，立即退出")

    args = parser.parse_args()

    if args.verbose:
        print(f"🔧 FunASR 转录 v2.0 (内存优化版)")
        print(f"   可用内存: {get_available_memory_mb():.0f} MB")

    if not args.audio:
        parser.print_help()
        return

    # 任务锁
    lock_fd, acquired = acquire_lock(args.audio)
    if not acquired:
        print(f"⏳ 该音频正在被其他任务处理: {args.audio}", file=sys.stderr)
        if args.no_wait:
            sys.exit(1)

    try:
        result = split_and_transcribe(
            args.audio,
            mode=args.mode,
            segment_seconds=args.segment,
            output_format=args.format,
        )
        sys.exit(0 if result else 1)
    finally:
        release_lock(lock_fd)

if __name__ == "__main__":
    main()
