"""AgentScout 主流程 - 搜索→选择→分析→生成"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

from src.config import load_config, AppConfig
from src.storage.database import Database
from src.storage.models import Post
from src.utils.llm_client import LLMClient
from src.discover.github_searcher import GitHubSearcher
from src.discover.scorer import ProjectScorer
from src.discover.ranking import RankingManager
from src.analyze.project_analyzer import ProjectAnalyzer
from src.content.copywriter import Copywriter
from src.visual.composer import CardComposer
from src.visual.code_card import CodeCardGenerator
from src.visual.screenshot import ScreenshotCapture
from src.visual.ai_image import AIImageGenerator


def run_scout_pipeline(config: AppConfig = None):
    """完整流水线（同步入口）"""
    if config is None:
        config = load_config()

    # 初始化
    db = Database(config.db_path)
    db.init()
    llm = LLMClient(config.llm)
    ranking = RankingManager(db, config.topk_size)

    print("=" * 60)
    print("🔍 AgentScout - GitHub Agent 项目发现与内容生成")
    print("=" * 60)

    # ── 阶段 1: 搜索 + 评分 ──
    print("\n📡 阶段 1: 搜索 GitHub 项目...")
    searcher = GitHubSearcher(config.github, db)
    candidates = searcher.search()

    if candidates:
        print(f"  发现 {len(candidates)} 个新项目，开始评分...")
        scorer = ProjectScorer(config, llm, db)
        scorer.score_batch(candidates)
    else:
        print("  未发现新项目（可能已全部入库）")

    # ── 阶段 2: 展示 Top N，等待用户选择 ──
    print(f"\n🏆 阶段 2: 展示 Top {config.present_top_n} 项目")
    entries = ranking.present_top_n(config.present_top_n)
    if not entries:
        print("❌ 没有可展示的项目，请检查搜索配置或 API Token")
        return None

    selected = ranking.select_project(entries)
    project = selected.project

    # ── 阶段 3: 深度分析 ──
    print("\n📖 阶段 3: 深度分析项目...")
    analyzer = ProjectAnalyzer(config.github, llm)
    analysis = analyzer.analyze(project)

    # ── 阶段 4: 内容生成 ──
    print("\n✍️  阶段 4: 生成小红书文案...")
    writer = Copywriter(llm)
    post_content = writer.generate(analysis, project)

    # ── 阶段 5: 配图生成 ──
    print("\n🎨 阶段 5: 生成配图...")
    output_dir = _prepare_output_dir(config.output_dir, project.name)
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    _generate_images_sync(config, project, analysis, output_dir)

    # ── 阶段 6: 整理产出 ──
    print("\n📦 阶段 6: 整理产出...")
    # 保存 analysis.md
    analysis_path = output_dir / "analysis.md"
    analysis_path.write_text(analysis.full_markdown, encoding="utf-8")

    # 保存 post.md
    post_path = output_dir / "post.md"
    post_path.write_text(post_content.full_text, encoding="utf-8")

    # 保存 metadata.json
    metadata = {
        "project": {
            "name": project.name,
            "repo_full_name": project.repo_full_name,
            "repo_url": project.repo_url,
            "stars": project.stars,
            "language": project.language,
            "description": project.description,
        },
        "score": {
            "total": selected.score.total_score,
            "novelty": selected.score.novelty,
            "practicality": selected.score.practicality,
            "content_fit": selected.score.content_fit,
            "ease_of_use": selected.score.ease_of_use,
            "reason": selected.score.scoring_reason,
        },
        "generated_at": datetime.now().isoformat(),
        "tags": post_content.tags,
    }
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 记录到 DB
    post_record = Post(
        project_id=project.id,
        analysis_path=str(analysis_path),
        post_path=str(post_path),
        images_dir=str(images_dir),
        status="ready",
    )
    db.insert_post(post_record)

    # 保存排行榜快照
    ranking.save_snapshot()

    print("\n" + "=" * 60)
    print(f"✅ 完成！产出目录: {output_dir}")
    print(f"   📄 analysis.md  - 项目分析教程")
    print(f"   📝 post.md      - 小红书文案")
    print(f"   🖼️  images/      - 配图")
    print(f"   📊 metadata.json - 元数据")
    print("=" * 60)

    return str(output_dir)


def _prepare_output_dir(base_dir: str, project_name: str) -> Path:
    """创建产出目录"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_name = project_name.replace("/", "_").replace(" ", "_")
    output_dir = Path(base_dir) / f"{date_str}_{safe_name}"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def _generate_images_sync(config, project, analysis, output_dir):
    """同步方式生成配图"""
    images_dir = output_dir / "images"
    composer = CardComposer()
    code_gen = CodeCardGenerator()

    # P1: 封面图
    try:
        print("  🖼️  P1: 封面图...")
        composer.create_cover(
            project_name=project.name,
            description=project.description[:80],
            stars=project.stars,
            highlight="",
            output_path=str(images_dir / "P1_cover.png"),
            template_name="cover_tech_blue.html",
        )
    except Exception as e:
        print(f"  ⚠ P1 封面图失败: {e}")

    # P2: 终端风格封面
    try:
        print("  🖼️  P2: 终端风格封面...")
        composer.create_cover(
            project_name=project.name,
            description=project.description[:80],
            stars=project.stars,
            highlight="",
            output_path=str(images_dir / "P2_terminal.png"),
            template_name="cover_terminal_dark.html",
        )
    except Exception as e:
        print(f"  ⚠ P2 失败: {e}")

    # P3: 架构卡片
    try:
        print("  🖼️  P3: 架构卡片...")
        # 从分析中提取架构部分
        arch_text = _extract_section(analysis.full_markdown, "怎么做") or project.description
        composer.create_architecture_card(
            architecture_text=arch_text[:500],
            output_path=str(images_dir / "P3_architecture.png"),
            project_name=project.name,
        )
    except Exception as e:
        print(f"  ⚠ P3 失败: {e}")

    # P4-P5: 代码卡片
    try:
        print("  🖼️  P4-P5: 代码卡片...")
        code_sections = _extract_code_blocks(analysis.full_markdown)
        for i, (filename, code) in enumerate(code_sections[:2]):
            code_gen.generate_image(
                code=code[:600],
                output_path=str(images_dir / f"P{4+i}_code.png"),
                filename=filename,
                label=project.name,
            )
    except Exception as e:
        print(f"  ⚠ P4-P5 失败: {e}")

    # P6-P7: 步骤卡片
    try:
        print("  🖼️  P6-P7: 步骤卡片...")
        steps = _extract_steps(analysis.full_markdown)
        if steps:
            mid = len(steps) // 2
            for i, step_group in enumerate([steps[:mid] or steps, steps[mid:] or steps]):
                if step_group:
                    composer.create_step_card(
                        steps=step_group[:4],
                        output_path=str(images_dir / f"P{6+i}_steps.png"),
                        card_title="快速上手" if i == 0 else "进阶使用",
                    )
    except Exception as e:
        print(f"  ⚠ P6-P7 失败: {e}")

    # P9: 总结卡片
    try:
        print("  🖼️  P9: 总结卡片...")
        summary = _extract_section(analysis.full_markdown, "有意思") or project.description
        composer.create_summary_card(
            summary=summary[:200],
            project_name=project.name,
            repo_url=project.repo_url,
            output_path=str(images_dir / "P9_summary.png"),
        )
    except Exception as e:
        print(f"  ⚠ P9 失败: {e}")

    # AI 概念图（可选）
    ai_gen = AIImageGenerator(config.image)
    if ai_gen.enabled:
        try:
            print("  🖼️  P8: AI 概念图...")
            ai_gen.generate_concept(
                description=project.description,
                output_path=str(images_dir / "P8_concept.png"),
            )
        except Exception as e:
            print(f"  ⚠ P8 AI 概念图失败: {e}")

    # GitHub 截图（可选）
    try:
        print("  🖼️  GitHub 截图...")
        screenshot = ScreenshotCapture()
        asyncio.get_event_loop().run_until_complete(
            screenshot.capture_github_page(
                project.repo_url,
                str(images_dir / "github_screenshot.png"),
            )
        )
        asyncio.get_event_loop().run_until_complete(screenshot.close())
    except Exception as e:
        print(f"  ⚠ GitHub 截图失败（需要 playwright install）: {e}")


def _extract_section(markdown: str, keyword: str) -> str:
    """从 markdown 中提取包含关键词的段落"""
    lines = markdown.split("\n")
    capture = False
    result = []
    for line in lines:
        if keyword in line and line.startswith("#"):
            capture = True
            continue
        if capture:
            if line.startswith("#"):
                break
            result.append(line)
    return "\n".join(result).strip()


def _extract_code_blocks(markdown: str) -> list[tuple[str, str]]:
    """提取 markdown 中的代码块"""
    import re
    blocks = []
    pattern = re.compile(r"```(\w*)\n(.*?)```", re.DOTALL)
    for match in pattern.finditer(markdown):
        lang = match.group(1) or "code"
        code = match.group(2).strip()
        blocks.append((f"example.{lang}", code))
    return blocks


def _extract_steps(markdown: str) -> list[dict]:
    """提取步骤列表"""
    import re
    steps = []
    # 匹配编号列表
    pattern = re.compile(r"(\d+)\.\s+(.*)")
    lines = markdown.split("\n")
    for line in lines:
        m = pattern.match(line.strip())
        if m:
            steps.append({
                "title": f"步骤 {m.group(1)}",
                "description": m.group(2),
                "code": "",
            })
    # 如果没找到编号列表，尝试从 bash 代码块提取
    if not steps:
        code_blocks = _extract_code_blocks(markdown)
        for i, (_, code) in enumerate(code_blocks[:6]):
            for cmd_line in code.split("\n"):
                cmd_line = cmd_line.strip()
                if cmd_line and not cmd_line.startswith("#"):
                    steps.append({
                        "title": f"步骤 {len(steps) + 1}",
                        "description": "",
                        "code": cmd_line,
                    })
                    break
    return steps


def main():
    """CLI 入口"""
    import sys
    config = load_config()

    if not config.github.token:
        print("⚠️  未设置 GITHUB_TOKEN，搜索可能受限。")
        print("   请在 .env 文件中设置: GITHUB_TOKEN=ghp_xxx\n")

    if not config.llm.api_key:
        print("❌ 未设置 LLM_API_KEY，无法进行评分和内容生成。")
        print("   请在 .env 文件中设置: LLM_API_KEY=sk-xxx")
        sys.exit(1)

    run_scout_pipeline(config)


if __name__ == "__main__":
    main()
