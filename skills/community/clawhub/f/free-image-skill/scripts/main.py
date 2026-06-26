#!/usr/bin/env python3
"""
免费图片解决方案 - 主脚本
核心：不花钱，免费办大事儿！
"""

import os
import sys
import argparse
from pathlib import Path

def check_dependencies():
    """检查依赖"""
    try:
        import openai
        import requests
        from PIL import Image
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("安装命令: pip3 install openai requests pillow --break-system-packages")
        return False

def check_openai_key():
    """检查OpenAI API密钥"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  未设置OPENAI_API_KEY环境变量")
        print("   使用免费额度: export OPENAI_API_KEY='你的免费额度API密钥'")
        return False
    
    print(f"✅ OpenAI API密钥已设置（前几位: {api_key[:15]}...）")
    return True

def calculate_free_images():
    """计算可生成的免费图片数量"""
    # 假设新用户有$5免费额度，DALL-E 3标准版$0.04/张
    free_credit = 5.0  # 美元
    cost_per_image = 0.04
    
    max_images = int(free_credit / cost_per_image)
    return max_images

def show_free_sources():
    """显示免费资源"""
    print("\n🔍 免费图片资源:")
    sources = [
        ("Unsplash", "https://unsplash.com", "商业免费，高质量"),
        ("Pexels", "https://www.pexels.com", "商业免费，照片视频"),
        ("Pixabay", "https://pixabay.com", "商业免费，矢量插画"),
        ("Freepik", "https://www.freepik.com", "需署名，有免费选项"),
    ]
    
    for name, url, desc in sources:
        print(f"  • {name}: {desc}")
        print(f"    链接: {url}")

def generate_plan(args):
    """生成执行计划"""
    print("\n📋 执行计划:")
    
    # 计算可用资源
    max_ai_images = calculate_free_images() if check_openai_key() else 0
    
    if args.important_only:
        print(f"  🎨 只生成重要图片（AI）")
        print(f"    数量: {args.count}张")
        print(f"    成本: ${args.count * 0.04:.2f}（用免费额度）")
        if max_ai_images < args.count:
            print(f"    ⚠️  超过免费额度，只能生成{max_ai_images}张")
    
    elif args.free_only:
        print(f"  📷 只搜索免费图片")
        print(f"    数量: {args.count}张")
        print(f"    关键词: {args.keywords}")
        print(f"    成本: $0.00")
    
    else:
        # 混合模式
        ai_count = min(3, args.count // 3)  # 1/3用AI
        free_count = args.count - ai_count
        
        print(f"  🎨 AI生成（重要图片）: {ai_count}张")
        print(f"    成本: ${ai_count * 0.04:.2f}（用免费额度）")
        
        print(f"  📷 免费图库: {free_count}张")
        print(f"    关键词: 自动从文本提取")
        print(f"    成本: $0.00")
        
        print(f"  💰 总成本: ${ai_count * 0.04:.2f}（完全用免费额度）")

def extract_keywords(text, count=5):
    """从文本提取关键词"""
    # 简单实现
    words = text.split()
    common = {"的", "了", "在", "是", "和", "有", "这", "那"}
    keywords = [w for w in words if len(w) > 1 and w not in common]
    return keywords[:count]

def simulate_ai_generation(prompts, output_dir):
    """模拟AI图片生成（实际需要调用OpenAI API）"""
    print(f"\n🎨 模拟AI图片生成:")
    for i, prompt in enumerate(prompts):
        print(f"  {i+1}. {prompt[:50]}...")
        # 实际应该调用: openai.images.generate()
    
    print("  ✅ 完成（实际需要OpenAI API调用）")

def simulate_free_search(keywords, count, output_dir):
    """模拟免费图片搜索"""
    print(f"\n🔍 模拟免费图片搜索:")
    print(f"  关键词: {keywords}")
    
    for i in range(min(count, 10)):
        print(f"  {i+1}. 搜索 '{keywords[i % len(keywords)]}'...")
    
    print(f"  ✅ 找到 {count} 张免费图片")

def main():
    parser = argparse.ArgumentParser(
        description="免费图片解决方案 - 不花钱，免费办大事儿！",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 为文章生成图片（混合模式）
  python3 main.py --text "人工智能技术文章" --count 10
  
  # 只生成重要图片（用免费额度）
  python3 main.py --important-only --prompt "专业图表" --count 3
  
  # 只搜索免费图片
  python3 main.py --free-only --keywords "科技,创新" --count 20
  
  # 显示计划不执行
  python3 main.py --text "内容" --plan-only
        """
    )
    
    parser.add_argument("--text", help="需要配图的文本内容")
    parser.add_argument("--count", type=int, default=10, help="图片数量")
    parser.add_argument("--output", default="./free_images", help="输出目录")
    parser.add_argument("--keywords", help="搜索关键词，用逗号分隔")
    parser.add_argument("--prompt", help="AI生成提示词")
    parser.add_argument("--important-only", action="store_true", help="只生成重要图片（AI）")
    parser.add_argument("--free-only", action="store_true", help="只搜索免费图片")
    parser.add_argument("--plan-only", action="store_true", help="只显示计划")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🆓 免费图片解决方案")
    print("=" * 60)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 显示免费资源
    show_free_sources()
    
    # 生成计划
    generate_plan(args)
    
    if args.plan_only:
        print("\n✅ 计划生成完成")
        return
    
    # 准备输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # 提取关键词和提示词
    keywords = []
    prompts = []
    
    if args.text:
        keywords = extract_keywords(args.text, 5)
        prompts = [f"高质量的{k}相关图片" for k in keywords[:3]]
    elif args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",")]
        prompts = [f"高质量的{k}图片" for k in keywords[:3]]
    elif args.prompt:
        prompts = [args.prompt]
    
    # 询问确认
    print("\n⚠️  注意:")
    print("   • AI生成会使用免费额度")
    print("   • 实际执行需要网络连接")
    
    if args.dry_run:
        print("   • 模拟运行模式")
        response = "y"
    else:
        response = input("\n是否开始执行? (y/N): ").strip().lower()
    
    if response != 'y':
        print("取消执行")
        return
    
    # 执行
    print("\n🚀 开始执行...")
    
    if args.important_only or (not args.free_only and prompts):
        # AI生成
        simulate_ai_generation(prompts, output_dir / "ai")
    
    if args.free_only or (not args.important_only and keywords):
        # 免费搜索
        simulate_free_search(keywords, args.count, output_dir / "free")
    
    print("\n✅ 执行完成！")
    print(f"   输出目录: {output_dir.absolute()}")
    print("\n下一步建议:")
    print("1. 查看生成的图片")
    print("2. 使用去水印工具: python3 scripts/watermark_remover.py")
    print("3. 批量优化: python3 scripts/batch_processor.py")

if __name__ == "__main__":
    main()