# -*- coding: utf-8 -*-
"""
fanqie-novel-auto-publish 技能包

整合 open-novel-writing 和 fanqie-publisher 实现一键发布
"""

from .novel_generator import NovelPipeline, NovelChapter, get_recent_chapters
from .fanqie_publisher import FanQiePublisher, Chapter, create_chapter, extract_chapter_from_file
from .auto_publish import AutoPublishWorkflow

__all__ = [
    "NovelPipeline",
    "NovelChapter", 
    "get_recent_chapters",
    "FanQiePublisher",
    "Chapter",
    "create_chapter",
    "extract_chapter_from_file",
    "AutoPublishWorkflow",
]
