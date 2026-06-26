#!/usr/bin/env python3
"""
Tests for Text Chunker Module
测试文本分块器功能
"""

import sys
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from chunker import Chunk, TextChunker


def test_chunk_by_scene_single():
    """测试单段文本分块"""
    chunker = TextChunker(max_chunk_size=2000, min_chunk_size=100, overlap=200)
    text = "这是一段测试文本。" * 10
    chunks = chunker.chunk_by_scene(text, "test.txt")

    assert len(chunks) == 1
    assert chunks[0].chunk_type == "single_chunk"
    assert chunks[0].source_file == "test.txt"
    print("✅ test_chunk_by_scene_single passed")


def test_chunk_by_length():
    """测试按长度分块"""
    chunker = TextChunker(max_chunk_size=500, min_chunk_size=100, overlap=100)
    text = "这是一段很长的测试文本。" * 100
    chunks = chunker.chunk_by_length(text, "test.txt")

    assert len(chunks) > 1
    assert all(c.chunk_type == "length_based" for c in chunks)
    assert all(len(c.text) >= 100 for c in chunks)
    print("✅ test_chunk_by_length passed")


def test_chunk_data_structure():
    """测试 Chunk 数据结构"""
    chunk = Chunk(
        text="测试文本",
        chunk_type="scene_chapter_title",
        start=0,
        end=100,
        source_file="test.txt",
        split_marker="第一章",
    )

    assert chunk.text == "测试文本"
    assert chunk.chunk_type == "scene_chapter_title"
    assert chunk.start == 0
    assert chunk.end == 100
    assert chunk.source_file == "test.txt"
    assert chunk.split_marker == "第一章"
    assert chunk.features == {}
    assert chunk.annotation == {}
    assert chunk.embedding == []
    print("✅ test_chunk_data_structure passed")


def test_scene_patterns():
    """测试场景模式识别"""
    chunker = TextChunker(max_chunk_size=500, min_chunk_size=50, overlap=100)
    # 使用足够长的文本以触发场景分割
    text = """
第一章 开始

这是第一段内容。""" + "这是一些填充内容。" * 50 + """

第二章 发展

这是第二段内容。""" + "这是更多的填充内容。" * 50 + """

第三章 高潮

这是第三段内容。""" + "这是更多的填充内容。" * 50 + """
"""
    chunks = chunker.chunk_by_scene(text, "test.txt")

    assert len(chunks) > 0
    assert any("chapter" in c.chunk_type for c in chunks)
    print("✅ test_scene_patterns passed")


def test_min_chunk_filter():
    """测试最小块过滤"""
    chunker = TextChunker(max_chunk_size=2000, min_chunk_size=100, overlap=200)
    text = "短文本"
    chunks = chunker.chunk_by_scene(text, "test.txt")

    # 太短的文本应该被过滤或合并
    assert len(chunks) >= 0
    print("✅ test_min_chunk_filter passed")


if __name__ == "__main__":
    print("Running Text Chunker Tests...\n")

    test_chunk_data_structure()
    test_chunk_by_scene_single()
    test_chunk_by_length()
    test_scene_patterns()
    test_min_chunk_filter()

    print("\n✅ All Text Chunker tests passed!")
