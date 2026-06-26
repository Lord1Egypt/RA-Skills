from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any


SKILL_SCRIPTS = Path("/Users/Abigale/.codex/skills/wechat-article-workflow/scripts").resolve()
DEFAULT_THEME_NAME = "elegant-gold"
DEFAULT_TEMPLATE_NAME = "default"

if str(SKILL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SKILL_SCRIPTS))

from wechat_html_renderer import (  # noqa: E402
    apply_template,
    available_template_catalog,
    available_themes,
    load_theme,
    markdown_to_wechat_html,
    render_standalone_document,
    theme_to_dict,
)


def hex_to_rgb(value: str, default: tuple[int, int, int] = (179, 131, 47)) -> tuple[int, int, int]:
    raw = str(value or "").strip().lstrip("#")
    if len(raw) == 3:
        raw = "".join(char * 2 for char in raw)
    if len(raw) != 6:
        return default
    try:
        return tuple(int(raw[index:index + 2], 16) for index in range(0, 6, 2))
    except ValueError:
        return default


def rgba_string(value: str, alpha: float) -> str:
    red, green, blue = hex_to_rgb(value)
    clamped_alpha = max(0.0, min(1.0, alpha))
    return f"rgba({red},{green},{blue},{clamped_alpha:.2f})"


def replace_style_color(style: str, color: str) -> str:
    if re.search(r"color\s*:[^;]+;", style):
        return re.sub(r"color\s*:[^;]+;", f"color:{color};", style, count=1)
    return f"{style}color:{color};"


def style_has_white_text(style: str) -> bool:
    return bool(re.search(r"color\s*:\s*(?:#fff(?:fff)?|white|rgba\(255\s*,\s*255\s*,\s*255\s*,\s*1(?:\.0+)?\))", style, re.I))


def apply_theme_highlight_overrides(html: str, theme: Any) -> str:
    primary = str(getattr(theme, "primary", "") or "#b3832f").strip() or "#b3832f"

    def recolor_heading(match: re.Match[str]) -> str:
        tag = match.group(1)
        style = match.group(2)
        if style_has_white_text(style):
            return match.group(0)
        return f'<{tag} style="{replace_style_color(style, primary)}">'

    def decorate_strong(match: re.Match[str]) -> str:
        style = match.group(1) or ""
        next_style = replace_style_color(style, primary)
        if "font-weight:" not in next_style:
            next_style += "font-weight:800;"
        return f'<strong style="{next_style}">'

    def decorate_inline_code(match: re.Match[str]) -> str:
        style = match.group(1) or ""
        normalized = style.lower()
        if not any(token in normalized for token in ("background:", "border:", "padding:", "border-radius:")):
            return match.group(0)
        return f'<code style="font-family:inherit;font-size:1em;color:{primary};font-weight:700;">'

    highlighted = re.sub(r"<(h[1-3]) style=\"([^\"]*?)\">", recolor_heading, html)
    highlighted = re.sub(r"<strong(?: style=\"([^\"]*?)\")?>", decorate_strong, highlighted)
    highlighted = re.sub(r"<code style=\"([^\"]*?)\">", decorate_inline_code, highlighted)

    if str(getattr(theme, "hero_variant", "") or "").strip() == "winter-ins":
        highlighted = re.sub(
            r'(<p style="margin:18px 0 6px;[^"]*?)color:[^;]+;([^"]*font-weight:700;[^"]*">)',
            rf"\1color:{primary};\2",
            highlighted,
            count=0,
        )

    return highlighted


def apply_html_typography_overrides(html: str, typography: dict[str, Any], theme: Any | None = None) -> str:
    paragraph_gap = clamp_int(typography.get("paragraphGap"), 8, 32, 16)

    def replace_paragraph_margin(match: re.Match[str]) -> str:
        style = match.group(1)
        updated = re.sub(r"margin:0 0 \d+px;", f"margin:0 0 {paragraph_gap}px;", style, count=1)
        return f'<p style="{updated}">'

    updated_html = re.sub(r'<p style="([^"]*?)">', replace_paragraph_margin, html)
    if theme is None:
        return updated_html
    return apply_theme_highlight_overrides(updated_html, theme)


def clamp_int(value: Any, minimum: int, maximum: int, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(maximum, parsed))


def resolve_theme(theme_name: str | None = None, template_name: str | None = None) -> tuple[Any, str, str]:
    normalized_theme = str(theme_name or DEFAULT_THEME_NAME).strip() or DEFAULT_THEME_NAME
    if normalized_theme not in available_themes():
        normalized_theme = DEFAULT_THEME_NAME

    supported_templates = {item.get("id") for item in available_template_catalog()}
    normalized_template = str(template_name or DEFAULT_TEMPLATE_NAME).strip() or DEFAULT_TEMPLATE_NAME
    if normalized_template not in supported_templates:
        normalized_template = DEFAULT_TEMPLATE_NAME

    return apply_template(load_theme(normalized_theme), normalized_template), normalized_theme, normalized_template


def strip_winter_ins_hero_copy(html: str, theme: Any) -> str:
    if str(getattr(theme, "hero_variant", "") or "").strip() != "winter-ins":
        return html

    cleaned = html
    cleaned = re.sub(
        r'(<p style="margin:0 0 \d+px;font-size:12px;line-height:1\.6;color:[^"]+;">[^<]*<span style="color:[^"]+;margin-left:12px;">).*?(</span></p>)',
        r"\1&nbsp;\2",
        cleaned,
        count=1,
        flags=re.S,
    )
    cleaned = re.sub(
        r'(<table style="width:100%;border-collapse:collapse;margin:0 0 18px;background:[^"]+;color:#fff;"><tr><td style="padding:7px 12px;font-size:11px;letter-spacing:0\.12em;font-weight:700;text-transform:uppercase;">).*?(</td><td style="padding:7px 12px;font-size:11px;letter-spacing:0\.12em;font-weight:700;text-transform:uppercase;text-align:right;">).*?(</td></tr></table>)',
        r"\1&nbsp;\2&nbsp;\3",
        cleaned,
        count=1,
        flags=re.S,
    )
    cleaned = re.sub(
        r'(<div style="display:grid;grid-template-columns:1fr 1fr;gap:0;margin-bottom:18px;background:[^"]+;color:#fff;"><div style="padding:7px 12px;font-size:11px;letter-spacing:0\.12em;font-weight:700;text-transform:uppercase;">).*?(</div><div style="padding:7px 12px;font-size:11px;letter-spacing:0\.12em;font-weight:700;text-transform:uppercase;text-align:right;">).*?(</div></div>)',
        r"\1&nbsp;\2&nbsp;\3",
        cleaned,
        count=1,
        flags=re.S,
    )
    cleaned = re.sub(
        r'(<div style="margin-bottom:16px;">.*?</div><p style="margin:0 0 )\d+(px;text-align:center;font-size:\d+px;line-height:1\.95;color:[^"]+;">)',
        r"\g<1>0\2",
        cleaned,
        count=1,
        flags=re.S,
    )
    cleaned = re.sub(
        r'<p style="margin:0;text-align:center;font-size:11px;line-height:1\.7;color:[^"]+;font-style:italic;">.*?</p>',
        "",
        cleaned,
        count=1,
        flags=re.S,
    )
    cleaned = re.sub(
        r'<p style="margin:16px 0 0;text-align:center;font-size:13px;color:[^"]+;letter-spacing:0\.32em;">.*?</p>',
        "",
        cleaned,
        count=1,
        flags=re.S,
    )
    return cleaned


def render_wechat_preview(
    markdown_text: str,
    *,
    theme: Any,
    typography: dict[str, Any] | None = None,
    metadata_overrides: dict[str, Any] | None = None,
    template_name: str | None = None,
    wechat_safe: bool = True,
) -> dict[str, Any]:
    typography = typography or {}
    metadata_overrides = metadata_overrides or {}

    body_html = apply_html_typography_overrides(
        markdown_to_wechat_html(
            markdown_text,
            theme=theme,
            template_name=template_name,
            metadata_overrides=metadata_overrides,
            wechat_safe=wechat_safe,
        ),
        typography,
        theme,
    )
    standalone_html = apply_html_typography_overrides(
        render_standalone_document(
            markdown_text,
            theme=theme,
            template_name=template_name,
            metadata_overrides=metadata_overrides,
            wechat_safe=wechat_safe,
        ),
        typography,
        theme,
    )
    body_html = strip_winter_ins_hero_copy(body_html, theme)
    standalone_html = strip_winter_ins_hero_copy(standalone_html, theme)
    return {
        "bodyHtml": body_html,
        "standaloneHtml": standalone_html,
        "sourceHtml": standalone_html,
        "wechatSafeBodyHtml": body_html,
        "wechatSafeStandaloneHtml": standalone_html,
        "wechatSafeSourceHtml": standalone_html,
        "theme": theme_to_dict(theme),
    }


def render_article_html(
    markdown_text: str,
    *,
    theme_name: str | None = None,
    template_name: str | None = None,
    typography: dict[str, Any] | None = None,
    metadata_overrides: dict[str, Any] | None = None,
    wechat_safe: bool = True,
) -> dict[str, Any]:
    theme, resolved_theme_name, resolved_template_name = resolve_theme(theme_name, template_name)
    rendered = render_wechat_preview(
        markdown_text,
        theme=theme,
        typography=typography,
        metadata_overrides=metadata_overrides,
        template_name=None,
        wechat_safe=wechat_safe,
    )
    rendered["themeName"] = resolved_theme_name
    rendered["templateName"] = resolved_template_name
    return rendered
