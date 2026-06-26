#!/usr/bin/env python3
"""TOS 工具模块

提供 TOS 文件上传功能，用于本地文件上传到火山引擎 TOS。
支持本地图片自动转换为 PDF 后上传。

所有过程日志输出到 stderr，stdout 保持干净。
"""

from __future__ import annotations

import io
import json
import logging
import os
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)


DEFAULT_REGION = "cn-beijing"
TOS_REGION_TO_ENDPOINT = {
    "cn-beijing": "tos-cn-beijing.volces.com",
    "cn-shanghai": "tos-cn-shanghai.volces.com",
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff", ".tif"}

# LLM 模型名称（可配置化）
DEFAULT_LLM_MODEL = "doubao-seed-2-0-pro-260215"
# LLM endpoint 域名映射（与 LAS API 共用 region 体系）
_LLM_REGION_TO_DOMAIN = {
    "cn-beijing": "operator.las.cn-beijing.volces.com",
    "cn-shanghai": "operator.las.cn-shanghai.volces.com",
}


def _get_llm_endpoint(region: Optional[str] = None) -> str:
    """根据 region 返回 LLM chat/completions endpoint。"""
    r = region or DEFAULT_REGION
    domain = _LLM_REGION_TO_DOMAIN.get(r)
    if not domain:
        domain = _LLM_REGION_TO_DOMAIN[DEFAULT_REGION]
        _log(f"警告: region '{r}' 无对应 LLM endpoint，回退到 {DEFAULT_REGION}")
    return f"https://{domain}/api/v1/chat/completions"

# 长图检测阈值
LONG_IMAGE_ASPECT_RATIO_THRESHOLD = 0.334
TARGET_ASPECT_RATIO = 0.5

# LLM 裁剪提示词
_CROP_PROMPT = """你是一个长图自动分页计算器。
根据以下规则分析输入长竖图并返回切分点数组，输出必须为**单行 JSON 数组**，所有数值精确到小数点后 4 位，不附加任何解释文字。

## 任务规则
1. **计算图片整体宽高比（宽 ÷ 高）**
   - 如果宽/高 ≥ 0.3330，则不切分，直接输出 `[1.0000]` 并结束。
2. **切分条件**
   - 如果宽/高 < 0.3330，则按目标比例 **宽/高 = 0.5000 ±10%**（即 0.4500 ~ 0.5500）计算每段的理想高度。
3. **安全位置调整（严格字符保护）**
   - 对每个理论切分点，如果所在行包含文字笔画，从切分点开始向上或向下各扫描 ±20px 范围，寻找最近的空白行。
   - 确保调整后宽高比仍在目标范围 0.4500 ~ 0.5500 内。
4. **归一化切分位置**
   - 调整后的切分点位置 ÷ 图片总高度，四舍五入到 4 位小数。
5. **排序输出**
   - 排除 `0.0000`，最后一个值必须为 `1.0000`。
   - 所有数值按升序排列。

## 输出要求
- 仅输出单行 JSON 数组，所有数字精确到小数点后四位。
- 无需切分时输出：`[1.0000]`
- 需要切分时输出（示例）：`[0.2200, 0.4520, 0.6840, 0.9160, 1.0000]`"""


def _log(msg: str) -> None:
    """过程日志统一输出到 stderr，保持 stdout 干净。"""
    print(msg, file=sys.stderr)


def get_tos_credentials() -> Tuple[str, str]:
    """获取 TOS 凭证。"""
    ak = os.environ.get("TOS_ACCESS_KEY")
    sk = os.environ.get("TOS_SECRET_KEY")
    if not ak or not sk:
        raise ValueError(
            "TOS 凭证未配置。请设置环境变量 TOS_ACCESS_KEY 和 TOS_SECRET_KEY，"
            "或在 env.sh 中配置。"
        )
    return ak, sk


def get_tos_endpoint(region: Optional[str] = None) -> str:
    """获取 TOS endpoint。"""
    endpoint = os.environ.get("TOS_ENDPOINT")
    if endpoint:
        return endpoint

    region = region or DEFAULT_REGION
    endpoint = TOS_REGION_TO_ENDPOINT.get(region)
    if endpoint:
        return endpoint

    raise ValueError(f"未知的 region: {region}，请设置 TOS_ENDPOINT 环境变量")


def get_tos_bucket(cli_bucket: Optional[str] = None) -> str:
    """获取 TOS bucket 名称。"""
    if cli_bucket:
        return cli_bucket

    bucket = os.environ.get("TOS_BUCKET")
    if bucket:
        return bucket

    raise ValueError("TOS bucket 未配置。请通过参数指定，或设置 TOS_BUCKET 环境变量。")


def generate_tos_key(local_path: str, prefix: Optional[str] = None, suffix: Optional[str] = None) -> str:
    """生成 TOS 对象 key，格式 {prefix}/{timestamp}_{uuid}/{filename}。"""
    p = Path(local_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]

    filename = p.stem + suffix if suffix else p.name

    if prefix:
        return f"{prefix.rstrip('/')}/{timestamp}_{unique_id}/{filename}"
    return f"las_pdf_parse/uploads/{timestamp}_{unique_id}/{filename}"


def is_local_file(path: str) -> bool:
    """检查路径是否为本地文件。"""
    if not path:
        return False
    if path.startswith(("http://", "https://", "tos://")):
        return False
    p = Path(path)
    return p.exists() and p.is_file()


def is_image_file(path: str) -> bool:
    """检查路径是否为图片文件。"""
    if not path:
        return False
    return Path(path).suffix.lower() in IMAGE_EXTENSIONS


def upload_to_tos(
    local_path: str,
    bucket: str,
    key: str,
    *,
    region: Optional[str] = None,
) -> str:
    """上传本地文件到 TOS，返回 tos://bucket/key。"""
    try:
        import tos
    except ImportError:
        raise ImportError(
            "tos SDK 未安装。请运行: pip install tos\n"
            "或参考文档: https://www.volcengine.com/docs/6349/74982"
        )

    ak, sk = get_tos_credentials()
    endpoint = get_tos_endpoint(region)
    region = region or DEFAULT_REGION

    client = tos.TosClientV2(ak, sk, endpoint, region)
    try:
        file_size = os.path.getsize(local_path)
        _log(f"正在上传文件到 TOS: {local_path} ({file_size / 1024 / 1024:.2f} MB)")

        with open(local_path, "rb") as f:
            client.put_object(bucket, key, content=f)

        tos_url = f"tos://{bucket}/{key}"
        _log(f"上传成功: {tos_url}")
        return tos_url
    except tos.exceptions.TosClientError as e:
        raise RuntimeError(f"TOS 客户端错误: {e.message}, cause: {e.cause}")
    except tos.exceptions.TosServerError as e:
        raise RuntimeError(
            f"TOS 服务端错误: code={e.code}, message={e.message}, "
            f"request_id={e.request_id}, status={e.status_code}"
        )
    finally:
        try:
            client.close()
        except Exception:
            pass


def upload_bytes_to_tos(
    content: bytes,
    bucket: str,
    key: str,
    *,
    region: Optional[str] = None,
    content_type: str = "application/octet-stream",
) -> str:
    """上传字节数据到 TOS，返回 tos://bucket/key。"""
    try:
        import tos
    except ImportError:
        raise ImportError(
            "tos SDK 未安装。请运行: pip install tos\n"
            "或参考文档: https://www.volcengine.com/docs/6349/74982"
        )

    ak, sk = get_tos_credentials()
    endpoint = get_tos_endpoint(region)
    region = region or DEFAULT_REGION

    client = tos.TosClientV2(ak, sk, endpoint, region)
    try:
        _log(f"正在上传数据到 TOS: {key} ({len(content) / 1024 / 1024:.2f} MB)")
        client.put_object(bucket, key, content=content, content_type=content_type)
        tos_url = f"tos://{bucket}/{key}"
        _log(f"上传成功: {tos_url}")
        return tos_url
    except tos.exceptions.TosClientError as e:
        raise RuntimeError(f"TOS 客户端错误: {e.message}, cause: {e.cause}")
    except tos.exceptions.TosServerError as e:
        raise RuntimeError(
            f"TOS 服务端错误: code={e.code}, message={e.message}, "
            f"request_id={e.request_id}, status={e.status_code}"
        )
    finally:
        try:
            client.close()
        except Exception:
            pass


def _image_to_rgb_jpeg_base64(img) -> str:
    """将 PIL Image 转为 base64 编码的 JPEG，处理 RGBA/其他模式。"""
    from PIL import Image

    buf = io.BytesIO()
    if img.mode == "RGBA":
        rgb_img = Image.new("RGB", img.size, (255, 255, 255))
        rgb_img.paste(img, mask=img.split()[3])
        rgb_img.save(buf, format="JPEG", quality=85)
    elif img.mode != "RGB":
        img.convert("RGB").save(buf, format="JPEG", quality=85)
    else:
        img.save(buf, format="JPEG", quality=85)

    import base64
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def _parse_llm_crop_result(llm_content: str) -> List[float]:
    """安全解析 LLM 返回的裁剪位置 JSON 数组（使用 json.loads 替代 eval）。"""
    if not llm_content:
        return [1.0]

    try:
        json_match = re.search(r"\[.*?\]", llm_content, re.DOTALL)
        if json_match:
            positions = json.loads(json_match.group())
            if isinstance(positions, list) and all(isinstance(p, (int, float)) for p in positions):
                positions = [float(p) for p in positions]
                if positions and positions[-1] != 1.0:
                    positions.append(1.0)
                return positions
    except (json.JSONDecodeError, ValueError) as e:
        logger.warning(f"解析 LLM 裁剪结果失败: {e}, content: {llm_content[:200]}")

    return [1.0]


def _find_safe_crop_line(img, target_y: int, scan_range: int = 50) -> int:
    """在目标位置附近寻找安全的裁剪行（空白行），使用亮度方差分析。"""
    try:
        import numpy as np
    except ImportError:
        logger.warning("numpy 未安装，跳过安全裁剪行检测")
        return target_y

    width, height = img.size
    target_y = max(0, min(target_y, height - 1))

    gray_img = img.convert("L") if img.mode != "L" else img
    pixels = np.array(gray_img)

    start_y = max(0, target_y - scan_range)
    end_y = min(height, target_y + scan_range + 1)

    best_y = target_y
    min_var = float("inf")

    for y in range(start_y, end_y):
        v = float(np.var(pixels[y, :]))
        if v < min_var:
            min_var = v
            best_y = y

    if min_var < 100:
        return best_y

    return best_y


def _refine_crop_positions(img, positions: List[float], scan_range_px: int = 80) -> List[float]:
    """使用图像处理精修 LLM 返回的裁剪位置。"""
    if positions == [1.0]:
        return [1.0]

    width, height = img.size
    refined = []

    for pos in positions:
        if pos >= 1.0:
            refined.append(1.0)
            continue

        target_y = int(pos * height)
        safe_y = _find_safe_crop_line(img, target_y, scan_range_px)
        refined.append(round(safe_y / height, 4))

    return refined


def _get_llm_crop_positions(img, api_key: str, *, region: Optional[str] = None) -> List[float]:
    """使用 LLM 获取智能裁剪位置，并通过图像处理精修。"""
    import requests
    from PIL import Image

    max_width = 1200
    width, height = img.size

    if width > max_width:
        scale = max_width / width
        new_width = max_width
        new_height = int(height * scale)
        img_for_llm = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    else:
        img_for_llm = img

    image_base64 = _image_to_rgb_jpeg_base64(img_for_llm)

    endpoint = _get_llm_endpoint(region)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": DEFAULT_LLM_MODEL,
        "messages": [
            {"role": "system", "content": _CROP_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
                    {"type": "text", "text": f"图片尺寸为:{img.size[0]}x{img.size[1]}"},
                ],
            },
        ],
        "temperature": 0.1,
        "max_tokens": 4096,
    }

    max_attempts = 2
    for attempt in range(1, max_attempts + 1):
        try:
            _log(f"正在调用 LLM 获取智能裁剪位置 (attempt {attempt}/{max_attempts})...")
            response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
            response.raise_for_status()

            result = response.json()
            resp_content = result.get("choices", [{}])[0].get("message", {}).get("content", "")

            raw_positions = _parse_llm_crop_result(resp_content)
            logger.info(f"LLM 原始裁剪位置: {raw_positions}")

            refined_positions = _refine_crop_positions(img, raw_positions)
            _log(f"LLM 裁剪位置（精修后）: {refined_positions}")
            return refined_positions
        except Exception as e:
            _log(f"LLM 调用失败 (attempt {attempt}/{max_attempts}): {e}")
            if attempt < max_attempts:
                import time
                time.sleep(2)
                continue
            _log("LLM 重试耗尽，使用简单分割")

    return _calculate_simple_crop_positions(img.size[1], int(img.size[0] / TARGET_ASPECT_RATIO))


def _calculate_simple_crop_positions(height: int, ideal_height: int) -> List[float]:
    """计算简单的等距裁剪位置。"""
    positions = []
    current = ideal_height

    while current < height:
        positions.append(current / height)
        current += ideal_height

    if not positions or positions[-1] < 1.0:
        positions.append(1.0)

    return positions


def _crop_by_positions(img, positions: List[float]) -> List:
    """根据归一化位置裁剪图片。"""
    if positions == [1.0]:
        return [img.copy()]

    width, height = img.size
    cropped_images = []

    all_positions = [0.0] + positions if positions[0] != 0.0 else positions

    for i in range(len(all_positions) - 1):
        top = int(all_positions[i] * height)
        bottom = int(all_positions[i + 1] * height)

        if bottom <= top:
            continue

        cropped = img.crop((0, top, width, bottom))
        cropped_images.append(cropped)

    return cropped_images


def _images_to_pdf_bytes(images: List) -> bytes:
    """将图片列表转换为 PDF 字节。"""
    from PIL import Image

    if not images:
        raise ValueError("没有图片可转换")

    rgb_images = []
    for img in images:
        if img.mode == "RGBA":
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            rgb_images.append(background)
        elif img.mode != "RGB":
            rgb_images.append(img.convert("RGB"))
        else:
            rgb_images.append(img)

    output = io.BytesIO()
    first = rgb_images[0]
    rest = rgb_images[1:] if len(rgb_images) > 1 else []

    first.save(output, format="PDF", save_all=True, append_images=rest, resolution=100.0)

    return output.getvalue()


def convert_image_to_pdf(
    image_path: str,
    *,
    use_llm: bool = False,
    llm_api_key: Optional[str] = None,
    region: Optional[str] = None,
) -> Tuple[bytes, dict]:
    """将图片转换为 PDF。长图自动分页。

    Returns:
        (pdf_bytes, meta) 其中 meta 包含 {"pages": int, "is_long_image": bool, "aspect_ratio": float}
    """
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("Pillow 未安装。请运行: pip install Pillow")

    _log(f"正在将图片转换为 PDF: {image_path}")

    img = Image.open(image_path)
    img.load()

    width, height = img.size
    aspect_ratio = width / height
    is_long_image = aspect_ratio < LONG_IMAGE_ASPECT_RATIO_THRESHOLD

    if is_long_image:
        _log(f"检测到长图 (宽高比={aspect_ratio:.4f})，将进行分页处理...")
        if use_llm and llm_api_key:
            crop_positions = _get_llm_crop_positions(img, llm_api_key, region=region)
        else:
            ideal_height = int(width / TARGET_ASPECT_RATIO)
            crop_positions = _calculate_simple_crop_positions(height, ideal_height)
        cropped_images = _crop_by_positions(img, crop_positions)
    else:
        cropped_images = [img]

    pdf_bytes = _images_to_pdf_bytes(cropped_images)
    num_pages = len(cropped_images)
    _log(f"PDF 生成成功，共 {num_pages} 页")

    # 释放 PIL 对象，避免峰值内存过高（长图场景可达原图 3 倍）
    for ci in cropped_images:
        if ci is not img:
            ci.close()
    img.close()
    del cropped_images

    meta = {
        "pages": num_pages,
        "is_long_image": is_long_image,
        "aspect_ratio": round(aspect_ratio, 4),
    }
    return pdf_bytes, meta


def generate_presigned_download_url(
    bucket: str,
    key: str,
    expires: int = 86400,
    *,
    region: Optional[str] = None,
) -> str:
    """生成 TOS 对象的预签名下载 URL。

    Args:
        bucket: 桶名
        key: 对象 key
        expires: URL 有效期（秒），默认 86400（24小时）
        region: TOS region

    Returns:
        预签名的 HTTPS 下载 URL，可直接在浏览器中打开下载
    """
    try:
        import tos
        from tos.enum import HttpMethodType
    except ImportError:
        raise ImportError(
            "tos SDK 未安装。请运行: pip install tos\n"
            "或参考文档: https://www.volcengine.com/docs/6349/74982"
        )

    ak, sk = get_tos_credentials()
    endpoint = get_tos_endpoint(region)
    region = region or DEFAULT_REGION

    client = tos.TosClientV2(ak, sk, endpoint, region)
    try:
        out = client.pre_signed_url(
            http_method=HttpMethodType.Http_Method_Get,
            bucket=bucket,
            key=key,
            expires=expires,
        )
        signed_url = out.signed_url
        _log(f"预签名下载 URL 已生成（有效期 {expires // 3600} 小时）")
        return signed_url
    except tos.exceptions.TosClientError as e:
        raise RuntimeError(f"TOS 客户端错误: {e.message}, cause: {e.cause}")
    except tos.exceptions.TosServerError as e:
        raise RuntimeError(
            f"TOS 服务端错误: code={e.code}, message={e.message}, "
            f"request_id={e.request_id}, status={e.status_code}"
        )
    finally:
        try:
            client.close()
        except Exception:
            pass


def _get_pdf_page_count(file_path: str) -> int:
    """尝试获取本地 PDF 的页数，用于更准确地预估耗时。"""
    try:
        import pypdf
        with open(file_path, "rb") as f:
            pdf = pypdf.PdfReader(f)
            return len(pdf.pages)
    except ImportError:
        pass
    except Exception as e:
        _log(f"使用 pypdf 读取页数失败: {e}")

    try:
        import PyPDF2
        with open(file_path, "rb") as f:
            pdf = PyPDF2.PdfReader(f)
            return len(pdf.pages)
    except ImportError:
        pass
    except Exception as e:
        _log(f"使用 PyPDF2 读取页数失败: {e}")

    try:
        import fitz  # PyMuPDF
        with fitz.open(file_path) as doc:
            return len(doc)
    except ImportError:
        pass
    except Exception as e:
        _log(f"使用 fitz 读取页数失败: {e}")

    # 如果没有可用的库，默认返回 1
    return 1


def handle_url_input(
    url: str,
    *,
    region: Optional[str] = None,
    tos_bucket: Optional[str] = None,
    tos_prefix: Optional[str] = None,
    use_llm: bool = False,
    llm_api_key: Optional[str] = None,
) -> Tuple[str, dict]:
    """处理 URL 输入，支持本地文件自动上传。

    Returns:
        (final_url, meta) 其中 meta 包含输入类型和处理信息，用于预估耗时。
        meta keys: input_type ("remote_url"|"tos_path"|"local_pdf"|"local_image"),
                   pages (int, 图片转 PDF 时), is_long_image (bool), aspect_ratio (float)
    """
    if not is_local_file(url):
        if url.startswith("tos://"):
            return url, {"input_type": "tos_path"}
        return url, {"input_type": "remote_url"}

    bucket = get_tos_bucket(tos_bucket)

    if is_image_file(url):
        _log(f"检测到图片文件: {url}")
        pdf_bytes, img_meta = convert_image_to_pdf(url, use_llm=use_llm, llm_api_key=llm_api_key, region=region)
        key = generate_tos_key(url, tos_prefix, suffix=".pdf")
        tos_url = upload_bytes_to_tos(pdf_bytes, bucket, key, region=region, content_type="application/pdf")
        meta = {"input_type": "local_image", **img_meta}
        return tos_url, meta
    else:
        key = generate_tos_key(url, tos_prefix)
        tos_url = upload_to_tos(url, bucket, key, region=region)
        pages = _get_pdf_page_count(url)
        return tos_url, {"input_type": "local_pdf", "pages": pages}
