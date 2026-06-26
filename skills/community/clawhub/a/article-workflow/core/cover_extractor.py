#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
封面图片提取器 - 从网页内容中提取封面图片

功能：
1. 从 Markdown/HTML 中提取第一张图片
2. 下载图片到本地
3. 上传到飞书云文档
4. 填充到 Bitable"封面图片"字段

设计原则：
- ✅ 不增加模型请求次数
- ✅ 自动提取和上传
- ✅ 支持多种图片格式
"""

import re
import os
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.parse import urljoin


class CoverImageExtractor:
    """封面图片提取器"""
    
    # 支持的图片格式
    SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
    
    # 图片尺寸要求（飞书）
    MAX_SIZE_MB = 10  # 最大 10MB
    MIN_WIDTH = 200   # 最小宽度
    MIN_HEIGHT = 200  # 最小高度
    
    def __init__(self, temp_dir: str = "/tmp/openclaw/covers"):
        """
        初始化提取器
        
        Args:
            temp_dir: 临时目录
        """
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_from_content(self, content: str, base_url: str = "") -> Optional[str]:
        """
        从内容中提取第一张图片 URL
        
        Args:
            content: 文章内容（Markdown/HTML）
            base_url: 基础 URL（用于解析相对路径）
        
        Returns:
            图片 URL 或 None
        """
        # 1. 匹配 Markdown 图片 ![alt](url)
        md_pattern = r'!\[.*?\]\((.*?)\)'
        md_matches = re.findall(md_pattern, content)
        
        if md_matches:
            img_url = md_matches[0]
            return self._resolve_url(img_url, base_url)
        
        # 2. 匹配 HTML 图片 <img src="url">
        html_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
        html_matches = re.findall(html_pattern, content, re.IGNORECASE)
        
        if html_matches:
            img_url = html_matches[0]
            return self._resolve_url(img_url, base_url)
        
        # 3. 匹配 HTML 图片（单引号）
        html_pattern_single = r"<img[^>]+src='([^']+)' "
        html_matches_single = re.findall(html_pattern_single, content, re.IGNORECASE)
        
        if html_matches_single:
            img_url = html_matches_single[0]
            return self._resolve_url(img_url, base_url)
        
        return None
    
    def _resolve_url(self, img_url: str, base_url: str) -> str:
        """
        解析图片 URL（处理相对路径）
        
        Args:
            img_url: 图片 URL（可能是相对路径）
            base_url: 基础 URL
        
        Returns:
            完整的图片 URL
        """
        if img_url.startswith('http://') or img_url.startswith('https://'):
            return img_url
        
        if base_url:
            return urljoin(base_url, img_url)
        
        return img_url
    
    async def download_and_upload(self, img_url: str, article_title: str) -> Optional[Dict[str, Any]]:
        """
        下载图片并上传到飞书
        
        Args:
            img_url: 图片 URL
            article_title: 文章标题
        
        Returns:
            飞书文件信息或 None
        
        Returns:
            {
                "file_token": "baxxxxxxx",
                "name": "cover.jpg",
                "size": 123456
            }
        """
        try:
            # 1. 下载图片
            local_path = await self._download_image(img_url, article_title)
            if not local_path:
                return None
            
            # 2. 验证图片
            if not self._validate_image(local_path):
                return None
            
            # 3. 上传到飞书
            # TODO: 调用飞书 API 上传
            # file_info = await feishu_drive_file.upload(
            #     file_path=str(local_path),
            #     parent_node="folder_token"
            # )
            
            # 演示用：返回模拟信息
            file_info = {
                "file_token": f"ba_{article_title[:10]}",
                "name": local_path.name,
                "size": local_path.stat().st_size
            }
            
            return file_info
            
        except Exception as e:
            print(f"❌ 下载上传失败：{e}")
            return None
    
    async def _download_image(self, img_url: str, article_title: str) -> Optional[Path]:
        """
        下载图片到本地
        
        Args:
            img_url: 图片 URL
            article_title: 文章标题
        
        Returns:
            本地文件路径或 None
        """
        try:
            # 生成文件名
            safe_title = self._sanitize_filename(article_title[:30])
            ext = self._get_file_extension(img_url)
            filename = f"{safe_title}{ext}"
            local_path = self.temp_dir / filename
            
            # TODO: 实际下载
            # import aiohttp
            # async with aiohttp.ClientSession() as session:
            #     async with session.get(img_url) as response:
            #         if response.status == 200:
            #             content = await response.read()
            #             with open(local_path, 'wb') as f:
            #                 f.write(content)
            
            # 演示用：创建空文件
            local_path.touch()
            
            return local_path
            
        except Exception as e:
            print(f"❌ 下载失败：{e}")
            return None
    
    def _validate_image(self, local_path: Path) -> bool:
        """
        验证图片
        
        Args:
            local_path: 本地文件路径
        
        Returns:
            是否有效
        """
        # 检查文件大小
        size_mb = local_path.stat().st_size / (1024 * 1024)
        if size_mb > self.MAX_SIZE_MB:
            print(f"⚠️  图片过大：{size_mb:.2f}MB > {self.MAX_SIZE_MB}MB")
            return False
        
        # 检查文件扩展名
        if local_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            print(f"⚠️  不支持的格式：{local_path.suffix}")
            return False
        
        # TODO: 检查图片尺寸
        # from PIL import Image
        # with Image.open(local_path) as img:
        #     if img.width < self.MIN_WIDTH or img.height < self.MIN_HEIGHT:
        #         return False
        
        return True
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        清理文件名（移除非法字符）
        
        Args:
            filename: 原始文件名
        
        Returns:
            清理后的文件名
        """
        # 移除非法字符
        illegal_chars = r'[<>:"/\\|？*]'
        sanitized = re.sub(illegal_chars, '_', filename)
        
        # 移除空格
        sanitized = sanitized.replace(' ', '_')
        
        return sanitized[:50]  # 限制长度
    
    def _get_file_extension(self, img_url: str) -> str:
        """
        从 URL 获取文件扩展名
        
        Args:
            img_url: 图片 URL
        
        Returns:
            文件扩展名（如 .jpg）
        """
        # 从 URL 提取扩展名
        parsed = img_url.split('?')[0]  # 移除查询参数
        
        for ext in self.SUPPORTED_FORMATS:
            if parsed.lower().endswith(ext):
                return ext
        
        # 默认返回 .jpg
        return '.jpg'


# 便捷函数
async def extract_cover_image(content: str, url: str = "", title: str = "") -> Optional[str]:
    """
    便捷函数：提取封面图片
    
    Args:
        content: 文章内容
        url: 文章 URL
        title: 文章标题
    
    Returns:
        图片 URL 或 None
    """
    extractor = CoverImageExtractor()
    
    # 1. 从内容中提取图片 URL
    img_url = extractor.extract_from_content(content, url)
    
    if not img_url:
        return None
    
    # 2. 下载并上传到飞书
    file_info = await extractor.download_and_upload(img_url, title or "cover")
    
    if file_info:
        # 返回飞书文件 token（用于 Bitable 附件字段）
        return file_info["file_token"]
    
    # 如果上传失败，返回原始 URL
    return img_url


# 测试
if __name__ == "__main__":
    import asyncio
    
    async def test():
        extractor = CoverImageExtractor()
        
        # 测试 1: Markdown 图片
        md_content = """
        # 文章标题
        
        ![封面图](https://example.com/cover.jpg)
        
        文章内容...
        """
        
        img_url = extractor.extract_from_content(md_content)
        print(f"测试 1 (Markdown): {img_url}")
        
        # 测试 2: HTML 图片
        html_content = """
        <html>
        <body>
            <img src="https://example.com/image.png" alt="封面">
            <p>文章内容...</p>
        </body>
        </html>
        """
        
        img_url = extractor.extract_from_content(html_content)
        print(f"测试 2 (HTML): {img_url}")
        
        # 测试 3: 无图片
        no_img_content = "只有文字内容，没有图片"
        img_url = extractor.extract_from_content(no_img_content)
        print(f"测试 3 (无图片): {img_url}")
    
    asyncio.run(test())
