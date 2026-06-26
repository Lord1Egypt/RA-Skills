#!/usr/bin/env python3
"""
使用OpenAI免费额度生成图片
"""

import os
import sys
import argparse
from pathlib import Path

def generate_with_free_credit(prompt, count=1, size="1024x1024", output_dir="./ai_images"):
    """使用免费额度生成图片"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ 未设置OPENAI_API_KEY")
        return False
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        print(f"🎨 使用免费额度生成图片...")
        print(f"  提示词: {prompt}")
        print(f"  数量: {count}")
        print(f"  尺寸: {size}")
        
        # 计算成本
        cost_per_image = 0.04  # DALL-E 3标准版
        total_cost = count * cost_per_image
        
        print(f"  预估成本: ${total_cost:.2f}（用免费额度）")
        
        # 实际生成
        print(f"  🎨 实际生成中...")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=count,
        )
        
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # 实际保存图片
        for i, img_response in enumerate(response.data):
            image_url = img_response.url
            filename = f"ai_{i+1:03d}.jpg"
            filepath = output_path / filename
            
            # 下载图片
            import requests
            img_data = requests.get(image_url).content
            with open(filepath, 'wb') as f:
                f.write(img_data)
            
            print(f"  ✅ 生成: {filename}")
            print(f"     URL: {image_url}")
        
        print(f"\n💰 成本统计:")
        print(f"  生成数量: {count}张")
        print(f"  总成本: ${total_cost:.2f}")
        print(f"  文件保存到: {output_path.absolute()}")
        
        return True
        
    except ImportError:
        print("❌ 需要安装openai包: pip install openai")
        return False
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="使用OpenAI免费额度生成图片")
    parser.add_argument("--prompt", required=True, help="图片描述")
    parser.add_argument("--count", type=int, default=1, help="生成数量")
    parser.add_argument("--size", default="1024x1024", help="图片尺寸")
    parser.add_argument("--output", default="./ai_images", help="输出目录")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行")
    
    args = parser.parse_args()
    
    print("🎨 AI图片生成器（使用免费额度）")
    print("=" * 50)
    
    if args.dry_run:
        print("⚠️  模拟运行模式")
        print(f"  提示词: {args.prompt}")
        print(f"  数量: {args.count}")
        print(f"  预估成本: ${args.count * 0.04:.2f}")
        return
    
    # 确认
    cost = args.count * 0.04
    print(f"⚠️  这将使用免费额度: ${cost:.2f}")
    
    # 自动执行，不需要确认
    if True:  # 自动执行
        success = generate_with_free_credit(
            prompt=args.prompt,
            count=args.count,
            size=args.size,
            output_dir=args.output
        )
        
        if success:
            print("\n✅ 完成！")
            print("注意：实际使用时取消代码中的注释")
    else:
        print("取消生成")

if __name__ == "__main__":
    main()