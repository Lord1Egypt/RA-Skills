#!/usr/bin/env python3
"""
test_extractor.py - extractor.py 的测试用例

运行方式：
    python test_extractor.py          # 直接运行
    python -m pytest test_extractor.py -v  # 使用 pytest
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# 确保可以导入同目录的 extractor
sys.path.insert(0, str(Path(__file__).parent))
from extractor import PageExtractor, load_html_from_file


# ── 测试用 HTML 样本 ──────────────────────────────────────────────

SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head><title>测试页面</title></head>
<body>
    <div id="main">
        <h1 class="title">产品名称 ABC-123</h1>
        <div class="product-info">
            <span class="price">¥299.00</span>
            <span class="original-price">¥399.00</span>
            <p class="description">这是一款高质量产品，适合家庭使用。</p>
            <ul class="specs">
                <li>重量: 1.5kg</li>
                <li>尺寸: 30x20x10cm</li>
                <li>颜色: 白色</li>
            </ul>
        </div>
        <div class="contact">
            <a href="mailto:sales@example.com">联系我们</a>
            <p>邮箱: sales@example.com</p>
            <a href="tel:+8613800138000">电话: 13800138000</a>
            <p>地址: 广东省佛山市顺德区美的总部</p>
        </div>
        <div class="reviews">
            <div class="review">
                <span class="author">张三</span>
                <span class="rating">5</span>
                <p class="content">非常好用！</p>
            </div>
            <div class="review">
                <span class="author">李四</span>
                <span class="rating">4</span>
                <p class="content">性价比不错</p>
            </div>
        </div>
    </div>
</body>
</html>
"""


class TestCSSExtraction(unittest.TestCase):
    """测试 CSS Selector 提取。"""

    def setUp(self):
        self.ext = PageExtractor(SAMPLE_HTML)

    def test_single_element(self):
        """提取单个元素。"""
        result = self.ext.extract_by_css({"title": "h1.title"})
        self.assertEqual(result["title"], "产品名称 ABC-123")

    def test_multiple_elements_simple(self):
        """简单选择器提取多个元素（默认返回第一个）。"""
        result = self.ext.extract_by_css({"spec": "ul.specs li"})
        self.assertEqual(result["spec"], "重量: 1.5kg")

    def test_multiple_elements_all(self):
        """提取所有匹配元素。"""
        result = self.ext.extract_by_css({
            "specs": {"selector": "ul.specs li", "all": True}
        })
        self.assertIsInstance(result["specs"], list)
        self.assertEqual(len(result["specs"]), 3)
        self.assertIn("重量: 1.5kg", result["specs"])
        self.assertIn("颜色: 白色", result["specs"])

    def test_attribute_extraction(self):
        """提取属性值。"""
        result = self.ext.extract_by_css({
            "email_link": {"selector": "a[href^='mailto']", "attr": "href"}
        })
        self.assertEqual(result["email_link"], "mailto:sales@example.com")

    def test_no_match_returns_none(self):
        """无匹配返回 None。"""
        result = self.ext.extract_by_css({"nonexistent": ".does-not-exist"})
        self.assertIsNone(result["nonexistent"])

    def test_multiple_fields(self):
        """批量提取多个字段。"""
        result = self.ext.extract_by_css({
            "title": "h1.title",
            "price": "span.price",
            "desc": "p.description",
        })
        self.assertEqual(result["title"], "产品名称 ABC-123")
        self.assertEqual(result["price"], "¥299.00")
        self.assertEqual(result["desc"], "这是一款高质量产品，适合家庭使用。")


class TestXPathExtraction(unittest.TestCase):
    """测试 XPath 提取。"""

    def setUp(self):
        self.ext = PageExtractor(SAMPLE_HTML)

    def test_text_extraction(self):
        """提取文本内容。"""
        result = self.ext.extract_by_xpath({
            "title": {"xpath": "//h1/text()", "all": False}
        })
        self.assertEqual(result["title"], "产品名称 ABC-123")

    def test_all_items(self):
        """提取所有列表项。"""
        result = self.ext.extract_by_xpath({"specs": "//ul[@class='specs']/li/text()"})
        self.assertIsInstance(result["specs"], list)
        self.assertEqual(len(result["specs"]), 3)

    def test_attribute_extraction(self):
        """提取属性值。"""
        result = self.ext.extract_by_xpath({
            "email": {"xpath": "//a[contains(@href,'mailto')]/@href", "all": False}
        })
        self.assertIn("sales@example.com", result["email"])

    def test_single_result(self):
        """只取第一个结果。"""
        result = self.ext.extract_by_xpath({
            "first_spec": {"xpath": "//ul[@class='specs']/li/text()", "all": False}
        })
        self.assertEqual(result["first_spec"], "重量: 1.5kg")

    def test_no_match(self):
        """无匹配返回 None。"""
        result = self.ext.extract_by_xpath({"none": "//nonexistent/text()"})
        self.assertIsNone(result["none"])

    def test_complex_xpath(self):
        """复杂 XPath 表达式。"""
        result = self.ext.extract_by_xpath({
            "review_authors": "//div[@class='review']/span[@class='author']/text()"
        })
        self.assertIsInstance(result["review_authors"], list)
        self.assertIn("张三", result["review_authors"])
        self.assertIn("李四", result["review_authors"])


class TestRegexExtraction(unittest.TestCase):
    """测试正则表达式提取。"""

    def setUp(self):
        self.ext = PageExtractor(SAMPLE_HTML)

    def test_email_extraction(self):
        """提取邮箱。"""
        result = self.ext.extract_by_regex({"email": r"[\w.]+@[\w.]+"})
        self.assertIsNotNone(result["email"])
        # 默认 all=True，返回列表
        self.assertIn("sales@example.com", result["email"])

    def test_phone_extraction(self):
        """提取手机号。"""
        result = self.ext.extract_by_regex({
            "phone": {"pattern": r"1[3-9]\d{9}", "all": False}
        })
        self.assertEqual(result["phone"], "13800138000")

    def test_price_extraction(self):
        """提取价格。"""
        result = self.ext.extract_by_regex({
            "prices": {"pattern": r"¥(\d+\.\d{2})", "all": True}
        })
        self.assertIsNotNone(result["prices"])
        self.assertIn("299.00", result["prices"])
        self.assertIn("399.00", result["prices"])

    def test_no_match(self):
        """无匹配返回 None。"""
        result = self.ext.extract_by_regex({"none": r"IMPOSSIBLE_PATTERN_XYZ"})
        self.assertIsNone(result["none"])

    def test_case_insensitive(self):
        """忽略大小写。"""
        html = "<p>Contact: Admin@Example.COM</p>"
        ext = PageExtractor(html)
        result = ext.extract_by_regex({
            "email": {"pattern": r"admin@example\.com", "ignorecase": True, "all": False}
        })
        self.assertEqual(result["email"], "Admin@Example.COM")


class TestBatchExtraction(unittest.TestCase):
    """测试多字段批量提取。"""

    def setUp(self):
        self.ext = PageExtractor(SAMPLE_HTML)

    def test_mixed_methods(self):
        """混合使用多种提取方式。"""
        result = self.ext.extract_all(
            css={"title": "h1.title", "price": "span.price"},
            xpath={"specs": "//ul[@class='specs']/li/text()"},
            regex={"phone": {"pattern": r"1[3-9]\d{9}", "all": False}},
        )
        self.assertEqual(result["title"], "产品名称 ABC-123")
        self.assertEqual(result["price"], "¥299.00")
        self.assertIsInstance(result["specs"], list)
        self.assertEqual(result["phone"], "13800138000")

    def test_extract_all_empty(self):
        """所有方式都为空时返回空 dict。"""
        result = self.ext.extract_all()
        self.assertEqual(result, {})


class TestFileInput(unittest.TestCase):
    """测试从文件加载 HTML。"""

    def test_load_from_file(self):
        """从临时文件加载并提取。"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(SAMPLE_HTML)
            temp_path = f.name

        try:
            html = load_html_from_file(temp_path)
            ext = PageExtractor(html)
            result = ext.extract_by_css({"title": "h1"})
            self.assertEqual(result["title"], "产品名称 ABC-123")
        finally:
            os.unlink(temp_path)

    def test_file_not_found(self):
        """文件不存在时抛出异常。"""
        with self.assertRaises(FileNotFoundError):
            load_html_from_file("/nonexistent/path/page.html")


class TestEdgeCases(unittest.TestCase):
    """边界情况测试。"""

    def test_empty_html(self):
        """空 HTML 不崩溃。"""
        ext = PageExtractor("")
        result = ext.extract_by_css({"title": "h1"})
        self.assertIsNone(result["title"])

    def test_malformed_html(self):
        """格式错误的 HTML 能容错处理。"""
        html = "<h1>Unclosed heading<div><p>Nested wrong</h1></div>"
        ext = PageExtractor(html)
        result = ext.extract_by_css({"heading": "h1"})
        self.assertIsNotNone(result["heading"])

    def test_unicode_content(self):
        """Unicode 内容正确处理。"""
        html = "<p>日本語テスト 中文测试 한국어</p>"
        ext = PageExtractor(html)
        result = ext.extract_by_css({"text": "p"})
        self.assertIn("中文测试", result["text"])


class TestLLMExtraction(unittest.TestCase):
    """LLM 提取测试（使用 mock）。"""

    @patch("extractor.urllib.request.urlopen")
    def test_llm_basic_extraction(self, mock_urlopen):
        """基本 LLM 提取：mock API 返回 JSON。"""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "choices": [{"message": {"content": '{"title": "Test Page", "author": "John"}'}}]
        }).encode("utf-8")
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        ext = PageExtractor("<html><body><h1>Test Page</h1><p>By John</p></body></html>")
        result = ext.extract_by_llm(["title", "author"])
        self.assertEqual(result["title"], "Test Page")
        self.assertEqual(result["author"], "John")

    @patch("extractor.urllib.request.urlopen")
    def test_llm_markdown_wrapped_json(self, mock_urlopen):
        """LLM 返回 markdown code block 包裹的 JSON。"""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "choices": [{"message": {"content": '```json\n{"price": "99.99"}\n```'}}]
        }).encode("utf-8")
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        ext = PageExtractor("<p>Price: $99.99</p>")
        result = ext.extract_by_llm(["price"])
        self.assertEqual(result["price"], "99.99")

    @patch("extractor.urllib.request.urlopen")
    def test_llm_null_fields(self, mock_urlopen):
        """LLM 返回 null 表示字段不存在。"""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "choices": [{"message": {"content": '{"title": "Found", "missing_field": null}'}}]
        }).encode("utf-8")
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        ext = PageExtractor("<h1>Found</h1>")
        result = ext.extract_by_llm(["title", "missing_field"])
        self.assertEqual(result["title"], "Found")
        self.assertIsNone(result["missing_field"])

    def test_llm_connection_error(self):
        """LLM API 不可达时抛出 ConnectionError。"""
        ext = PageExtractor("<p>test</p>")
        with self.assertRaises(ConnectionError):
            ext.extract_by_llm(
                ["field"],
                base_url="http://localhost:99999/v1",  # 不存在的端口
            )

    @patch("extractor.urllib.request.urlopen")
    def test_llm_html_truncation(self, mock_urlopen):
        """超长 HTML 被截断。"""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "choices": [{"message": {"content": '{"title": "ok"}'}}]
        }).encode("utf-8")
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        long_html = "<p>" + "x" * 20000 + "</p>"
        ext = PageExtractor(long_html)
        result = ext.extract_by_llm(["title"], max_html_chars=5000)
        # 验证调用时 HTML 被截断
        call_args = mock_urlopen.call_args
        request = call_args[0][0]
        body = json.loads(request.data.decode("utf-8"))
        self.assertIn("truncated", body["messages"][1]["content"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
