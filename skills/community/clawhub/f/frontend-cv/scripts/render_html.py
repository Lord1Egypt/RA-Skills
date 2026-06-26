#!/usr/bin/env python3
"""Render resume YAML to HTML with five RenderCV-inspired themes."""

from __future__ import annotations

import html
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import yaml

SKILL_DIR = Path(__file__).parent.parent
THEME_DIR = SKILL_DIR / "references" / "themes"

SECTION_TITLES = {
    "summary": "个人评价",
    "experience": "工作经历",
    "projects": "项目经历",
    "skills": "专业技能",
    "education": "教育背景",
}

THEME_ALIASES = {
    "moderncv": "modern",
}

ICON_SVGS = {
    "location": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 22s7-7.2 7-13a7 7 0 1 0-14 0c0 5.8 7 13 7 13Zm0-9.5a3 3 0 1 1 0-6 3 3 0 0 1 0 6Z"/></svg>',
    "email": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm0 2v.5l9 5.7 9-5.7V7l-9 5.7L3 7Z"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6.6 10.8a15.5 15.5 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.24 11.2 11.2 0 0 0 3.52.56 1 1 0 0 1 1 1V21a1 1 0 0 1-1 1C10.85 22 2 13.15 2 2a1 1 0 0 1 1-1h4.5a1 1 0 0 1 1 1 11.2 11.2 0 0 0 .56 3.52 1 1 0 0 1-.24 1l-2.22 2.28Z"/></svg>',
    "website": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M10.6 13.4a1 1 0 0 1 0-1.4l3.4-3.4a3 3 0 1 1 4.24 4.24l-1.82 1.82a3 3 0 0 1-4.24 0 .99.99 0 1 1 1.4-1.42 1 1 0 0 0 1.42 0l1.82-1.82a1 1 0 1 0-1.42-1.42l-3.4 3.4a1 1 0 0 1-1.4 0Zm2.8-2.8a1 1 0 0 1 0 1.4l-3.4 3.4a3 3 0 0 1-4.24-4.24l1.82-1.82a3 3 0 0 1 4.24 0 .99.99 0 1 1-1.4 1.42 1 1 0 0 0-1.42 0l-1.82 1.82a1 1 0 0 0 1.42 1.42l3.4-3.4a1 1 0 0 1 1.4 0Z"/></svg>',
    "github": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 .5a12 12 0 0 0-3.8 23.4c.6.1.82-.26.82-.58v-2.1c-3.33.72-4.03-1.42-4.03-1.42-.55-1.38-1.33-1.74-1.33-1.74-1.08-.74.08-.73.08-.73 1.2.08 1.83 1.22 1.83 1.22 1.06 1.82 2.79 1.3 3.46 1 .1-.77.42-1.3.76-1.6-2.66-.31-5.45-1.33-5.45-5.9 0-1.3.47-2.36 1.23-3.2-.12-.3-.53-1.56.12-3.23 0 0 1-.32 3.3 1.23a11.4 11.4 0 0 1 6 0c2.3-1.55 3.3-1.23 3.3-1.23.65 1.67.24 2.93.12 3.23.77.84 1.23 1.9 1.23 3.2 0 4.59-2.8 5.58-5.47 5.88.43.38.82 1.11.82 2.25v3.33c0 .32.21.7.83.58A12 12 0 0 0 12 .5Z"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M5.5 8.5A1.5 1.5 0 1 1 5.5 5a1.5 1.5 0 0 1 0 3.5ZM4 10h3v10H4V10Zm5 0h2.9v1.4h.04c.4-.77 1.4-1.58 2.88-1.58C18.1 9.82 20 11.5 20 14.7V20h-3v-4.7c0-1.12-.02-2.56-1.56-2.56-1.57 0-1.81 1.22-1.81 2.48V20H10V10Z"/></svg>',
}


def esc(value: object) -> str:
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def format_top_note(theme: dict) -> str:
    mode = theme.get("meta", {}).get("top_note", "english")
    now = datetime.now()
    if mode == "zh":
        return now.strftime("更新于 %Y年%m月")
    return now.strftime("Last updated in %b %Y")


def format_date(value: object) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if not text:
        return ""

    lowered = text.lower()
    if lowered in {"present", "current", "now", "ongoing"}:
        return "至今"

    year_month = re.fullmatch(r"(\d{4})-(\d{2})", text)
    if year_month:
        return f"{year_month.group(1)}.{year_month.group(2)}"

    year_only = re.fullmatch(r"(\d{4})", text)
    if year_only:
        return year_only.group(1)

    return text


def format_date_range(start: object, end: object) -> str:
    start_text = format_date(start)
    end_text = format_date(end)

    if start_text and end_text:
        return f"{start_text} – {end_text}"
    return start_text or end_text


def normalize_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url):
        return url
    return f"https://{url}"


def url_display(url: str, mode: str) -> str:
    normalized = normalize_url(url)
    if not normalized:
        return ""

    parsed = urlparse(normalized)
    base = parsed.netloc or parsed.path
    base = base.removeprefix("www.")
    path = parsed.path.rstrip("/")
    if mode == "full":
        return f"{base}{path}"
    return base


def social_link(network: str, username: str) -> str:
    if network == "GitHub":
        return f"https://github.com/{username}"
    if network == "LinkedIn":
        return f"https://linkedin.com/in/{username}"
    return username


def social_display(network: str, username: str, mode: str) -> str:
    if mode == "url":
        return url_display(social_link(network, username), "full")
    return username


def load_theme(name: str) -> dict:
    theme_name = THEME_ALIASES.get(name, name)
    theme_path = THEME_DIR / f"{theme_name}.yaml"
    if not theme_path.exists():
        available = ", ".join(sorted(path.stem for path in THEME_DIR.glob("*.yaml")))
        raise ValueError(f"未知主题: {name}。可用主题: {available}")

    with open(theme_path, "r", encoding="utf-8") as handle:
        theme = yaml.safe_load(handle) or {}

    theme.setdefault("meta", {})
    theme.setdefault("fonts", {})
    theme.setdefault("colors", {})
    theme.setdefault("page", {})
    theme.setdefault("header", {})
    theme.setdefault("section", {})
    theme.setdefault("entry", {})
    theme["theme_name"] = theme_name
    theme["variant"] = theme["meta"].get("variant", theme_name)
    return theme


def make_connections(cv: dict, theme: dict) -> list[dict]:
    header = theme["header"]
    items = []

    if cv.get("location"):
        items.append({"kind": "location", "label": cv["location"], "href": ""})
    if cv.get("email"):
        items.append(
            {
                "kind": "email",
                "label": cv["email"],
                "href": f"mailto:{cv['email']}",
            }
        )
    if cv.get("phone"):
        phone_label = str(cv["phone"])
        phone_href = "tel:" + re.sub(r"[^\d+]", "", phone_label)
        items.append({"kind": "phone", "label": phone_label, "href": phone_href})
    if cv.get("website"):
        items.append(
            {
                "kind": "website",
                "label": url_display(cv["website"], header.get("website_display", "domain")),
                "href": normalize_url(cv["website"]),
            }
        )

    for network in cv.get("social_networks", []):
        net = network.get("network", "")
        username = network.get("username", "")
        if not net or not username:
            continue
        items.append(
            {
                "kind": net.lower(),
                "label": social_display(net, username, header.get("social_display", "username")),
                "href": social_link(net, username),
            }
        )

    return items


def render_connections(cv: dict, theme: dict) -> str:
    items = make_connections(cv, theme)
    if not items:
        return ""

    show_icons = theme["header"].get("show_icons", False)
    separator = theme["header"].get("separator", "")
    rendered = []
    for item in items:
        icon = ""
        if show_icons:
            icon_markup = ICON_SVGS.get(item["kind"], ICON_SVGS.get("website", ""))
            icon = f'<span class="connection-icon">{icon_markup}</span>'

        tag = "a" if item["href"] else "span"
        href = f' href="{esc(item["href"])}"' if item["href"] else ""
        rendered.append(
            f'<{tag} class="connection connection--{esc(item["kind"])}"{href}>{icon}<span>{esc(item["label"])}</span></{tag}>'
        )

    if separator:
        joiner = f'<span class="connection-separator" aria-hidden="true">{esc(separator)}</span>'
        return joiner.join(rendered)
    return "".join(rendered)


def render_header(cv: dict, theme: dict) -> str:
    headline = esc(cv.get("headline", ""))
    headline_markup = f'<p class="resume-headline">{headline}</p>' if headline else ""
    connections = render_connections(cv, theme)
    connections_markup = (
        f'<div class="resume-connections">{connections}</div>' if connections else ""
    )

    return f"""
    <div class="top-note">{esc(format_top_note(theme))}</div>
    <header class="resume-header">
      <h1 class="resume-name">{esc(cv.get("name", ""))}</h1>
      {headline_markup}
      {connections_markup}
    </header>"""


def compose_primary_line(item: dict, section_name: str, variant: str) -> tuple[str, str]:
    if section_name == "experience":
        position = esc(item.get("position", ""))
        company = esc(item.get("company", ""))
        location = esc(item.get("location", ""))

        if variant == "sb2nov":
            primary = f"<strong>{position}</strong>" if position else f"<strong>{company}</strong>"
            subtitle = f"<span>{company}</span>" if company and company != position else ""
            return primary, subtitle

        chunks = []
        if position:
            chunks.append(f"<strong>{position}</strong>")
        if company:
            chunks.append(company if not chunks else f", {company}")
        if location:
            chunks.append(f" – {location}" if chunks else location)
        return "".join(chunks), ""

    if section_name == "education":
        institution = esc(item.get("institution", ""))
        degree = esc(item.get("degree", ""))
        area = esc(item.get("area", ""))
        location = esc(item.get("location", ""))
        degree_bits = " · ".join(bit for bit in [degree, area] if bit)

        if variant == "sb2nov":
            primary = f"<strong>{institution}</strong>"
            if degree_bits:
                subtitle = f"<span>{degree_bits}</span>"
            else:
                subtitle = ""
            return primary, subtitle

        parts = [f"<strong>{institution}</strong>" if institution else ""]
        if degree_bits:
            parts.append(f", {degree_bits}" if parts[0] else degree_bits)
        if location:
            parts.append(f" – {location}" if parts[0] or degree_bits else location)
        return "".join(parts), ""

    if section_name == "projects":
        name = esc(item.get("name", ""))
        summary = esc(item.get("summary", ""))
        primary = f"<strong>{name}</strong>" if name else ""
        subtitle = f"<span>{summary}</span>" if summary else ""
        return primary, subtitle

    title = esc(item.get("name", ""))
    summary = esc(item.get("summary", ""))
    return f"<strong>{title}</strong>" if title else "", f"<span>{summary}</span>" if summary else ""


def render_highlights(highlights: list) -> str:
    if not highlights:
        return ""
    items = "\n".join(f"          <li>{esc(point)}</li>" for point in highlights)
    return f"""
        <ul class="highlights">
{items}
        </ul>"""


def render_regular_entry(item: dict, section_name: str, theme: dict) -> str:
    variant = theme["variant"]
    entry = theme["entry"]
    layout_class = "entry--left-meta" if entry.get("layout") == "left-meta" else "entry--right-meta"
    title_line, subtitle_line = compose_primary_line(item, section_name, variant)

    if section_name == "experience":
        meta_lines = []
        if variant == "sb2nov" and item.get("location"):
            meta_lines.append(esc(item["location"]))
        meta_lines.append(format_date_range(item.get("start_date"), item.get("end_date")))
        summary_text = esc(item.get("summary", ""))
    elif section_name == "education":
        meta_lines = []
        if variant == "sb2nov" and item.get("location"):
            meta_lines.append(esc(item["location"]))
        meta_lines.append(format_date_range(item.get("start_date"), item.get("end_date")))
        summary_text = esc(item.get("summary", ""))
    elif section_name == "projects":
        meta_lines = [format_date_range(item.get("start_date"), item.get("end_date", item.get("date")))]
        summary_text = ""
    else:
        meta_lines = [format_date_range(item.get("start_date"), item.get("end_date", item.get("date")))]
        summary_text = esc(item.get("summary", ""))

    meta_parts = [line for line in meta_lines if line]
    if meta_parts:
        meta_markup = '<div class="entry-meta">' + "".join(
            f'<span class="entry-meta-line">{line}</span>' for line in meta_parts
        ) + "</div>"
    else:
        meta_markup = ""
    subtitle_markup = f'<div class="entry-subtitle">{subtitle_line}</div>' if subtitle_line else ""
    summary_markup = f'<div class="entry-summary">{summary_text}</div>' if summary_text else ""
    highlights_markup = render_highlights(item.get("highlights", []))

    return f"""
      <article class="entry {layout_class}">
        <div class="entry-main">
          <div class="entry-title-line">{title_line}</div>
          {subtitle_markup}
          {summary_markup}
          {highlights_markup}
        </div>
        {meta_markup}
      </article>"""


def render_summary_section(items: list[str]) -> str:
    paragraphs = "\n".join(f"      <p>{esc(item)}</p>" for item in items if item)
    return f"""
    <div class="section-body">
{paragraphs}
    </div>"""


def render_skill_section(items: list[dict]) -> str:
    rows = []
    for item in items:
        label = esc(item.get("label", ""))
        details = esc(item.get("details", ""))
        rows.append(
            f'      <div class="skill-row"><span class="skill-label">{label}：</span><span>{details}</span></div>'
        )
    return """
    <div class="section-body skill-list">
{rows}
    </div>""".format(rows="\n".join(rows))


def render_regular_section(items: list[dict], section_name: str, theme: dict) -> str:
    entries = "\n".join(render_regular_entry(item, section_name, theme) for item in items)
    return f"""
    <div class="section-body entry-list">
{entries}
    </div>"""


def render_section(title: str, items: list, section_name: str, theme: dict) -> str:
    if not items:
        return ""

    heading = (
        '<div class="section-heading">'
        f'<h2 class="section-title">{esc(title)}</h2>'
        "</div>"
    )

    if section_name == "summary":
        body = render_summary_section(items)
    elif section_name == "skills":
        body = render_skill_section(items)
    else:
        body = render_regular_section(items, section_name, theme)

    return f"""
  <section class="section section--{esc(section_name)}">
    {heading}
    {body}
  </section>"""


def css_variables(theme: dict) -> str:
    fonts = theme["fonts"]
    colors = theme["colors"]
    page = theme["page"]
    header = theme["header"]
    section = theme["section"]
    entry = theme["entry"]
    connection_justify = "center" if header.get("align", "left") == "center" else "flex-start"
    name_weight = str(header.get("name_weight", 700))

    return f"""
:root {{
  --body-font: {fonts.get("body_stack", '"Noto Sans SC","PingFang SC",sans-serif')};
  --heading-font: {fonts.get("heading_stack", fonts.get("body_stack", '"Noto Sans SC","PingFang SC",sans-serif'))};
  --section-font: {fonts.get("section_stack", fonts.get("heading_stack", fonts.get("body_stack", '"Noto Sans SC","PingFang SC",sans-serif')))};
  --name-color: {colors.get("name", "#004f90")};
  --headline-color: {colors.get("headline", colors.get("name", "#004f90"))};
  --section-color: {colors.get("section", colors.get("name", "#004f90"))};
  --link-color: {colors.get("links", colors.get("name", "#004f90"))};
  --text: {colors.get("text", "#1f2933")};
  --muted: {colors.get("muted", "#666")};
  --muted-soft: {colors.get("muted_soft", "#9a9a9a")};
  --rule: {colors.get("rule", "#d6dde7")};
  --title-color: {colors.get("title", colors.get("text", "#111"))};
  --subtitle-color: {colors.get("subtitle", colors.get("muted", "#666"))};
  --bullet-color: {colors.get("bullet", colors.get("text", "#111"))};
  --page-top: {page.get("top", "0.7in")};
  --page-right: {page.get("right", "0.7in")};
  --page-bottom: {page.get("bottom", "0.7in")};
  --page-left: {page.get("left", "0.7in")};
  --name-size: {header.get("name_size", "30pt")};
  --headline-size: {header.get("headline_size", "10pt")};
  --connections-size: {header.get("connection_size", "9.2pt")};
  --section-size: {section.get("title_size", "18pt")};
  --section-weight: {section.get("title_weight", 700)};
  --body-size: {entry.get("body_size", "10pt")};
  --meta-size: {entry.get("meta_size", "9.1pt")};
  --meta-width: {entry.get("meta_width", "3.3cm")};
  --entry-gap: {entry.get("gap", "0.4cm")};
  --entry-column-gap: {entry.get("column_gap", "0.45cm")};
  --header-align: {header.get("align", "left")};
  --connection-justify: {connection_justify};
  --header-gap: {header.get("gap", "0.55cm")};
  --section-space: {section.get("space_above", "0.55cm")};
  --bullet-indent: {entry.get("bullet_indent", "0.22cm")};
  --bullet-text-gap: {entry.get("bullet_text_gap", "0.35cm")};
  --highlights-top: {entry.get("highlights_top", "0.12cm")};
  --bullet-gap: {entry.get("bullet_gap", "0.08cm")};
  --name-weight: {name_weight};
  --name-tracking: {header.get("name_tracking", "0")};
  --bullet: "{entry.get("bullet", "•")}";
}}"""


BASE_CSS = """
* {
  box-sizing: border-box;
}

html {
  background: #fff;
}

body {
  margin: 0;
  background: #fff;
  color: var(--text);
  font-family: var(--body-font);
  font-size: var(--body-size);
  line-height: 1.35;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

a {
  color: var(--link-color);
  text-decoration: none;
}

.page {
  width: 210mm;
  min-height: 297mm;
  margin: 10px auto 18px;
  padding: var(--page-top) var(--page-right) var(--page-bottom) var(--page-left);
  background: #fff;
  position: relative;
}

.top-note {
  position: absolute;
  top: 9mm;
  right: var(--page-right);
  color: var(--muted-soft);
  font-size: 9pt;
  font-style: italic;
}

.resume-header {
  text-align: var(--header-align);
  margin-bottom: var(--header-gap);
}

.resume-name {
  margin: 0;
  font-family: var(--heading-font);
  font-size: var(--name-size);
  line-height: 1;
  color: var(--name-color);
  font-weight: var(--name-weight);
  letter-spacing: var(--name-tracking);
}

.resume-headline {
  margin: 0.18cm 0 0;
  color: var(--headline-color);
  font-size: var(--headline-size);
}

.resume-connections {
  margin-top: 0.34cm;
  display: flex;
  flex-wrap: wrap;
  gap: 0.12cm 0.32cm;
  justify-content: var(--connection-justify);
  align-items: center;
}

.connection {
  display: inline-flex;
  align-items: center;
  gap: 0.14cm;
  color: var(--link-color);
  font-size: var(--connections-size);
}

.connection-icon {
  width: 11px;
  height: 11px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: none;
}

.connection-icon svg {
  width: 11px;
  height: 11px;
  display: block;
}

.connection-separator {
  color: var(--muted);
  font-size: var(--connections-size);
}

.section {
  margin-top: var(--section-space);
}

.section-heading {
  margin: 0 0 0.18cm;
  page-break-after: avoid;
}

.section-title {
  margin: 0;
  font-family: var(--section-font);
  font-size: var(--section-size);
  line-height: 1.05;
  font-weight: var(--section-weight);
  color: var(--section-color);
}

.section-body p {
  margin: 0 0 0.12cm;
}

.entry-list {
  display: flex;
  flex-direction: column;
  gap: var(--entry-gap);
}

.entry {
  display: grid;
  grid-template-columns: minmax(0, 1fr) var(--meta-width);
  gap: var(--entry-column-gap);
  align-items: start;
  break-inside: avoid;
  page-break-inside: avoid;
}

.entry--left-meta {
  grid-template-columns: var(--meta-width) minmax(0, 1fr);
}

.entry--left-meta .entry-meta {
  order: -1;
  text-align: left;
}

.entry-main {
  min-width: 0;
}

.entry-title-line {
  font-size: var(--body-size);
  line-height: 1.32;
}

.entry-title-line strong {
  color: var(--title-color);
  font-weight: 700;
}

.entry-subtitle {
  margin-top: 0.04cm;
  color: var(--subtitle-color);
  font-size: var(--body-size);
}

.entry-summary {
  margin-top: 0.06cm;
}

.entry-meta {
  color: var(--muted);
  font-size: var(--meta-size);
  line-height: 1.26;
  text-align: right;
}

.entry-meta-line {
  display: block;
}

.highlights {
  list-style: none;
  margin: var(--highlights-top) 0 0;
  padding: 0 0 0 var(--bullet-indent);
}

.highlights li {
  position: relative;
  padding-left: var(--bullet-text-gap);
  margin-bottom: var(--bullet-gap);
  line-height: 1.28;
}

.highlights li::before {
  content: var(--bullet);
  position: absolute;
  left: 0;
  top: 0;
  color: var(--bullet-color);
}

.skill-list {
  display: flex;
  flex-direction: column;
  gap: 0.08cm;
}

.skill-row {
  display: flex;
  gap: 0.12cm;
  align-items: baseline;
  line-height: 1.3;
}

.skill-label {
  color: var(--title-color);
  font-weight: 700;
}

@page {
  size: A4;
  margin: 0;
}

@media print {
  html,
  body {
    background: #fff;
  }

  .page {
    margin: 0;
    width: auto;
    min-height: auto;
    box-shadow: none;
  }

  a {
    color: inherit;
    text-decoration: none;
  }

  * {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
}
"""


THEME_CSS = {
    "classic": """
.theme--classic .section-heading {
  border-bottom: 1px solid var(--rule);
  padding-bottom: 0.08cm;
}

.theme--classic .resume-headline {
  letter-spacing: 0.01em;
}

.theme--classic .entry-meta {
  padding-top: 0.03cm;
}

.theme--classic .skill-row {
  gap: 0.16cm;
}
""",
    "modern": """
.theme--modern .resume-name {
  font-weight: 400;
}

.theme--modern .resume-headline {
  color: var(--muted);
}

.theme--modern .section-heading {
  display: flex;
  align-items: center;
  gap: 0.34cm;
}

.theme--modern .section-heading::before {
  content: "";
  flex: none;
  width: 3.7cm;
  height: 0.13cm;
  background: var(--section-color);
}

.theme--modern .section-title {
  font-weight: 400;
}

.theme--modern .section-body {
  padding-left: 3.76cm;
}

.theme--modern .entry {
  grid-template-columns: var(--meta-width) minmax(0, 1fr);
}

.theme--modern .entry-meta {
  order: -1;
  text-align: left;
  color: var(--text);
}

.theme--modern .entry-title-line,
.theme--modern .entry-subtitle,
.theme--modern .entry-summary,
.theme--modern .highlights li,
.theme--modern .skill-row,
.theme--modern .section-body p {
  line-height: 1.3;
}
""",
    "sb2nov": """
.theme--sb2nov .resume-name {
  letter-spacing: 0.01em;
}

.theme--sb2nov .resume-headline {
  color: var(--muted);
}

.theme--sb2nov .section-heading {
  border-bottom: 1px solid var(--rule);
  padding-bottom: 0.07cm;
}

.theme--sb2nov .entry-meta {
  font-style: italic;
  line-height: 1.15;
}

.theme--sb2nov .entry-subtitle {
  font-style: italic;
}

.theme--sb2nov .entry-meta-line + .entry-meta-line {
  margin-top: 0.04cm;
}

.theme--sb2nov .entry-title-line strong {
  font-weight: 700;
}

.theme--sb2nov .skill-row {
  display: block;
}

.theme--sb2nov .skill-label {
  margin-right: 0.14cm;
}
""",
    "engineeringclassic": """
.theme--engineeringclassic .resume-name {
  font-weight: 400;
}

.theme--engineeringclassic .resume-headline {
  color: var(--muted);
}

.theme--engineeringclassic .section-heading {
  border-bottom: 1px solid var(--rule);
  padding-bottom: 0.06cm;
}

.theme--engineeringclassic .section-title {
  font-weight: 400;
}

.theme--engineeringclassic .entry-meta {
  color: var(--text);
}

.theme--engineeringclassic .entry-title-line strong {
  font-weight: 700;
}
""",
    "engineeringresumes": """
.theme--engineeringresumes .resume-name {
  font-weight: 400;
}

.theme--engineeringresumes .resume-headline {
  color: var(--muted);
}

.theme--engineeringresumes .section-heading {
  border-bottom: 1px solid var(--rule);
  padding-bottom: 0.06cm;
}

.theme--engineeringresumes .entry-list {
  gap: 0.28cm;
}

.theme--engineeringresumes .entry-meta {
  color: var(--text);
  line-height: 1.15;
}

.theme--engineeringresumes .skill-row {
  gap: 0.16cm;
}

.theme--engineeringresumes .entry-meta-line + .entry-meta-line {
  margin-top: 0.03cm;
}

.theme--engineeringresumes .highlights li::before,
.theme--sb2nov .highlights li::before {
  font-size: 0.92em;
  transform: translateY(-0.01em);
}
""",
}


def build_css(theme: dict) -> str:
    variant = theme["variant"]
    theme_css = THEME_CSS.get(variant, "")
    return css_variables(theme) + BASE_CSS + theme_css


def render_document(data: dict, theme: dict) -> str:
    cv = data.get("cv", {})
    sections = cv.get("sections", {})
    theme_name = theme["theme_name"]
    font_links = theme["fonts"].get("links", [])
    fonts_markup = "\n".join(
        f'  <link rel="stylesheet" href="{esc(link)}">' for link in font_links
    )

    rendered_sections = []
    for key in ["summary", "education", "experience", "projects", "skills"]:
        rendered_sections.append(
            render_section(SECTION_TITLES[key], sections.get(key, []), key, theme)
        )

    css = build_css(theme)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(cv.get("name", ""))} - 简历</title>
  {fonts_markup}
  <style>
{css}
  </style>
</head>
<body>
  <div class="page theme--{esc(theme_name)}">
{render_header(cv, theme)}
{''.join(rendered_sections)}
  </div>
</body>
</html>
"""


def render_html(yaml_path: str, output_path: str, theme_name: str = "modern") -> None:
    with open(yaml_path, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    theme = load_theme(theme_name)
    html_output = render_document(data, theme)

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(html_output)

    print(f"✓ {output_path} (主题: {theme['theme_name']})")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 render_html.py <yaml> [输出html] [主题]")
        sys.exit(1)

    yaml_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else str(Path(yaml_path).with_suffix(".html"))
    theme_name = sys.argv[3] if len(sys.argv) > 3 else "modern"
    render_html(yaml_path, output_path, theme_name)
