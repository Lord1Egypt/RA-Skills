#!/usr/bin/env python3
"""
批量图片处理器
"""

import argparse
import subprocess
from pathlib import Path
import json

def check_imagemagick():
    """检查ImageMagick"""
    try:
        result = subprocess.run(["convert", "--version"], 
                              capture_output=True, text=True)
        if "ImageMagick" in result.stdout:
            print("✅ ImageMagick已安装")
            return True
    except:
        pass
    
    print("❌ ImageMagick未安装")
    print("安装命令:")
    print("  macOS: brew install imagemagick")
    print("  Ubuntu: sudo apt-get install imagemagick")
    return False

def batch_resize(input_dir, output_dir, width, height):
    """批量调整尺寸"""
    print(f"📏 批量调整尺寸: {width}x{height}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    processed = []
    
    # 查找图片文件
    image_exts = ["*.jpg", "*.jpeg", "*.png", "*.webp", "*.gif"]
    files = []
    for ext in image_exts:
        files.extend(input_dir.glob(ext))
    
    for filepath in files:
        output_file = output_dir / f"resized_{filepath.name}"
        
        # 构建convert命令
        cmd = [
            "convert", str(filepath),
            "-resize", f"{width}x{height}^",
            "-gravity", "center",
            "-extent", f"{width}x{height}",
            str(output_file)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            processed.append(str(output_file))
            print(f"  ✅ {filepath.name} → {output_file.name}")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ 失败: {filepath.name} - {e}")
    
    return processed

def batch_convert(input_dir, output_dir, format):
    """批量转换格式"""
    print(f"🔄 批量转换格式: {format}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    processed = []
    
    image_exts = ["*.jpg", "*.jpeg", "*.png", "*.webp", "*.gif"]
    files = []
    for ext in image_exts:
        files.extend(input_dir.glob(ext))
    
    for filepath in files:
        output_file = output_dir / f"{filepath.stem}.{format}"
        
        cmd = ["convert", str(filepath), str(output_file)]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            processed.append(str(output_file))
            print(f"  ✅ {filepath.name} → {output_file.name}")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ 失败: {filepath.name} - {e}")
    
    return processed

def batch_optimize(input_dir, output_dir, quality):
    """批量优化质量"""
    print(f"✨ 批量优化质量: {quality}%")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    processed = []
    
    image_exts = ["*.jpg", "*.jpeg", "*.png"]
    files = []
    for ext in image_exts:
        files.extend(input_dir.glob(ext))
    
    for filepath in files:
        output_file = output_dir / f"optimized_{filepath.name}"
        
        cmd = ["convert", str(filepath), "-quality", str(quality), str(output_file)]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            
            # 计算文件大小变化
            orig_size = filepath.stat().st_size
            opt_size = output_file.stat().st_size
            savings = 100 - (opt_size * 100 / orig_size) if orig_size > 0 else 0
            
            processed.append({
                "file": str(output_file),
                "original_size": orig_size,
                "optimized_size": opt_size,
                "savings": round(savings, 1)
            })
            
            print(f"  ✅ {filepath.name} (节省: {savings:.1f}%)")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ 失败: {filepath.name} - {e}")
    
    return processed

def main():
    parser = argparse.ArgumentParser(description="批量图片处理器")
    parser.add_argument("--input", required=True, help="输入目录")
    parser.add_argument("--output", default="./processed", help="输出目录")
    
    # 处理选项
    parser.add_argument("--resize", help="调整尺寸，格式: 宽度x高度")
    parser.add_argument("--convert", choices=["jpg", "png", "webp"], help="转换格式")
    parser.add_argument("--optimize", type=int, help="优化质量(1-100)")
    parser.add_argument("--all", action="store_true", help="执行所有优化")
    
    args = parser.parse_args()
    
    print("⚡ 批量图片处理器")
    print("=" * 50)
    
    # 检查ImageMagick
    if not check_imagemagick():
        return
    
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    
    if not input_dir.exists():
        print(f"❌ 输入目录不存在: {input_dir}")
        return
    
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    
    results = {}
    
    # 执行处理
    if args.all or args.resize:
        if args.resize:
            try:
                width, height = map(int, args.resize.split('x'))
                resized = batch_resize(input_dir, output_dir / "resized", width, height)
                results["resize"] = {
                    "count": len(resized),
                    "size": args.resize,
                    "files": resized[:10]  # 只记录前10个
                }
            except:
                print("❌ 尺寸格式错误，使用: 宽度x高度")
    
    if args.all or args.convert:
        converted = batch_convert(input_dir, output_dir / "converted", args.convert)
        results["convert"] = {
            "count": len(converted),
            "format": args.convert,
            "files": converted[:10]
        }
    
    if args.all or args.optimize:
        if args.optimize and 1 <= args.optimize <= 100:
            optimized = batch_optimize(input_dir, output_dir / "optimized", args.optimize)
            results["optimize"] = {
                "count": len(optimized),
                "quality": args.optimize,
                "files": optimized[:10]
            }
    
    # 保存处理记录
    if results:
        record_file = output_dir / "batch_process.json"
        with open(record_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 批量处理完成！")
        print(f"   输出目录: {output_dir.absolute()}")
        print(f"   记录文件: {record_file}")
        
        # 显示统计
        print(f"\n📊 处理统计:")
        for action, info in results.items():
            print(f"  {action}: {info['count']} 个文件")
    else:
        print("\n⚠️  未执行任何处理")
        print("   使用 --resize, --convert, --optimize 或 --all")

if __name__ == "__main__":
    main()