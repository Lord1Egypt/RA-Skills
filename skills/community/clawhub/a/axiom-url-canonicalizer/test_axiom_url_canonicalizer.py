"""Tests — axiom-url-canonicalizer """

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent))

from axiom_url_canonicalizer import (
    analyze,
    canonicalize,
    urls_equivalent,
)


class TestCanonicalizeBasic(unittest.TestCase):
    def test_01_lowercase_scheme(self):
        self.assertEqual(
            canonicalize("HTTP://example.com/"),
            "http://example.com/"
        )

    def test_02_lowercase_host(self):
        self.assertEqual(
            canonicalize("http://EXAMPLE.com/"),
            "http://example.com/"
        )

    def test_03_strip_default_port_http(self):
        self.assertEqual(
            canonicalize("http://example.com:80/path"),
            "http://example.com/path"
        )

    def test_04_strip_default_port_https(self):
        self.assertEqual(
            canonicalize("https://example.com:443/path"),
            "https://example.com/path"
        )

    def test_05_keep_non_default_port(self):
        self.assertEqual(
            canonicalize("http://example.com:8080/path"),
            "http://example.com:8080/path"
        )

    def test_06_strip_fragment(self):
        self.assertEqual(
            canonicalize("http://example.com/path#frag"),
            "http://example.com/path"
        )

    def test_07_keep_fragment(self):
        self.assertEqual(
            canonicalize("http://example.com/path#frag", strip_fragment=False),
            "http://example.com/path#frag"
        )


class TestCanonicalizeQuery(unittest.TestCase):
    def test_08_sort_query(self):
        self.assertEqual(
            canonicalize("http://example.com/?b=2&a=1"),
            "http://example.com/?a=1&b=2"
        )

    def test_09_remove_tracking(self):
        result = canonicalize(
            "http://example.com/?a=1&utm_source=fb",
            remove_tracking_params=True
        )
        self.assertNotIn("utm_source", result)
        self.assertIn("a=1", result)

    def test_10_keep_blank(self):
        self.assertEqual(
            canonicalize("http://example.com/?a="),
            "http://example.com/?a="
        )


class TestCanonicalizePath(unittest.TestCase):
    def test_11_resolve_dot(self):
        self.assertEqual(
            canonicalize("http://example.com/a/./b"),
            "http://example.com/a/b"
        )

    def test_12_resolve_dotdot(self):
        self.assertEqual(
            canonicalize("http://example.com/a/b/../c"),
            "http://example.com/a/c"
        )

    def test_13_multiple_slashes(self):
        self.assertEqual(
            canonicalize("http://example.com/a//b///c"),
            "http://example.com/a/b/c"
        )

    def test_14_decode_unreserved(self):
        # %2D is "-" (unreserved)
        self.assertEqual(
            canonicalize("http://example.com/a%2Db"),
            "http://example.com/a-b"
        )

    def test_15_force_trailing(self):
        self.assertEqual(
            canonicalize("http://example.com/path", force_trailing_slash=True),
            "http://example.com/path/"
        )


class TestCanonicalizeScheme(unittest.TestCase):
    def test_16_force_https(self):
        self.assertEqual(
            canonicalize("http://example.com/", force_https=True),
            "https://example.com/"
        )

    def test_17_no_scheme(self):
        self.assertEqual(
            canonicalize("example.com/path"),
            "http://example.com/path"
        )


class TestEquivalence(unittest.TestCase):
    def test_18_equivalent(self):
        self.assertTrue(urls_equivalent(
            "HTTP://Example.COM:80/path?b=2&a=1",
            "http://example.com/path?a=1&b=2"
        ))

    def test_19_not_equivalent(self):
        self.assertFalse(urls_equivalent(
            "http://example.com/page1",
            "http://example.com/page2"
        ))


class TestDeterminism(unittest.TestCase):
    def test_20_1000_runs(self):
        u = "HTTP://Example.COM:80/Path/?b=2&a=1#frag"
        first = canonicalize(u)
        for _ in range(1000):
            self.assertEqual(canonicalize(u), first)


if __name__ == "__main__":
    unittest.main(verbosity=2)
