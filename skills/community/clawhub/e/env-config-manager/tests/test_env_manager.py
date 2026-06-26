"""
Unit tests for env-config-manager
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from env_manager import load_env, save_env, validate_schema, diff_env, get_var


class TestEnvManager(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.env_path = os.path.join(self.temp_dir, ".env")
    
    def tearDown(self):
        if os.path.exists(self.env_path):
            os.remove(self.env_path)
        os.rmdir(self.temp_dir)
    
    def test_load_empty(self):
        env = load_env("nonexistent.env")
        self.assertEqual(env, {})
    
    def test_save_and_load(self):
        data = {"KEY1": "value1", "KEY2": "value2"}
        save_env(data, self.env_path)
        loaded = load_env(self.env_path)
        self.assertEqual(loaded.get("KEY1"), "value1")
        self.assertEqual(loaded.get("KEY2"), "value2")
    
    def test_validate_required(self):
        env = {"PORT": "8080"}
        schema = {"DATABASE_URL": {"required": True}, "PORT": {"required": True}}
        errors = validate_schema(env, schema)
        self.assertIn("Missing required variable: DATABASE_URL", errors)
    
    def test_validate_int(self):
        env = {"PORT": "abc"}
        schema = {"PORT": {"type": "int"}}
        errors = validate_schema(env, schema)
        self.assertIn("PORT must be an integer, got: abc", errors)
    
    def test_validate_int_range(self):
        env = {"PORT": "80"}
        schema = {"PORT": {"type": "int", "min": 1024, "max": 65535}}
        errors = validate_schema(env, schema)
        self.assertIn("PORT must be >= 1024", errors)
    
    def test_validate_bool(self):
        env = {"DEBUG": "maybe"}
        schema = {"DEBUG": {"type": "bool"}}
        errors = validate_schema(env, schema)
        self.assertIn("DEBUG must be a boolean, got: maybe", errors)
    
    def test_validate_url(self):
        env = {"API_URL": "ftp://example.com"}
        schema = {"API_URL": {"type": "url"}}
        errors = validate_schema(env, schema)
        self.assertIn("API_URL must be a valid URL, got: ftp://example.com", errors)
    
    def test_diff(self):
        env1 = {"A": "1", "B": "2"}
        env2 = {"A": "1", "B": "3", "C": "4"}
        diff = diff_env(env1, env2)
        self.assertEqual(diff["B"], {"old": "2", "new": "3"})
        self.assertEqual(diff["C"], {"old": None, "new": "4"})
    
    def test_empty_value(self):
        data = {"EMPTY_KEY": ""}
        save_env(data, self.env_path)
        loaded = load_env(self.env_path)
        self.assertEqual(loaded.get("EMPTY_KEY"), "")


if __name__ == "__main__":
    unittest.main()
