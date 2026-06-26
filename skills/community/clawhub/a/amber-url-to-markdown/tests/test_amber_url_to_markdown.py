#!/usr/bin/env python3
"""
Amber Url to Markdown - 单元测试

运行测试：
    pytest tests/ -v

或：
    python3 -m pytest tests/ -v
"""

import pytest
import os
import sys
import tempfile
import shutil

# 添加脚本路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, '..', 'scripts'))


# ============================================================================
# 测试 fetcher 模块
# ============================================================================

class TestFetcher:
    """测试 URL 请求模块"""
    
    def test_fetch_valid_url(self):
        """测试正常 URL 的请求"""
        from fetcher import fetch_url_content
        
        url = "https://example.com"
        content = fetch_url_content(url)
        
        assert content is not None
        assert "Example Domain" in content
    
    def test_fetch_404_url(self):
        """测试 404 页面的请求"""
        from fetcher import fetch_url_content
        
        url = "https://example.com/404-not-exist"
        content = fetch_url_content(url)
        
        assert content is None
    
    def test_fetch_timeout_url(self):
        """测试超时场景"""
        from fetcher import fetch_url_content
        
        # httpbin.org 的延迟接口，延迟 20 秒，超时 10 秒
        url = "https://httpbin.org/delay/20"
        content = fetch_url_content(url, timeout=10)
        
        assert content is None
    
    def test_fetch_invalid_url(self):
        """测试无效 URL"""
        from fetcher import fetch_url_content
        
        url = "not-a-valid-url"
        content = fetch_url_content(url)
        
        assert content is None
    
    def test_robots_txt_allowed(self):
        """测试 robots.txt 允许爬取"""
        from fetcher import is_allowed_by_robots
        
        url = "https://example.com"
        allowed = is_allowed_by_robots(url)
        
        # example.com 通常允许爬取
        assert allowed is True
    
    def test_batch_fetch(self):
        """测试批量抓取"""
        from fetcher import batch_fetch_urls
        
        urls = [
            "https://example.com",
            "https://example.org",
        ]
        
        results = batch_fetch_urls(urls, random_delay=False)
        
        assert len(results) > 0
        assert all(isinstance(r, tuple) and len(r) == 2 for r in results)


# ============================================================================
# 测试 parser 模块
# ============================================================================

class TestParser:
    """测试 HTML 解析模块"""
    
    def test_html_to_markdown_basic(self):
        """测试基本 HTML 转 Markdown"""
        from parser import html_to_markdown
        
        html = """
        <html>
            <body>
                <h1>标题</h1>
                <p>这是一个<strong>测试</strong>段落。</p>
            </body>
        </html>
        """
        
        md = html_to_markdown(html)
        
        assert "# 标题" in md
        assert "测试" in md
    
    def test_html_to_markdown_empty(self):
        """测试空 HTML"""
        from parser import html_to_markdown
        
        md = html_to_markdown("")
        assert md == ""
        
        md = html_to_markdown(None)
        assert md == ""
    
    def test_extract_title(self):
        """测试标题提取"""
        from parser import extract_title_from_html
        
        html = """
        <html>
            <head><title>测试页面</title></head>
            <body><h1>主标题</h1></body>
        </html>
        """
        
        title = extract_title_from_html(html)
        assert title == "测试页面"
    
    def test_extract_title_from_h1(self):
        """测试从 h1 提取标题"""
        from parser import extract_title_from_html
        
        html = """
        <html>
            <body><h1>主标题</h1></body>
        </html>
        """
        
        title = extract_title_from_html(html)
        assert title == "主标题"
    
    def test_optimize_code_blocks(self):
        """测试代码块优化"""
        from parser import optimize_html_for_markdown
        
        html = """
        <html>
            <body>
                <span>"""</span>
                <div>代码内容</div>
                <span>"""</span>
            </body>
        </html>
        """
        
        optimized = optimize_html_for_markdown(html)
        
        assert "<pre>" in optimized
        assert "<code>" in optimized


# ============================================================================
# 测试 utils 模块
# ============================================================================

class TestUtils:
    """测试工具函数模块"""
    
    def test_sanitize_title_basic(self):
        """测试基本标题清理"""
        from utils import sanitize_title
        
        title = "测试文章：如何学习 Python？"
        safe = sanitize_title(title)
        
        assert ":" not in safe
        assert "?" not in safe
        assert "测试文章" in safe
    
    def test_sanitize_title_special_chars(self):
        """测试特殊字符清理"""
        from utils import sanitize_title
        
        title = "Hello <World> 测试/文件名"
        safe = sanitize_title(title)
        
        assert "<" not in safe
        assert ">" not in safe
        assert "/" not in safe
    
    def test_sanitize_title_length(self):
        """测试标题长度限制"""
        from utils import sanitize_title
        
        title = "这是一篇非常非常非常非常非常非常非常非常长的文章标题需要截断"
        safe = sanitize_title(title, max_length=20)
        
        assert len(safe) <= 20
    
    def test_sanitize_title_empty(self):
        """测试空标题"""
        from utils import sanitize_title
        
        safe = sanitize_title("")
        assert safe == "untitled"
        
        safe = sanitize_title("   ")
        assert safe == "untitled"
    
    def test_format_timestamp(self):
        """测试时间戳格式"""
        from utils import format_timestamp
        import re
        
        ts = format_timestamp()
        
        # 格式：YYYYMMDD_HHMMSS
        assert re.match(r'\d{8}_\d{6}', ts)
    
    def test_create_output_directories(self):
        """测试创建输出目录"""
        from utils import create_output_directories
        
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        
        try:
            output_dir, images_dir = create_output_directories(
                output_dir=temp_dir,
                download_images=True
            )
            
            assert os.path.exists(output_dir)
            assert os.path.exists(images_dir)
            
        finally:
            shutil.rmtree(temp_dir)
    
    def test_download_image(self):
        """测试图片下载"""
        from utils import download_image
        
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        
        try:
            img_url = "https://example.com/image.jpg"
            save_path = os.path.join(temp_dir, "test.jpg")
            
            # 这个测试可能会失败（取决于网络）
            result = download_image(img_url, save_path)
            
            # 不强制要求成功（可能网络问题）
            # 如果成功，文件应该存在
            if result:
                assert os.path.exists(save_path)
                
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


# ============================================================================
# 测试主流程
# ============================================================================

class TestMainFlow:
    """测试主流程"""
    
    def test_wechat_url_recognition(self):
        """测试微信公众号 URL 识别"""
        from url_handler import get_url_config, identify_url
        from fetcher import LinkType
        
        url = "https://mp.weixin.qq.com/s/xxx"
        link_type = identify_url(url)
        
        assert link_type == LinkType.WECHAT
    
    def test_zhihu_url_recognition(self):
        """测试知乎 URL 识别"""
        from url_handler import get_url_config, identify_url
        from fetcher import LinkType
        
        url = "https://zhuanlan.zhihu.com/p/xxx"
        link_type = identify_url(url)
        
        assert link_type == LinkType.ZHIHU
    
    def test_juejin_url_recognition(self):
        """测试掘金 URL 识别"""
        from url_handler import get_url_config, identify_url
        from fetcher import LinkType
        
        url = "https://juejin.cn/post/xxx"
        link_type = identify_url(url)
        
        assert link_type == LinkType.JUEJIN


# ============================================================================
# 运行测试
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
