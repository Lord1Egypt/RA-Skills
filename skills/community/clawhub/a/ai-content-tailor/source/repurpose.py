#!/usr/bin/env python3
"""
Content Repurposer - 一文章多平台适配器
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("❌ 未设置 OPENAI_API_KEY，请编辑 .env 文件")
    sys.exit(1)

try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
except ImportError:
    print("❌ 未安装 openai 库，运行：pip install openai")
    sys.exit(1)


PLATFORM_PROMPTS = {
    "wechat": """将以下文章改写成适合微信公众号发布的形式。

要求：
- 标题：简洁有力，20字以内，吸引点击
- 开头：引入话题，快速抓住读者
- 段落：每段2-3行，多换行，避免大段文字
- 语气：正式但有亲和力，口语化但专业
- 配图：用 [图片：描述] 标注配图位置（至少3处）
- 结尾：总结+互动引导（点赞/在看/分享）
- 格式：使用 Markdown，多用标题、加粗、列表

输出为完整的 Markdown 文章""",

    "xhs": """将以下文章改写成适合小红书笔记的形式。

要求：
- 标题：爆款风格，10-15字，加表情符号（如：💡、🌟、🔥）
- 开头：立刻引起兴趣/痛点/悬念（前三行最关键）
- 正文：口语化，像和朋友分享，用短句和分段
- 标签：文末添加3-5个相关话题标签（如：#AI技能 #内容创作）
- 语气：真实、亲切、有感染力
- 长度：500-800字左右，适合快速阅读
- 多用emoji点缀（适度）

输出为笔记文案""",

    "zhihu": """将以下文章改写成适合知乎回答的形式。

要求：
- 标题：可以是疑问句或干货陈述，清晰具体
- 开头：直接给出核心观点/结论（知乎读者喜欢先看结论）
- 正文：逻辑清晰，分点论述，有深度
  - 每个观点要有论证或案例支撑
  - 数据、引用、对比会增加可信度
- 语气：理性、专业、有见地
- 结尾：总结+开放式问题或延伸思考
- 格式：Markdown，多用标题、引用、列表

输出为知乎回答全文""",

    "dy": """将以下文章改写成适合抖音口播文案的形式。

要求：
- 标题：极简短，引发好奇（"你知道吗？""千万别..."）
- 结构：黄金3秒开头 → 快速推进 → 结尾留钩子
- 语言：口语化，像在和朋友聊天
  - 多用"你""咱们"
  - 短句，每句10-20字
  - 节奏快，信息密度高
- 时长：适合60秒内说完（约300-500字）
- 结尾：引导互动（"关注我，下期讲..."）
- 不需要详细段落，保持连贯即可

输出为口播脚本"""
}


def read_article(filepath):
    """读取文章内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def rewrite_for_platform(article, platform, tone="auto", model="gpt-4o-mini"):
    """使用 LLM 改写文章"""
    prompt = PLATFORM_PROMPTS[platform]

    if tone and tone != "auto":
        prompt += f"\n\n语气：{tone}"

    full_prompt = f"{prompt}\n\n原文：\n{article}\n\n请输出改写后的内容："

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个专业的跨平台内容编辑，擅长将同一内容适配不同平台。"},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ 改写失败 ({platform}): {e}")
        return None


def process_single(article_path, output_dir=None, platforms=None, model="gpt-4o-mini", tone="auto", preview=False):
    """处理单篇文章"""
    article_path = Path(article_path)
    if not article_path.exists():
        print(f"❌ 文件不存在: {article_path}")
        return False

    article = read_article(article_path)
    if not platforms:
        platforms = list(PLATFORM_PROMPTS.keys())

    results = {}
    for platform in platforms:
        if platform not in PLATFORM_PROMPTS:
            print(f"⚠️  跳过未知平台: {platform}")
            continue
        print(f"🔄 改写为 {platform}...")
        rewritten = rewrite_for_platform(article, platform, tone, model)
        if rewritten:
            results[platform] = rewritten

    if preview:
        print("\n" + "="*50)
        print("预览模式 - 各平台版本：")
        print("="*50)
        for platform, content in results.items():
            print(f"\n## {platform.upper()}\n")
            print(content[:500] + "..." if len(content) > 500 else content)
            print("\n" + "-"*30)
        print("="*50)
        print("预览完成，未保存文件")
        return True

    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        for platform, content in results.items():
            out_file = output_dir / f"{article_path.stem}_{platform}.md"
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已保存: {out_file}")

    return True


def batch_process(input_dir, output_dir=None, platforms=None, model="gpt-4o-mini", tone="auto", preview=False):
    """批量处理文件夹"""
    input_dir = Path(input_dir)
    if not input_dir.exists():
        print(f"❌ 文件夹不存在: {input_dir}")
        return

    if not output_dir:
        output_dir = input_dir
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    articles = list(input_dir.glob("*.md")) + list(input_dir.glob("*.txt"))
    print(f"发现 {len(articles)} 篇文章")

    for article in articles:
        print(f"\n📄 处理: {article.name}")
        process_single(article, output_dir, platforms, model, tone, preview)


def main():
    parser = argparse.ArgumentParser(
        description="Content Repurposer - 一篇文章多平台适配",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  content-repurposer repurpose article.md
  content-repurposer repurpose article.md --platforms wechat,xhs --output ./versions/
  content-repurposer batch ./articles/ --preview
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="命令")

    # repurpose 命令
    rep_parser = subparsers.add_parser("repurpose", help="改写单篇文章")
    rep_parser.add_argument("input", help="输入文章文件路径")
    rep_parser.add_argument("--output", "-o", help="输出目录")
    rep_parser.add_argument("--platforms", "-p", help="平台列表，逗号分隔 (wechat,xhs,zhihu,dy)")
    rep_parser.add_argument("--model", "-m", default="gpt-4o-mini", help="LLM 模型")
    rep_parser.add_argument("--tone", "-t", choices=["auto", "professional", "casual", "storytelling"], default="auto", help="语气")
    rep_parser.add_argument("--preview", action="store_true", help="预览模式")

    # batch 命令
    batch_parser = subparsers.add_parser("batch", help="批量处理")
    batch_parser.add_argument("input", help="输入文件夹路径")
    batch_parser.add_argument("--output", "-o", help="输出目录")
    batch_parser.add_argument("--platforms", "-p", help="平台列表")
    batch_parser.add_argument("--model", "-m", default="gpt-4o-mini", help="LLM 模型")
    batch_parser.add_argument("--tone", "-t", default="auto", help="语气")
    batch_parser.add_argument("--preview", action="store_true", help="预览模式")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    platforms = args.platforms.split(",") if args.platforms else None

    if args.command == "repurpose":
        success = process_single(args.input, args.output, platforms, args.model, args.tone, args.preview)
        sys.exit(0 if success else 1)
    elif args.command == "batch":
        batch_process(args.input, args.output, platforms, args.model, args.tone, args.preview)


if __name__ == "__main__":
    main()