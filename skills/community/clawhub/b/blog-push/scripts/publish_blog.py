#!/usr/bin/env python3
"""
Hugo 博客文章发布脚本
将 Markdown 文档和封面图发布到 Hugo 博客

支持环境变量配置：
- HUGO_BLOG_DIR: 博客项目根目录
- HUGO_POSTS_DIR: posts 目录相对路径（默认: content/zh/posts）
- HUGO_TEMPLATE_PATH: 模板文件相对路径（默认: archetypes/default.md）

优先级：命令行参数 > 环境变量 > 默认值

语法优化（基于 CLAUDE.md）：
- 自动检测数学公式和 Mermaid 图表，添加 libraries 字段
- 智能分类和标签建议
- Shortcodes 使用提示
"""

import os
import sys
import shutil
import datetime
import argparse
import re
from pathlib import Path


ENV_BLOG_DIR = "HUGO_BLOG_DIR"
ENV_POSTS_DIR = "HUGO_POSTS_DIR"
ENV_TEMPLATE_PATH = "HUGO_TEMPLATE_PATH"
ENV_DAILY_DIR = "HUGO_DAILY_DIR"
ENV_WEEKLY_DIR = "HUGO_WEEKLY_DIR"
ENV_DAILY_TEMPLATE = "HUGO_DAILY_TEMPLATE"
ENV_WEEKLY_TEMPLATE = "HUGO_WEEKLY_TEMPLATE"

DEFAULT_POSTS_DIR = "content/zh/posts"
DEFAULT_DAILY_DIR = "content/zh/daily"
DEFAULT_WEEKLY_DIR = "content/zh/weekly"
DEFAULT_TEMPLATE = "archetypes/default.md"
DEFAULT_DAILY_TEMPLATE = "archetypes/daily.md"
DEFAULT_WEEKLY_TEMPLATE = "archetypes/weekly.md"

# 分类建议映射
CATEGORY_SUGGESTIONS = {
    "技术": {
        "keywords": [
            "代码",
            "编程",
            "开发",
            "架构",
            "系统",
            "API",
            "数据库",
            "服务器",
            "部署",
            "Docker",
            "Git",
            "算法",
            "数据结构",
        ],
        "tags": ["技术", "编程", "开发", "架构"],
    },
    "AI": {
        "keywords": [
            "AI",
            "人工智能",
            "机器学习",
            "深度学习",
            "LLM",
            "大模型",
            "ChatGPT",
            "Claude",
            "GPT",
            "Prompt",
            "神经网络",
            "NLP",
            "计算机视觉",
        ],
        "tags": ["AI", "LLM", "机器学习", "人工智能"],
    },
    "生活": {
        "keywords": [
            "读书",
            "电影",
            "旅行",
            "咖啡",
            "美食",
            "运动",
            "健康",
            "日常",
            "随笔",
            "感悟",
        ],
        "tags": ["生活", "随笔", "感悟"],
    },
    "思考": {
        "keywords": [
            "思考",
            "观点",
            "方法论",
            "职业规划",
            "成长",
            "效率",
            "时间管理",
            "习惯",
            "目标",
            "复盘",
        ],
        "tags": ["思考", "方法论", "成长"],
    },
}

# 常用标签映射
TAG_SUGGESTIONS = {
    "AI/LLM": ["AI", "Claude", "GPT", "LLM", "Prompt", "OpenAI", "Anthropic", "大模型"],
    "编程": [
        "Python",
        "Java",
        "Go",
        "JavaScript",
        "TypeScript",
        "架构",
        "微服务",
        "云原生",
    ],
    "工具": ["Obsidian", "Docker", "Git", "Hugo", "Cursor", "VSCode"],
    "效率": ["工作流", "自动化", "时间管理", "效率工具"],
    "生活": ["读书", "电影", "旅行", "咖啡", "健康"],
}


def validate_hugo_project(blog_dir: str) -> bool:
    """验证是否为有效的 Hugo 项目"""
    blog_path = Path(blog_dir)
    if not blog_path.exists():
        return False

    config_files = [
        "config.toml",
        "config.yaml",
        "config.yml",
        "config.json",
    ]

    for config_file in config_files:
        if (blog_path / config_file).exists():
            return True

    if (blog_path / "config").exists():
        return True

    return False


def resolve_paths(args, content_type="posts") -> tuple:
    """
    解析路径配置
    优先级：命令行参数 > 环境变量 > 默认值

    返回：(blog_dir, target_dir, template_path, sources)
    """
    sources = {}

    blog_dir = args.blog_dir if args.blog_dir else os.environ.get(ENV_BLOG_DIR, ".")
    sources["blog_dir"] = (
        "命令行参数"
        if args.blog_dir
        else ("环境变量" if os.environ.get(ENV_BLOG_DIR) else "默认值(当前目录)")
    )

    # 根据内容类型确定目录
    if content_type == "daily":
        if args.posts_dir:
            if os.path.isabs(args.posts_dir):
                target_dir = args.posts_dir
            else:
                target_dir = os.path.join(blog_dir, args.posts_dir)
            sources["target_dir"] = "命令行参数"
        else:
            relative_target = os.environ.get(ENV_DAILY_DIR, DEFAULT_DAILY_DIR)
            target_dir = os.path.join(blog_dir, relative_target)
            sources["target_dir"] = (
                "环境变量" if os.environ.get(ENV_DAILY_DIR) else "默认值"
            )
    elif content_type == "weekly":
        if args.posts_dir:
            if os.path.isabs(args.posts_dir):
                target_dir = args.posts_dir
            else:
                target_dir = os.path.join(blog_dir, args.posts_dir)
            sources["target_dir"] = "命令行参数"
        else:
            relative_target = os.environ.get(ENV_WEEKLY_DIR, DEFAULT_WEEKLY_DIR)
            target_dir = os.path.join(blog_dir, relative_target)
            sources["target_dir"] = (
                "环境变量" if os.environ.get(ENV_WEEKLY_DIR) else "默认值"
            )
    else:  # posts (default)
        if args.posts_dir:
            if os.path.isabs(args.posts_dir):
                target_dir = args.posts_dir
            else:
                target_dir = os.path.join(blog_dir, args.posts_dir)
            sources["target_dir"] = "命令行参数"
        else:
            relative_target = os.environ.get(ENV_POSTS_DIR, DEFAULT_POSTS_DIR)
            target_dir = os.path.join(blog_dir, relative_target)
            sources["target_dir"] = (
                "环境变量" if os.environ.get(ENV_POSTS_DIR) else "默认值"
            )

    # 根据内容类型确定模板
    if content_type == "daily":
        if args.template:
            if os.path.isabs(args.template):
                template_path = args.template
            else:
                template_path = os.path.join(blog_dir, args.template)
            sources["template"] = "命令行参数"
        else:
            relative_template = os.environ.get(
                ENV_DAILY_TEMPLATE, DEFAULT_DAILY_TEMPLATE
            )
            template_path = os.path.join(blog_dir, relative_template)
            sources["template"] = (
                "环境变量" if os.environ.get(ENV_DAILY_TEMPLATE) else "默认值"
            )
    elif content_type == "weekly":
        if args.template:
            if os.path.isabs(args.template):
                template_path = args.template
            else:
                template_path = os.path.join(blog_dir, args.template)
            sources["template"] = "命令行参数"
        else:
            relative_template = os.environ.get(
                ENV_WEEKLY_TEMPLATE, DEFAULT_WEEKLY_TEMPLATE
            )
            template_path = os.path.join(blog_dir, relative_template)
            sources["template"] = (
                "环境变量" if os.environ.get(ENV_WEEKLY_TEMPLATE) else "默认值"
            )
    else:  # posts (default)
        if args.template:
            if os.path.isabs(args.template):
                template_path = args.template
            else:
                template_path = os.path.join(blog_dir, args.template)
            sources["template"] = "命令行参数"
        else:
            relative_template = os.environ.get(ENV_TEMPLATE_PATH, DEFAULT_TEMPLATE)
            template_path = os.path.join(blog_dir, relative_template)
            sources["template"] = (
                "环境变量" if os.environ.get(ENV_TEMPLATE_PATH) else "默认值"
            )

    return blog_dir, target_dir, template_path, sources


def display_config(
    blog_dir: str,
    target_dir: str,
    template_path: str,
    sources: dict,
    content_type: str = "posts",
):
    """显示当前配置信息"""
    print(f"\n✓ Hugo 博客配置信息 ({content_type})")
    print("=" * 60)
    print(f"博客根目录: {blog_dir}")
    print(f"  来源: {sources['blog_dir']}")

    blog_valid = validate_hugo_project(blog_dir)
    if blog_valid:
        print(f"  状态: ✓ 有效 (检测到 Hugo 配置文件)")
    else:
        print(f"  状态: ✗ 无效 (未检测到 Hugo 配置文件)")

    print(f"\n目标目录: {target_dir}")
    print(f"  来源: {sources['target_dir']}")

    target_path = Path(target_dir)
    if target_path.exists():
        print(f"  状态: ✓ 存在")
    else:
        print(f"  状态: ✗ 不存在")

    print(f"\n模板路径: {template_path}")
    print(f"  来源: {sources['template']}")

    template_file = Path(template_path)
    if template_file.exists():
        print(f"  状态: ✓ 存在")
    else:
        print(f"  状态: ✗ 不存在")

    print("=" * 60)

    print("\n环境变量配置:")
    print(f"  {ENV_BLOG_DIR}: {os.environ.get(ENV_BLOG_DIR, '(未设置)')}")
    print(f"  {ENV_POSTS_DIR}: {os.environ.get(ENV_POSTS_DIR, '(未设置)')}")
    print(f"  {ENV_DAILY_DIR}: {os.environ.get(ENV_DAILY_DIR, '(未设置)')}")
    print(f"  {ENV_WEEKLY_DIR}: {os.environ.get(ENV_WEEKLY_DIR, '(未设置)')}")
    print(f"  {ENV_TEMPLATE_PATH}: {os.environ.get(ENV_TEMPLATE_PATH, '(未设置)')}")
    print(f"  {ENV_DAILY_TEMPLATE}: {os.environ.get(ENV_DAILY_TEMPLATE, '(未设置)')}")
    print(f"  {ENV_WEEKLY_TEMPLATE}: {os.environ.get(ENV_WEEKLY_TEMPLATE, '(未设置)')}")


def get_target_categories(target_dir: str) -> list:
    """获取目标目录下的所有子目录（用于 posts 类型）"""
    categories = []
    target_path = Path(target_dir)

    if not target_path.exists():
        print(f"错误: 目标目录不存在: {target_dir}")
        sys.exit(1)

    for item in target_path.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            categories.append(item.name)

    return sorted(categories)


def get_target_files(target_dir: str) -> list:
    """获取目标目录下的所有 Markdown 文件（用于 daily/weekly 类型）"""
    files = []
    target_path = Path(target_dir)

    if not target_path.exists():
        print(f"错误: 目标目录不存在: {target_dir}")
        sys.exit(1)

    for item in target_path.iterdir():
        if item.is_file() and item.suffix == ".md" and not item.name.startswith("_"):
            files.append(item.name)

    return sorted(files)


def display_categories(categories: list, content_type: str = "posts"):
    """显示所有分类"""
    print(f"\n可用的 {content_type} 分类目录:")
    print("=" * 50)
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    print("=" * 50)

    # 显示分类建议
    print("\n💡 分类建议:")
    print("- 技术: 技术文章、编程、工具、系统架构")
    print("- AI: 人工智能、机器学习、LLM、Prompt")
    print("- 生活: 日常记录、读书、电影、旅行")
    print("- 思考: 深度思考、观点、方法论、成长")


def display_files(files: list, content_type: str = "daily"):
    """显示所有文件（用于 daily/weekly）"""
    print(f"\n现有的 {content_type} 文章:")
    print("=" * 50)
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    print("=" * 50)


def validate_category(category: str, categories: list) -> bool:
    """验证分类是否存在，ROOT 表示直接发布到 posts_dir"""
    if category == "ROOT":
        return True
    return category in categories


def get_current_time() -> str:
    """获取当前时间，格式为 Hugo 需要的格式"""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%dT%H:%M:%S+08:00")


def sanitize_filename(name: str) -> str:
    """清理文件名，替换特殊字符"""
    # 保留中文字符，只替换空格和特殊符号
    name = name.replace(" ", "-").replace(" ", "-")
    # 移除非法字符但保留中文
    name = re.sub(r'[\\/*?<>"|:]', "", name)
    return name


def read_template(template_path: str) -> str:
    """读取模板文件"""
    template_file = Path(template_path)

    if not template_file.exists():
        print(f"错误: 模板文件不存在: {template_path}")
        sys.exit(1)

    with open(template_file, "r", encoding="utf-8") as f:
        return f.read()


def detect_content_features(content: str) -> dict:
    """检测内容特性，用于自动添加 libraries"""
    features = {
        "math": False,
        "mermaid": False,
        "chart": False,
    }

    # 检测数学公式 ($...$ 或 $$...$$ 或 \begin{}...\end{})
    if (
        re.search(r"\$\$.+?\$\$", content, re.DOTALL)
        or re.search(r"[^$]\$[^$]+?\$[^$]", content)
        or re.search(r"\\begin\{.*?\}", content)
    ):
        features["math"] = True

    # 检测 Mermaid 图表
    if re.search(r"```mermaid\s+", content, re.IGNORECASE) or "{{< mermaid" in content:
        features["mermaid"] = True

    # 检测图表相关内容
    if re.search(r"```(chart|flowchart|graph)\s+", content, re.IGNORECASE):
        features["chart"] = True

    return features


def suggest_category_and_tags(content: str, title: str) -> tuple:
    """根据内容智能建议分类和标签"""
    content_lower = (content + " " + title).lower()

    # 分类建议
    category_scores = {}
    for category, info in CATEGORY_SUGGESTIONS.items():
        score = 0
        for keyword in info["keywords"]:
            if keyword.lower() in content_lower:
                score += 1
        if score > 0:
            category_scores[category] = score

    suggested_category = (
        max(category_scores, key=category_scores.get) if category_scores else None
    )

    # 标签建议
    suggested_tags = []
    for tag_category, tags in TAG_SUGGESTIONS.items():
        for tag in tags:
            if tag.lower() in content_lower and tag not in suggested_tags:
                suggested_tags.append(tag)

    return suggested_category, suggested_tags[:5]  # 最多返回5个标签


def process_frontmatter(
    template: str,
    title: str,
    current_time: str,
    content: str = "",
    cover_filename: str = "",
    draft: bool = False,
    custom_tags: list = None,
    custom_category: str = None,
) -> str:
    """处理 front matter，替换标题和时间，智能添加 libraries"""
    # 检测内容特性
    features = detect_content_features(content)

    # 智能建议分类和标签
    suggested_category, suggested_tags = suggest_category_and_tags(content, title)

    # 合并建议的标签和自定义标签
    if custom_tags:
        all_tags = list(dict.fromkeys(custom_tags + suggested_tags))  # 去重
    else:
        all_tags = suggested_tags

    # 使用建议或自定义的分类
    final_category = custom_category if custom_category else suggested_category

    lines = template.split("\n")
    processed_lines = []
    in_frontmatter = False
    libraries_added = False
    tags_added = False
    categories_added = False

    for line in lines:
        stripped = line.strip()

        if stripped == "---":
            in_frontmatter = not in_frontmatter
            processed_lines.append(line)
            continue

        if in_frontmatter:
            if line.startswith("title:"):
                processed_lines.append(f'title: "{title}"')
            elif line.startswith("date:"):
                processed_lines.append(f"date: {current_time}")
            elif line.startswith("publishDate:"):
                processed_lines.append(f"publishDate: {current_time}")
            elif line.startswith("draft:"):
                processed_lines.append(f"draft: {'true' if draft else 'false'}")
            elif line.startswith("image:") and cover_filename:
                processed_lines.append(f"image: {cover_filename}")
            elif line.startswith("categories:"):
                categories_added = True
                if final_category:
                    processed_lines.append("categories:")
                    processed_lines.append(f"  - {final_category}")
                else:
                    processed_lines.append(line)
            elif line.startswith("tags:"):
                tags_added = True
                if all_tags:
                    processed_lines.append("tags:")
                    for tag in all_tags:
                        processed_lines.append(f"  - {tag}")
                else:
                    processed_lines.append(line)
            elif line.startswith("libraries:"):
                libraries_added = True
                libraries = []
                if features["math"]:
                    libraries.append("katex")
                if features["mermaid"]:
                    libraries.append("mermaid")
                if features["chart"]:
                    libraries.extend(["chart", "flowchartjs"])
                if libraries:
                    processed_lines.append(f"libraries: {libraries}")
                else:
                    processed_lines.append(line)
            else:
                processed_lines.append(line)
        else:
            processed_lines.append(line)

    # 如果没有找到 libraries 字段，在 front matter 结束前添加
    if not libraries_added:
        libraries = []
        if features["math"]:
            libraries.append("katex")
        if features["mermaid"]:
            libraries.append("mermaid")
        if features["chart"]:
            libraries.extend(["chart", "flowchartjs"])
        if libraries:
            # 找到第二个 --- 的位置
            for i, line in enumerate(processed_lines):
                if line.strip() == "---" and i > 0:
                    processed_lines.insert(i, f"libraries: {libraries}")
                    break

    result = "\n".join(processed_lines)

    # 打印智能建议
    print("\n📝 智能内容分析:")
    if features["math"]:
        print("  ✓ 检测到数学公式，已添加 katex 库")
    if features["mermaid"]:
        print("  ✓ 检测到 Mermaid 图表，已添加 mermaid 库")
    if features["chart"]:
        print("  ✓ 检测到图表内容，已添加 chart/flowchartjs 库")
    if final_category:
        print(f"  ✓ 建议分类: {final_category}")
    if all_tags:
        print(f"  ✓ 建议标签: {', '.join(all_tags)}")

    return result


def copy_cover_image(cover_path: str, target_dir: str, article_name: str) -> str:
    """复制封面图到目标目录"""
    if not cover_path or not Path(cover_path).exists():
        return ""

    cover_file = Path(cover_path)
    ext = cover_file.suffix
    target_filename = f"{article_name}-cover{ext}"
    target_path = Path(target_dir) / target_filename

    shutil.copy2(cover_file, target_path)
    print(f"✓ 封面图已复制到: {target_path}")

    return target_filename


def read_markdown_content(md_path: str) -> str:
    """读取 Markdown 文件内容"""
    md_file = Path(md_path)

    if not md_file.exists():
        print(f"错误: Markdown 文件不存在: {md_path}")
        sys.exit(1)

    with open(md_file, "r", encoding="utf-8") as f:
        return f.read()


def extract_content_without_frontmatter(content: str) -> str:
    """提取内容，去除原有的 front matter"""
    lines = content.split("\n")
    content_lines = []
    in_frontmatter = False
    frontmatter_started = False

    for line in lines:
        if line.strip() == "---":
            if not frontmatter_started:
                frontmatter_started = True
                in_frontmatter = True
                continue
            elif in_frontmatter:
                in_frontmatter = False
                continue
            else:
                content_lines.append(line)
                continue

        if not in_frontmatter:
            content_lines.append(line)

    return "\n".join(content_lines)


def display_shortcodes_guide():
    """显示 Shortcodes 使用指南"""
    print("\n" + "=" * 60)
    print("📚 Hugo Shortcodes 快速参考")
    print("=" * 60)
    print("""
盒子（支持 Markdown）:
  {{< boxmd >}}
  这是 **粗体** 文本
  {{< /boxmd >}}

彩色提示框:
  {{< alert theme="info" >}}**信息** 内容{{< /alert >}}
  {{< alert theme="warning" >}}**警告** 内容{{< /alert >}}
  {{< alert theme="success" >}}**成功** 内容{{< /alert >}}
  {{< alert theme="danger" >}}**危险** 内容{{< /alert >}}

可折叠内容:
  {{< expand "点击展开" >}}
  折叠的内容
  {{< /expand >}}

选项卡（多平台对比）:
  {{< tabs Windows MacOS Ubuntu >}}
    {{< tab >}}Windows 内容{{< /tab >}}
    {{< tab >}}MacOS 内容{{< /tab >}}
    {{< tab >}}Ubuntu 内容{{< /tab >}}
  {{< /tabs >}}

图片（带标题）:
  {{< img src="image.jpg" title="标题" caption="描述" >}}

按钮:
  {{< button href="https://example.com" >}}点击访问{{< /button >}}

封面图:
  {{< featuredImage >}}
    """)
    print("=" * 60)


def create_article(
    template_path: str,
    md_path: str,
    posts_dir: str,
    category: str,
    article_name: str,
    cover_path: str = None,
    draft: bool = False,
    custom_tags: list = None,
):
    """创建博客文章"""
    if category == "ROOT":
        category_dir = Path(posts_dir)
    else:
        category_dir = Path(posts_dir) / category
        if not category_dir.exists():
            print(f"创建新分类目录: {category}")
            category_dir.mkdir(parents=True, exist_ok=True)

    article_file = category_dir / f"{article_name}.md"

    if article_file.exists():
        print(f"警告: 文章已存在，将被覆盖: {article_file}")

    template = read_template(template_path)
    current_time = get_current_time()
    md_content = read_markdown_content(md_path)
    article_body = extract_content_without_frontmatter(md_content)

    cover_filename = ""
    if cover_path:
        cover_filename = copy_cover_image(cover_path, str(category_dir), article_name)

    processed_template = process_frontmatter(
        template,
        article_name,
        current_time,
        content=article_body,
        cover_filename=cover_filename,
        draft=draft,
        custom_tags=custom_tags,
        custom_category=category if category != "ROOT" else None,
    )

    final_content = processed_template + "\n\n" + article_body

    with open(article_file, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"\n✅ 文章已成功创建!")
    print(f"   位置: {article_file}")
    print(f"   标题: {article_name}")
    if category != "ROOT":
        print(f"   分类: {category}")
    if cover_filename:
        print(f"   封面: {cover_filename}")

    return str(article_file)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Hugo 博客文章发布工具 (优化版)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
环境变量配置:
  HUGO_BLOG_DIR          博客项目根目录（完整路径）
  HUGO_POSTS_DIR         posts 目录相对路径（默认: content/zh/posts）
  HUGO_DAILY_DIR         daily 目录相对路径（默认: content/zh/daily）
  HUGO_WEEKLY_DIR        weekly 目录相对路径（默认: content/zh/weekly）
  HUGO_TEMPLATE_PATH     模板文件相对路径（默认: archetypes/default.md）
  HUGO_DAILY_TEMPLATE    daily 模板路径（默认: archetypes/daily.md）
  HUGO_WEEKLY_TEMPLATE   weekly 模板路径（默认: archetypes/weekly.md）

优先级: 命令行参数 > 环境变量 > 默认值

智能功能:
  • 自动检测数学公式 ($...$) 并添加 katex 库
  • 自动检测 Mermaid 图表并添加 mermaid 库
  • 根据内容智能建议分类和标签
  • 支持 Shortcodes 语法提示

示例:
  # 设置环境变量（推荐在 ~/.zshrc 中配置）
  export HUGO_BLOG_DIR=/path/to/your/hugo/blog

  # 查看配置信息
  %(prog)s --check-config

  # 查看可用分类（posts 类型）
  %(prog)s --type posts --list-categories

  # 查看已有文章（daily/weekly 类型）
  %(prog)s --type daily --list

  # 发布到 posts（需指定分类）
  %(prog)s --md ./article.md --type posts --category 技术

  # 发布到 daily（直接放入目录）
  %(prog)s --md ./ai-news.md --type daily

  # 发布到 weekly（直接放入目录）
  %(prog)s --md ./weekly-log.md --type weekly

  # 发布文章并设置封面
  %(prog)s --md ./my-article.md --cover ./cover.png --type daily

  # 发布为草稿
  %(prog)s --md ./draft.md --type daily --draft
  
  # 查看 Shortcodes 使用指南
  %(prog)s --shortcodes
        """,
    )

    parser.add_argument(
        "--type",
        "-t",
        choices=["posts", "daily", "weekly"],
        default="posts",
        help="内容类型: posts(博客文章), daily(日报), weekly(周报). 默认: posts",
    )

    parser.add_argument(
        "--check-config", action="store_true", help="检查并显示当前配置信息"
    )

    parser.add_argument(
        "--list-categories",
        "-l",
        action="store_true",
        help="显示所有可用的分类目录（仅 posts 类型）",
    )

    parser.add_argument(
        "--list", action="store_true", help="显示所有现有的文章（仅 daily/weekly 类型）"
    )

    parser.add_argument("--md", "-m", help="Markdown 文件路径")

    parser.add_argument("--cover", "-c", help="封面图片路径")

    parser.add_argument(
        "--category", "-cat", help="博客分类目录名称（仅 posts 类型需要）"
    )

    parser.add_argument("--name", "-n", help="文章名称（默认使用 Markdown 文件名）")

    parser.add_argument("--draft", "-d", action="store_true", help="将文章标记为草稿")

    parser.add_argument(
        "--tags",
        help="自定义标签，多个标签用逗号分隔（例如：AI,Python,技术）",
    )

    parser.add_argument(
        "--shortcodes", action="store_true", help="显示 Shortcodes 使用指南"
    )

    parser.add_argument(
        "--blog-dir",
        help="Hugo 博客项目根目录（完整路径），优先级高于环境变量 HUGO_BLOG_DIR",
    )

    parser.add_argument(
        "--posts-dir",
        help="目标目录路径（支持相对路径，相对于 blog_dir；或绝对路径），优先级高于环境变量",
    )

    parser.add_argument(
        "--template",
        help="模板文件路径（支持相对路径，相对于 blog_dir；或绝对路径），优先级高于环境变量",
    )

    args = parser.parse_args()

    # 显示 Shortcodes 指南
    if args.shortcodes:
        display_shortcodes_guide()
        sys.exit(0)

    content_type = args.type

    blog_dir, target_dir, template_path, sources = resolve_paths(args, content_type)

    if args.check_config:
        display_config(blog_dir, target_dir, template_path, sources, content_type)
        sys.exit(0)

    # posts 类型需要获取分类
    if content_type == "posts":
        categories = get_target_categories(target_dir)

        if args.list_categories:
            display_categories(categories, content_type)
            sys.exit(0)

        if not args.md:
            print("错误: 必须指定 Markdown 文件路径 (--md)")
            parser.print_help()
            sys.exit(1)

        if not args.category:
            print("错误: posts 类型必须指定分类目录 (--category)")
            display_categories(categories, content_type)
            sys.exit(1)

        if not validate_category(args.category, categories):
            print(f"错误: 分类 '{args.category}' 不存在")
            display_categories(categories, content_type)
            sys.exit(1)

        category = args.category
    else:
        # daily/weekly 类型直接列出现有文件
        if args.list_categories:
            print(f"提示: {content_type} 类型没有分类，使用 --list 查看现有文章")
            sys.exit(0)

        if args.list:
            files = get_target_files(target_dir)
            display_files(files, content_type)
            sys.exit(0)

        if not args.md:
            print("错误: 必须指定 Markdown 文件路径 (--md)")
            parser.print_help()
            sys.exit(1)

        # daily/weekly 不需要 category，使用 ROOT 表示直接放入目标目录
        category = "ROOT"

    if args.name:
        article_name = sanitize_filename(args.name)
    else:
        md_file = Path(args.md)
        article_name = sanitize_filename(md_file.stem)

    # 解析自定义标签
    custom_tags = None
    if args.tags:
        custom_tags = [tag.strip() for tag in args.tags.split(",")]

    create_article(
        template_path=template_path,
        md_path=args.md,
        posts_dir=target_dir,
        category=category,
        article_name=article_name,
        cover_path=args.cover,
        draft=args.draft,
        custom_tags=custom_tags,
    )

    # 显示 Shortcodes 提示
    print("\n💡 提示: 使用 --shortcodes 查看 Shortcodes 语法指南")


if __name__ == "__main__":
    main()
