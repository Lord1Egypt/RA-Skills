#!/usr/bin/env python3
"""
Fish Speech TTS 技能 — 完整命令行接口
支持声音克隆、情绪分析、多段合成、音色库管理
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 添加 src 目录到路径
SCRIPT_DIR = Path(__file__).parent
SRC_DIR = SCRIPT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from text_analyzer import TextAnalyzer, analyze_line
from synthesizer import MultiSegmentSynthesizer, SimpleSynthesizer
from voice_library import VoiceLibrary


def cmd_tts(args):
    """简单 TTS（向后兼容）"""
    try:
        synth = SimpleSynthesizer(
            api_base=args.api_base,
            default_format=args.format
        )
        
        success = synth.synthesize(
            text=args.text,
            output_path=args.output,
            ref_audio=args.ref,
            voice_id=args.voice_id,
            temperature=args.temperature,
            top_p=args.top_p,
            repetition_penalty=args.repetition_penalty,
            max_new_tokens=args.max_tokens
        )
        
        sys.exit(0 if success else 1)
    
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_smart_tts(args):
    """智能 TTS（带情绪分析）"""
    try:
        synth = MultiSegmentSynthesizer(
            api_base=args.api_base,
            output_dir=args.output_dir,
            default_format=args.format,
            ffmpeg_path=args.ffmpeg
        )
        
        # 构建上下文
        context = None
        if args.emotion:
            context = {"emotion_hint": args.emotion}
        
        results = synth.synthesize_with_analysis(
            text=args.text,
            output_path=args.output,
            ref_audio=args.ref,
            voice_id=args.voice_id,
            context=context,
            add_silence=not args.no_silence,
            silence_duration_ms=args.silence_ms
        )
        
        # 输出分析结果
        if args.verbose:
            print("\n=== 情绪分析结果 ===")
            for r in results:
                if r.success:
                    print(f"  段 {r.segment_index + 1}: {r.emotion} ({r.duration_ms:.0f}ms)")
                    print(f"    文本: {r.text}")
        
        success_count = sum(1 for r in results if r.success)
        print(f"\n合成完成: {success_count}/{len(results)} 段成功")
        
        sys.exit(0 if success_count > 0 else 1)
    
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_analyze(args):
    """分析台词情绪"""
    analyzer = TextAnalyzer()
    
    if args.text:
        result = analyzer.analyze(args.text)
        print(f"文本: {args.text}")
        print(f"情绪: {result.emotion.emotion} (强度: {result.emotion.intensity:.2f})")
        print(f"节奏: {result.rhythm.speed}")
        print(f"停顿: {result.rhythm.pause_after:.1f}s")
        print(f"重音: {', '.join(result.rhythm.emphasis_words) or '无'}")
        print(f"\nFish Speech 参数:")
        print(f"  temperature: {result.voice_params['temperature']:.2f}")
        print(f"  top_p: {result.voice_params['top_p']:.2f}")
        print(f"  repetition_penalty: {result.voice_params['repetition_penalty']:.2f}")
        print(f"  chunk_length: {result.voice_params['chunk_length']}")
    
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        print(f"分析文件: {args.file} ({len(lines)} 行)\n")
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            
            result = analyzer.analyze(line)
            print(f"[{i:03d}] {line[:60]}...")
            print(f"     情绪: {result.emotion.emotion} | 节奏: {result.rhythm.speed}")
            print()


def cmd_voice_add(args):
    """添加音色"""
    try:
        library = VoiceLibrary(
            library_dir=args.library_dir,
            api_base=args.api_base
        )
        
        profile = library.add_voice(
            voice_id=args.id,
            name=args.name,
            ref_audio_path=args.audio,
            description=args.description or "",
            gender=args.gender or "neutral",
            age_range=args.age or "",
            language=args.language or "zh",
            emotion_tags=args.emotion or [],
            ref_text=args.ref_text
        )
        
        # 如果指定了自动注册
        if args.register:
            library.register_to_api(args.id)
        
        print(f"\n音色档案:")
        print(f"  ID: {profile.id}")
        print(f"  名称: {profile.name}")
        print(f"  性别: {profile.gender}")
        print(f"  语言: {profile.language}")
        print(f"  情绪: {', '.join(profile.emotion_tags) or '未指定'}")
        print(f"  音频: {profile.ref_audio_path}")
        
        sys.exit(0)
    
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_voice_list(args):
    """列出音色"""
    try:
        library = VoiceLibrary(
            library_dir=args.library_dir,
            api_base=args.api_base
        )
        
        voices = library.list_voices(
            gender=args.gender,
            language=args.language,
            emotion=args.emotion,
            registered_only=args.registered
        )
        
        if not voices:
            print("暂无音色")
            sys.exit(0)
        
        print(f"共 {len(voices)} 个音色:\n")
        
        for v in voices:
            status = "✅ 已注册" if v.registered else "⚪ 未注册"
            print(f"[{v.id}] {v.name} {status}")
            print(f"  {v.description}")
            print(f"  性别: {v.gender} | 语言: {v.language} | 情绪: {', '.join(v.emotion_tags) or '无'}")
            print(f"  音频: {v.ref_audio_path}")
            print()
        
        sys.exit(0)
    
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_voice_register(args):
    """注册音色到 API"""
    try:
        library = VoiceLibrary(
            library_dir=args.library_dir,
            api_base=args.api_base
        )
        
        if args.all:
            # 注册所有未注册的音色
            unregistered = library.sync_with_api()
            success_count = 0
            for profile in unregistered:
                if library.register_to_api(profile.id):
                    success_count += 1
            print(f"\n注册完成: {success_count}/{len(unregistered)} 成功")
        else:
            # 注册指定音色
            success = library.register_to_api(args.id)
            sys.exit(0 if success else 1)
        
        sys.exit(0)
    
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_voice_remove(args):
    """移除音色"""
    try:
        library = VoiceLibrary(
            library_dir=args.library_dir,
            api_base=args.api_base
        )
        
        library.remove_voice(args.id, delete_audio=args.delete_audio)
        sys.exit(0)
    
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_voice_sync(args):
    """同步本地库与 API"""
    try:
        library = VoiceLibrary(
            library_dir=args.library_dir,
            api_base=args.api_base
        )
        
        unregistered = library.sync_with_api()
        
        if unregistered:
            print(f"\n是否注册这些音色到 API? (y/n)", end=" ")
            choice = input().strip().lower()
            if choice == "y":
                success_count = 0
                for profile in unregistered:
                    if library.register_to_api(profile.id):
                        success_count += 1
                print(f"\n注册完成: {success_count}/{len(unregistered)} 成功")
        else:
            print("✅ 所有音色已同步")
        
        sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n已取消")
        sys.exit(130)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_batch(args):
    """批量配音"""
    try:
        # 读取脚本文件
        with open(args.script, "r", encoding="utf-8") as f:
            script_data = json.load(f)
        
        if not isinstance(script_data, list):
            print("错误: 脚本文件必须是 JSON 数组", file=sys.stderr)
            sys.exit(1)
        
        print(f"批量配音: {len(script_data)} 条台词\n")
        
        # 初始化合成器
        synth = MultiSegmentSynthesizer(
            api_base=args.api_base,
            output_dir=args.output_dir,
            default_format=args.format,
            ffmpeg_path=args.ffmpeg
        )
        
        # 逐条处理
        success_count = 0
        for i, item in enumerate(script_data, 1):
            text = item.get("text", "")
            output = item.get("output", f"line_{i:03d}.mp3")
            ref = item.get("ref")
            voice_id = item.get("voice_id")
            emotion = item.get("emotion")
            
            print(f"[{i}/{len(script_data)}] {text[:50]}...")
            
            # 构建上下文
            context = None
            if emotion:
                context = {"emotion_hint": emotion}
            
            # 合成
            results = synth.synthesize_with_analysis(
                text=text,
                output_path=os.path.join(args.output_dir, output),
                ref_audio=ref,
                voice_id=voice_id,
                context=context,
                add_silence=False
            )
            
            success = all(r.success for r in results)
            if success:
                success_count += 1
                print(f"  ✅ 完成")
            else:
                print(f"  ❌ 失败")
            
            print()
        
        print(f"\n批量配音完成: {success_count}/{len(script_data)} 成功")
        sys.exit(0 if success_count > 0 else 1)
    
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Fish Speech TTS 技能 — 声音克隆 + 情绪分析 + 多段合成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 简单配音
  python main.py tts --text "你好世界" --output hello.mp3
  
  # 声音克隆
  python main.py tts --text "你好" --ref reference.mp3 --output cloned.mp3
  
  # 智能配音（带情绪分析）
  python main.py smart-tts --text "太好了！我们成功了！" --output success.mp3
  
  # 分析台词
  python main.py analyze --text "顾栖上台缺了这件首饰，狂热粉丝能掀翻整栋场馆！"
  
  # 添加音色
  python main.py voice add --id momo --name "MOMO" --audio momo_ref.mp3
  
  # 列出音色
  python main.py voice list
  
  # 批量配音
  python main.py batch --script scene1.json --output-dir output/
        """
    )
    
    # 全局参数
    parser.add_argument("--api-base", default="http://127.0.0.1:18791", help="Fish Speech API 地址")
    parser.add_argument("--library-dir", default="voice_profiles", help="音色库目录")
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # === tts 命令 ===
    tts_parser = subparsers.add_parser("tts", help="简单 TTS（无情绪分析）")
    tts_parser.add_argument("--text", required=True, help="要朗读的文本")
    tts_parser.add_argument("--output", required=True, help="输出文件路径")
    tts_parser.add_argument("--ref", help="参考音频（声音克隆）")
    tts_parser.add_argument("--voice-id", help="已注册的音色 ID")
    tts_parser.add_argument("--format", default="mp3", choices=["mp3", "wav", "opus", "pcm"])
    tts_parser.add_argument("--temperature", type=float, default=0.7)
    tts_parser.add_argument("--top-p", type=float, default=0.8)
    tts_parser.add_argument("--repetition-penalty", type=float, default=1.1)
    tts_parser.add_argument("--max-tokens", type=int, default=2048)
    tts_parser.set_defaults(func=cmd_tts)
    
    # === smart-tts 命令 ===
    smart_tts_parser = subparsers.add_parser("smart-tts", help="智能 TTS（带情绪分析）")
    smart_tts_parser.add_argument("--text", required=True, help="要朗读的文本")
    smart_tts_parser.add_argument("--output", required=True, help="输出文件路径")
    smart_tts_parser.add_argument("--output-dir", default="output", help="临时文件目录")
    smart_tts_parser.add_argument("--ref", help="参考音频（声音克隆）")
    smart_tts_parser.add_argument("--voice-id", help="已注册的音色 ID")
    smart_tts_parser.add_argument("--emotion", help="情绪提示（覆盖自动分析）")
    smart_tts_parser.add_argument("--format", default="mp3", choices=["mp3", "wav", "opus", "pcm"])
    smart_tts_parser.add_argument("--no-silence", action="store_true", help="不在段落间插入停顿")
    smart_tts_parser.add_argument("--silence-ms", type=int, default=500, help="停顿时长（毫秒）")
    smart_tts_parser.add_argument("--ffmpeg", help="FFmpeg 路径（pydub 需要）")
    smart_tts_parser.add_argument("--verbose", "-v", action="store_true", help="显示详细分析结果")
    smart_tts_parser.set_defaults(func=cmd_smart_tts)
    
    # === analyze 命令 ===
    analyze_parser = subparsers.add_parser("analyze", help="分析台词情绪")
    analyze_group = analyze_parser.add_mutually_exclusive_group(required=True)
    analyze_group.add_argument("--text", help="要分析的文本")
    analyze_group.add_argument("--file", help="台词文件（每行一句）")
    analyze_parser.set_defaults(func=cmd_analyze)
    
    # === voice 命令 ===
    voice_parser = subparsers.add_parser("voice", help="音色库管理")
    voice_subparsers = voice_parser.add_subparsers(dest="voice_command")
    
    # voice add
    voice_add_parser = voice_subparsers.add_parser("add", help="添加音色")
    voice_add_parser.add_argument("--id", required=True, help="音色 ID（英文）")
    voice_add_parser.add_argument("--name", required=True, help="音色名称")
    voice_add_parser.add_argument("--audio", required=True, help="参考音频文件")
    voice_add_parser.add_argument("--description", help="音色描述")
    voice_add_parser.add_argument("--gender", choices=["male", "female", "neutral"])
    voice_add_parser.add_argument("--age", help="年龄段")
    voice_add_parser.add_argument("--language", default="zh", help="语言")
    voice_add_parser.add_argument("--emotion", nargs="*", help="情绪标签")
    voice_add_parser.add_argument("--ref-text", help="参考音频对应文本")
    voice_add_parser.add_argument("--register", action="store_true", help="自动注册到 API")
    
    # voice list
    voice_list_parser = voice_subparsers.add_parser("list", help="列出音色")
    voice_list_parser.add_argument("--gender", choices=["male", "female", "neutral"])
    voice_list_parser.add_argument("--language", help="语言")
    voice_list_parser.add_argument("--emotion", help="情绪标签")
    voice_list_parser.add_argument("--registered", action="store_true", help="仅显示已注册")
    
    # voice register
    voice_reg_parser = voice_subparsers.add_parser("register", help="注册音色到 API")
    voice_reg_parser.add_argument("--id", help="音色 ID")
    voice_reg_parser.add_argument("--all", action="store_true", help="注册所有未注册音色")
    
    # voice remove
    voice_rm_parser = voice_subparsers.add_parser("remove", help="移除音色")
    voice_rm_parser.add_argument("--id", required=True, help="音色 ID")
    voice_rm_parser.add_argument("--delete-audio", action="store_true", help="删除音频文件")
    
    # voice sync
    voice_sync_parser = voice_subparsers.add_parser("sync", help="同步本地库与 API")
    
    voice_parser.set_defaults(func=cmd_voice_list)
    voice_add_parser.set_defaults(func=cmd_voice_add)
    voice_list_parser.set_defaults(func=cmd_voice_list)
    voice_reg_parser.set_defaults(func=cmd_voice_register)
    voice_rm_parser.set_defaults(func=cmd_voice_remove)
    voice_sync_parser.set_defaults(func=cmd_voice_sync)
    
    # === batch 命令 ===
    batch_parser = subparsers.add_parser("batch", help="批量配音")
    batch_parser.add_argument("--script", required=True, help="脚本文件（JSON）")
    batch_parser.add_argument("--output-dir", required=True, help="输出目录")
    batch_parser.add_argument("--format", default="mp3", choices=["mp3", "wav", "opus", "pcm"])
    batch_parser.add_argument("--ffmpeg", help="FFmpeg 路径")
    batch_parser.set_defaults(func=cmd_batch)
    
    # 解析参数
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 执行命令
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
