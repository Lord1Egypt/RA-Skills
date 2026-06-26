#!/usr/bin/env python3
"""
图片预处理器（共享模块）

提供图片格式转换、尺寸缩放、透明通道处理等预处理能力。
被 image_search 和 compare 共同复用。
"""

import os
import tempfile
import logging
from typing import Dict, Any
from pathlib import Path

from PIL import Image

from _errors import ServiceError
import settings

logger = logging.getLogger("1688_image")

# API 仅稳定支持 JPEG，非 JPEG 格式需在上传前转换
_JPEG_EXTENSIONS = {".jpg", ".jpeg"}


class ImagePreprocessor:
    """图片预处理器"""

    def preprocess(self, image_path: str) -> Dict[str, Any]:
        """
        预处理图片

        Args:
            image_path: 本地路径或 URL

        Returns:
            处理后的图片信息
        """
        # 检查是否是 URL
        if image_path.startswith("http"):
            return self._process_url(image_path)

        # 本地文件
        return self._process_local(image_path)

    def _process_local(self, path: str) -> Dict[str, Any]:
        """处理本地图片，超尺寸自动缩放，非 JPEG 格式自动转换为 JPEG"""
        # 将相对路径转为绝对路径，避免因 cwd 不一致导致找不到文件
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"图片不存在：{path}")

        # 检查文件大小
        file_size_mb = os.path.getsize(path) / (1024 * 1024)
        if file_size_mb > settings.settings.IMAGE_MAX_SIZE_MB:
            raise ValueError(f"图片太大 ({file_size_mb:.1f}MB)，最大支持 {settings.settings.IMAGE_MAX_SIZE_MB}MB")

        ext = Path(path).suffix.lower()
        converted = False

        # 检查是否需要缩放或格式转换
        needs_resize = False
        try:
            img = Image.open(path)
            max_w, max_h = settings.settings.IMAGE_STANDARD_SIZE
            if img.width > max_w or img.height > max_h:
                needs_resize = True
            img.close()
        except Exception:
            pass

        # 超尺寸或非 JPEG 格式 → 统一转换（缩放 + 转 JPEG）
        if needs_resize or ext not in _JPEG_EXTENSIONS:
            path, converted = self._convert_to_jpeg(path, resize_to=settings.settings.IMAGE_STANDARD_SIZE if needs_resize else None)
            ext = ".jpg"
            logger.info("已预处理图片 (resize=%s, convert=%s): %s", needs_resize, ext not in _JPEG_EXTENSIONS, path)

        return {
            "path": path,
            "type": "local",
            "size_bytes": os.path.getsize(path),
            "format": ext,
            "converted": converted,
        }

    @staticmethod
    def _convert_to_jpeg(src_path: str, quality: int = 90, resize_to: tuple = None) -> tuple:
        """
        将任意格式的图片转换为 JPEG，可选缩放。

        Args:
            src_path: 原始图片路径
            quality: JPEG 压缩质量 (1-100)
            resize_to: 目标最大尺寸 (max_width, max_height)，等比缩放，None 则不缩放

        Returns:
            (转换后的临时文件路径, True)
        """
        try:
            img = Image.open(src_path)
        except Exception as e:
            raise ServiceError(f"无法打开图片文件: {e}")

        # 等比缩放到目标尺寸内
        if resize_to:
            max_w, max_h = resize_to
            if img.width > max_w or img.height > max_h:
                orig_w, orig_h = img.width, img.height
                img.thumbnail((max_w, max_h), Image.LANCZOS)
                logger.info("已缩放图片: %dx%d → %dx%d",
                           orig_w, orig_h, img.width, img.height)

        # 处理透明通道：RGBA / LA / P(带透明) → RGB 白色底
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            background = Image.new("RGB", img.size, (255, 255, 255))
            # P 模式先转 RGBA 再合成
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1])  # 用 alpha 通道作为 mask
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # 写入临时文件（后缀 .jpg 便于调试识别）
        # Windows 沙箱可能限制默认 temp 目录（C:\Users\...），fallback 到图片同目录
        tmp = None
        try:
            tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        except OSError:
            # 默认临时目录不可写，fallback 到原图片所在目录
            fallback_dir = os.path.dirname(os.path.abspath(src_path))
            logger.warning("默认临时目录不可写，fallback 到: %s", fallback_dir)
            tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False, dir=fallback_dir)
        try:
            img.save(tmp, format="JPEG", quality=quality)
            tmp.close()
        except Exception as e:
            tmp.close()
            os.unlink(tmp.name)
            raise ServiceError(f"图片转换 JPEG 失败: {e}")

        return tmp.name, True

    def _process_url(self, url: str) -> Dict[str, Any]:
        """处理图片 URL"""
        return {
            "url": url,
            "type": "url"
        }
