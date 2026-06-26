#!/usr/bin/env python3
"""
图片/视频生成快速脚本

使用方法:
    python generate.py "一只可爱的橘猫"                    # 生成图片
    python generate.py "海边日落" --video                 # 生成视频
    python generate.py "日出 山落 海滩 森林" --batch       # 批量生成
"""

import sys
import os
import argparse
import json

# 添加 lib 目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(script_dir, '..', 'lib')
sys.path.insert(0, lib_dir)

from image_video import generate_image, generate_video, wait_for_video, batch_generate_images


def print_result(result, result_type="image"):
    """格式化输出结果"""
    if result_type == "image":
        url = result.get("data", [{}])[0].get("url", "")
        print(f"\n✅ 图片生成成功！")
        print(f"📸 URL: {url}")
        return url
    elif result_type == "video":
        url = result.get("video_result", [{}])[0].get("url", "")
        cover = result.get("video_result", [{}])[0].get("cover_image_url", "")
        print(f"\n✅ 视频生成成功！")
        print(f"🎬 视频 URL: {url}")
        if cover:
            print(f"🖼️  封面 URL: {cover}")
        return url


def generate_single_image(prompt, args):
    """生成单张图片"""
    result = generate_image(
        prompt=prompt,
        model=args.model,
        quality=args.quality,
        size=args.size,
    )
    return print_result(result, "image")


def generate_batch_images(prompts, args):
    """批量生成图片"""
    print(f"🔄 正在批量生成 {len(prompts)} 张图片...")
    results = batch_generate_images(
        prompts=prompts,
        model=args.model,
        max_concurrent=args.concurrent,
    )

    urls = []
    for i, result in enumerate(results):
        print(f"\n[{i+1}/{len(prompts)}]", end=" ")
        url = print_result(result, "image")
        urls.append(url)

    # 保存结果到文件
    output_file = "batch_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"prompts": prompts, "urls": urls}, f, ensure_ascii=False, indent=2)
    print(f"\n💾 结果已保存到: {output_file}")

    return urls


def generate_video_file(prompt, args):
    """生成视频"""
    print("🔄 正在启动视频生成任务...")
    video = generate_video(
        prompt=prompt,
        model=args.video_model,
        duration=args.duration,
        quality=args.quality,
    )

    task_id = video["id"]
    print(f"📋 任务 ID: {task_id}")
    print("⏳ 等待生成完成...")

    final = wait_for_video(task_id, max_wait_time=args.max_wait * 1000)
    return print_result(final, "video")


def main():
    parser = argparse.ArgumentParser(
        description="图片/视频生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # 输入参数
    parser.add_argument("prompt", help="图片/视频描述（批量生成时用空格分隔多个描述）")

    # 模式选择
    parser.add_argument("-v", "--video", action="store_true", help="生成视频模式")
    parser.add_argument("-b", "--batch", action="store_true", help="批量生成模式")

    # 图片参数
    parser.add_argument("-m", "--model", default="cogview-3-flash",
                       choices=["cogview-3-flash", "cogview-4-250304", "cogview-4"],
                       help="图片模型（默认: cogview-3-flash）")
    parser.add_argument("-q", "--quality", default="standard",
                       choices=["standard", "hd"],
                       help="图片质量（默认: standard）")
    parser.add_argument("-s", "--size", default="1024x1024",
                       choices=["1024x1024", "1024x1792", "1792x1024"],
                       help="图片尺寸（默认: 1024x1024）")

    # 视频参数
    parser.add_argument("--video-model", default="cogvideox-flash",
                       choices=["cogvideox-flash", "cogvideox-2", "cogvideox-3"],
                       help="视频模型（默认: cogvideox-flash）")
    parser.add_argument("-d", "--duration", type=int, default=5,
                       choices=[5, 10],
                       help="视频时长（默认: 5秒）")
    parser.add_argument("--max-wait", type=int, default=180,
                       help="最大等待时间（秒，默认: 180）")

    # 批量参数
    parser.add_argument("-c", "--concurrent", type=int, default=3,
                       help="并发数（默认: 3）")

    args = parser.parse_args()

    # 检查环境变量
    if not os.environ.get("BIGMODEL_API_KEY"):
        print("❌ 错误: 未设置 BIGMODEL_API_KEY 环境变量")
        print("\n请先设置 API Key:")
        print("  export BIGMODEL_API_KEY=your_api_key_here")
        print("\n或添加到 ~/.zshrc:")
        print("  echo 'export BIGMODEL_API_KEY=your_api_key_here' >> ~/.zshrc")
        sys.exit(1)

    # 根据模式执行
    try:
        if args.video:
            generate_video_file(args.prompt, args)
        elif args.batch:
            prompts = args.prompt.split()
            if len(prompts) < 2:
                print("❌ 批量模式需要至少 2 个描述（用空格分隔）")
                sys.exit(1)
            generate_batch_images(prompts, args)
        else:
            generate_single_image(args.prompt, args)
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
