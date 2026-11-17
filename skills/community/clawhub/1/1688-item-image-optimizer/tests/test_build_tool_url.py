"""build_tool_url 单元测试 — 覆盖 URL 构建 + 参数校验"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from capabilities.build_tool_url.service import build_tool_url, BASE_URL


class BuildToolUrlMainTest(unittest.TestCase):
    """主图优化 — type=main"""

    def test_main_with_img_url(self):
        result = build_tool_url(type_="main", img_url="/Users/seller/Desktop/product.jpg")
        self.assertTrue(result["success"])
        url = result["data"]["open_tab"]["url"]
        self.assertIn("type=oneOptimization", url)
        self.assertIn("imgUrl=", url)
        self.assertEqual(result["data"]["open_tab"]["title"], "主图优化")

    def test_main_with_offer_id(self):
        result = build_tool_url(type_="main", img_url="/path/img.jpg", offer_id="123456")
        url = result["data"]["open_tab"]["url"]
        self.assertIn("offerId=123456", url)

    def test_main_url_encode(self):
        """imgUrl 值必须经过 URL encode"""
        result = build_tool_url(type_="main", img_url="/Users/航神/图片.jpg")
        url = result["data"]["open_tab"]["url"]
        self.assertNotIn("航神", url)
        self.assertIn("imgUrl=", url)

    def test_main_missing_img_url(self):
        """type=main 时缺少 img_url 仍可打开工具页（页面自带上传入口）"""
        result = build_tool_url(type_="main")
        self.assertTrue(result["success"])
        url = result["data"]["open_tab"]["url"]
        self.assertIn("type=oneOptimization", url)
        self.assertNotIn("imgUrl=", url)

    def test_main_empty_img_url(self):
        """img_url 为空字符串应失败"""
        result = build_tool_url(type_="main", img_url="")
        self.assertFalse(result["success"])
        self.assertIn("图片路径无效", result["markdown"])


class BuildToolUrlCarouselTest(unittest.TestCase):
    """轮播图 — type=carousel"""

    def test_carousel_with_img_url_list(self):
        result = build_tool_url(type_="carousel", img_url_list="/path/1.jpg,/path/2.jpg")
        self.assertTrue(result["success"])
        url = result["data"]["open_tab"]["url"]
        self.assertIn("type=carouselImage", url)
        self.assertIn("imgUrlList=", url)
        self.assertEqual(result["data"]["open_tab"]["title"], "轮播图制作")

    def test_carousel_missing_img_url_list(self):
        """轮播图缺少图片仍可打开工具页"""
        result = build_tool_url(type_="carousel")
        self.assertTrue(result["success"])
        url = result["data"]["open_tab"]["url"]
        self.assertIn("type=carouselImage", url)
        self.assertNotIn("imgUrlList=", url)

    def test_carousel_empty_img_url_list(self):
        result = build_tool_url(type_="carousel", img_url_list="")
        self.assertFalse(result["success"])

    def test_carousel_img_url_mismatch_fails(self):
        """多图工具误传 img_url 应报错（C-4：不再静默忽略，让 LLM 自纠）"""
        result = build_tool_url(type_="carousel", img_url="/path/single.jpg")
        self.assertFalse(result["success"])
        self.assertIn("多图工具", result["markdown"])
        self.assertIn("--img-url-list", result["markdown"])
        self.assertEqual(result["data"], {})


class BuildToolUrlDetailTest(unittest.TestCase):
    """详情图 — type=detail"""

    def test_detail_with_img_url_list(self):
        result = build_tool_url(type_="detail", img_url_list="/path/1.jpg,/path/2.jpg,/path/3.jpg")
        self.assertTrue(result["success"])
        url = result["data"]["open_tab"]["url"]
        self.assertIn("type=detailImage", url)
        self.assertEqual(result["data"]["open_tab"]["title"], "详情图制作")

    def test_detail_missing_img_url_list(self):
        """详情图缺少图片仍可打开工具页"""
        result = build_tool_url(type_="detail")
        self.assertTrue(result["success"])
        url = result["data"]["open_tab"]["url"]
        self.assertIn("type=detailImage", url)
        self.assertNotIn("imgUrlList=", url)


class BuildToolUrlSingleImageToolTest(unittest.TestCase):
    """新增单图工具 — matting / replaceSubject / outpainting / digitalModel"""

    CASES = [
        ("matting",               "白底图"),
        ("replaceSubject",        "背景替换"),
        ("outpainting",           "一键扩图"),
        ("digitalModel",          "数字模特"),
    ]

    def test_with_img_url(self):
        """传 img_url：URL 含 type 与 imgUrl，title 正确，且不带 imgUrlList"""
        for type_, title in self.CASES:
            with self.subTest(type_=type_):
                result = build_tool_url(type_=type_, img_url="/path/product.jpg")
                self.assertTrue(result["success"])
                url = result["data"]["open_tab"]["url"]
                self.assertIn(f"type={type_}", url)
                self.assertIn("imgUrl=", url)
                self.assertNotIn("imgUrlList=", url)
                self.assertEqual(result["data"]["open_tab"]["title"], title)

    def test_missing_img_url(self):
        """缺图仍可打开工具页（页面自带上传入口）"""
        for type_, _title in self.CASES:
            with self.subTest(type_=type_):
                result = build_tool_url(type_=type_)
                self.assertTrue(result["success"])
                url = result["data"]["open_tab"]["url"]
                self.assertIn(f"type={type_}", url)
                self.assertNotIn("imgUrl=", url)

    def test_img_url_list_mismatch_fails(self):
        """单图工具误传 img_url_list 应报错（C-4：不再静默忽略，让 LLM 自纠）"""
        result = build_tool_url(type_="matting", img_url_list="/path/1.jpg,/path/2.jpg")
        self.assertFalse(result["success"])
        self.assertIn("单图工具", result["markdown"])
        self.assertIn("--img-url", result["markdown"])
        self.assertEqual(result["data"], {})

    def test_empty_img_url(self):
        """img_url 为空字符串应失败"""
        result = build_tool_url(type_="matting", img_url="")
        self.assertFalse(result["success"])
        self.assertIn("图片路径无效", result["markdown"])


class BuildToolUrlValidationTest(unittest.TestCase):
    """参数校验"""

    def test_invalid_type(self):
        result = build_tool_url(type_="invalid")
        self.assertFalse(result["success"])
        self.assertIn("不支持", result["markdown"])

    def test_base_url_present(self):
        """所有成功结果的 URL 必须包含基础 URL"""
        result = build_tool_url(type_="main", img_url="/path/img.jpg")
        url = result["data"]["open_tab"]["url"]
        self.assertTrue(url.startswith(BASE_URL))

    def test_success_no_open_tab(self):
        """失败结果不应包含 open_tab 数据"""
        result = build_tool_url(type_="invalid")
        self.assertEqual(result["data"], {})


if __name__ == "__main__":
    unittest.main()
