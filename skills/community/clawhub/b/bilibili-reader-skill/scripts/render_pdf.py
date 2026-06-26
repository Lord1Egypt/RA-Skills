#!/usr/bin/env python3
"""接收 summary JSON，渲染 PDF 并记录到记忆系统

用法:
  python scripts/render_pdf.py summary.json

输入: JSON 文件路径
输出: PDF 文件路径到 stdout
"""

import sys
import json
from pathlib import Path

skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))

from src.config import Config
from src.summarizer import VideoSummary, MyAnalysis, VideoTranscript, ConceptBlock, OperationStep, ThinkingQuestion, TranscriptSegment
from src.pdf_generator import generate_pdf
from src.memory import Memory
from src.progress import calculate_progress, render_mini_progress


def _parse_nested(data: dict):
    """将嵌套的 JSON dict 转为 dataclass"""
    # my_analysis
    ma_data = data.get("my_analysis") or {}
    my_analysis = MyAnalysis(
        overview=ma_data.get("overview", ""),
        concepts=[
            ConceptBlock(
                name=c.get("name", ""),
                definition=c.get("definition", ""),
                principle=c.get("principle", ""),
                analogy=c.get("analogy", {}) or {},
                insight=c.get("insight", ""),
                layer=c.get("layer", ""),
            )
            for c in ma_data.get("concepts", [])
        ],
        operations=[
            OperationStep(
                step=o.get("step", ""),
                description=o.get("description", ""),
                expected_result=o.get("expected_result", ""),
                pitfall=o.get("pitfall", ""),
            )
            for o in ma_data.get("operations", [])
        ],
        thinking_questions=[
            ThinkingQuestion(question=q.get("question", ""), hint=q.get("hint", ""))
            for q in ma_data.get("thinking_questions", [])
        ],
    )

    # video_transcript
    vt_data = data.get("video_transcript") or {}
    video_transcript = VideoTranscript(
        outline=vt_data.get("outline", ""),
        segments=[
            TranscriptSegment(
                time_range=s.get("time_range", ""),
                title=s.get("title", ""),
                content=s.get("content", ""),
            )
            for s in vt_data.get("segments", [])
        ],
        up_main_insights=vt_data.get("up_main_insights", ""),
        up_main_credibility=vt_data.get("up_main_credibility", ""),
    )

    return my_analysis, video_transcript


def main():
    if len(sys.argv) < 2:
        print("用法: python render_pdf.py <summary.json>", file=sys.stderr)
        sys.exit(1)

    # 读取 JSON
    arg = sys.argv[1]
    path = Path(arg)
    if not path.exists():
        print(f"错误: 文件不存在 {arg}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误: JSON 解析失败 {e}", file=sys.stderr)
        sys.exit(1)

    my_analysis, video_transcript = _parse_nested(data)

    # 兼容处理：top_comments 中的 content → content_cn
    # 确保与 PDF 模板中的 comment.content_cn 一致
    raw_comments = data.get("top_comments", [])
    processed_comments = []
    for c in raw_comments:
        if isinstance(c, dict):
            # 如果有 content 但没有 content_cn，补充 content_cn
            if "content" in c and "content_cn" not in c:
                c = dict(c)  # 不修改原数据
                c["content_cn"] = c["content"]
            processed_comments.append(c)
        else:
            processed_comments.append(c)
    data["top_comments"] = processed_comments

    # 构建 VideoSummary（包含 v2.0 字段）
    summary = VideoSummary(
        title_cn=data.get("title_cn", ""),
        title_en=data.get("title_en", ""),
        tldr_cn=data.get("tldr_cn", ""),
        tldr_en=data.get("tldr_en", ""),
        summary_cn=data.get("summary_cn", ""),
        summary_en=data.get("summary_en", ""),
        key_points_cn=data.get("key_points_cn", []),
        key_points_en=data.get("key_points_en", []),
        tool_stack=data.get("tool_stack", []),
        code_snippets=data.get("code_snippets", []),
        pitfalls_cn=data.get("pitfalls_cn", []),
        pitfalls_en=data.get("pitfalls_en", []),
        insights_cn=data.get("insights_cn", ""),
        insights_en=data.get("insights_en", ""),
        top_comments=data.get("top_comments", []),
        recommendation_cn=data.get("recommendation_cn", ""),
        recommendation_en=data.get("recommendation_en", ""),
        prerequisites_cn=data.get("prerequisites_cn", ""),
        prerequisites_en=data.get("prerequisites_en", ""),
        difficulty_cn=data.get("difficulty_cn", ""),
        difficulty_en=data.get("difficulty_en", ""),
        next_steps_cn=data.get("next_steps_cn", ""),
        next_steps_en=data.get("next_steps_en", ""),
        key_misconceptions_cn=data.get("key_misconceptions_cn", ""),
        key_misconceptions_en=data.get("key_misconceptions_en", ""),
        expected_outcome_cn=data.get("expected_outcome_cn", ""),
        expected_outcome_en=data.get("expected_outcome_en", ""),
        exam_format_cn=data.get("exam_format_cn", ""),
        exam_format_en=data.get("exam_format_en", ""),
        vocabulary_list=data.get("vocabulary_list", []),
        data_sources_cn=data.get("data_sources_cn", ""),
        data_sources_en=data.get("data_sources_en", ""),
        practice_template_cn=data.get("practice_template_cn", ""),
        practice_template_en=data.get("practice_template_en", ""),
        scripts_templates=data.get("scripts_templates", []),
        reference_works_cn=data.get("reference_works_cn", ""),
        reference_works_en=data.get("reference_works_en", ""),
        key_quotes=data.get("key_quotes", []),
        materials_list=data.get("materials_list", []),
        related_topics_cn=data.get("related_topics_cn", ""),
        related_topics_en=data.get("related_topics_en", ""),
        owner=data.get("owner", ""),
        duration_str=data.get("duration_str", ""),
        view_count=data.get("view_count", 0),
        like_count=data.get("like_count", 0),
        genre=data.get("genre", ""),
        genre_list=data.get("genre_list", []),
        my_analysis=my_analysis,
        video_transcript=video_transcript,
        quizzes=data.get("quizzes", []),
    )

    Config.ensure_dirs()

    # 记忆系统
    bvid = data.get("bvid", "")
    memory = Memory(Config.DATA_DIR / "processed.json")
    folder_name = data.get("folder_name", "")
    folder_total = data.get("folder_total", 0)

    # 生成 PDF
    progress_stats = calculate_progress(memory, total_in_folder=folder_total)
    progress_text = render_mini_progress(progress_stats)
    pdf_path = generate_pdf(summary, Config.OUTPUT_DIR, bvid=bvid, progress_text=progress_text)

    # 记录已处理
    if bvid:
        memory.mark_processed(bvid, summary.title_cn, summary=summary)

    # 输出 PDF 路径
    print(str(pdf_path))


if __name__ == "__main__":
    main()
