"""
AutoDream Core 单元测试

测试核心功能（平台无关）。
"""

import unittest
from pathlib import Path
from datetime import datetime, timezone, timedelta
import tempfile
import shutil

# 导入核心模块
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.utils.frontmatter import parse_frontmatter, extract_frontmatter_and_body
from core.utils.text import normalize, canonical, stable_id, detect_contradiction, extract_entries_from_text
from core.utils.dates import parse_relative_dates, is_stale
from core.utils.state import DreamState, StateManager
from core.analytics import AnalyticsLogger


class TestFrontmatter(unittest.TestCase):
    """测试 frontmatter 解析"""
    
    def test_parse_simple(self):
        content = """---
type: decision
description: 技术栈选择
---
正文"""
        result = parse_frontmatter(content)
        self.assertEqual(result["type"], "decision")
        self.assertEqual(result["description"], "技术栈选择")
    
    def test_parse_no_frontmatter(self):
        content = "正文内容"
        result = parse_frontmatter(content)
        self.assertEqual(result, {})
    
    def test_extract_both(self):
        content = """---
type: note
---
正文内容"""
        frontmatter, body = extract_frontmatter_and_body(content)
        self.assertEqual(frontmatter["type"], "note")
        self.assertEqual(body, "正文内容")


class TestTextProcessing(unittest.TestCase):
    """测试文本处理"""
    
    def test_normalize(self):
        result = normalize("  多个   空格  ")
        self.assertEqual(result, "多个 空格")
    
    def test_canonical(self):
        result = canonical("Hello, World!")
        self.assertEqual(result, "hello world")
    
    def test_stable_id_consistency(self):
        id1 = stable_id("测试")
        id2 = stable_id("测试")
        self.assertEqual(id1, id2)
    
    def test_stable_id_uniqueness(self):
        id1 = stable_id("文本 A")
        id2 = stable_id("文本 B")
        self.assertNotEqual(id1, id2)
    
    def test_detect_contradiction(self):
        entry1 = {"text": "使用 Redis"}
        entry2 = {"text": "弃用 Redis"}
        self.assertTrue(detect_contradiction(entry1, entry2))
    
    def test_extract_entries(self):
        content = """- 条目 1
- 条目 2
* 条目 3"""
        entries = extract_entries_from_text(content)
        self.assertEqual(len(entries), 3)


class TestDates(unittest.TestCase):
    """测试日期处理"""
    
    def test_parse_yesterday(self):
        ref = datetime(2026, 4, 2, tzinfo=timezone.utc)
        result = parse_relative_dates("昨天我们讨论了", ref)
        self.assertIn("2026-04-01", result)
    
    def test_parse_last_week(self):
        ref = datetime(2026, 4, 2, tzinfo=timezone.utc)
        result = parse_relative_dates("上周完成了", ref)
        self.assertIn("2026-03", result)


class TestStateManager(unittest.TestCase):
    """测试状态管理"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_create_state(self):
        state = DreamState()
        self.assertEqual(state.status, "running")
        self.assertIsNotNone(state.started_at)
    
    def test_state_manager(self):
        manager = StateManager(self.temp_dir)
        state = DreamState(status="running")
        manager.write(state)
        
        loaded = manager.load()
        self.assertEqual(loaded.status, "running")


class TestAnalytics(unittest.TestCase):
    """测试 Analytics"""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_log_event(self):
        logger = AnalyticsLogger(self.temp_dir)
        logger.log("test_event", {"key": "value"})
        
        events = logger.read_all()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event"], "test_event")
    
    def test_get_stats(self):
        logger = AnalyticsLogger(self.temp_dir)
        logger.log("autodream_started")
        logger.log("autodream_completed", {"duration_seconds": 100})
        
        stats = logger.get_stats()
        self.assertEqual(stats["total_runs"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
