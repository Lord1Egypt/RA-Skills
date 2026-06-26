#!/usr/bin/env python3
"""
Text Chunker - 文本分块器

支持按场景智能切分文本，识别章节、时间、地点、视角等场景切换标志。
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class Chunk:
    """语料块数据结构"""

    text: str
    chunk_type: str  # scene/chapter/length_based
    start: int
    end: int
    source_file: str
    split_marker: str = ""
    features: Optional[Dict] = field(default_factory=dict)
    annotation: Optional[Dict] = field(default_factory=dict)
    embedding: Optional[List] = field(default_factory=list)


class TextChunker:
    """文本分块器 - 按场景智能切分"""

    SCENE_PATTERNS = [
        (r"\n#{0,2}\s*(第.章)", "chapter_title"),
        (r"\n#{0,2}\s*(CHAPTER\s*\d+)", "chapter_title_en"),
        (r"\n(此时 | 与此同时 | 话说 | 且说 | 却说 | 转眼 | 次日 | 三日后)", "time_transition"),
        (r"\n(地点：| 来到 | 到了 | 返回 | 进入 | 离开\s*[a-zA-Z]+)", "location_change"),
        (r"\n(镜头转向 | 目光投向 | 视线落在 | 另一边)", "pov_change"),
        (r"\n\n\s{2,}", "paragraph_break"),
    ]

    def __init__(
        self, max_chunk_size: int = 2000, min_chunk_size: int = 100, overlap: int = 200
    ):
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        self.overlap = overlap

    def chunk_by_scene(self, text: str, source_file: str = "") -> List[Chunk]:
        """
        按场景分块

        策略:
        1. 识别场景切换标志（章节、时间、地点、视角）
        2. 按标志切分文本
        3. 过滤太短的块
        4. 过长的块进一步切分
        """
        if len(text) < self.max_chunk_size:
            return [
                Chunk(
                    text=text.strip(),
                    chunk_type="single_chunk",
                    start=0,
                    end=len(text),
                    source_file=source_file,
                )
            ]

        split_points = self._find_split_points(text)

        if not split_points:
            return self.chunk_by_length(text, source_file)

        chunks = []
        for i, (start, end, marker_type, marker_text) in enumerate(split_points):
            chunk_text = text[start:end].strip()

            if len(chunk_text) < self.min_chunk_size:
                continue

            if len(chunk_text) > self.max_chunk_size * 1.5:
                sub_chunks = self.chunk_by_length(chunk_text, source_file)
                for sub_chunk in sub_chunks:
                    sub_chunk.start += start
                    sub_chunk.end += start
                chunks.extend(sub_chunks)
            else:
                chunks.append(
                    Chunk(
                        text=chunk_text,
                        chunk_type=f"scene_{marker_type}",
                        start=start,
                        end=end,
                        source_file=source_file,
                        split_marker=marker_text[:50],
                    )
                )

        # 处理开头部分
        if split_points and split_points[0][0] > 0:
            intro_text = text[: split_points[0][0]].strip()
            if len(intro_text) >= self.min_chunk_size:
                chunks.insert(
                    0,
                    Chunk(
                        text=intro_text,
                        chunk_type="initial",
                        start=0,
                        end=split_points[0][0],
                        source_file=source_file,
                    ),
                )

        return chunks

    def _find_split_points(self, text: str) -> List[Tuple[int, int, str, str]]:
        """找到所有场景分割点"""
        matches = []

        for pattern, pattern_type in self.SCENE_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                matches.append((match.start(), match.group(), pattern_type))

        # 按位置排序
        matches.sort(key=lambda x: x[0])

        # 去重（至少间隔 500 字）
        unique_matches = []
        last_pos = -500
        for pos, marker, ptype in matches:
            if pos - last_pos > 500:
                unique_matches.append((pos, marker, ptype))
                last_pos = pos

        # 转换为分割区间
        split_points = []
        for i, (pos, marker, ptype) in enumerate(unique_matches):
            start = pos
            end = unique_matches[i + 1][0] if i + 1 < len(unique_matches) else len(text)
            split_points.append((start, end, ptype, marker))

        return split_points

    def chunk_by_length(self, text: str, source_file: str = "") -> List[Chunk]:
        """按长度切分（备用方案）"""
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.max_chunk_size

            if end >= len(text):
                chunk_text = text[start:].strip()
                if len(chunk_text) >= self.min_chunk_size:
                    chunks.append(
                        Chunk(
                            text=chunk_text,
                            chunk_type="length_based",
                            start=start,
                            end=len(text),
                            source_file=source_file,
                        )
                    )
                break

            # 在标点处切分
            segment = text[start:end]
            last_punct = max(
                segment.rfind("。"),
                segment.rfind("！"),
                segment.rfind("？"),
                segment.rfind("\n"),
            )

            if last_punct > self.overlap:
                end = start + last_punct + 1
            else:
                end = start + self.overlap

            chunk_text = text[start:end].strip()

            if len(chunk_text) >= self.min_chunk_size:
                chunks.append(
                    Chunk(
                        text=chunk_text,
                        chunk_type="length_based",
                        start=start,
                        end=end,
                        source_file=source_file,
                    )
                )

            start = max(start + self.overlap, end - self.overlap)

        return chunks
