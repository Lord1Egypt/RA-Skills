"""
BiliYouTik2Brain — 知识库查询测试
"""

import sys, os, shutil, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.knowledge_store import query, query_by_uploader, _fuzzy_match


# ── knowledge/*.md 文件格式（匹配 node_save._node_auto_archive 输出的格式） ──

TEST_KNOWLEDGE = """# 张聚贤

> 来源: https://www.bilibili.com/video/BV1xxx | 领域: 交易

## 概述

张聚贤的交易体系以供需区为核心，结合机构订单原理。

**关键词**: 供需区, 机构订单原理, 价格行为
---

## 视频条目

### 孕线交易策略详解
> 日期: 2026-05-01

孕线是最可靠的入场信号之一。
"""

# — 自动归档输出的格式（含 **摘要**: 字段）—

TEST_AUTO_ARCHIVE = """# test_auto

> 来源: https://www.bilibili.com/video/BV1test | 处理日期: 2026-05-24 | 领域: 交易

**摘要**: 自动归档的测试摘要内容。

**关键词**: 测试, 自动归档
"""


class TestKnowledgeQuery:
    """知识库查询测试"""

    def setup_method(self):
        self.tmpdir = tempfile.mkdtemp()
        self.knowledge_dir = os.path.join(self.tmpdir, "knowledge")
        os.makedirs(self.knowledge_dir, exist_ok=True)
        with open(os.path.join(self.knowledge_dir, "张聚贤.md"), "w") as f:
            f.write(TEST_KNOWLEDGE)
        # 自动归档格式
        with open(os.path.join(self.knowledge_dir, "test_auto.md"), "w") as f:
            f.write(TEST_AUTO_ARCHIVE)
        import core.knowledge_store as ks
        self.old_known_dir = ks.KNOWLEDGE_DIR
        self.old_wiki_dir = ks.WIKI_DIR
        ks.KNOWLEDGE_DIR = self.knowledge_dir
        # 空wiki目录避免被真实文件干扰
        self.wiki_dir = os.path.join(self.tmpdir, "wiki")
        os.makedirs(self.wiki_dir, exist_ok=True)
        ks.WIKI_DIR = self.wiki_dir

    def teardown_method(self):
        import core.knowledge_store as ks
        ks.KNOWLEDGE_DIR = self.old_known_dir
        ks.WIKI_DIR = self.old_wiki_dir
        shutil.rmtree(self.tmpdir)

    def test_query_by_speaker(self):
        """按说话人查询 — 自动归档格式匹配"""
        results = query(speaker="test_auto")
        assert len(results) == 1
        assert "测试摘要" in results[0].summary

    def test_query_all(self):
        """无过滤 → 返回所有"""
        results = query()
        # 应该返回2个（张聚贤的概述 + test_auto的摘要）
        assert len(results) >= 1

    def test_no_results_empty(self):
        """不存在的说话人"""
        results = query(speaker="不存在的人")
        assert len(results) == 0

    def test_fuzzy_match(self):
        assert _fuzzy_match("张聚贤", "张聚贤") is True
        assert _fuzzy_match("张_聚_贤", "张聚贤") is True
        assert _fuzzy_match("张三", "李四") is False

    def test_query_by_uploader_text(self):
        """query_by_uploader 返回纯文本"""
        result = query_by_uploader("test_auto")
        assert "测试摘要" in result


class TestEmptyQuery:
    """没有知识库文件时"""

    def setup_method(self):
        import core.knowledge_store as ks
        self.old_known_dir = ks.KNOWLEDGE_DIR
        self.old_wiki_dir = ks.WIKI_DIR
        self.empty_dir = tempfile.mkdtemp()
        self.empty_wiki = os.path.join(self.empty_dir, "wiki")
        os.makedirs(self.empty_wiki, exist_ok=True)
        ks.KNOWLEDGE_DIR = os.path.join(self.empty_dir, "knowledge")
        os.makedirs(ks.KNOWLEDGE_DIR, exist_ok=True)
        ks.WIKI_DIR = self.empty_wiki

    def teardown_method(self):
        import core.knowledge_store as ks
        ks.KNOWLEDGE_DIR = self.old_known_dir
        ks.WIKI_DIR = self.old_wiki_dir
        shutil.rmtree(self.empty_dir)

    def test_empty_knowledge_dir(self):
        """空目录返回空列表"""
        results = query()
        assert results == []

    def test_query_by_uploader_empty(self):
        """不存在的UP主"""
        result = query_by_uploader("不存在的人")
        assert result == ""
