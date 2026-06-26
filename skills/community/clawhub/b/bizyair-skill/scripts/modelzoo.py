"""modelzoo.py — BizyAir ModelZoo 任务模块。

覆盖：列表 / 详情 / 价格 / 创建任务 / 轮询状态 / 调用记录。
与 webapp（AI 应用）的区别：
  - create 始终异步（< 5s 返回 request_id），不需要 X-Bizyair-Task-Async header
  - field_name 直接是 payload key（不需要 contract 映射）
  - field_options 已经是 dict（不需要 JSON.parse）
  - field_type=images 必须传 list[str]
  - outputs 四种字段并存：{texts, images, videos, audios}
"""
from __future__ import annotations

import json
import sys
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from common import API_BASE, POLL_INTERVAL, MAX_POLL_SECONDS

import api

X_BASE = f"{API_BASE}/x/v1"


def _coerce_param(field_type: str, value: Any) -> Any:
    """根据 field_type 强制转换参数类型，避免服务端 500。"""
    if value is None:
        return value
    ft = (field_type or "").lower()
    if ft in ("number", "slider", "slides"):
        try:
            return float(value) if "." in str(value) else int(value)
        except (ValueError, TypeError):
            return value
    if ft == "seed":
        try:
            return int(value)
        except (ValueError, TypeError):
            return -1
    if ft == "boolean":
        if isinstance(value, bool):
            return value
        return str(value).lower() in ("true", "1", "yes")
    if ft == "images":
        if isinstance(value, list):
            return value
        return [str(value)]  # 单张也包成 list
    return value


# 参数名别名映射。ModelZoo 不同 endpoint 的 field_name 命名不统一，
# 这里定义 field_name → 可能的别名列表。当 user_params 里没有精确匹配时，
# build_task_payload 会尝试从别名取值。
_FIELD_ALIASES: dict[str, list[str]] = {
    'ratio': ['aspect_ratio'],           # happyhorse/wan 用 ratio
    'aspect_ratio': ['ratio'],           # 反向
    'size': ['resolution', 'image_size'], # seedream 用 size
    'resolution': ['size', 'image_size'], # 反向
    'image_size': ['resolution', 'size'], # 部分 endpoint
}


def _resolve_user_param(field_name: str, user_params: dict[str, Any]) -> tuple[Any, bool]:
    """从 user_params 取值，支持别名回退。返回 (value, found)。"""
    if field_name in user_params:
        return user_params[field_name], True
    for alias in _FIELD_ALIASES.get(field_name, []):
        if alias in user_params:
            return user_params[alias], True
    return None, False


def _strip_default_media(value: Any, default_urls: set[str]) -> Any:
    """从用户传的媒体值里剥离混入的默认示例 URL。

    场景：Agent 看到 detail 里的 field_value 是 ["demo.jpg"]，
    用户又提供了自己的图片，Agent 可能错误地组装成 ["user.jpg", "demo.jpg"]。
    本函数把属于默认值的 URL 剔除，只保留用户自己的。
    如果剔除后为空（说明用户传的全是默认值），则返回原值不做处理。
    """
    if isinstance(value, list):
        filtered = [u for u in value if str(u) not in default_urls]
        return filtered if filtered else value
    if isinstance(value, str) and value in default_urls:
        return value  # 单值且就是默认 → 不剥（否则字段会空）
    return value


def list_endpoints(
    api_key: str,
    *,
    keyword: str = "",
    tags: list[str] | None = None,
    categories: list[str] | None = None,
    sort: str = "Auto",
    page: int = 1,
    page_size: int = 20,
    show_deprecated: bool = False,
) -> dict[str, Any]:
    """搜索 modelzoo endpoint 列表。"""

    url = f"{X_BASE}/modelzoo/list?current={page}&page_size={page_size}"
    if keyword:
        # 必须 URL encode，否则中文 keyword 会被服务器拒（urllib.error 或 0 条结果）。
        url += f"&keyword={urllib.parse.quote(keyword)}"
    if sort:
        url += f"&sort={sort}"
    body = {
        "tags": tags or [],
        "categories": categories or [],
        "show_deprecated": show_deprecated,
    }
    return api.safe_request_json("POST", url, api_key, payload=body)


def get_detail(api_key: str, endpoint: str) -> dict[str, Any]:
    """获取 endpoint 详情（input_params + outputs_example）。"""

    return api.safe_request_json("GET", f"{X_BASE}/modelzoo/detail/{endpoint}", api_key)


def get_price(api_key: str, endpoint: str) -> dict[str, Any]:
    """获取 endpoint 价格表。优先用 simple_price_text 展示。"""

    return api.safe_request_json("GET", f"{X_BASE}/modelzoo/price_table/{endpoint}", api_key)


def build_task_payload(
    detail_data: dict[str, Any],
    user_params: dict[str, Any],
    *,
    media_overrides: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    """根据 detail 的 input_params + 用户参数构建 create payload。

    规则（优先级从高到低）：
    1. media_overrides：按 field_type 匹配（images/audios/videos），
       整体替换默认值，不与默认值合并。用于 --image/--audio/--video 上传的文件。
    2. user_params：用户通过 --param key=value 显式传的参数
    3. input_params 的 field_value（default）：兜底默认值
    - 按 field_type 做类型强转

    media_overrides 格式：{"images": ["url1", ...], "audios": ["url1"], ...}
    """
    input_params = detail_data.get("input_params") or []
    payload: dict[str, Any] = {}
    overrides = media_overrides or {}
    consumed_media_types: set[str] = set()

    # 收集所有媒体字段的默认 URL，用于兜底过滤
    _default_media_urls: set[str] = set()
    for param in input_params:
        ft = (param.get("field_type") or "").lower()
        if ft in ("images", "audios", "videos"):
            dv = param.get("field_value")
            if isinstance(dv, list):
                _default_media_urls.update(str(u) for u in dv)
            elif isinstance(dv, str) and dv:
                _default_media_urls.add(dv)

    for param in input_params:
        field_name = param.get("field_name")
        field_type = param.get("field_type") or ""
        default_value = param.get("field_value")
        ft = field_type.lower()

        if not field_name:
            continue

        # media_overrides 最高优先：匹配 field_type，整体替换默认值
        if ft in overrides and ft not in consumed_media_types:
            payload[field_name] = _coerce_param(field_type, overrides[ft])
            consumed_media_types.add(ft)
            continue

        # 用户通过 --param 显式传的参数（支持别名回退）
        user_value, user_found = _resolve_user_param(field_name, user_params)
        raw_value = user_value if user_found else default_value

        # 兜底：媒体字段如果用户显式传了值，自动剥离混入的默认示例 URL
        if ft in ("images", "audios", "videos") and user_found and _default_media_urls:
            raw_value = _strip_default_media(raw_value, _default_media_urls)

        # 跳过 None 且非必填的
        if raw_value is None and not param.get("required"):
            continue

        payload[field_name] = _coerce_param(field_type, raw_value)

    return payload


def create_task(api_key: str, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
    """创建 modelzoo 任务。始终异步，< 5s 返回 request_id。"""

    return api.safe_request_json(
        "POST",
        f"{X_BASE}/modelzoo/tasks/openapi/{endpoint}",
        api_key,
        payload=payload,
    )


def query_task(api_key: str, request_id: str) -> dict[str, Any]:
    """查询 modelzoo 任务状态。"""

    return api.safe_request_json(
        "GET",
        f"{X_BASE}/modelzoo/tasks/openapi/{request_id}",
        api_key,
    )


def poll_until_done(api_key: str, request_id: str) -> dict[str, Any]:
    """轮询直到任务完成或失败。返回最终 data。"""

    start = time.time()
    last_status = None

    while time.time() - start < MAX_POLL_SECONDS:
        result = query_task(api_key, request_id)
        data = (result.get("data") or {}).get("data") or result.get("data") or {}
        status = data.get("status")

        if status != last_status:
            print(f"STATUS:{status}", file=sys.stderr)
            last_status = status

        if status == "Success":
            return data
        if status == "Failed":
            message = data.get("message") or "Unknown error"
            print(
                json.dumps(
                    {"error": "MODELZOO_TASK_FAILED", "status": status, "message": message},
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )
            return data

        time.sleep(POLL_INTERVAL)

    print(
        json.dumps({"error": "TIMEOUT", "message": "Polling timed out", "request_id": request_id}, ensure_ascii=False),
        file=sys.stderr,
    )
    return {"status": "Timeout", "request_id": request_id}


def get_mycalls(
    api_key: str,
    *,
    call_type: str = "trd_api_record",
    endpoint: str | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict[str, Any]:
    """查询调用记录列表。"""

    body: dict[str, Any] = {"call_type": call_type}
    if endpoint:
        body["endpoint"] = endpoint
    if status:
        body["status"] = status

    return api.safe_request_json(
        "POST",
        f"{X_BASE}/modelzoo/mycalls?current={page}&page_size={page_size}",
        api_key,
        payload=body,
    )


def get_mycall_detail(api_key: str, call_type: str, request_id: str) -> dict[str, Any]:
    """查询单条调用详情（含 usage.charge_amount）。"""

    return api.safe_request_json(
        "GET",
        f"{X_BASE}/modelzoo/mycalls/{call_type}/{request_id}",
        api_key,
    )


# ---- ModelZoo endpoint 候选搜索（菜单 6 号 / v6 入口）----

# 模态推断：直接看 server 返回的 category 字段，权威 + 简单。
# 旧版用关键词扫描 display_name + endpoint + description 一坨 blob，把品牌名（wan/hunyuan）
# 当视频信号导致万相图片版被错杀。category 字段值是 "Text to Image" / "Text to Video" /
# "FLF to Video" / "Image to Image" / "Vision" 等，包含 video/image 子串就足以分流。


def infer_modality_hint(item: dict[str, Any]) -> tuple[str, str]:
    """根据 ModelZoo 服务端 category 字段判断模态。返回 (hint, reason)。

    hint: 'image' / 'video' / 'unknown'（Vision / LLM / TTS 等非图视类落 unknown）
    reason: 给 LLM / debug 看的简短说明
    """
    category = item.get("category") or ""
    cat_low = category.lower()
    if "video" in cat_low:
        return "video", f"category={category}"
    if "image" in cat_low:
        return "image", f"category={category}"
    return "unknown", f"category={category or '(空)'}"


def summarize_modelzoo_candidate(item: dict[str, Any]) -> dict[str, Any]:
    """挑出展示给用户的几个字段，避免把整个 raw item 透传出去。

    cover_image 优先级：
      1. outputs_example.images[0] / videos[0]（detail API 拿的真示例图，需要 picker 提前注入到 raw item 的 _cover_image_url 字段）
      2. icon_url（list 阶段就有，是模型 logo 不是真示例）
      3. None
    cover_image_source 字段告诉调用方这是真示例还是 logo。
    """
    endpoint = item.get("endpoint")
    hint, reason = infer_modality_hint(item)

    cover_url = item.get("_cover_image_url")
    cover_source = item.get("_cover_image_source")
    if not cover_url:
        icon = item.get("icon_url")
        if icon:
            cover_url = icon
            cover_source = "icon_url"
        else:
            cover_source = "none"

    return {
        "endpoint": endpoint,
        "display_name": item.get("display_name"),
        "category": item.get("category"),
        "description": item.get("description") or item.get("introduction"),
        "cover_image": cover_url,
        "cover_image_source": cover_source,
        "tags": item.get("tags") or [],
        "modality_hint": hint,
        "modality_reason": reason,
    }


def _modelzoo_number_badge(index: int) -> str:
    return f"{index}."


def _modality_label(hint: str) -> str:
    """渲染 reply_markdown 时挂在标题后的标签。unknown 不打标签。"""
    if hint == "image":
        return " [图片]"
    if hint == "video":
        return " [视频]"
    return ""


def build_modelzoo_reply_markdown(candidates: list[dict[str, Any]], *, modality: str, query: str = "") -> str:
    """构建给用户看的 reply_markdown。

    现在 picker 不再按 modality 截断，候选可能图视混合，所以 heading 用中性表述；
    每条候选标题后挂 [图片] / [视频] 标签，便于 LLM 按用户意图重排。
    """
    if not candidates:
        return (
            "📭 **这轮 ModelZoo 没搜到合适的 endpoint**\n\n"
            f"当前关键词「{query}」没匹配到任何模型。\n\n"
            "---\n\n"
            "⚠️ **以下是给 agent / LLM 看的指令，不要原样转发给用户：**\n\n"
            f"如果「{query}」是：\n\n"
            "- **语义需求**（\"高清写实\"、\"产品图\"、\"赛博朋克\" 等）→ 翻译成 ModelZoo 真实存在的「模型名 / 系列名 / 任务类型」后用 `pick-modelzoo-image` / `pick-modelzoo-video` 重搜一次。\n"
            "- **模型词 / 系列 / 任务词**（Flux / Kling / 通用图片 / 文生图 / 首尾帧 等）→ 换同类的其他模型词再试，最多 3 轮。\n"
        )
    target = (modality or "image").lower()
    target_label = "视频" if target == "video" else "图片"
    heading = f"🎯 **ModelZoo 找到的 endpoint（已按 {target_label} 意图排序）**"
    intro = "ModelZoo 走底层模型 API，参数明确、按次扣费稳定。候选如下（标签是模态提示，跨模态的请按用户意图重排或忽略）："
    lines = [heading, "", intro, ""]
    for index, item in enumerate(candidates, start=1):
        title = item.get("display_name") or item.get("endpoint") or f"endpoint {index}"
        label = _modality_label(item.get("modality_hint", "unknown"))
        lines.append(f"{_modelzoo_number_badge(index)} **{title}**{label}")
        lines.append("")
        description = item.get("description")
        if description:
            text = str(description).strip().replace("\n", " ")
            if len(text) > 120:
                text = text[:120] + "..."
            lines.append(f"- **简介**：{text}")
        if item.get("category"):
            lines.append(f"- **分类**：{item['category']}")
        cover = item.get("cover_image")
        if cover:
            # outputs_example 是真实示例图，icon_url 是 logo —— 两个都能告诉用户视觉风格
            label_text = "示例" if item.get("cover_image_source") == "outputs_example" else "图标"
            # 视频示例用裸 URL（SKILL.md 第 6 条），图片用 markdown 图
            cover_lower = str(cover).lower()
            is_video_cover = any(cover_lower.endswith(ext) for ext in (".mp4", ".mov", ".webm"))
            if is_video_cover:
                lines.append(f"- **{label_text}**（视频）：")
                lines.append(cover)
            else:
                lines.append(f"- **{label_text}**：![{title}]({cover})")
        lines.append("- **能否直接执行**：✅ 支持，参数确认后即可开跑")
        if item.get("endpoint"):
            lines.append(f"- **endpoint**：`{item['endpoint']}`")
            lines.append(
                f"- **下一步**：`cli.py modelzoo-detail {item['endpoint']}` 看参数 / "
                f"`cli.py modelzoo-price {item['endpoint']}` 看价格"
            )
        lines.append("")
    lines.append("告诉我编号或 endpoint 名，我接着往下帮你出参数卡。")
    return "\n".join(lines).strip()


def _fetch_outputs_example_url(api_key: str, endpoint: str) -> tuple[str | None, str]:
    """对单个 endpoint 打一次 detail，从 outputs_example 拿第一张示例图/视频 URL。

    返回 (url, source)。source 取值：
      - 'outputs_example'：拿到了真示例图
      - 'none'：没拿到（detail 失败 / outputs_example 空 / endpoint 是 LLM/TTS 类没图）
    单条失败静默兜底，不抛异常，不影响其他候选。
    """
    if not endpoint:
        return None, "none"
    try:
        result = get_detail(api_key, endpoint)
    except Exception:
        return None, "none"
    data = (result.get("data") or {}).get("data") or result.get("data") or {}
    outputs = data.get("outputs_example") or {}
    if not isinstance(outputs, dict):
        return None, "none"
    images = outputs.get("images") or []
    if images:
        first = images[0] if isinstance(images, list) else None
        if isinstance(first, str) and first.strip():
            return first.strip(), "outputs_example"
    videos = outputs.get("videos") or []
    if videos:
        first = videos[0] if isinstance(videos, list) else None
        if isinstance(first, str) and first.strip():
            return first.strip(), "outputs_example"
    return None, "none"


def pick_endpoint_candidates(
    api_key: str,
    query: str,
    modality: str,
    *,
    limit: int = 10,
    page_size: int = 50,
) -> dict[str, Any]:
    """搜 ModelZoo endpoint，全部召回不截断；只按 modality 排序。

    设计变化（vs 旧版）：
    - 不再按 modality 过滤候选，全部返回（旧版误杀「万相图片版」等真实 case）
    - 每条候选挂 modality_hint / modality_reason，供 LLM 按用户意图重排呈现
    - 只对最终进入 limit 的候选并行打 detail 拿 outputs_example 示例图（list API 不带）
    - limit 默认 10，调用方可放大到 30（cli.py 上限 30）
    """
    keyword = (query or "").strip()
    target = (modality or "image").lower()
    result = list_endpoints(
        api_key,
        keyword=keyword,
        page=1,
        page_size=page_size,
        sort="Auto",
    )
    data = (result.get("data") or {}).get("data") or result.get("data") or {}
    items = data.get("list") or []

    # 去重，保留原始 raw item（后续要给它注入 cover_image）
    seen: set[str] = set()
    raw_unique: list[dict[str, Any]] = []
    for item in items:
        endpoint = str(item.get("endpoint") or "").strip()
        if not endpoint or endpoint in seen:
            continue
        seen.add(endpoint)
        raw_unique.append(item)

    # 按 modality 排序（用 infer_modality_hint，不需要先 summarize）
    def sort_key(it: dict[str, Any]) -> int:
        hint, _ = infer_modality_hint(it)
        if hint == target:
            return 0
        if hint == "unknown":
            return 1
        return 2

    raw_unique.sort(key=sort_key)
    top_n = raw_unique[:limit]

    # 并行打 detail 拿 outputs_example 示例图（只对最终 top N 打）
    if top_n:
        with ThreadPoolExecutor(max_workers=min(10, len(top_n))) as pool:
            cover_results = list(pool.map(
                lambda it: _fetch_outputs_example_url(api_key, str(it.get("endpoint") or "")),
                top_n,
            ))
        for it, (url, source) in zip(top_n, cover_results):
            if url:
                it["_cover_image_url"] = url
                it["_cover_image_source"] = source

    candidates = [summarize_modelzoo_candidate(it) for it in top_n]

    return {
        "source": "modelzoo-pick",
        "modality": "video" if target == "video" else "image",
        "query": keyword,
        "candidates": candidates,
        "reply_markdown": build_modelzoo_reply_markdown(candidates, modality=target, query=keyword),
    }
