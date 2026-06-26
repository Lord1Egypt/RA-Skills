#!/usr/bin/env python3
"""
LLM Monitor - Test Suite
Tests for collector, analyzer, and reporter modules
"""

import unittest
import json
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import collector
import analyzer

class TestCollector(unittest.TestCase):
    """Test data collection"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_data_dir = collector.DATA_DIR
        collector.DATA_DIR = Path(self.test_dir)
        collector.ensure_session_dir()
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
        collector.DATA_DIR = self.original_data_dir
    
    def test_create_session(self):
        """Test session creation"""
        session_id = collector.create_session("test-model")
        self.assertIsNotNone(session_id)
        self.assertEqual(len(session_id), 8)
        
        # Check file was created
        session_file = collector.DATA_DIR / f"{session_id}.json"
        self.assertTrue(session_file.exists())
    
    def test_detect_correction(self):
        """Test correction detection"""
        config = {
            "patterns": {
                "correction_keywords": ["不对", "错了", "重新"]
            }
        }
        
        # Should detect
        is_correction, kw = collector.detect_correction("不对，我要的是Excel", config)
        self.assertTrue(is_correction)
        self.assertEqual(kw, "不对")
        
        # Should not detect
        is_correction, kw = collector.detect_correction("好的，我明白了", config)
        self.assertFalse(is_correction)
    
    def test_detect_promises(self):
        """Test promise detection"""
        config = {
            "patterns": {
                "promise_patterns": ["接下来我会", "首先让我"],
                "over_promise_patterns": ["我可以轻松", "完全没问题"]
            }
        }
        
        # Should detect promise
        has_promise, promises, is_over = collector.detect_promises(
            "接下来我会分3步完成", config
        )
        self.assertTrue(has_promise)
        self.assertIn("接下来我会", promises)
        self.assertFalse(is_over)
        
        # Should detect over-promise
        has_promise, promises, is_over = collector.detect_promises(
            "我可以轻松完成这个复杂任务", config
        )
        self.assertTrue(has_promise)
        self.assertTrue(is_over)

class TestAnalyzer(unittest.TestCase):
    """Test metric analysis"""
    
    def test_calculate_health_score_perfect(self):
        """Test perfect session scoring"""
        score = analyzer.calculate_health_score(
            first_try=True,
            rework=0,
            promise_rate=1.0,
            inflation=1.0,
            token_eff=0.2
        )
        self.assertGreaterEqual(score, 85)
        self.assertEqual(analyzer.get_health_status(score), "excellent")
    
    def test_calculate_health_score_poor(self):
        """Test poor session scoring"""
        score = analyzer.calculate_health_score(
            first_try=False,
            rework=5,
            promise_rate=0.5,
            inflation=3.0,
            token_eff=0.05
        )
        self.assertLess(score, 50)
        self.assertEqual(analyzer.get_health_status(score), "danger")
    
    def test_get_health_status(self):
        """Test status classification"""
        self.assertEqual(analyzer.get_health_status(90), "excellent")
        self.assertEqual(analyzer.get_health_status(75), "good")
        self.assertEqual(analyzer.get_health_status(60), "warning")
        self.assertEqual(analyzer.get_health_status(40), "danger")

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_data_dir = collector.DATA_DIR
        collector.DATA_DIR = Path(self.test_dir)
        collector.ensure_session_dir()
    
    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.test_dir)
        collector.DATA_DIR = self.original_data_dir
    
    def test_full_session_lifecycle(self):
        """Test complete session from creation to analysis"""
        # Create session
        sid = collector.create_session("test-model")
        
        # Record turns
        collector.record_turn(sid, "Task A", "I'll do this in 2 steps", 100, 200)
        collector.record_turn(sid, "Wrong, redo", "Sorry, let me fix", 50, 150)
        
        # Complete
        collector.complete_session(sid, True)
        
        # Analyze
        session = collector.load_session(sid)
        analysis = analyzer.analyze_session(session)
        
        # Verify
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis["total_turns"], 2)
        self.assertEqual(analysis["rework_count"], 1)
        self.assertFalse(analysis["first_try_success"])

def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestCollector))
    suite.addTests(loader.loadTestsFromTestCase(TestAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
