"""Tests — axiom-markdown-link-auditor """

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent))

from axiom_markdown_link_auditor import (
    BARE_URL_PATTERN,
    audit,
    check_url,
    extract_links,
)


class TestExtractLinks(unittest.TestCase):
    def test_01_simple_link(self):
        md = "[text](https://example.com)"
        links = extract_links(md)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["url"], "https://example.com")
        self.assertEqual(links[0]["text"], "text")

    def test_02_image(self):
        md = "![alt](https://example.com/img.png)"
        links = extract_links(md)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["type"], "image")

    def test_03_bare_url(self):
        md = "Visit https://example.com for more"
        links = extract_links(md)
        self.assertGreaterEqual(len(links), 1)

    def test_04_mixed(self):
        md = """
# Title

[link1](https://a.com)
![img](https://b.com/p.png)
Bare: https://c.com
"""
        links = extract_links(md)
        self.assertEqual(len(links), 3)
        types = [l["type"] for l in links]
        self.assertIn("link", types)
        self.assertIn("image", types)
        self.assertIn("bare_url", types)

    def test_05_line_numbers(self):
        md = "para 1\n\n[link](https://a.com)\n"
        links = extract_links(md)
        self.assertEqual(links[0]["line"], 3)

    def test_06_empty(self):
        self.assertEqual(extract_links(""), [])


class TestCheckUrl(unittest.TestCase):
    def test_07_skip_non_http(self):
        result = check_url("mailto:foo@bar.com")
        self.assertTrue(result.get("skipped"))

    def test_08_invalid_url(self):
        result = check_url("https://this-domain-does-not-exist-12345.invalid")
        self.assertFalse(result.get("ok", True))


class TestAudit(unittest.TestCase):
    def test_09_basic(self):
        md = "[a](https://x.com) [b](https://y.com)"
        result = audit(md)
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["by_type"]["link"], 2)

    def test_10_no_remote(self):
        md = "[a](https://x.com)"
        result = audit(md, check_remote=False)
        self.assertNotIn("broken_count", result)


class TestDeterminism(unittest.TestCase):
    def test_11_1000_runs(self):
        md = "[a](https://x.com) [b](https://y.com)"
        first = extract_links(md)
        for _ in range(1000):
            self.assertEqual(extract_links(md), first)


if __name__ == "__main__":
    unittest.main(verbosity=2)
