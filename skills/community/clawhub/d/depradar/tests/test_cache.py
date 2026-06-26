"""Tests for scripts/lib/cache.py"""
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "lib"))

import cache


class TestCacheSaveLoad(unittest.TestCase):

    def setUp(self):
        # Use a temp directory for all tests
        self.tmp_dir = tempfile.mkdtemp()
        self._cache_dir_patcher = patch.dict(
            os.environ, {"APIWATCH_CACHE_DIR": self.tmp_dir}
        )
        self._cache_dir_patcher.start()

    def tearDown(self):
        self._cache_dir_patcher.stop()
        # Clean up temp files
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_save_and_load_roundtrip_dict(self):
        data = {"key": "value", "number": 42, "list": [1, 2, 3]}
        cache.save("test_key", data, namespace="test")
        loaded = cache.load("test_key", ttl_hours=1.0, namespace="test")
        self.assertEqual(loaded, data)

    def test_save_and_load_roundtrip_string(self):
        cache.save("str_key", "hello world", namespace="test")
        loaded = cache.load("str_key", ttl_hours=1.0, namespace="test")
        self.assertEqual(loaded, "hello world")

    def test_save_and_load_roundtrip_list(self):
        data = [1, 2, {"nested": True}]
        cache.save("list_key", data, namespace="test")
        loaded = cache.load("list_key", ttl_hours=1.0, namespace="test")
        self.assertEqual(loaded, data)

    def test_save_and_load_roundtrip_none(self):
        # None is a valid value to cache (not a miss)
        cache.save("none_key", None, namespace="test")
        loaded = cache.load("none_key", ttl_hours=1.0, namespace="test")
        self.assertIsNone(loaded)

    def test_load_miss_returns_none(self):
        result = cache.load("nonexistent_key", ttl_hours=1.0, namespace="test")
        self.assertIsNone(result)

    def test_ttl_not_expired(self):
        cache.save("ttl_key", {"value": 1}, namespace="test")
        # TTL of 1 hour — should still be there
        loaded = cache.load("ttl_key", ttl_hours=1.0, namespace="test")
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["value"], 1)

    def test_ttl_expired(self):
        cache.save("expired_key", {"value": 99}, namespace="test")
        # Load with TTL of effectively 0 — should expire
        loaded = cache.load("expired_key", ttl_hours=0.0, namespace="test")
        self.assertIsNone(loaded)

    def test_ttl_expiry_via_mocked_time(self):
        now = time.time()
        with patch("time.time", return_value=now):
            cache.save("mock_ttl_key", {"v": 42}, namespace="test")

        # Advance time by 7 hours (beyond the 6-hour TTL)
        future = now + 7 * 3600
        with patch("time.time", return_value=future):
            loaded = cache.load("mock_ttl_key", ttl_hours=6.0, namespace="test")
        self.assertIsNone(loaded)

    def test_ttl_not_expired_via_mocked_time(self):
        now = time.time()
        with patch("time.time", return_value=now):
            cache.save("fresh_key", {"v": 77}, namespace="test")

        # Advance only 2 hours (within the 6-hour TTL)
        future = now + 2 * 3600
        with patch("time.time", return_value=future):
            loaded = cache.load("fresh_key", ttl_hours=6.0, namespace="test")
        self.assertEqual(loaded, {"v": 77})


class TestLoadWithAge(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self._patcher = patch.dict(os.environ, {"APIWATCH_CACHE_DIR": self.tmp_dir})
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_returns_data_and_age(self):
        now = time.time()
        with patch("time.time", return_value=now):
            cache.save("age_key", {"data": True}, namespace="test")

        # Advance 1 hour
        with patch("time.time", return_value=now + 3600):
            data, age = cache.load_with_age("age_key", ttl_hours=6.0, namespace="test")

        self.assertIsNotNone(data)
        self.assertAlmostEqual(age, 1.0, delta=0.01)

    def test_returns_none_none_on_miss(self):
        data, age = cache.load_with_age("missing_key", ttl_hours=1.0, namespace="test")
        self.assertIsNone(data)
        self.assertIsNone(age)

    def test_returns_none_none_when_expired(self):
        now = time.time()
        with patch("time.time", return_value=now):
            cache.save("exp_age_key", {"x": 1}, namespace="test")
        with patch("time.time", return_value=now + 8 * 3600):
            data, age = cache.load_with_age("exp_age_key", ttl_hours=6.0, namespace="test")
        self.assertIsNone(data)
        self.assertIsNone(age)

    def test_age_is_positive(self):
        cache.save("pos_age_key", {"v": 1}, namespace="test")
        data, age = cache.load_with_age("pos_age_key", ttl_hours=6.0, namespace="test")
        self.assertIsNotNone(age)
        self.assertGreaterEqual(age, 0.0)


class TestCacheClear(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self._patcher = patch.dict(os.environ, {"APIWATCH_CACHE_DIR": self.tmp_dir})
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_clear_removes_files(self):
        cache.save("k1", {"a": 1}, namespace="ns_clear")
        cache.save("k2", {"b": 2}, namespace="ns_clear")
        cache.save("k3", {"c": 3}, namespace="ns_clear")

        count = cache.clear(namespace="ns_clear")
        self.assertEqual(count, 3)

        # Verify files are gone
        self.assertIsNone(cache.load("k1", ttl_hours=1.0, namespace="ns_clear"))
        self.assertIsNone(cache.load("k2", ttl_hours=1.0, namespace="ns_clear"))

    def test_clear_empty_namespace_returns_zero(self):
        count = cache.clear(namespace="nonexistent_ns")
        self.assertEqual(count, 0)

    def test_clear_does_not_affect_other_namespaces(self):
        cache.save("shared_key", {"val": "keep"}, namespace="ns_keep")
        cache.save("del_key", {"val": "delete"}, namespace="ns_delete")

        cache.clear(namespace="ns_delete")

        remaining = cache.load("shared_key", ttl_hours=1.0, namespace="ns_keep")
        self.assertIsNotNone(remaining)
        self.assertEqual(remaining["val"], "keep")


class TestCacheNamespaceIsolation(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self._patcher = patch.dict(os.environ, {"APIWATCH_CACHE_DIR": self.tmp_dir})
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_same_key_different_namespaces(self):
        cache.save("key", {"ns": "alpha"}, namespace="alpha")
        cache.save("key", {"ns": "beta"}, namespace="beta")

        alpha = cache.load("key", ttl_hours=1.0, namespace="alpha")
        beta  = cache.load("key", ttl_hours=1.0, namespace="beta")

        self.assertEqual(alpha["ns"], "alpha")
        self.assertEqual(beta["ns"],  "beta")

    def test_different_namespaces_dont_collide_on_clear(self):
        cache.save("shared", {"v": 1}, namespace="ns_a")
        cache.save("shared", {"v": 2}, namespace="ns_b")

        cache.clear(namespace="ns_a")

        result = cache.load("shared", ttl_hours=1.0, namespace="ns_b")
        self.assertIsNotNone(result)
        self.assertEqual(result["v"], 2)


class TestCacheKey(unittest.TestCase):

    def test_reproducible(self):
        k1 = cache.cache_key("npm", "stripe", "7.0.0")
        k2 = cache.cache_key("npm", "stripe", "7.0.0")
        self.assertEqual(k1, k2)

    def test_different_inputs_different_keys(self):
        k1 = cache.cache_key("npm", "stripe")
        k2 = cache.cache_key("pypi", "stripe")
        self.assertNotEqual(k1, k2)

    def test_key_is_32_hex_chars(self):
        k = cache.cache_key("any", "thing")
        self.assertRegex(k, r"^[0-9a-f]{32}$")

    def test_single_part(self):
        k = cache.cache_key("test")
        self.assertEqual(len(k), 32)


if __name__ == "__main__":
    unittest.main()
