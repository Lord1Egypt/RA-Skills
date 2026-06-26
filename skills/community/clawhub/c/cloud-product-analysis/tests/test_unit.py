"""
Unit tests for cloud_doc_scraper.py core functions
Run: pytest tests/test_unit.py -v
"""
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from cloud_doc_scraper import (
    score_link,
    denoise_text,
    is_security_block,
    is_404_page,
    huawei_cn_to_com,
    PRIORITY_KEYWORDS,
)


class TestScoreLink:
    """Test link scoring logic"""

    def test_product_overview_high_score(self):
        assert score_link("产品概述", "/product-overview") >= 3
        assert score_link("What is ECS", "/what-is") >= 3

    def test_specs_medium_score(self):
        score = score_link("实例规格", "/specs")
        assert 2 <= score < 3

    def test_pricing_medium_score(self):
        score = score_link("计费说明", "/pricing")
        assert 2 <= score < 3

    def test_faq_negative_score(self):
        assert score_link("常见问题", "/faq") < 0
        assert score_link("FAQ", "/faq") < 0

    def test_sdk_negative_score(self):
        assert score_link("SDK参考", "/sdk") < 0
        assert score_link("API Reference", "/api") < 0

    def test_component_version_high_score(self):
        score = score_link("组件版本", "/components")
        assert score == 2

    def test_scenario_positive_score(self):
        score = score_link("应用场景", "/scenarios")
        assert score == 1


class TestDenoiseText:
    """Test content denoising"""

    def test_remove_noise_patterns(self):
        text = "产品介绍\n为什么选择阿里云\n核心功能"
        result = denoise_text(text)
        assert "为什么选择阿里云" not in result
        assert "产品介绍" in result
        assert "核心功能" in result

    def test_remove_footer_noise(self):
        text = "内容\n法律声明\nCookies政策\n联系我们"
        result = denoise_text(text)
        assert "法律声明" not in result
        assert "Cookies政策" not in result
        assert "联系我们" not in result
        assert "内容" in result

    def test_remove_tencent_security_noise(self):
        text = "正文内容\nProtected by Tencent\n正在验证连接安全性"
        result = denoise_text(text)
        assert "Protected by Tencent" not in result
        assert "正在验证连接安全性" not in result
        assert "正文内容" in result

    def test_collapse_multiple_empty_lines(self):
        text = "Line1\n\n\n\nLine2"
        result = denoise_text(text)
        assert result.count("\n\n") <= 1

    def test_preserve_content_structure(self):
        text = "标题\n\n段落1\n段落2"
        result = denoise_text(text)
        assert "标题" in result
        assert "段落1" in result
        assert "段落2" in result


class TestSecurityBlock:
    """Test security block detection"""

    def test_detect_tencent_block(self):
        assert is_security_block("正在验证连接安全性")
        assert is_security_block("Protected by Tencent Cloud EdgeOne")
        assert is_security_block("Security Verification in progress")

    def test_normal_content_not_blocked(self):
        assert not is_security_block("产品概述：这是一个云服务产品")
        assert not is_security_block("This is normal documentation content")


class Test404Detection:
    """Test 404 page detection"""

    def test_detect_huawei_404(self):
        assert is_404_page("很抱歉，没发现您要的页面")
        assert is_404_page("抱歉，很抱歉，没发现您要的页面，请检查链接")

    def test_normal_content_not_404(self):
        assert not is_404_page("产品概述")
        assert not is_404_page("This is documentation content")


class TestDomainFallback:
    """Test domain fallback logic"""

    def test_huawei_cn_to_com_conversion(self):
        cn_url = "https://support.huaweicloud.cn/obs/index.html"
        com_url = huawei_cn_to_com(cn_url)
        assert "huaweicloud.com" in com_url
        assert "huaweicloud.cn" not in com_url

    def test_preserve_non_huawei_urls(self):
        url = "https://help.aliyun.com/zh/oss"
        assert huawei_cn_to_com(url) == url.replace("support.huaweicloud.cn", "support.huaweicloud.com")


class TestPriorityKeywords:
    """Test keyword priority configuration"""

    def test_keywords_structure(self):
        assert isinstance(PRIORITY_KEYWORDS, list)
        for item in PRIORITY_KEYWORDS:
            assert len(item) == 2
            weight, keywords = item
            assert isinstance(weight, int)
            assert isinstance(keywords, list)
            assert all(isinstance(k, str) for k in keywords)

    def test_keywords_coverage(self):
        # Check essential categories are covered
        all_keywords = " ".join(
            " ".join(keywords) for _, keywords in PRIORITY_KEYWORDS
        ).lower()
        assert "产品概述" in all_keywords or "what is" in all_keywords
        assert "规格" in all_keywords or "specification" in all_keywords
        assert "计费" in all_keywords or "pricing" in all_keywords
        assert "应用场景" in all_keywords or "scenario" in all_keywords


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
