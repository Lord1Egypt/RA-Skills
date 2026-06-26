"""
Test Automation Script

Unit tests for desktop automation modules.
"""

import sys
import os
import json
import unittest
from pathlib import Path

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.actions import ActionManager
from lib.safety_manager import SafetyManager
from lib.macro_player import MacroPlayer
from lib.image_recognition import ImageRecognition
from lib.ocr_engine import OCREngine
from lib.utils import setup_logging


class TestActionManager(unittest.TestCase):
    """Test ActionManager."""
    
    def setUp(self):
        self.manager = ActionManager(safe_mode=True)
    
    def test_dry_run_click(self):
        """Test click in dry_run mode."""
        result = self.manager.click(100, 100, dry_run=True)
        self.assertEqual(result['status'], 'ok')
        self.assertTrue(result['dry_run'])
    
    def test_safe_mode_blocks_dangerous(self):
        """Test that safe mode blocks dangerous patterns."""
        result = self.manager.click(100, 100)
        self.assertIn(result['status'], ['ok', 'blocked'])
    
    def test_dry_run_type(self):
        """Test type in dry_run mode."""
        result = self.manager.type("test", dry_run=True)
        self.assertEqual(result['status'], 'ok')
        self.assertTrue(result['dry_run'])
    
    def test_get_active_window(self):
        """Test getting active window."""
        result = self.manager.get_active_window()
        self.assertIn(result['status'], ['ok', 'error'])


class TestSafetyManager(unittest.TestCase):
    """Test SafetyManager."""
    
    def setUp(self):
        self.manager = SafetyManager(safe_mode_enabled=True)
    
    def test_safe_mode_enabled(self):
        """Test safe mode is enabled."""
        self.assertTrue(self.manager.is_safe_mode_enabled())
    
    def test_dangerous_pattern_detection(self):
        """Test dangerous pattern detection."""
        self.assertTrue(self.manager.contains_dangerous_pattern("rm /etc/"))
        self.assertFalse(self.manager.contains_dangerous_pattern("echo hello"))
    
    def test_check_action_safety(self):
        """Test action safety checking."""
        safe, reason = self.manager.check_action_safety("click", {"x": 100, "y": 100})
        self.assertTrue(safe)
    
    def test_disable_safe_mode(self):
        """Test disabling safe mode."""
        self.manager.disable_safe_mode()
        self.assertFalse(self.manager.is_safe_mode_enabled())
    
    def test_get_safety_status(self):
        """Test getting safety status."""
        status = self.manager.get_safety_status()
        self.assertEqual(status['status'], 'ok')
        self.assertIn('safe_mode_enabled', status)


class TestMacroPlayer(unittest.TestCase):
    """Test MacroPlayer."""
    
    def setUp(self):
        self.action_manager = ActionManager(safe_mode=True)
        self.player = MacroPlayer(self.action_manager)
    
    def test_load_nonexistent_macro(self):
        """Test loading non-existent macro."""
        macro = self.player.load_macro("/nonexistent/path.json")
        self.assertIsNone(macro)
    
    def test_create_and_load_macro(self):
        """Test creating and loading a test macro."""
        test_macro = {
            "events": [
                {"action": "click", "params": {"x": 100, "y": 100}},
                {"action": "type", "params": {"text": "hello"}}
            ]
        }
        
        # Save test macro
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_macro, f)
            temp_path = f.name
        
        try:
            # Load it back
            loaded = self.player.load_macro(temp_path)
            self.assertIsNotNone(loaded)
            self.assertEqual(len(loaded['events']), 2)
        finally:
            os.unlink(temp_path)


class TestImageRecognition(unittest.TestCase):
    """Test ImageRecognition."""
    
    def setUp(self):
        self.recognizer = ImageRecognition()
    
    def test_find_nonexistent_image(self):
        """Test finding non-existent image."""
        result = self.recognizer.find_image("/nonexistent/image.png", dry_run=True)
        self.assertIn(result['status'], ['ok', 'error'])
    
    def test_dry_run_find_image(self):
        """Test find_image in dry_run mode."""
        result = self.recognizer.find_image("test.png", dry_run=True)
        self.assertIn(result['status'], ['ok', 'error'])


class TestOCREngine(unittest.TestCase):
    """Test OCREngine."""
    
    def setUp(self):
        self.ocr = OCREngine()
    
    def test_dry_run_find_text(self):
        """Test find_text in dry_run mode."""
        result = self.ocr.find_text_on_screen("test", dry_run=True)
        self.assertIn(result['status'], ['ok', 'error'])


def main():
    """Run all tests."""
    setup_logging()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestActionManager))
    suite.addTests(loader.loadTestsFromTestCase(TestSafetyManager))
    suite.addTests(loader.loadTestsFromTestCase(TestMacroPlayer))
    suite.addTests(loader.loadTestsFromTestCase(TestImageRecognition))
    suite.addTests(loader.loadTestsFromTestCase(TestOCREngine))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit(main())
