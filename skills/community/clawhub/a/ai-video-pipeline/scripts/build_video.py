"""
AI视频合成管线 v16 (入口)
文稿 → 播客API TTS → 即梦AI视频片段(100%) → BGM混音 → MP4

用法:
  python3 build_video.py script.txt -o output.mp4          # 自动铺满（每段一个动画）
  python3 build_video.py script.txt -o output.mp4 --no-clips  # 仅TTS+BGM+字幕
  python3 build_video.py script.txt --tts-only              # 仅生成音频
"""
import os, argparse
from tts import generate_tts
from bgm import pick_bgm, pick_or_generate_bgm, mix_audio_with_bgm
from compose import compose
from clips import generate_video_clips


def _auto_clip_configs(subs, script_text):
    """自动为每个段落生成一个即梦AI片段配置，铺满整个时长"""
    paragraphs = [p.strip() for p in script_text.split("\n\n") if p.strip()]
    configs = []
    for i, para in enumerate(paragraphs):
        if i >= len(subs):
            break
        configs.append({
            "prompt": para[:200],
            "mode": "t2v_720p",
        })
    return configs


def build(script_text, output_path="output.mp4", work_dir="/tmp/video-poc",
          voice="zh_male_dayixiansheng_v2_saturn_bigtts",
          video_clip_configs="auto",
          bgm_path=None, bgm_volume=0.35, bgm_style=None,
          tts_only=False,
          font_path=None, font_size=44, y_ratio=0.92, max_chars=20,
          verbose=True):
    """一键生成视频 (v14)

    Args:
        script_text: 文稿文本
        output_path: 输出视频路径
        work_dir: 工作目录
        voice: 播客发音人
        video_clip_configs: "auto"(默认，每个段落一个片段铺满) 或
            [{"prompt": "...", "mode": "t2v_720p"}, ...] 或
            None/[] (跳过视频片段)
        bgm_path: BGM 文件路径 (None=自动选择，支持 MiniMax 生成)
        bgm_volume: BGM 音量 (0.0~1.0, 默认 0.35 即 35%)
        bgm_style: BGM 风格 (lofi/calm/dark/uplifting/piano/corporate)，优先本地匹配，无匹配则 MiniMax 生成
        tts_only: 仅生成音频
    """
    os.makedirs(work_dir, exist_ok=True)
    audio_path = os.path.join(work_dir, "voice.mp3")

    if verbose:
        print("=" * 50)
        print("🎬 AI视频合成 v14")
        print(f"   TTS: 火山播客API ({voice.split('_')[-1]})")
        print("=" * 50)

    # Step 1: TTS
    if verbose: print("\nStep 1: 语音合成")
    tts_subs = generate_tts(script_text, audio_path, voice, work_dir, verbose,
                         skip_if_exists=True)

    # Step 1.5: FunASR 字幕时间轴对齐（失败时 fallback 到 TTS 原始 subs）
    subs = tts_subs
    try:
        from asr import align_subtitles
        if verbose: print("\nStep 1.5: FunASR 字幕对齐...")
        asr_subs = align_subtitles(audio_path, script_text, work_dir, verbose)
        if asr_subs and len(asr_subs) > 0:
            subs = asr_subs
        else:
            if verbose: print("  ⚠️ ASR 对齐无结果，使用 TTS 原始字幕")
    except Exception as e:
        if verbose:
            print(f"\nStep 1.5: ⚠️ FunASR 对齐失败，使用 TTS 原始字幕: {e}")

    if tts_only:
        return audio_path, subs

    # Step 2: BGM 混音 (ffmpeg，在视频合成之前完成)
    if bgm_path is None and bgm_style:
        bgm_path = pick_or_generate_bgm(style=bgm_style, verbose=verbose)
    elif bgm_path is None:
        bgm_path = pick_bgm(verbose=verbose)
    mixed_audio = None
    if bgm_path:
        mixed_audio = os.path.join(work_dir, "voice_bgm.mp3")
        mix_audio_with_bgm(audio_path, mixed_audio, bgm_path, bgm_volume, verbose=verbose)

    # Step 3: 即梦AI视频片段
    video_clips = []
    # 自动铺满：每个段落一个片段
    if video_clip_configs == "auto":
        video_clip_configs = _auto_clip_configs(subs, script_text)

    if video_clip_configs:
        if verbose:
            print(f"\nStep 3: 即梦AI视频片段生成 ({len(video_clip_configs)}个片段, 铺满模式)")
        video_clips = generate_video_clips(work_dir, video_clip_configs, subs, verbose)

    # Step 4: 视频合成 (用混合后的音频)
    step = 4 if video_clips else (3 if mixed_audio else 2)
    if verbose: print(f"\nStep {step}: 视频合成 (预提取帧+frame_map)")
    compose(work_dir, audio_path, subs, output_path,
            font_path=font_path, font_size=font_size, y_ratio=y_ratio,
            max_chars=max_chars, video_clips=video_clips,
            mixed_audio_path=mixed_audio, verbose=verbose)

    if verbose: print(f"\n🎉 完成!")
    return output_path, subs


def main():
    parser = argparse.ArgumentParser(description="AI视频合成 v16: 文稿 → MP4 (自动铺满)")
    parser.add_argument("script", help="文稿文件路径 (段落用空行分隔)")
    parser.add_argument("-o", "--output", default="output.mp4", help="输出视频路径")
    parser.add_argument("--work-dir", default="/tmp/video-poc", help="工作目录")
    parser.add_argument("--voice", default="zh_male_dayixiansheng_v2_saturn_bigtts")
    parser.add_argument("--tts-only", action="store_true")
    parser.add_argument("--no-clips", action="store_true",
                        help="跳过即梦AI视频片段，仅TTS+BGM+字幕")
    parser.add_argument("--bgm", default=None, help="BGM 文件路径 (默认自动选择)")
    parser.add_argument("--bgm-volume", type=float, default=0.35)
    parser.add_argument("--bgm-style", default=None,
                        help="BGM 风格 (lofi/calm/dark/uplifting/piano/corporate)，优先本地，无匹配则 MiniMax 生成")
    parser.add_argument("--font-size", type=int, default=44)
    parser.add_argument("--max-chars", type=int, default=20)
    parser.add_argument("--y-ratio", type=float, default=0.92,
                        help="字幕垂直位置 (0.0=顶部, 1.0=底部, 默认0.92)")
    args = parser.parse_args()

    with open(args.script, 'r', encoding='utf-8') as f:
        script_text = f.read().strip()

    clip_configs = [] if args.no_clips else "auto"

    build(script_text, args.output, args.work_dir, args.voice,
          video_clip_configs=clip_configs,
          bgm_path=args.bgm, bgm_volume=args.bgm_volume,
          bgm_style=args.bgm_style,
          tts_only=args.tts_only,
          font_size=args.font_size, max_chars=args.max_chars,
          y_ratio=args.y_ratio)


if __name__ == "__main__":
    main()
