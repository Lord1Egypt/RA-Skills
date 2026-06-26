"""数据模型定义"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import json


@dataclass
class Project:
    """GitHub 项目数据"""
    repo_full_name: str             # e.g. "thunlp/OpenMAIC"
    repo_url: str
    name: str
    description: str = ""
    language: str = ""
    stars: int = 0
    forks: int = 0
    open_issues: int = 0
    last_updated: str = ""
    created_at: str = ""
    owner_type: str = ""            # "User" or "Organization"
    topics: list[str] = field(default_factory=list)
    readme_excerpt: str = ""
    source: str = "search"          # "search", "org_watch", "manual"
    discovered_at: str = ""
    id: Optional[int] = None

    @property
    def topics_json(self) -> str:
        return json.dumps(self.topics, ensure_ascii=False)

    @classmethod
    def from_db_row(cls, row: dict) -> "Project":
        data = dict(row)
        topics_raw = data.pop("topics", "[]")
        try:
            topics = json.loads(topics_raw) if topics_raw else []
        except (json.JSONDecodeError, TypeError):
            topics = []
        return cls(topics=topics, **data)


@dataclass
class Score:
    """评分记录"""
    project_id: int
    rubric_version: str
    novelty: float
    practicality: float
    content_fit: float
    ease_of_use: float
    total_score: float
    scoring_reason: str = ""
    llm_model: str = ""
    scored_at: str = ""
    id: Optional[int] = None

    @classmethod
    def from_db_row(cls, row: dict) -> "Score":
        return cls(**dict(row))


@dataclass
class RankingEntry:
    """排行榜条目"""
    rank: int
    project: Project
    score: Score


@dataclass
class Post:
    """生成的内容记录"""
    project_id: int
    analysis_path: str = ""
    post_path: str = ""
    images_dir: str = ""
    status: str = "draft"           # draft / ready / published
    created_at: str = ""
    id: Optional[int] = None

    @classmethod
    def from_db_row(cls, row: dict) -> "Post":
        return cls(**dict(row))


@dataclass
class AnalysisResult:
    """项目分析结果（内存中使用，不直接存 DB）"""
    project: Project
    one_liner: str = ""
    problem: str = ""
    architecture: str = ""
    quickstart: str = ""
    highlights: str = ""
    pitfalls: str = ""
    resources: str = ""
    full_markdown: str = ""


@dataclass
class PostContent:
    """小红书文案内容（内存中使用）"""
    title: str = ""
    body: str = ""
    tags: list[str] = field(default_factory=list)
    full_text: str = ""
