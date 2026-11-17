#!/usr/bin/env python3
"""
矩阵内技能封装：腾讯云 OCR 全家桶。

本模块是本技能与"腾讯云 AI Skills 技能矩阵"的对接层，全部使用矩阵内能力：
1. tencentcloud-ocr            → GeneralAccurateOCR（通用高精度识别）：简历图片/PDF → 全文文本
2. tencentcloud-ocr-extractdocagent → ExtractDocAgent（实时文档抽取 Agent）：按自定义字段抽取简历关键信息

需要环境变量: TENCENTCLOUD_SECRET_ID, TENCENTCLOUD_SECRET_KEY
"""

import base64
import json
import os
import sys

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

# 简历结构化抽取字段定义（ExtractDocAgent ItemNames）
RESUME_ITEM_NAMES = [
    {"KeyName": "姓名", "KeyType": 0, "KeyPrompt": "简历中的姓名"},
    {"KeyName": "电话", "KeyType": 0, "KeyPrompt": "简历中的联系电话"},
    {"KeyName": "邮箱", "KeyType": 0, "KeyPrompt": "简历中的邮箱地址"},
    {"KeyName": "学校", "KeyType": 0, "KeyPrompt": "简历中的毕业院校"},
    {"KeyName": "专业", "KeyType": 0, "KeyPrompt": "简历中的所学专业"},
    {"KeyName": "学历", "KeyType": 0, "KeyPrompt": "简历中的学历层次"},
    {"KeyName": "实习经历", "KeyType": 1, "KeyPrompt": "实习经历表格"},
    {"KeyName": "项目经历", "KeyType": 1, "KeyPrompt": "项目经历表格"},
    {"KeyName": "技能特长", "KeyType": 0, "KeyPrompt": "简历中的技能特长"},
]


def load_base64(value: str) -> str:
    """加载 Base64 文件内容：文件路径自动编码，或直接作为 Base64 字符串。"""
    if os.path.isfile(value):
        with open(value, "rb") as f:
            raw = f.read()
        try:
            raw_str = raw.decode("utf-8").strip()
            base64.b64decode(raw_str, validate=True)
            return raw_str
        except (UnicodeDecodeError, ValueError):
            pass
        if len(raw) > MAX_FILE_SIZE_BYTES:
            raise RuntimeError(f"文件大小超过 {MAX_FILE_SIZE_BYTES // (1024 * 1024)}MB 限制")
        return base64.b64encode(raw).decode("utf-8")
    try:
        decoded = base64.b64decode(value, validate=True)
        if len(decoded) > MAX_FILE_SIZE_BYTES:
            raise RuntimeError(f"文件大小超过 {MAX_FILE_SIZE_BYTES // (1024 * 1024)}MB 限制")
    except ValueError:
        raise RuntimeError("输入不是合法的 Base64 编码，也不是有效的文件路径")
    return value


def _get_client():
    """构建 OCR 客户端（复用矩阵内技能的接入方式）。"""
    try:
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.ocr.v20181119 import ocr_client, models
    except ImportError:
        raise RuntimeError("缺少依赖 tencentcloud-sdk-python，请执行: pip install tencentcloud-sdk-python")

    secret_id = os.getenv("TENCENTCLOUD_SECRET_ID")
    secret_key = os.getenv("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        raise RuntimeError("未配置腾讯云密钥，请设置环境变量 TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY")

    cred = credential.Credential(secret_id, secret_key)
    http_profile = HttpProfile()
    http_profile.endpoint = os.getenv("TENCENTCLOUD_ENDPOINT", "ocr.tencentcloudapi.com")
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    client = ocr_client.OcrClient(cred, "ap-guangzhou", client_profile)
    return client, models


def extract_resume_text(image_path: str, is_pdf: bool = False, pdf_page: int = 1) -> str:
    """
    能力来源：tencentcloud-ocr（矩阵内）· GeneralAccurateOCR 通用高精度识别。
    返回简历全文文本。
    """
    client, models = _get_client()
    req = models.GeneralAccurateOCRRequest()
    req.ImageBase64 = load_base64(image_path)
    if is_pdf:
        req.IsPdf = True
        req.PdfPageNumber = pdf_page
    try:
        resp = client.call_json("GeneralAccurateOCR", req._serialize())
        if isinstance(resp, str):
            resp = json.loads(resp)
        if isinstance(resp, dict) and isinstance(resp.get("Response"), dict):
            resp = resp["Response"]
    except Exception as exc:
        raise RuntimeError(f"OCR 识别失败: {exc}")

    detections = resp.get("TextDetections", []) or []
    lines = [d.get("DetectedText", "") for d in detections if d.get("DetectedText")]
    return "\n".join(lines)


def extract_resume_fields(image_path: str, pdf_page: int = 1) -> dict:
    """
    能力来源：tencentcloud-ocr-extractdocagent（矩阵内）· ExtractDocAgent 实时文档抽取 Agent。
    按自定义字段从简历图片/PDF 中结构化抽取关键信息。
    失败时返回空 dict（不影响主流程，主评分基于全文文本）。
    """
    client, models = _get_client()
    req = models.ExtractDocAgentRequest()
    req.ImageBase64 = load_base64(image_path)
    items = []
    for item_data in RESUME_ITEM_NAMES:
        item = models.ItemNames()
        item.KeyName = item_data["KeyName"]
        item.KeyType = item_data.get("KeyType", 0)
        if item_data.get("KeyPrompt"):
            item.KeyPrompt = item_data["KeyPrompt"]
        items.append(item)
    req.ItemNames = items
    req.PdfPageNumber = pdf_page
    try:
        resp = client.ExtractDocAgent(req)
        resp_json = json.loads(resp.to_json_string())
    except Exception as exc:
        print(f"[warn] ExtractDocAgent 字段抽取失败（不影响主流程）: {exc}", file=sys.stderr)
        return {}

    fields = {}
    structural_list = resp_json.get("StructuralList") or []
    for group in structural_list:
        for group_item in (group.get("Groups") or []):
            for line_info in (group_item.get("Lines") or []):
                item_info = line_info or {}
                key_obj = item_info.get("Key") or {}
                value_obj = item_info.get("Value") or {}
                name = key_obj.get("ConfigName") or key_obj.get("AutoName") or ""
                content = value_obj.get("AutoContent") or ""
                if name and content:
                    fields.setdefault(name, content)
    return fields
