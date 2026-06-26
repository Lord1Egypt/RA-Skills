#!/usr/bin/env python3
"""
图片去背景工具 - 使用 rembg 库实现 AI 智能去背景
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

try:
    from rembg import remove
    from PIL import Image
except ImportError:
    print("错误: 请先安装依赖库")
    print("执行: pip install rembg pillow")
    sys.exit(1)


def process_image(
    input_path: str,
    output_path: str,
    model: str = "u2net",
    threshold: float = 0.5,
    alpha_matting: bool = False,
    alpha_matting_foreground: int = 240,
    alpha_matting_background: int = 10,
    force: bool = False
) -> bool:
    """处理单张图片去背景"""
    try:
        input_file = Path(input_path)
        output_file = Path(output_path)

        # 检查输入文件
        if not input_file.exists():
            print(f"错误: 输入文件不存在: {input_path}")
            return False

        # 检查输出文件是否已存在
        if output_file.exists() and not force:
            print(f"跳过: 文件已存在 (使用 --force 覆盖): {output_path}")
            return False

        # 确保输出目录存在
        output_file.parent.mkdir(parents=True, exist_ok=True)

        print(f"处理: {input_file.name} -> {output_file.name}")

        # 读取图片
        input_image = Image.open(input_file)

        # 执行去背景
        output_image = remove(
            input_image,
            model_name=model,
            alpha_matting=alpha_matting,
            alpha_matting_foreground_threshold=alpha_matting_foreground,
            alpha_matting_background_threshold=alpha_matting_background
        )

        # 保存结果
        output_image.save(output_file, "PNG")
        print(f"完成: {output_file.absolute()}")
        return True

    except Exception as e:
        print(f"错误: 处理失败 {input_path}: {str(e)}")
        return False


def process_directory(
    input_dir: str,
    output_dir: str,
    model: str = "u2net",
    threshold: float = 0.5,
    keep_name: bool = False,
    alpha_matting: bool = False,
    alpha_matting_foreground: int = 240,
    alpha_matting_background: int = 10,
    force: bool = False
) -> tuple:
    """批量处理目录下所有图片"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # 支持的图片格式
    image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.tif'}

    # 获取所有图片文件
    image_files = [
        f for f in input_path.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]

    if not image_files:
        print(f"警告: 目录中没有找到图片文件: {input_dir}")
        return (0, 0)

    print(f"找到 {len(image_files)} 张图片，开始处理...")

    # 确保输出目录存在
    output_path.mkdir(parents=True, exist_ok=True)

    success = 0
    failed = 0

    for image_file in image_files:
        # 生成输出文件名
        if keep_name:
            output_name = image_file.stem + ".png"
        else:
            output_name = image_file.stem + "_nobg.png"

        output_file = output_path / output_name

        if process_image(
            str(image_file),
            str(output_file),
            model=model,
            threshold=threshold,
            alpha_matting=alpha_matting,
            alpha_matting_foreground=alpha_matting_foreground,
            alpha_matting_background=alpha_matting_background,
            force=force
        ):
            success += 1
        else:
            failed += 1

    return (success, failed)


def main():
    parser = argparse.ArgumentParser(
        description="图片智能去背景工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --input photo.jpg
  %(prog)s --input photo.jpg --output result.png
  %(prog)s --input ./photos --output ./results
  %(prog)s --input photo.jpg --model RMBG-1.4 --alpha-matting
        """
    )

    parser.add_argument(
        "--input", "-i",
        required=True,
        help="输入图片路径或文件夹路径"
    )

    parser.add_argument(
        "--output", "-o",
        default=None,
        help="输出路径（文件或文件夹），默认与输入同目录"
    )

    parser.add_argument(
        "--model", "-m",
        default="u2net",
        choices=["u2net", "u2netp", "u2net_human_seg", "RMBG-1.4"],
        help="使用的模型 (默认: u2net)"
    )

    parser.add_argument(
        "--threshold", "-t",
        type=float,
        default=0.5,
        help="分割阈值 0-1 (默认: 0.5)"
    )

    parser.add_argument(
        "--keep-name", "-k",
        action="store_true",
        help="保持原始文件名（仅添加.png后缀）"
    )

    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="覆盖已存在的文件"
    )

    parser.add_argument(
        "--alpha-matting",
        action="store_true",
        help="启用 Alpha Matting 增强边缘"
    )

    parser.add_argument(
        "--alpha-matting-foreground",
        type=int,
        default=240,
        help="Alpha Matting 前景阈值 (默认: 240)"
    )

    parser.add_argument(
        "--alpha-matting-background",
        type=int,
        default=10,
        help="Alpha Matting 背景阈值 (默认: 10)"
    )

    args = parser.parse_args()

    # 确定输入路径
    input_path = Path(args.input)

    # 确定输出路径
    if args.output:
        output_path = args.output
    else:
        if input_path.is_file():
            # 如果是文件，默认输出到同目录
            output_path = str(input_path.parent / f"{input_path.stem}_nobg.png")
        else:
            # 如果是目录，默认输出到同目录的 nobg 子目录
            output_path = str(input_path.parent / "nobg")

    # 判断是文件还是目录
    if input_path.is_file():
        # 处理单个文件
        success = process_image(
            str(input_path),
            output_path,
            model=args.model,
            threshold=args.threshold,
            alpha_matting=args.alpha_matting,
            alpha_matting_foreground=args.alpha_matting_foreground,
            alpha_matting_background=args.alpha_matting_background,
            force=args.force
        )
        sys.exit(0 if success else 1)

    elif input_path.is_dir():
        # 批量处理目录
        success, failed = process_directory(
            str(input_path),
            output_path,
            model=args.model,
            threshold=args.threshold,
            keep_name=args.keep_name,
            alpha_matting=args.alpha_matting,
            alpha_matting_foreground=args.alpha_matting_foreground,
            alpha_matting_background=args.alpha_matting_background,
            force=args.force
        )

        print(f"\n处理完成: 成功 {success} 张, 失败 {failed} 张")
        sys.exit(0 if failed == 0 else 1)

    else:
        print(f"错误: 输入路径不存在: {args.input}")
        sys.exit(1)


if __name__ == "__main__":
    main()
