"""
电商产品描述批量生成器 - 测试用例
覆盖：基础功能、CSV批量生成、输出格式、关键词覆盖、空输入处理
"""

import pytest
import csv
import io
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from generator import (
    ProductDescGenerator, parse_csv_input, generate_amazon,
    generate_taobao, generate_pinduoduo, generate_tiktok,
    generate_shopify, build_vars, fill_template
)


class TestBuildVars:
    """测试变量构建"""

    def test_build_vars_basic(self):
        vars_d = build_vars("蓝牙耳机", "3C数码", "无线,降噪,运动", "某品牌", "199")
        assert vars_d["product_name"] == "蓝牙耳机"
        assert vars_d["category"] == "3C数码"
        assert "无线" in vars_d["keywords"]
        assert "降噪" in vars_d["keywords"]
        assert vars_d["brand"] == "某品牌"

    def test_build_vars_empty_keywords(self):
        vars_d = build_vars("充电宝", "电子产品", "", "", "")
        assert vars_d["product_name"] == "充电宝"
        assert vars_d["keywords"] == "充电宝"

    def test_build_vars_no_brand(self):
        vars_d = build_vars("水杯", "日用品", "大容量", "", "")
        assert vars_d["brand"] == "PremiumBrand"


class TestFillTemplate:
    """测试模板填充"""

    def test_fill_simple(self):
        result = fill_template("Hello {name}", {"name": "World"})
        assert result == "Hello World"

    def test_fill_multiple(self):
        result = fill_template("{a} {b} {a}", {"a": "X", "b": "Y"})
        assert result == "X Y X"

    def test_fill_no_replace(self):
        result = fill_template("Hello {name}", {"other": "X"})
        assert result == "Hello {name}"


class TestAmazonGenerator:
    """测试亚马逊生成器"""

    def test_amazon_title_not_empty(self):
        result = generate_amazon("蓝牙耳机", "3C数码", "无线", "品牌X", "199")
        assert len(result["title"]) > 0
        assert len(result["title"]) <= 210  # 200 + ...

    def test_amazon_bullets_count(self):
        result = generate_amazon("蓝牙耳机", "3C数码", "无线")
        assert len(result["bullets"]) == 5

    def test_amazon_description_has_product_name(self):
        result = generate_amazon("蓝牙耳机", "3C数码", "无线")
        assert "蓝牙耳机" in result["description"]
        assert len(result["description"]) > 100


class TestTaobaoGenerator:
    """测试淘宝生成器"""

    def test_taobao_title_length_limit(self):
        result = generate_taobao("真丝围巾", "服饰", "保暖", "某品牌", "299")
        assert len(result["title"]) <= 30

    def test_taobao_description_has_product_name(self):
        result = generate_taobao("真丝围巾", "服饰", "保暖")
        assert "真丝围巾" in result["description"]


class TestPinduoduoGenerator:
    """测试拼多多生成器"""

    def test_pinduoduo_title_length_limit(self):
        result = generate_pinduoduo("纸巾", "日用品", "柔软", "品牌", "19.9")
        assert len(result["title"]) <= 30

    def test_pinduoduo_description_contains_price_signal(self):
        result = generate_pinduoduo("纸巾", "日用品", "柔软")
        assert "拼团" in result["description"] or "价格" in result["description"]


class TestTikTokGenerator:
    """测试TikTok Shop生成器"""

    def test_tiktok_title_has_emoji(self):
        result = generate_tiktok("运动水壶", "户外", "大容量")
        assert "✨" in result["title"] or "😍" in result["title"] or "Must-Have" in result["title"]

    def test_tiktok_bullets_count(self):
        result = generate_tiktok("运动水壶", "户外", "大容量")
        assert len(result["bullets"]) == 5


class TestShopifyGenerator:
    """测试Shopify生成器"""

    def test_shopify_title_has_brand(self):
        result = generate_shopify("咖啡机", "家电", "全自动", "MyCafe", "999")
        assert "MyCafe" in result["title"]

    def test_shopify_description_has_sections(self):
        result = generate_shopify("咖啡机", "家电", "全自动")
        assert "Key Features" in result["description"] or "Overview" in result["description"]


class TestProductDescGenerator:
    """测试主生成器类"""

    def test_generate_single_all_platforms(self):
        gen = ProductDescGenerator()
        results = gen.generate_single("蓝牙耳机", "3C数码", "无线")
        assert "amazon" in results
        assert "taobao" in results
        assert "pinduoduo" in results
        assert "tiktok" in results
        assert "shopify" in results

    def test_generate_single_specific_platforms(self):
        gen = ProductDescGenerator()
        results = gen.generate_single("充电宝", "电子产品", "", platforms=["amazon", "taobao"])
        assert "amazon" in results
        assert "taobao" in results
        assert "tiktok" not in results

    def test_generate_single_label_names(self):
        gen = ProductDescGenerator()
        results = gen.generate_single("水杯", "日用品", "")
        assert results["amazon"]["label"] == "亚马逊"
        assert results["taobao"]["label"] == "淘宝"
        assert results["pinduoduo"]["label"] == "拼多多"
        assert results["tiktok"]["label"] == "TikTok Shop"
        assert results["shopify"]["label"] == "Shopify"

    def test_to_markdown_output(self):
        gen = ProductDescGenerator()
        results = gen.generate_single("蓝牙耳机", "3C数码", "无线")
        md = gen.to_markdown(results, "蓝牙耳机")
        assert "蓝牙耳机" in md
        assert "亚马逊" in md
        assert "**标题**" in md
        assert "详情描述" in md

    def test_to_txt_output(self):
        gen = ProductDescGenerator()
        results = gen.generate_single("蓝牙耳机", "3C数码", "无线")
        txt = gen.to_txt(results, "蓝牙耳机")
        assert "===" in txt
        assert "蓝牙耳机" in txt

    def test_to_csv_output(self):
        gen = ProductDescGenerator()
        results = gen.generate_single("蓝牙耳机", "3C数码", "无线")
        csv_str = gen.to_csv(results)
        reader = csv.DictReader(io.StringIO(csv_str))
        rows = list(reader)
        assert len(rows) == 5  # 5 platforms
        assert rows[0]["平台"] == "亚马逊"


class TestBatchGeneration:
    """测试批量生成"""

    def test_batch_two_products(self):
        gen = ProductDescGenerator()
        products = [
            {"product_name": "蓝牙耳机", "category": "3C数码", "keywords": "无线"},
            {"product_name": "充电宝", "category": "电子产品", "keywords": "大容量"},
        ]
        result = gen.generate_batch(products, platforms=["amazon"], output_format="markdown")
        assert "蓝牙耳机" in result
        assert "充电宝" in result
        assert "亚马逊" in result

    def test_batch_csv_format(self):
        gen = ProductDescGenerator()
        products = [
            {"product_name": "蓝牙耳机", "category": "3C数码", "keywords": "无线"},
            {"product_name": "充电宝", "category": "电子产品", "keywords": "大容量"},
        ]
        csv_out = gen.generate_batch(products, platforms=["amazon"], output_format="csv")
        reader = csv.DictReader(io.StringIO(csv_out))
        rows = list(reader)
        assert len(rows) == 2


class TestCSVParser:
    """测试CSV解析"""

    def test_parse_basic_csv(self):
        csv_text = "product_name,category,keywords\n蓝牙耳机,3C数码,无线\n充电宝,电子产品,大容量"
        products = parse_csv_input(csv_text)
        assert len(products) == 2
        assert products[0]["product_name"] == "蓝牙耳机"
        assert products[1]["keywords"] == "大容量"

    def test_parse_csv_chinese_headers(self):
        csv_text = "产品名称,类目,关键词\n真丝围巾,服饰,保暖"
        products = parse_csv_input(csv_text)
        assert len(products) == 1
        assert products[0]["product_name"] == "真丝围巾"

    def test_parse_csv_skips_empty(self):
        csv_text = "product_name,category\n蓝牙耳机,3C\n,,"  # empty row
        products = parse_csv_input(csv_text)
        assert len(products) == 1


class TestEdgeCases:
    """边界情况测试"""

    def test_empty_product_name(self):
        gen = ProductDescGenerator()
        results = gen.generate_single("", "3C数码", "无线")
        # 应该仍然生成内容（用空字符串作为product_name）
        assert "amazon" in results

    def test_special_chars_in_product_name(self):
        gen = ProductDescGenerator()
        # 特殊字符会被 safe_keyword 处理，但模板用原始 product_name 插入
        results = gen.generate_single("蓝牙耳机（旗舰版）", "3C数码", "无线")
        assert "amazon" in results

    def test_all_platforms_seed_reproducible(self):
        """相同种子应该产生相同结果"""
        import random
        random.seed(42)
        gen1 = ProductDescGenerator()
        r1 = gen1.generate_single("测试产品", "测试类目", "关键词")
        random.seed(42)
        gen2 = ProductDescGenerator()
        r2 = gen2.generate_single("测试产品", "测试类目", "关键词")
        assert r1["amazon"]["title"] == r2["amazon"]["title"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
