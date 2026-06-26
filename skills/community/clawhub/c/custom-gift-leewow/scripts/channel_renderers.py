#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable


def normalize_plain_text(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def escape_table_cell(value: object) -> str:
    text = normalize_plain_text(value)
    if not text:
        return "-"
    return text.replace("|", "\\|")


def compact_description(value: object, limit: int = 56) -> str:
    text = normalize_plain_text(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def build_customer_subtitle(name: str, sku_type: str, shipping: str) -> str:
    title = normalize_plain_text(name).lower()
    sku = normalize_plain_text(sku_type).lower()
    key = f"{title} {sku}"

    mapping = [
        (("hoodie", "sweatshirt"), "可定制连帽卫衣，适合大面积图案展示"),
        (("tote", "bag"), "可定制通勤包袋，适合日常使用"),
        (("crossbody",), "可定制斜挎包，适合轻便出行"),
        (("socks",), "可定制袜子，适合趣味图案设计"),
        (("pillowcase", "pillow case"), "可定制家居用品，适合照片或插画"),
        (("travel pillow",), "可定制旅行枕，适合舒适出行场景"),
        (("iphone", "phone case"), "可定制手机壳，适合个性化图案"),
        (("framed print", "print", "poster"), "可定制装饰画，适合展示你的作品"),
    ]

    for keywords, subtitle in mapping:
        if any(keyword in key for keyword in keywords):
            return subtitle

    shipping_suffix = f" · Ships from {shipping}" if shipping else ""
    return f"支持自定义设计的商品{shipping_suffix}".strip()


def normalize_browse_item(template: dict, price_display: str) -> dict:
    sku_type = normalize_plain_text(template.get("skuType")) or "-"
    shipping = normalize_plain_text(template.get("shippingOrigin")) or "CN"
    description = build_customer_subtitle(
        name=normalize_plain_text(template.get("name", "Unnamed Product")) or "Unnamed Product",
        sku_type=sku_type,
        shipping=shipping,
    )
    info_parts = [f"SKU: {sku_type}", f"Ships: {shipping}"]
    return {
        "templateId": template.get("templateId", "?"),
        "name": normalize_plain_text(template.get("name", "Unnamed Product")) or "Unnamed Product",
        "coverImage": normalize_plain_text(template.get("coverImage")),
        "price": price_display or "-",
        "skuType": sku_type,
        "shippingOrigin": shipping,
        "description": description,
        "info": " · ".join(info_parts),
    }


class ChannelRenderer(ABC):
    channel: str = "plain"

    @abstractmethod
    def render_browse(self, items: Iterable[dict]) -> str:
        raise NotImplementedError

    def render_browse_messages(self, items: Iterable[dict]) -> list[str]:
        return [self.render_browse(items)]


class PlainTextRenderer(ChannelRenderer):
    channel = "plain"

    def render_browse(self, items: Iterable[dict]) -> str:
        rows = list(items)
        if not rows:
            return "No matching templates found. Try a different category or browse all."

        lines = [f"Available Product Templates ({len(rows)} results)", ""]
        for index, item in enumerate(rows, 1):
            lines.append(f"{index}. {item['name']}")
            lines.append(f"Template ID: `{item['templateId']}`")
            lines.append(f"Price: {item['price']}")
            lines.append(item["info"])
            if item["coverImage"]:
                lines.append(f"Preview: {item['coverImage']}")
            lines.append("")
        lines.append("Use `generate_preview` with a `Template ID` to create a customized design.")
        return "\n".join(lines)


class FeishuRenderer(ChannelRenderer):
    channel = "feishu"

    def render_browse(self, items: Iterable[dict]) -> str:
        messages = self.render_browse_messages(items)
        return "\n\n".join(messages)

    def render_browse_messages(self, items: Iterable[dict]) -> list[str]:
        rows = list(items)
        if not rows:
            return ["No matching templates found. Try a different category or browse all."]

        messages: list[str] = []
        for item in rows:
            description = item["description"] or item["info"]
            price_display = str(item["price"]).replace("|", "\\|")
            lines = [
                f"## {escape_table_cell(item['name'])}",
                description,
                f"**Template ID:** `{item['templateId']}`",
                f"**Price:** {price_display}",
            ]
            if item["coverImage"]:
                lines.extend(["", f"![{escape_table_cell(item['name'])}]({item['coverImage']})"])
            messages.append("\n".join(lines))
        return messages

    @staticmethod
    def _format_image_cell(name: str, cover_url: str) -> str:
        if not cover_url:
            return "-"
        return f"![{escape_table_cell(name or 'Preview')}]({cover_url})"

    @staticmethod
    def _format_preview_link(cover_url: str) -> str:
        if not cover_url:
            return "-"
        return f"[Open image]({cover_url})"


_RENDERERS = {
    PlainTextRenderer.channel: PlainTextRenderer(),
    FeishuRenderer.channel: FeishuRenderer(),
}


def get_channel_renderer(channel: str | None) -> ChannelRenderer:
    normalized = normalize_plain_text(channel).lower() or FeishuRenderer.channel
    if normalized not in _RENDERERS:
        supported = ", ".join(sorted(_RENDERERS))
        raise ValueError(f"Unsupported channel '{channel}'. Supported: {supported}")
    return _RENDERERS[normalized]
