#!/usr/bin/env python3
"""
裁剪透明背景图片的非透明区域最大矩形。

输入：带透明背景的 PNG 图片（本地路径或 URL）
输出：裁剪后的 PNG 图片保存到指定路径

用法：
    from crop_alpha import crop_alpha_bbox

    # 从本地文件裁剪
    out_path, (w, h) = crop_alpha_bbox("/path/to/cutout.png", "/path/to/cropped.png")

    # 从 URL 裁剪
    out_path, (w, h) = crop_alpha_bbox("https://example.com/cutout.png", "/tmp/cropped.png")
"""

import os
import sys
import tempfile
import socket
import ipaddress
from urllib.parse import urlparse
import requests as req
from PIL import Image
import numpy as np
from typing import Tuple, Optional


def _is_private_host(hostname: str) -> bool:
    if not hostname:
        return True
    h = hostname.strip().lower()
    if h in {"localhost", "ip6-localhost"} or h.endswith(".local"):
        return True
    try:
        ip = ipaddress.ip_address(h)
        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast
    except ValueError:
        pass
    try:
        infos = socket.getaddrinfo(h, None)
    except socket.gaierror:
        return True
    for info in infos:
        addr = info[4][0]
        try:
            ip = ipaddress.ip_address(addr)
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
                return True
        except ValueError:
            return True
    return False


def _validate_remote_url(input_url: str) -> None:
    parsed = urlparse(input_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http/https URLs are allowed")
    if not parsed.hostname:
        raise ValueError("URL hostname is missing")
    if _is_private_host(parsed.hostname):
        raise ValueError(f"Refusing private or localhost URL: {parsed.hostname}")


def crop_alpha_bbox(
    input_path_or_url: str,
    output_path: Optional[str] = None,
    padding: int = 0,
) -> Tuple[str, Tuple[int, int]]:
    """
    裁剪 PNG 图片中非透明区域的最小外接矩形。

    Args:
        input_path_or_url: 本地文件路径或 HTTP(S) URL
        output_path: 输出文件路径，为 None 时自动生成 /tmp/cropped_xxx.png
        padding: 裁剪后四周保留的像素边距（默认 0）

    Returns:
        (output_path, (width, height)) — 裁剪后图片路径和尺寸
    """
    # 1. 获取图片
    tmp_download = None
    if input_path_or_url.startswith(("http://", "https://")):
        _validate_remote_url(input_path_or_url)
        resp = req.get(input_path_or_url, timeout=30)
        resp.raise_for_status()
        tmp_download = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp_download.write(resp.content)
        tmp_download.close()
        local_path = tmp_download.name
    else:
        local_path = input_path_or_url

    try:
        img = Image.open(local_path).convert("RGBA")
        arr = np.array(img)

        # 2. 提取 alpha 通道，找非透明像素
        alpha = arr[:, :, 3]
        rows = np.any(alpha > 0, axis=1)
        cols = np.any(alpha > 0, axis=0)

        if not rows.any() or not cols.any():
            # 全透明图片，原样返回
            if output_path is None:
                output_path = tempfile.mktemp(suffix=".png", dir="/tmp", prefix="cropped_")
            img.save(output_path, "PNG")
            return output_path, (img.width, img.height)

        # 3. 计算边界
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]

        # 应用 padding
        if padding > 0:
            rmin = max(0, rmin - padding)
            rmax = min(arr.shape[0] - 1, rmax + padding)
            cmin = max(0, cmin - padding)
            cmax = min(arr.shape[1] - 1, cmax + padding)

        # 4. 裁剪
        cropped = img.crop((cmin, rmin, cmax + 1, rmax + 1))

        # 5. 保存
        if output_path is None:
            output_path = tempfile.mktemp(suffix=".png", dir="/tmp", prefix="cropped_")
        cropped.save(output_path, "PNG")
        return output_path, (cropped.width, cropped.height)

    finally:
        if tmp_download and os.path.exists(tmp_download.name):
            os.unlink(tmp_download.name)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python crop_alpha.py <input_path_or_url> [output_path] [padding]")
        sys.exit(1)

    input_arg = sys.argv[1]
    output_arg = sys.argv[2] if len(sys.argv) > 2 else None
    pad = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    out, (w, h) = crop_alpha_bbox(input_arg, output_arg, pad)
    print(f"Cropped: {out} ({w}x{h})")
