"""PDF生成模块 — Jinja2模板渲染 + weasyprint转PDF"""

from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from .summarizer import VideoSummary


def generate_pdf(summary: VideoSummary, output_dir: Path, bvid: str = "", progress_text: str = "") -> Path:
    """生成PDF文件

    Args:
        summary: 视频总结数据
        output_dir: 输出目录
        bvid: 视频BV号（用于文件名）
        progress_text: 进度展示文本（可选）

    Returns:
        生成的PDF文件路径
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # 模板目录
    template_dir = Path(__file__).parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template("summary.html")

    # ── v2.0 新增字段（dataclass → dict）──
    my_analysis_dict = summary.my_analysis.to_dict() if hasattr(summary.my_analysis, "to_dict") else {}
    video_transcript_dict = summary.video_transcript.to_dict() if hasattr(summary.video_transcript, "to_dict") else {}

    html_content = template.render(
        title_cn=summary.title_cn,
        title_en=summary.title_en,
        owner=summary.owner,
        duration_str=summary.duration_str,
        view_count=summary.view_count,
        like_count=summary.like_count,
        genre=summary.genre,
        tldr_cn=summary.tldr_cn,
        tldr_en=summary.tldr_en,
        # ── 原有字段 ──
        summary_cn=summary.summary_cn,
        summary_en=summary.summary_en,
        key_points_cn=summary.key_points_cn,
        key_points_en=summary.key_points_en,
        insights_cn=summary.insights_cn,
        insights_en=summary.insights_en,
        tool_stack=summary.tool_stack,
        code_snippets=summary.code_snippets,
        pitfalls_cn=summary.pitfalls_cn,
        pitfalls_en=summary.pitfalls_en,
        top_comments=summary.top_comments,
        recommendation_cn=summary.recommendation_cn,
        recommendation_en=summary.recommendation_en,
        # 通用学习导向字段
        prerequisites_cn=summary.prerequisites_cn,
        prerequisites_en=summary.prerequisites_en,
        difficulty_cn=summary.difficulty_cn,
        difficulty_en=summary.difficulty_en,
        next_steps_cn=summary.next_steps_cn,
        next_steps_en=summary.next_steps_en,
        key_misconceptions_cn=summary.key_misconceptions_cn,
        key_misconceptions_en=summary.key_misconceptions_en,
        # 体裁专用字段
        expected_outcome_cn=summary.expected_outcome_cn,
        exam_format_cn=summary.exam_format_cn,
        vocabulary_list=summary.vocabulary_list,
        data_sources_cn=summary.data_sources_cn,
        practice_template_cn=summary.practice_template_cn,
        scripts_templates=summary.scripts_templates,
        reference_works_cn=summary.reference_works_cn,
        key_quotes=summary.key_quotes,
        materials_list=summary.materials_list,
        related_topics_cn=summary.related_topics_cn,
        # ── v2.0 新增字段 ──
        my_analysis=my_analysis_dict,
        video_transcript=video_transcript_dict,
        quizzes=summary.quizzes if hasattr(summary, "quizzes") else [],
        thinking_questions=summary.thinking_questions if hasattr(summary, "thinking_questions") else [],
        progress_text=progress_text,
    )

    # 生成PDF
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = _sanitize_filename(summary.title_cn[:30])
    filename = f"{timestamp}_{safe_title}.pdf"
    if bvid:
        filename = f"{timestamp}_{bvid}_{safe_title}.pdf"
    pdf_path = output_dir / filename

    from weasyprint import HTML
    HTML(string=html_content).write_pdf(str(pdf_path))

    return pdf_path


def _sanitize_filename(name: str) -> str:
    """清理文件名中的非法字符"""
    import re
    # 替换非法字符
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    # 去除首尾空白
    name = name.strip()
    # 限制长度
    if len(name) > 50:
        name = name[:50]
    return name or "untitled"
