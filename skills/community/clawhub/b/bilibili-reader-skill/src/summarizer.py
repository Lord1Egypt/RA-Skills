"""LLM总结模块 — 统一基座提示词 + v2.0 字段 + 多体裁合并"""

import json
import random
from dataclasses import dataclass, field
from .bilibili_api import VideoInfo, Comment, Danmaku
from .intent_router import (
    VideoGenre, GenreResult, GENRE_DISPLAY,
    classify_genre, classify_genre_multi,
    build_prompt, get_prompts_for_genres,
)


@dataclass
class ConceptBlock:
    """单个核心概念"""
    name: str = ""
    definition: str = ""
    principle: str = ""
    analogy: dict = field(default_factory=dict)  # {scenario, mapping, limitation}
    insight: str = ""
    layer: str = ""  # "concept" | "operation"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "definition": self.definition,
            "principle": self.principle,
            "analogy": self.analogy,
            "insight": self.insight,
            "layer": self.layer,
        }


@dataclass
class OperationStep:
    """操作步骤"""
    step: str = ""
    description: str = ""
    expected_result: str = ""
    pitfall: str = ""

    def to_dict(self) -> dict:
        return {
            "step": self.step,
            "description": self.description,
            "expected_result": self.expected_result,
            "pitfall": self.pitfall,
        }


@dataclass
class ThinkingQuestion:
    """思考题"""
    question: str = ""
    hint: str = ""

    def to_dict(self) -> dict:
        return {"question": self.question, "hint": self.hint}


@dataclass
class MyAnalysis:
    """★ v2.0 我的解读"""
    overview: str = ""
    concepts: list = field(default_factory=list)  # list[ConceptBlock]
    operations: list = field(default_factory=list)  # list[OperationStep]
    thinking_questions: list = field(default_factory=list)  # list[ThinkingQuestion]

    def to_dict(self) -> dict:
        return {
            "overview": self.overview,
            "concepts": [
                c.to_dict() if hasattr(c, "to_dict") else c for c in self.concepts
            ],
            "operations": [
                o.to_dict() if hasattr(o, "to_dict") else o for o in self.operations
            ],
            "thinking_questions": [
                q.to_dict() if hasattr(q, "to_dict") else q
                for q in self.thinking_questions
            ],
        }


@dataclass
class TranscriptSegment:
    """视频陈述段落"""
    time_range: str = ""
    title: str = ""
    content: str = ""

    def to_dict(self) -> dict:
        return {
            "time_range": self.time_range,
            "title": self.title,
            "content": self.content,
        }


@dataclass
class VideoTranscript:
    """★ v2.0 视频完整陈述"""
    outline: str = ""
    segments: list = field(default_factory=list)  # list[TranscriptSegment]
    up_main_insights: str = ""
    up_main_credibility: str = ""

    def to_dict(self) -> dict:
        return {
            "outline": self.outline,
            "segments": [
                s.to_dict() if hasattr(s, "to_dict") else s
                for s in self.segments
            ],
            "up_main_insights": self.up_main_insights,
            "up_main_credibility": self.up_main_credibility,
        }


@dataclass
class Quiz:
    """理解度测验"""
    question_cn: str = ""
    options_cn: list = field(default_factory=list)
    answer: str = ""
    source: str = ""
    difficulty: str = "medium"
    type: str = "choice"

    def to_dict(self) -> dict:
        return {
            "question_cn": self.question_cn,
            "options_cn": self.options_cn,
            "answer": self.answer,
            "source": self.source,
            "difficulty": self.difficulty,
            "type": self.type,
        }


@dataclass
class VideoSummary:
    """视频总结数据结构（v2.0 扩展版）"""
    # 基本信息
    title_cn: str = ""
    title_en: str = ""
    owner: str = ""
    duration_str: str = ""
    view_count: int = 0
    like_count: int = 0
    # 体裁
    genre: str = ""
    genre_list: list[str] = field(default_factory=list)  # ★ 多体裁记录
    # ★ v2.0 新增：双视角结构
    my_analysis: MyAnalysis = field(default_factory=MyAnalysis)
    video_transcript: VideoTranscript = field(default_factory=VideoTranscript)
    # 核心内容
    tldr_cn: str = ""
    tldr_en: str = ""
    summary_cn: str = ""
    summary_en: str = ""
    key_points_cn: list[str] = field(default_factory=list)
    key_points_en: list[str] = field(default_factory=list)
    # 技术教程专用字段
    tool_stack: list[dict] = field(default_factory=list)
    code_snippets: list[dict] = field(default_factory=list)
    pitfalls_cn: list[str] = field(default_factory=list)
    pitfalls_en: list[str] = field(default_factory=list)
    # 洞察
    insights_cn: str = ""
    insights_en: str = ""
    # 评论
    top_comments: list[dict] = field(default_factory=list)
    # 推荐
    recommendation_cn: str = ""
    recommendation_en: str = ""
    # 通用学习导向字段
    prerequisites_cn: str = ""
    prerequisites_en: str = ""
    difficulty_cn: str = ""
    difficulty_en: str = ""
    next_steps_cn: str = ""
    next_steps_en: str = ""
    key_misconceptions_cn: str = ""
    key_misconceptions_en: str = ""
    # 体裁专用字段
    expected_outcome_cn: str = ""
    expected_outcome_en: str = ""
    exam_format_cn: str = ""
    exam_format_en: str = ""
    vocabulary_list: list = field(default_factory=list)
    data_sources_cn: str = ""
    data_sources_en: str = ""
    practice_template_cn: str = ""
    practice_template_en: str = ""
    scripts_templates: list = field(default_factory=list)
    reference_works_cn: str = ""
    reference_works_en: str = ""
    key_quotes: list = field(default_factory=list)
    materials_list: list = field(default_factory=list)
    related_topics_cn: str = ""
    related_topics_en: str = ""
    # ★ v2.0 新增：测验题
    quizzes: list = field(default_factory=list)
    thinking_questions: list = field(default_factory=list)

    def to_dict(self) -> dict:
        """序列化时将 dataclass 转为 dict"""
        d = {}
        for k, v in self.__dict__.items():
            if hasattr(v, "to_dict"):
                d[k] = v.to_dict()
            elif isinstance(v, list):
                d[k] = [
                    i.to_dict() if hasattr(i, "to_dict") else i for i in v
                ]
            else:
                d[k] = v
        return d


def format_duration(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def format_count(count: int) -> str:
    if count >= 10000:
        return f"{count / 10000:.1f}万"
    return str(count)


# ──────────────────────────────────────────────
# 字幕随机抽样 + 概括
def summarize_subtitles_with_chunking(subtitles: list[dict], duration_sec: int, llm_caller=None) -> str:
    """随机抽取最多100条字幕进行概括，不足100则全部使用，无字幕则返回空字符串"""
    if not subtitles:
        return ""
    sampled = random.sample(subtitles, min(100, len(subtitles)))
    text = "\n".join(s.get("content", "") for s in sampled)
    if not llm_caller:
        return text
    prompt = f"""请用中文概括以下B站视频字幕片段的核心内容（已从原字幕中随机抽取{max(1, len(sampled))}条）。
要求：提炼关键信息，保留技术术语、操作步骤、关键结论，控制在200-400字。

字幕内容：
{text}"""
    return llm_caller(prompt)


# ──────────────────────────────────────────────
# 内部工具函数
# ──────────────────────────────────────────────

def _parse_response(response_text: str) -> VideoSummary:
    """解析 LLM 返回的 JSON"""
    text = response_text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    data = json.loads(text)
    return _dict_to_summary(data)


def _dict_to_summary(data: dict) -> VideoSummary:
    """将 JSON dict 转换为 VideoSummary dataclass"""
    my_analysis_data = data.get("my_analysis", {}) or {}
    my_analysis = MyAnalysis(
        overview=my_analysis_data.get("overview", ""),
        concepts=_parse_concepts(my_analysis_data.get("concepts", [])),
        operations=_parse_operations(my_analysis_data.get("operations", [])),
        thinking_questions=_parse_thinking_questions(
            my_analysis_data.get("thinking_questions", [])
        ),
    )

    transcript_data = data.get("video_transcript", {}) or {}
    video_transcript = VideoTranscript(
        outline=transcript_data.get("outline", ""),
        segments=_parse_segments(transcript_data.get("segments", [])),
        up_main_insights=transcript_data.get("up_main_insights", ""),
        up_main_credibility=transcript_data.get("up_main_credibility", ""),
    )

    return VideoSummary(
        title_cn=data.get("title_cn", ""),
        title_en=data.get("title_en", ""),
        tldr_cn=data.get("tldr_cn", ""),
        tldr_en=data.get("tldr_en", ""),
        summary_cn=data.get("summary_cn", ""),
        summary_en=data.get("summary_en", ""),
        key_points_cn=data.get("key_points_cn", []),
        key_points_en=data.get("key_points_en", []),
        my_analysis=my_analysis,
        video_transcript=video_transcript,
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
        quizzes=_parse_quizzes(data.get("quizzes", [])),
        thinking_questions=my_analysis.thinking_questions,
    )


def _parse_concepts(data: list) -> list[ConceptBlock]:
    """解析 concepts 数组"""
    result = []
    for c in data:
        analogy = c.get("analogy", {}) or {}
        if isinstance(analogy, list):
            analogy = analogy[0] if analogy else {}
        result.append(ConceptBlock(
            name=c.get("name", ""),
            definition=c.get("definition", ""),
            principle=c.get("principle", ""),
            analogy={
                "scenario": analogy.get("scenario", ""),
                "mapping": analogy.get("mapping", ""),
                "limitation": analogy.get("limitation", ""),
            },
            insight=c.get("insight", ""),
            layer=c.get("layer", ""),
        ))
    return result


def _parse_operations(data: list) -> list[OperationStep]:
    """解析 operations 数组"""
    return [
        OperationStep(
            step=o.get("step", ""),
            description=o.get("description", ""),
            expected_result=o.get("expected_result", ""),
            pitfall=o.get("pitfall", ""),
        )
        for o in data
    ]


def _parse_thinking_questions(data: list) -> list[ThinkingQuestion]:
    """解析 thinking_questions 数组"""
    return [
        ThinkingQuestion(
            question=q.get("question", ""),
            hint=q.get("hint", ""),
        )
        for q in data
    ]


def _parse_segments(data: list) -> list[TranscriptSegment]:
    """解析 video_transcript.segments 数组"""
    return [
        TranscriptSegment(
            time_range=s.get("time_range", ""),
            title=s.get("title", ""),
            content=s.get("content", ""),
        )
        for s in data
    ]


def _parse_quizzes(data: list) -> list[Quiz]:
    """解析 quizzes 数组"""
    return [
        Quiz(
            question_cn=q.get("question_cn", ""),
            options_cn=q.get("options_cn", []),
            answer=q.get("answer", ""),
            source=q.get("source", ""),
            difficulty=q.get("difficulty", "medium"),
            type=q.get("type", "choice"),
        )
        for q in data
    ]


# ──────────────────────────────────────────────
# 多体裁合并
# ──────────────────────────────────────────────

def _merge_genre_fields(
    main: VideoSummary, secondary: VideoSummary, genre: VideoGenre
) -> VideoSummary:
    """将次级体裁的体裁专用字段合并到主 summary"""
    genre_key = genre.value

    if genre == VideoGenre.TECH_TUTORIAL:
        if secondary.tool_stack and not main.tool_stack:
            main.tool_stack = secondary.tool_stack
        if secondary.code_snippets and not main.code_snippets:
            main.code_snippets = secondary.code_snippets
        if secondary.expected_outcome_cn and not main.expected_outcome_cn:
            main.expected_outcome_cn = secondary.expected_outcome_cn
        if secondary.pitfalls_cn and not main.pitfalls_cn:
            main.pitfalls_cn = secondary.pitfalls_cn

    elif genre == VideoGenre.LANGUAGE:
        if secondary.vocabulary_list and not main.vocabulary_list:
            main.vocabulary_list = secondary.vocabulary_list

    elif genre == VideoGenre.ACADEMIC:
        if secondary.exam_format_cn and not main.exam_format_cn:
            main.exam_format_cn = secondary.exam_format_cn

    elif genre == VideoGenre.DEEP_DIVE:
        if secondary.data_sources_cn and not main.data_sources_cn:
            main.data_sources_cn = secondary.data_sources_cn

    elif genre == VideoGenre.METHODOLOGY:
        if secondary.practice_template_cn and not main.practice_template_cn:
            main.practice_template_cn = secondary.practice_template_cn

    elif genre == VideoGenre.CAREER:
        if secondary.scripts_templates and not main.scripts_templates:
            main.scripts_templates = secondary.scripts_templates

    elif genre == VideoGenre.CREATIVE:
        if secondary.reference_works_cn and not main.reference_works_cn:
            main.reference_works_cn = secondary.reference_works_cn

    elif genre == VideoGenre.BOOK:
        if secondary.key_quotes and not main.key_quotes:
            main.key_quotes = secondary.key_quotes

    elif genre == VideoGenre.LIFE_SKILL:
        if secondary.materials_list and not main.materials_list:
            main.materials_list = secondary.materials_list

    return main


# ──────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────

def generate_summary(
    video: VideoInfo,
    subtitles: list[dict],
    comments: list[Comment],
    danmakus: list[Danmaku],
    llm_caller=None,
) -> VideoSummary:
    """
    生成视频总结（兼容旧接口：单分类）
    """
    genres = classify_genre_multi(
        video.title, video.desc,
        "\n".join(s.get("content", "") for s in subtitles[:200]) if subtitles else "",
        llm_caller,
    )
    return generate_summary_multi(
        video=video,
        subtitles=subtitles,
        comments=comments,
        danmakus=danmakus,
        genres=genres,
        llm_caller=llm_caller,
    )


def generate_summary_multi(
    video: VideoInfo,
    subtitles: list[dict],
    comments: list[Comment],
    danmakus: list[Danmaku],
    genres: list[GenreResult],
    llm_caller=None,
) -> VideoSummary:
    """生成视频总结（多体裁模式）"""

    # 超长视频警告
    if video.duration > 3600:
        print(f"⚠ 警告: 视频时长 {format_duration(video.duration)}，处理时间可能较长")

    # 1. 概括字幕
    print("  概括字幕内容...")
    subtitle_summary = summarize_subtitles_with_chunking(subtitles, video.duration, llm_caller)

    # 2. 构建上下文
    comment_text = ""
    if comments:
        comment_text = "\n".join(
            f"- [{c.like}赞] {c.uname}: {c.content[:200]}" for c in comments
        )
    danmaku_text = ""
    if danmakus:
        danmaku_text = "\n".join(d.content for d in danmakus[:30])

    # 3. 生成主 summary
    primary_genre = genres[0].genre if genres else VideoGenre.GENERIC
    primary_conf = genres[0].confidence if genres else 1.0
    genre_display = GENRE_DISPLAY.get(primary_genre, "📚 通用知识")
    genre_list_display = [GENRE_DISPLAY.get(g.genre, str(g.genre)) for g in genres]
    print(f"  体裁: {genre_display}" + (f" (+ {len(genres)-1} 个)" if len(genres) > 1 else ""))

    if llm_caller:
        # 使用统一基座构建提示词
        prompt = build_prompt(
            genre=primary_genre,
            title=video.title,
            desc=video.desc[:500],
            duration=format_duration(video.duration),
            owner=video.owner,
            subtitle_summary=subtitle_summary or "（无字幕）",
            comments=comment_text or "（无评论）",
            danmakus=danmaku_text or "（无弹幕）",
        )

        print("  生成结构化总结...")
        response = llm_caller(prompt)
        main_summary = _parse_response(response)

        # 4. 多体裁合并
        if len(genres) > 1:
            for genre_result in genres[1:]:
                print(f"  补充体裁专用字段: {GENRE_DISPLAY.get(genre_result.genre)}")
                genre_prompt = build_prompt(
                    genre=genre_result.genre,
                    title=video.title,
                    desc=video.desc[:500],
                    duration=format_duration(video.duration),
                    owner=video.owner,
                    subtitle_summary=subtitle_summary or "（无字幕）",
                    comments=comment_text or "（无评论）",
                    danmakus=danmaku_text or "（无弹幕）",
                )
                secondary_response = llm_caller(genre_prompt)
                secondary_summary = _parse_response(secondary_response)
                main_summary = _merge_genre_fields(main_summary, secondary_summary, genre_result.genre)
    else:
        main_summary = VideoSummary(
            title_cn=video.title,
            title_en=video.title,
            tldr_cn=f"视频《{video.title}》由{video.owner}发布",
            tldr_en=f"Video '{video.title}' by {video.owner}",
            summary_cn=f"时长{format_duration(video.duration)}，播放量{format_count(video.view)}。{video.desc[:200]}",
            summary_en=f"Duration {format_duration(video.duration)}, {format_count(video.view)} views. {video.desc[:200]}",
        )

    # 5. 填充基本信息
    main_summary.owner = video.owner
    main_summary.duration_str = format_duration(video.duration)
    main_summary.view_count = video.view
    main_summary.like_count = video.like
    main_summary.genre = genre_display
    main_summary.genre_list = genre_list_display

    return main_summary
