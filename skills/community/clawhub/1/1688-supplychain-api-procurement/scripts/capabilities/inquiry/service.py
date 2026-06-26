# -*- coding: utf-8 -*-
"""
Direct inquiry capability.

This flow accepts one user requirement that already contains the product
search requirement and supplier inquiry questions, starts an inquiry instance,
and returns the instance id immediately. Instance data is fetched separately
by instance id.
"""

import time
import uuid
from typing import Any, Dict, List, Optional

from _digital_human import build_tool_body, get_session_id
from _errors import ParamError, ServiceError
from _http import api_post
from settings import settings
from capabilities.inquiry_data.service import fetch_inquiry_data


DEFAULT_INQUIRY_ITEM_SIZE = 30
DEFAULT_RECALL_ITEM_SIZE = 30


def normalize_question_list(question_list: Optional[List[Any]], fallback_text: str) -> List[Dict[str, str]]:
    """
    Normalize questions into DigitalHuman questionList format.

    If the caller cannot reliably split inquiry questions from the full user
    requirement, use the complete requirement as one question so the downstream
    inquiry model still receives all context.
    """
    source = question_list if question_list else [fallback_text]
    normalized: List[Dict[str, str]] = []

    for item in source:
        if isinstance(item, str):
            question = item.strip()
            question_type = "current"
        elif isinstance(item, dict):
            question = str(item.get("question", "")).strip()
            question_type = str(item.get("type") or "current").strip() or "current"
        else:
            continue

        if not question:
            continue

        normalized.append({
            "question": question,
            "type": question_type,
        })

    if not normalized:
        raise ParamError("询盘问题不能为空")

    return normalized


def _build_content_obj(
    requirement: str,
    question_list: List[Dict[str, str]],
    purchase_size: int,
    inquiry_item_size: int,
    recall_item_size: int,
    requirement_id: str,
    task_name: str,
    images: Optional[List[dict]] = None,
) -> dict:
    """Build content used both for task creation and tool start."""
    return {
        "evaluation": False,
        "recallInterrupt": True,
        "sessionId": get_session_id(),
        "purchaseSize": purchase_size,
        "inquiryItemSize": inquiry_item_size,
        "recallItemSize": recall_item_size,
        "skillVersion": settings.SKILL_VERSION,
        "textSummary": requirement[:20] or "询盘",
        "questionList": question_list,
        "aiBatchInquiryExt": {
            "wwCardExt": {
                "cardType": "digital_buyer",
                "taskName": task_name,
                "requirementId": requirement_id,
            },
            "appKey": "newton",
            "mockWwSellerIds": [],
        },
        "image": images if images else [],
        "questionGenerateRequestId": str(uuid.uuid4()),
        "requirementId": requirement_id,
        "scene": "newton",
        "subScene": "inquiry",
        "taskName": task_name,
        "text": requirement,
    }


def _create_inquiry_task(content_obj: dict) -> Dict[str, str]:
    """Create a new inquiry task and return instance metadata."""
    body = {
        "method": settings.CREATE_TASK_METHOD,
        "taskInfo": content_obj,
    }

    resp = api_post(
        path=settings.CREATE_TASK_PATH,
        body=body,
        timeout=settings.CREATE_TASK_TIMEOUT,
    )

    data = resp.get("data", {})
    if not data.get("__success__", resp.get("success")):
        raise ServiceError("创建询盘任务失败: {}".format(resp))

    model = data.get("__model__", {})
    instance_id = model.get("instanceId")
    if not instance_id:
        raise ServiceError("创建询盘任务返回缺少 instanceId")

    return {
        "instanceId": instance_id,
        "requirementId": model.get("requirementId", content_obj.get("requirementId", "")),
    }


def _trigger_inquiry_instance(instance_id: str, content_obj: dict) -> Dict[str, Any]:
    """Start the inquiry instance."""
    body_str = build_tool_body(content_obj, instance_id, type_name="start")
    resp = api_post(
        path=settings.TOOL_PATH,
        raw_body=body_str,
        timeout=settings.TOOL_TIMEOUT,
    )

    if not resp.get("success"):
        raise ServiceError("触发询盘失败: {}".format(resp))

    return resp


def _load_images(
    local_images: Optional[List[str]] = None,
    image_urls: Optional[List[str]] = None,
) -> List[dict]:
    """Build image payload from local files or image URLs."""
    images: List[dict] = []
    local_paths: List[str] = []
    remote_urls: List[str] = []

    from _img_upload import is_http_url, upload_image_urls, upload_images

    for image in local_images or []:
        image = (image or "").strip()
        if not image:
            continue
        if is_http_url(image):
            remote_urls.append(image)
        else:
            local_paths.append(image)

    for image_url in image_urls or []:
        image_url = (image_url or "").strip()
        if image_url:
            remote_urls.append(image_url)

    if local_paths:
        urls = upload_images(local_paths)
        images.extend({"type": "product", "url": url} for url in urls)
    if remote_urls:
        urls = upload_image_urls(remote_urls)
        images.extend({"type": "product", "url": url} for url in urls)
    return images


def start_direct_inquiry(
    requirement: str,
    question_list: Optional[List[Any]] = None,
    purchase_size: int = 1,
    inquiry_item_size: int = DEFAULT_INQUIRY_ITEM_SIZE,
    recall_item_size: int = DEFAULT_RECALL_ITEM_SIZE,
    local_images: Optional[List[str]] = None,
    image_urls: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Create and start a direct inquiry instance without polling."""
    requirement = (requirement or "").strip()
    if not requirement:
        raise ParamError("需求不能为空")
    if purchase_size <= 0:
        raise ParamError("采购数量必须大于 0")
    if inquiry_item_size <= 0:
        raise ParamError("询盘商品数必须大于 0")
    if recall_item_size <= 0:
        raise ParamError("找品商品数必须大于 0")

    normalized_questions = normalize_question_list(question_list, fallback_text=requirement)
    images = _load_images(local_images=local_images, image_urls=image_urls)

    requirement_id = str(uuid.uuid4())
    task_name = time.strftime("%m月%d日%H:%M")
    content_obj = _build_content_obj(
        requirement=requirement,
        question_list=normalized_questions,
        purchase_size=purchase_size,
        inquiry_item_size=inquiry_item_size,
        recall_item_size=recall_item_size,
        requirement_id=requirement_id,
        task_name=task_name,
        images=images,
    )

    task_info = _create_inquiry_task(content_obj)
    instance_id = task_info["instanceId"]
    returned_requirement_id = task_info.get("requirementId", "")
    if returned_requirement_id:
        content_obj["requirementId"] = returned_requirement_id
        content_obj["aiBatchInquiryExt"]["wwCardExt"]["requirementId"] = returned_requirement_id

    _trigger_inquiry_instance(instance_id, content_obj)

    return {"instance_id": instance_id}


def get_inquiry_result(instance_id: str) -> Dict[str, Any]:
    """Fetch inquiry instance data once by instance id."""
    if not instance_id or not instance_id.strip():
        raise ParamError("instance_id 不能为空")
    result = fetch_inquiry_data(instance_id.strip())
    return {
        "instance_id": instance_id.strip(),
        "instance_data": result.get("raw", {}),
    }
