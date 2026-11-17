#!/usr/bin/env python3
"""
简历图片/PDF OCR 提取模块（复用腾讯云通用高精度 OCR GeneralAccurateOCR）。

支持：
- 本地图片（jpg/png/webp/bmp）、网络图片 URL
- 本地 PDF（多页：逐页渲染后识别，可限制最大页数）
- 无 SDK 时自动安装 tencentcloud-sdk-python

用法：
    from ocr_utils import extract_resume_text
    text = extract_resume_text("/path/to/resume.jpg", max_pdf_pages=3)
"""

import os
import subprocess
import sys
import tempfile

from env_loader import validate_env

OCR_ENDPOINT = "ocr.tencentcloudapi.com"
OCR_REGION = "ap-guangzhou"


def ensure_dependencies():
    """确保 OCR 相关依赖已安装。"""
    try:
        import tencentcloud  # noqa: F401
    except (ImportError, ModuleNotFoundError):
        print("[INFO] tencentcloud-sdk-python 未安装，正在安装...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "tencentcloud-sdk-python", "-q"],
            stdout=sys.stderr,
            stderr=sys.stderr,
        )
        print("[INFO] 依赖安装完成。", file=sys.stderr)

    try:
        import PIL  # noqa: F401
    except (ImportError, ModuleNotFoundError):
        print("[INFO] Pillow 未安装，正在安装...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "Pillow", "-q"],
            stdout=sys.stderr,
            stderr=sys.stderr,
        )
        print("[INFO] 依赖安装完成。", file=sys.stderr)

    try:
        import fitz  # noqa: F401
    except (ImportError, ModuleNotFoundError):
        print("[INFO] PyMuPDF 未安装，正在安装...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "PyMuPDF", "-q"],
            stdout=sys.stderr,
            stderr=sys.stderr,
        )
        print("[INFO] 依赖安装完成。", file=sys.stderr)


def _download_image(url: str) -> str:
    """下载网络图片到临时文件，返回本地路径。"""
    import urllib.request

    suffix = os.path.splitext(url.split("?")[0])[1] or ".jpg"
    if suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp", ".bmp"):
        suffix = ".jpg"
    fd, tmp_path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    urllib.request.urlretrieve(url, tmp_path)  # noqa: S310
    return tmp_path


def _detect_kind(path: str) -> str:
    """根据扩展名判断资源类型：image / pdf / url / unknown。"""
    lower = path.lower()
    if lower.startswith("http://") or lower.startswith("https://"):
        return "url"
    ext = os.path.splitext(lower)[1]
    if ext == ".pdf":
        return "pdf"
    if ext in (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"):
        return "image"
    return "unknown"


def _general_accurate_ocr(image_path: str, secret_id: str, secret_key: str) -> str:
    """
    调用 GeneralAccurateOCR 识别单张图片，返回拼接后的文本。
    出错时抛出带可读中文说明的 RuntimeError。
    """
    import base64
    import json

    from tencentcloud.common import credential
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
        TencentCloudSDKException,
    )
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.ocr.v20181119 import models, ocr_client

    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    cred = credential.Credential(secret_id, secret_key)
    http_profile = HttpProfile()
    http_profile.endpoint = OCR_ENDPOINT
    http_profile.reqTimeout = 120
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    client = ocr_client.OcrClient(cred, OCR_REGION, client_profile)

    req = models.GeneralAccurateOCRRequest()
    req.from_json_string(json.dumps({"ImageBase64": image_base64}))

    try:
        resp = client.GeneralAccurateOCR(req)
        resp_json = json.loads(resp.to_json_string())
    except TencentCloudSDKException as e:
        code = getattr(e, "code", "") or ""
        message = getattr(e, "message", "") or ""
        guide = ""
        if "UnOpenError" in code or "UnsupportedOperation" in code:
            guide = (
                "OCR 服务未开通，请前往控制台开通通用印刷体识别（高精度）：\n"
                "  https://console.cloud.tencent.com/ocr/general\n"
                "注意：高精度 OCR 需要单独开通并购买资源包。"
            )
        elif "ResourceInsufficient" in code or "ResourcePackageEmpty" in code:
            guide = "OCR 资源包已用尽，请前往控制台购买资源包。"
        elif "AuthFailure" in code or "UnauthorizedOperation" in code:
            guide = "OCR 权限不足，请在 CAM 策略中授予 ocr:GeneralAccurateOCR 权限。"
        raise RuntimeError(f"OCR 识别失败 [{code}]: {message}\n{guide}")

    lines = []
    for item in resp_json.get("TextDetections", []):
        text = item.get("DetectedText", "").strip()
        if text:
            lines.append(text)
    return "\n".join(lines)


def _ocr_pdf(pdf_path: str, secret_id: str, secret_key: str, max_pages: int = 3) -> str:
    """
    将 PDF 逐页渲染为图片后识别。默认最多识别前 3 页（简历一般 1-2 页）。
    """
    import fitz  # PyMuPDF

    doc = fitz.open(pdf_path)
    total_pages = min(doc.page_count, max_pages)
    texts = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(total_pages):
            page = doc[i]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            img_path = os.path.join(tmpdir, f"page_{i + 1}.png")
            pix.save(img_path)
            page_text = _general_accurate_ocr(img_path, secret_id, secret_key)
            if page_text.strip():
                texts.append(f"--- 第 {i + 1} 页 ---\n{page_text}")
    doc.close()
    if not texts:
        raise RuntimeError("PDF 识别结果为空，请检查文件是否为可扫描的简历。")
    return "\n\n".join(texts)


def extract_resume_text(source: str, max_pdf_pages: int = 3) -> str:
    """
    从图片 / PDF / 网络图片 URL 提取简历文本。

    返回识别出的原始文本；识别为空或失败时抛 RuntimeError。
    """
    ensure_dependencies()
    secret_id, secret_key = validate_env()

    kind = _detect_kind(source)
    local_path = source

    if kind == "url":
        print(f"[INFO] 下载网络图片: {source}")
        local_path = _download_image(source)
        kind = _detect_kind(local_path)

    if kind == "pdf":
        print(f"[INFO] 识别 PDF（最多 {max_pdf_pages} 页）...")
        text = _ocr_pdf(local_path, secret_id, secret_key, max_pages=max_pdf_pages)
    elif kind == "image":
        print(f"[INFO] 识别图片: {local_path}")
        text = _general_accurate_ocr(local_path, secret_id, secret_key)
    else:
        raise RuntimeError(
            f"不支持的简历文件类型: {source}\n"
            "支持: 图片(.jpg/.png/.webp/.bmp)、PDF 文件、网络图片 URL"
        )

    if local_path != source and os.path.exists(local_path):
        try:
            os.remove(local_path)
        except OSError:
            pass

    if not text.strip():
        raise RuntimeError("OCR 识别结果为空，请确认图片清晰、非空白页。")
    return text.strip()
