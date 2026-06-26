#!/usr/bin/env python3
"""
Tests for Vector Store Module
测试向量存储功能
"""

import sys
import tempfile
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from chunker import Chunk
from store import VectorStore


def test_vector_store_init():
    """测试向量存储初始化"""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = VectorStore(persist_directory=tmpdir)

        assert store.persist_directory == tmpdir
        assert store.client is not None
        print("✅ test_vector_store_init passed")


def test_create_collection():
    """测试创建集合"""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = VectorStore(persist_directory=tmpdir)

        collection = store.create_collection(
            name="test_collection", metadata={"genre": "fantasy"}
        )

        assert collection.name == "test_collection"
        assert collection.metadata["genre"] == "fantasy"
        print("✅ test_create_collection passed")


def test_flatten_metadata():
    """测试元数据扁平化"""
    store = VectorStore()

    annotation = {
        "scene_type": ["打斗", "修炼"],
        "emotion": ["紧张", "热血"],
        "techniques": ["细节描写"],
        "key_elements": ["剑法", "突破"],
        "usage": ["学习打斗"],
        "pace": "快节奏",
        "pov": "第三人称",
        "quality_score": 8,
        "text_length": 1000,
    }

    metadata = store._flatten_metadata(annotation)

    assert "scene_type" in metadata
    assert "打斗" in metadata["scene_type"]
    assert "修炼" in metadata["scene_type"]
    assert metadata["pace"] == "快节奏"
    assert metadata["quality_score"] == "8"
    print("✅ test_flatten_metadata passed")


def test_add_chunks():
    """测试添加语料块"""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = VectorStore(persist_directory=tmpdir)
        collection = store.create_collection(name="test_add")

        chunks = [
            Chunk(
                text="测试文本 1",
                chunk_type="scene",
                start=0,
                end=100,
                source_file="test1.txt",
                annotation={"scene_type": ["打斗"], "quality_score": 8},
            ),
            Chunk(
                text="测试文本 2",
                chunk_type="scene",
                start=0,
                end=100,
                source_file="test2.txt",
                annotation={"scene_type": ["修炼"], "quality_score": 7},
            ),
        ]

        store.add_annotated_chunks(collection, chunks)

        # 验证添加成功
        assert collection.count() == 2
        print("✅ test_add_chunks passed")


def test_search():
    """测试搜索功能"""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = VectorStore(persist_directory=tmpdir)
        collection = store.create_collection(name="test_search")

        # 添加测试数据
        chunks = [
            Chunk(
                text="这是一个打斗场景",
                chunk_type="scene",
                start=0,
                end=100,
                source_file="test.txt",
                annotation={"scene_type": ["打斗"], "quality_score": 8},
            ),
        ]
        store.add_annotated_chunks(collection, chunks)

        # 测试搜索（不需要过滤器）
        results = collection.query(query_texts=["打斗"], n_results=1)

        assert "documents" in results
        assert len(results["documents"]) > 0
        print("✅ test_search passed")


def test_chunk_with_embedding():
    """测试带向量的语料块"""
    chunk = Chunk(
        text="测试文本",
        chunk_type="scene",
        start=0,
        end=100,
        source_file="test.txt",
        embedding=[0.1, 0.2, 0.3],
    )

    assert chunk.embedding == [0.1, 0.2, 0.3]
    print("✅ test_chunk_with_embedding passed")


if __name__ == "__main__":
    print("Running Vector Store Tests...\n")

    test_vector_store_init()
    test_create_collection()
    test_flatten_metadata()
    test_add_chunks()
    test_search()
    test_chunk_with_embedding()

    print("\n✅ All Vector Store tests passed!")
