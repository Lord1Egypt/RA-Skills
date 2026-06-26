"""
Intelligence Agent Module

보안 블로그 자동화 시스템:
- News Collector: RSS/News 수집
- LLM Writer: 보안 전문가 페르소나로 글 작성
- Notion Publisher: Notion DB 저장
- Git Publisher: 사용자 승인 후 Git Push → GitHub Actions 배포
"""

# Intelligence Agent 하위 모듈
from modules.intelligence.collector import NewsCollector
from modules.intelligence.writer import BlogWriter
from modules.intelligence.llm_client import GLMClient
from modules.intelligence.notion_publisher import NotionPublisher
from modules.intelligence.publisher_git import GitPublisher

__all__ = [
    "NewsCollector",
    "BlogWriter",
    "GLMClient",
    "NotionPublisher",
    "GitPublisher",
    "__all__",
    "__version__",
    "__author__",
]

__version__ = "1.0.0"
__author__ = "OpenClaw Team"
