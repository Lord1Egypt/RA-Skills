#!/usr/bin/env python3
"""Generate a configurable Agentic Development Services Agreement PDF.

The generator reads one or more INI files, renders a Markdown/Jinja2 contract
source, and compiles it into a formatted PDF with optional cover page,
letterhead, header, footer, watermark, and a separate printable addressed
envelope.
"""

from __future__ import annotations

import argparse
import configparser
import html
import re
from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_TEMPLATE = BASE_DIR / "references" / "agentic_development_agreement.md"
DEFAULT_CONFIG = BASE_DIR / "config.ini"

REQUIRED_SECTIONS = [
    "provider",
    "client",
    "agreement",
    "agentic_development",
    "confidentiality_data",
    "ip",
    "risk",
    "branding",
    "envelope",
]

ADDRESS_FIELDS = ["address_line1", "address_line2", "city", "state", "postal_code", "country"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an agentic development contract PDF.")
    parser.add_argument("--config", nargs="+", default=[str(DEFAULT_CONFIG)])
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    parser.add_argument("--out", default=str(BASE_DIR / "output" / "agentic_development_contract.pdf"))
    parser.add_argument("--markdown-out", default=None)
    parser.add_argument("--envelope-out", default=None)
    parser.add_argument("--no-envelope", action="store_true")
    parser.add_argument("--no-cover", action="store_true", help="Skip cover page even if enabled in config.")
    return parser.parse_args()


def resolve_path(raw: str | Path) -> Path:
    path = Path(raw).expanduser()
    if path.is_absolute() and path.exists():
        return path
    if path.exists():
        return path.resolve()
    base_relative = BASE_DIR / path
    if base_relative.exists():
        return base_relative.resolve()
    return path.resolve()


def read_config(paths: Sequence[str | Path]) -> configparser.ConfigParser:
    config = configparser.ConfigParser(interpolation=None)
    config.optionxform = lambda optionstr: optionstr.lower()
    resolved_paths = [resolve_path(p) for p in paths]
    missing = [str(p) for p in resolved_paths if not p.exists()]
    if missing:
        raise FileNotFoundError(f"Missing config file(s): {', '.join(missing)}")
    config.read([str(p) for p in resolved_paths], encoding="utf-8")
    return config


def section_dict(config: configparser.ConfigParser, section: str) -> Dict[str, str]:
    if not config.has_section(section):
        return {}
    return {key: value.strip() for key, value in config.items(section)}


def get_bool(mapping: Dict[str, str], key: str, default: bool = False) -> bool:
    value = str(mapping.get(key, "")).strip().lower()
    if value in {"1", "true", "yes", "y", "on"}:
        return True
    if value in {"0", "false", "no", "n", "off"}:
        return False
    return default


def clean_join(parts: Iterable[str], sep: str = ", ") -> str:
    cleaned = [p.strip() for p in parts if p and p.strip()]
    return sep.join(cleaned) if cleaned else "TBD"


def format_address(section: Dict[str, str]) -> str:
    line1 = section.get("address_line1", "").strip()
    line2 = section.get("address_line2", "").strip()
    city = section.get("city", "").strip()
    state = section.get("state", "").strip()
    postal = section.get("postal_code", "").strip()
    country = section.get("country", "").strip()
    city_state_postal = " ".join(p for p in [state, postal] if p)
    city_line = clean_join([city, city_state_postal]) if city or city_state_postal else ""
    return clean_join([line1, line2, city_line, country])


def address_lines(section: Dict[str, str], include_name: bool = True) -> List[str]:
    name = section.get("trade_name") or section.get("legal_name") or "TBD"
    city = section.get("city", "").strip()
    state = section.get("state", "").strip()
    postal = section.get("postal_code", "").strip()
    city_line = clean_join([city, " ".join(p for p in [state, postal] if p)]) if city or state or postal else ""
    lines: List[str] = []
    if include_name:
        lines.append(name)
    for key in ["address_line1", "address_line2"]:
        if section.get(key):
            lines.append(section[key])
    if city_line:
        lines.append(city_line)
    if section.get("country"):
        lines.append(section["country"])
    return lines or ["TBD"]


def build_context(config: configparser.ConfigParser) -> Dict[str, Dict[str, str]]:
    context: Dict[str, Dict[str, str]] = {}
    for section in REQUIRED_SECTIONS:
        context[section] = section_dict(config, section)

    fallback_keys = {
        "provider": ["legal_name", "trade_name", "entity_type", "state_of_formation", "email", "phone", "website", "signatory_name", "signatory_title", *ADDRESS_FIELDS],
        "client": ["legal_name", "trade_name", "entity_type", "state_of_formation", "email", "phone", "website", "signatory_name", "signatory_title", *ADDRESS_FIELDS],
        "agreement": ["title", "contract_id", "agreement_date", "effective_date", "term", "governing_law", "venue", "services_summary", "project_name", "fee_type", "fee_amount", "deposit", "payment_terms", "revision_rounds", "delivery_schedule", "acceptance_period_days", "support_period_days", "warranty_days"],
        "agentic_development": ["system_description", "autonomy_level", "human_in_loop", "model_or_stack", "deployment_environment", "evaluation_plan", "monitoring_plan", "excluded_uses"],
        "confidentiality_data": ["client_data", "provider_data", "privacy_terms", "retention_period_days", "backup_policy"],
        "ip": ["pre_existing_ip", "work_product_owner", "license_back", "open_source_policy"],
        "risk": ["liability_cap", "indemnity_summary", "ai_specific_notice"],
        "branding": ["logo_monogram", "brand_name", "brand_tagline", "accent_color", "watermark_text", "footer_text"],
        "envelope": ["recipient_attention", "postage_box_text", "include_return_address"],
    }
    for section, keys in fallback_keys.items():
        for key in keys:
            context[section].setdefault(key, "TBD")

    context["provider"]["full_address"] = format_address(context["provider"])
    context["client"]["full_address"] = format_address(context["client"])
    context["generated"] = {"date": date.today().isoformat()}
    return context


def render_markdown(template_path: Path, context: Dict[str, Dict[str, str]]) -> str:
    template_path = resolve_path(template_path)
    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_path.name)
    return template.render(**context)


# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------

def hex_color(raw: str | None, fallback: str = "#1E3A8A") -> colors.Color:
    try:
        return colors.HexColor(raw or fallback)
    except Exception:
        return colors.HexColor(fallback)


def palette(branding: Dict[str, str]) -> Dict[str, colors.Color]:
    return {
        "accent": hex_color(branding.get("accent_color"), "#1E3A8A"),
        "accent_dark": hex_color(branding.get("accent_color_dark"), "#0F172A"),
        "accent_soft": hex_color(branding.get("accent_color_soft"), "#EEF2FF"),
        "muted": hex_color(branding.get("muted_color"), "#64748B"),
        "border": hex_color(branding.get("border_color"), "#E2E8F0"),
        "zebra": hex_color(branding.get("zebra_color"), "#F8FAFC"),
        "ink": colors.HexColor("#0F172A"),
        "ink_soft": colors.HexColor("#1E293B"),
        "white": colors.white,
    }


# ---------------------------------------------------------------------------
# Logo rendering
# ---------------------------------------------------------------------------

def resolve_logo_path(branding: Dict[str, str]) -> Optional[Path]:
    raw = (branding.get("logo_path") or "").strip()
    if not raw:
        return None
    p = resolve_path(raw)
    return p if p.exists() else None


def draw_logo_badge(c: pdf_canvas.Canvas, x: float, y: float, size: float,
                    branding: Dict[str, str], pal: Dict[str, colors.Color],
                    on_dark: bool = False) -> None:
    """Draw the logo at (x, y) with given square size. If logo_path is set, embed image; otherwise draw vector badge."""
    logo = resolve_logo_path(branding)
    if logo:
        try:
            c.drawImage(ImageReader(str(logo)), x, y, width=size, height=size,
                        preserveAspectRatio=True, mask="auto")
            return
        except Exception:
            pass

    monogram = (branding.get("logo_monogram") or "CT").strip()[:3] or "CT"
    radius = size * 0.18
    c.saveState()
    fill = pal["white"] if on_dark else pal["accent"]
    stroke = pal["accent_soft"] if on_dark else pal["accent_dark"]
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.8)
    c.roundRect(x, y, size, size, radius, stroke=0, fill=1)
    text_color = pal["accent"] if on_dark else pal["white"]
    c.setFillColor(text_color)
    font_size = size * (0.50 if len(monogram) <= 2 else 0.38)
    c.setFont("Helvetica-Bold", font_size)
    c.drawCentredString(x + size / 2.0, y + size / 2.0 - font_size * 0.36, monogram)
    c.restoreState()


class LogoFlowable(Flowable):
    """Flowable that renders the logo badge for cover-page placement."""

    def __init__(self, branding: Dict[str, str], pal: Dict[str, colors.Color], size: float = 1.4 * inch):
        super().__init__()
        self.branding = branding
        self.pal = pal
        self.size = size
        self.width = size
        self.height = size

    def wrap(self, aW: float, aH: float) -> tuple[float, float]:
        del aW, aH
        return self.size, self.size

    def draw(self):
        draw_logo_badge(self.canv, 0, 0, self.size, self.branding, self.pal, on_dark=False)


# ---------------------------------------------------------------------------
# Paragraph styles
# ---------------------------------------------------------------------------

def make_styles(pal: Dict[str, colors.Color]) -> Dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "CoverEyebrow": ParagraphStyle(
            "CoverEyebrow", parent=base["BodyText"], fontName="Helvetica-Bold",
            fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=pal["accent"],
            spaceAfter=8,
        ),
        "CoverTitle": ParagraphStyle(
            "CoverTitle", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=28, leading=33, alignment=TA_CENTER, textColor=pal["ink"],
            spaceAfter=10,
        ),
        "CoverSubtitle": ParagraphStyle(
            "CoverSubtitle", parent=base["BodyText"], fontName="Times-Italic",
            fontSize=13, leading=17, alignment=TA_CENTER, textColor=pal["muted"],
            spaceAfter=12,
        ),
        "CoverParties": ParagraphStyle(
            "CoverParties", parent=base["BodyText"], fontName="Times-Roman",
            fontSize=11.5, leading=16, alignment=TA_CENTER, textColor=pal["ink_soft"],
            spaceAfter=4,
        ),
        "CoverFieldLabel": ParagraphStyle(
            "CoverFieldLabel", parent=base["BodyText"], fontName="Helvetica-Bold",
            fontSize=7.5, leading=10, alignment=TA_LEFT, textColor=pal["muted"],
            spaceAfter=2,
        ),
        "CoverFieldValue": ParagraphStyle(
            "CoverFieldValue", parent=base["BodyText"], fontName="Helvetica-Bold",
            fontSize=11.5, leading=14, alignment=TA_LEFT, textColor=pal["ink"],
            spaceAfter=0,
        ),
        "CoverDisclaimer": ParagraphStyle(
            "CoverDisclaimer", parent=base["BodyText"], fontName="Times-Italic",
            fontSize=9, leading=12.5, alignment=TA_CENTER, textColor=pal["muted"],
        ),
        "Title": ParagraphStyle(
            "ContractTitle", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=17, leading=21, alignment=TA_LEFT, spaceAfter=12,
            textColor=pal["ink"],
        ),
        "Heading2": ParagraphStyle(
            "ContractHeading2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=13, leading=17, spaceBefore=14, spaceAfter=7,
            textColor=pal["ink"],
        ),
        "Heading3": ParagraphStyle(
            "ContractHeading3", parent=base["Heading3"], fontName="Helvetica-Bold",
            fontSize=10.8, leading=14, spaceBefore=8, spaceAfter=4,
            textColor=pal["accent"],
        ),
        "Body": ParagraphStyle(
            "ContractBody", parent=base["BodyText"], fontName="Times-Roman",
            fontSize=9.8, leading=13.5, alignment=TA_JUSTIFY, spaceAfter=6,
            textColor=pal["ink_soft"],
        ),
        "Bullet": ParagraphStyle(
            "ContractBullet", parent=base["BodyText"], fontName="Times-Roman",
            fontSize=9.8, leading=13.2, leftIndent=8, spaceAfter=3,
            textColor=pal["ink_soft"],
        ),
        "Callout": ParagraphStyle(
            "ContractCallout", parent=base["BodyText"], fontName="Times-Roman",
            fontSize=9.5, leading=13, leftIndent=14, rightIndent=10,
            textColor=pal["ink"], spaceAfter=10,
            borderPadding=(8, 10, 8, 14),  # type: ignore[arg-type]  # reportlab accepts 4-tuple
        ),
        "TableCell": ParagraphStyle(
            "ContractTableCell", parent=base["BodyText"], fontName="Times-Roman",
            fontSize=9, leading=12, spaceAfter=0, textColor=pal["ink_soft"],
        ),
        "TableHeader": ParagraphStyle(
            "ContractTableHeader", parent=base["BodyText"], fontName="Helvetica-Bold",
            fontSize=8.5, leading=11, textColor=pal["white"], spaceAfter=0,
        ),
        "SignatureLabel": ParagraphStyle(
            "SignatureLabel", parent=base["BodyText"], fontName="Helvetica-Bold",
            fontSize=7.5, leading=10, textColor=pal["muted"], spaceAfter=2,
        ),
        "SignatureValue": ParagraphStyle(
            "SignatureValue", parent=base["BodyText"], fontName="Helvetica",
            fontSize=10.5, leading=13, textColor=pal["ink"], spaceAfter=0,
        ),
        "SignaturePartyName": ParagraphStyle(
            "SignaturePartyName", parent=base["BodyText"], fontName="Helvetica-Bold",
            fontSize=11, leading=14, textColor=pal["ink"], spaceAfter=0,
        ),
    }


# ---------------------------------------------------------------------------
# Markdown -> flowables
# ---------------------------------------------------------------------------

BR_SENTINEL = ""
SECTION_NUMBER_RE = re.compile(r"^\s*(\d+)\.\s+(.+)$")


def inline_markup(text: str) -> str:
    text = text.replace("<br/>", BR_SENTINEL)
    escaped = html.escape(text, quote=False)
    escaped = escaped.replace(BR_SENTINEL, "<br/>")
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"__(.+?)__", r"<b>\1</b>", escaped)
    return escaped


def color_to_hex(c: colors.Color) -> str:
    return "#%02X%02X%02X" % (int(round(c.red * 255)), int(round(c.green * 255)), int(round(c.blue * 255)))


def numbered_heading_markup(text: str, pal: Dict[str, colors.Color]) -> str:
    match = SECTION_NUMBER_RE.match(text)
    if not match:
        return inline_markup(text)
    number, label = match.group(1), match.group(2)
    accent_hex = color_to_hex(pal["accent"])
    muted_hex = color_to_hex(pal["muted"])
    return (
        f'<font name="Helvetica-Bold" size="20" color="{accent_hex}">{int(number):02d}</font>'
        f'&nbsp;&nbsp;<font color="{muted_hex}">|</font>&nbsp;&nbsp;'
        f'{inline_markup(label)}'
    )


def is_table_separator(cells: Sequence[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", c.strip()) for c in cells if c.strip())


def parse_table_rows(table_lines: Sequence[str]) -> List[List[str]]:
    rows: List[List[str]] = []
    for line in table_lines:
        stripped = line.strip().strip("|")
        cells = [cell.strip() for cell in stripped.split("|")]
        if is_table_separator(cells):
            continue
        rows.append(cells)
    return rows


def table_col_widths(rows: Sequence[Sequence[str]], available_width: float) -> List[float]:
    ncols = max((len(row) for row in rows), default=1)
    if ncols == 1:
        return [available_width]
    if ncols == 2:
        return [available_width * 0.32, available_width * 0.68]
    return [available_width / ncols] * ncols


def make_table(table_lines: Sequence[str], styles: Dict[str, ParagraphStyle],
               available_width: float, pal: Dict[str, colors.Color]) -> Table:
    rows = parse_table_rows(table_lines)
    if not rows:
        rows = [[""]]
    ncols = max(len(row) for row in rows)
    normalized = [list(row) + [""] * (ncols - len(row)) for row in rows]
    data: List[List[Paragraph]] = []
    for r, row in enumerate(normalized):
        style = styles["TableHeader"] if r == 0 else styles["TableCell"]
        data.append([Paragraph(inline_markup(cell), style) for cell in row])
    table = Table(data, colWidths=table_col_widths(normalized, available_width),
                  repeatRows=1, hAlign="LEFT")
    body_styles: List[Any] = [
        ("BACKGROUND", (0, 0), (-1, 0), pal["accent"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), pal["white"]),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, pal["accent_dark"]),
        ("LINEBELOW", (0, -1), (-1, -1), 0.4, pal["border"]),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 7),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [pal["white"], pal["zebra"]]),
        ("LINEABOVE", (0, 1), (-1, -1), 0.25, pal["border"]),
    ]
    table.setStyle(TableStyle(body_styles))
    return table


def make_callout(quote_lines: Sequence[str], styles: Dict[str, ParagraphStyle],
                 available_width: float, pal: Dict[str, colors.Color]) -> Table:
    """Render a block quote as a tinted callout with an accent left rule."""
    text = inline_markup(" ".join(quote_lines)).strip()
    para = Paragraph(text, ParagraphStyle(
        "CalloutBody", parent=styles["Body"], fontName="Times-Italic",
        textColor=pal["ink_soft"], leading=13.5, fontSize=9.5, alignment=TA_LEFT,
        spaceAfter=0,
    ))
    tbl = Table([[para]], colWidths=[available_width], hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), pal["accent_soft"]),
        ("LINEBEFORE", (0, 0), (0, -1), 3, pal["accent"]),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return tbl


def make_signature_block(context: Dict[str, Dict[str, str]], styles: Dict[str, ParagraphStyle],
                         available_width: float, pal: Dict[str, colors.Color]) -> Table:
    provider = context["provider"]
    client = context["client"]
    sig_line = "_" * 28

    def column(party: Dict[str, str], role_label: str) -> List[Any]:
        return [
            Paragraph(role_label, styles["SignatureLabel"]),
            Paragraph(party.get("legal_name", "TBD"), styles["SignaturePartyName"]),
            Spacer(1, 0.55 * inch),
            Paragraph(sig_line, styles["SignatureValue"]),
            Paragraph("SIGNATURE", styles["SignatureLabel"]),
            Spacer(1, 0.18 * inch),
            Paragraph(party.get("signatory_name", "TBD"), styles["SignatureValue"]),
            Paragraph("NAME", styles["SignatureLabel"]),
            Spacer(1, 0.10 * inch),
            Paragraph(party.get("signatory_title", "TBD"), styles["SignatureValue"]),
            Paragraph("TITLE", styles["SignatureLabel"]),
            Spacer(1, 0.10 * inch),
            Paragraph("&nbsp;", styles["SignatureValue"]),
            Paragraph("DATE", styles["SignatureLabel"]),
        ]

    data = [[column(provider, "PROVIDER"), column(client, "CLIENT")]]
    col_w = (available_width - 0.4 * inch) / 2.0
    tbl = Table(data, colWidths=[col_w, col_w], hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("BACKGROUND", (0, 0), (-1, -1), pal["zebra"]),
        ("LINEABOVE", (0, 0), (-1, 0), 2, pal["accent"]),
        ("LINEBELOW", (0, -1), (-1, -1), 0.4, pal["border"]),
        ("LINEAFTER", (0, 0), (0, -1), 0.4, pal["border"]),
    ]))
    return tbl


def is_block_start(line: str) -> bool:
    stripped = line.strip()
    return (
        stripped.startswith("#")
        or stripped.startswith("- ")
        or stripped.startswith("| ")
        or stripped.startswith("|")
        or stripped.startswith("> ")
        or stripped == "[PAGE_BREAK]"
        or stripped == "[SIGNATURE_BLOCK]"
    )


def paragraph_text(lines: Sequence[str]) -> str:
    parts = []
    for raw in lines:
        if raw.endswith("  "):
            parts.append(raw.strip() + "<br/>")
        else:
            parts.append(raw.strip())
    text = " ".join(parts)
    return re.sub(r"<br/>\s+", "<br/>", text)


def markdown_to_story(markdown: str, context: Dict[str, Dict[str, str]],
                      styles: Dict[str, ParagraphStyle], available_width: float,
                      pal: Dict[str, colors.Color]) -> List[Any]:
    story: List[Any] = []
    lines = markdown.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if not line:
            i += 1
            continue
        if line == "[PAGE_BREAK]":
            story.append(PageBreak())
            i += 1
            continue
        if line == "[SIGNATURE_BLOCK]":
            story.append(Spacer(1, 0.1 * inch))
            story.append(KeepTogether(make_signature_block(context, styles, available_width, pal)))
            i += 1
            continue
        if line.startswith("# "):
            story.append(Paragraph(inline_markup(line[2:].strip()), styles["Title"]))
            story.append(Spacer(1, 0.05 * inch))
            i += 1
            continue
        if line.startswith("## "):
            heading_text = line[3:].strip()
            story.append(Paragraph(numbered_heading_markup(heading_text, pal), styles["Heading2"]))
            i += 1
            continue
        if line.startswith("### "):
            story.append(Paragraph(inline_markup(line[4:].strip()), styles["Heading3"]))
            i += 1
            continue
        if line.startswith("> "):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            story.append(make_callout(quote_lines, styles, available_width, pal))
            continue
        if line.startswith("- "):
            bullet_items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                bullet_text = lines[i].strip()[2:].strip()
                bullet_items.append(ListItem(Paragraph(inline_markup(bullet_text), styles["Bullet"]),
                                             leftIndent=12, value="●",
                                             bulletColor=pal["accent"]))
                i += 1
            story.append(ListFlowable(bullet_items, bulletType="bullet",
                                      bulletFontName="Helvetica-Bold",
                                      bulletFontSize=6, leftIndent=20,
                                      bulletColor=pal["accent"]))
            story.append(Spacer(1, 0.04 * inch))
            continue
        if line.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            story.append(make_table(table_lines, styles, available_width, pal))
            story.append(Spacer(1, 0.10 * inch))
            continue

        para_lines = [raw]
        i += 1
        while i < len(lines) and lines[i].strip() and not is_block_start(lines[i]):
            para_lines.append(lines[i])
            i += 1
        story.append(Paragraph(inline_markup(paragraph_text(para_lines)), styles["Body"]))
    return story


# ---------------------------------------------------------------------------
# Page furniture
# ---------------------------------------------------------------------------

def draw_watermark(c: pdf_canvas.Canvas, width: float, height: float, text: str) -> None:
    if not text:
        return
    c.saveState()
    try:
        c.setFillColor(colors.Color(0.7, 0.7, 0.7, alpha=0.16))
    except TypeError:
        c.setFillColor(colors.HexColor("#D1D5DB"))
    c.translate(width / 2.0, height / 2.0)
    c.rotate(42)
    c.setFont("Helvetica-Bold", 58)
    c.drawCentredString(0, 0, text)
    c.restoreState()


def draw_letterhead_band(c: pdf_canvas.Canvas, context: Dict[str, Dict[str, str]],
                         width: float, height: float, pal: Dict[str, colors.Color]) -> None:
    """Tall dark accent band at top of page 1 (cover) or content page 1."""
    branding = context["branding"]
    provider = context["provider"]
    agreement = context["agreement"]

    band_height = 0.95 * inch
    c.saveState()
    c.setFillColor(pal["accent_dark"])
    c.rect(0, height - band_height, width, band_height, stroke=0, fill=1)
    c.setFillColor(pal["accent"])
    c.rect(0, height - band_height - 0.04 * inch, width, 0.04 * inch, stroke=0, fill=1)

    pad = 0.72 * inch
    logo_size = 0.52 * inch
    logo_x = pad
    logo_y = height - band_height + (band_height - logo_size) / 2.0
    draw_logo_badge(c, logo_x, logo_y, logo_size, branding, pal, on_dark=True)

    name_x = logo_x + logo_size + 0.18 * inch
    brand_name = branding.get("brand_name") or provider.get("trade_name") or provider.get("legal_name", "TBD")
    c.setFillColor(pal["white"])
    c.setFont("Helvetica-Bold", 13.5)
    c.drawString(name_x, height - 0.42 * inch, brand_name)
    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.78))
    tagline = branding.get("brand_tagline", "")
    if tagline:
        c.drawString(name_x, height - 0.58 * inch, tagline)
    contact = clean_join([provider.get("website", ""), provider.get("email", "")], "  ·  ")
    if contact and contact != "TBD":
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.Color(1, 1, 1, alpha=0.62))
        c.drawString(name_x, height - 0.74 * inch, contact)

    right = width - pad
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.7))
    c.setFont("Helvetica", 7.2)
    c.drawRightString(right, height - 0.36 * inch, "CONTRACT ID")
    c.setFillColor(pal["white"])
    c.setFont("Helvetica-Bold", 10.5)
    c.drawRightString(right, height - 0.50 * inch, agreement.get("contract_id", "TBD"))
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.7))
    c.setFont("Helvetica", 7.2)
    c.drawRightString(right, height - 0.66 * inch, "EFFECTIVE")
    c.setFillColor(pal["white"])
    c.setFont("Helvetica-Bold", 10.5)
    c.drawRightString(right, height - 0.80 * inch, agreement.get("effective_date", "TBD"))
    c.restoreState()


def draw_compact_header(c: pdf_canvas.Canvas, context: Dict[str, Dict[str, str]],
                        width: float, height: float, pal: Dict[str, colors.Color]) -> None:
    branding = context["branding"]
    provider = context["provider"]
    pad = 0.72 * inch
    logo_size = 0.30 * inch
    logo_y = height - 0.62 * inch
    draw_logo_badge(c, pad, logo_y, logo_size, branding, pal, on_dark=False)

    text_x = pad + logo_size + 0.12 * inch
    brand_name = branding.get("brand_name") or provider.get("trade_name") or provider.get("legal_name", "TBD")
    c.saveState()
    c.setFillColor(pal["ink"])
    c.setFont("Helvetica-Bold", 9)
    c.drawString(text_x, height - 0.46 * inch, brand_name)
    c.setFillColor(pal["muted"])
    c.setFont("Helvetica", 7.5)
    c.drawString(text_x, height - 0.58 * inch, branding.get("brand_tagline", ""))

    right = width - pad
    title = context["agreement"].get("title", "Agreement")
    contract_id = context["agreement"].get("contract_id", "")
    c.setFillColor(pal["ink"])
    c.setFont("Helvetica-Bold", 8.8)
    c.drawRightString(right, height - 0.46 * inch, title)
    c.setFillColor(pal["muted"])
    c.setFont("Helvetica", 7.5)
    c.drawRightString(right, height - 0.58 * inch, contract_id)

    c.setStrokeColor(pal["accent"])
    c.setLineWidth(0.8)
    c.line(pad, height - 0.74 * inch, right, height - 0.74 * inch)
    c.restoreState()


def draw_footer(c: pdf_canvas.Canvas, doc: SimpleDocTemplate, context: Dict[str, Dict[str, str]],
                width: float, pal: Dict[str, colors.Color]) -> None:
    branding = context["branding"]
    agreement = context["agreement"]
    pad = 0.72 * inch
    right = width - pad
    y = 0.46 * inch
    c.saveState()
    c.setStrokeColor(pal["border"])
    c.setLineWidth(0.5)
    c.line(pad, y + 0.18 * inch, right, y + 0.18 * inch)
    c.setFillColor(pal["accent"])
    c.rect(pad, y + 0.18 * inch, 0.32 * inch, 0.012 * inch, stroke=0, fill=1)
    c.setFillColor(pal["muted"])
    c.setFont("Helvetica", 7.4)
    c.drawString(pad, y, agreement.get("contract_id", ""))
    footer_text = branding.get("footer_text", "")
    c.drawCentredString(width / 2, y, footer_text[:120])
    c.setFillColor(pal["ink"])
    c.setFont("Helvetica-Bold", 7.6)
    c.drawRightString(right, y, f"Page {doc.page}")
    c.restoreState()


def page_drawer(context: Dict[str, Dict[str, str]], pal: Dict[str, colors.Color],
                first_page: bool = False, cover_first: bool = False):
    branding = context["branding"]
    watermark_enabled = get_bool(branding, "watermark_enabled", True)
    letterhead_enabled = get_bool(branding, "letterhead_enabled", True)
    header_enabled = get_bool(branding, "header_enabled", True)
    footer_enabled = get_bool(branding, "footer_enabled", True)
    watermark_text = branding.get("watermark_text", "")

    def draw(c: pdf_canvas.Canvas, doc: SimpleDocTemplate) -> None:
        width, height = doc.pagesize
        if watermark_enabled:
            draw_watermark(c, width, height, watermark_text)
        if first_page:
            if cover_first:
                # Cover already includes its own visual band as flowable layout;
                # we only render watermark + minimal footer mark.
                if footer_enabled:
                    draw_footer(c, doc, context, width, pal)
                return
            if letterhead_enabled:
                draw_letterhead_band(c, context, width, height, pal)
            elif header_enabled:
                draw_compact_header(c, context, width, height, pal)
        else:
            if header_enabled:
                draw_compact_header(c, context, width, height, pal)
        if footer_enabled:
            draw_footer(c, doc, context, width, pal)

    return draw


# ---------------------------------------------------------------------------
# Cover page (programmatic flowables)
# ---------------------------------------------------------------------------

def cover_page_flowables(context: Dict[str, Dict[str, str]], styles: Dict[str, ParagraphStyle],
                         available_width: float, pal: Dict[str, colors.Color]) -> List[Any]:
    provider = context["provider"]
    client = context["client"]
    agreement = context["agreement"]
    branding = context["branding"]

    story: List[Any] = []
    story.append(Spacer(1, 1.3 * inch))

    logo = LogoFlowable(branding, pal, size=1.5 * inch)
    logo.hAlign = "CENTER"
    story.append(logo)
    story.append(Spacer(1, 0.35 * inch))

    eyebrow = (branding.get("brand_name") or provider.get("trade_name", "")).upper()
    if eyebrow and eyebrow != "TBD":
        story.append(Paragraph(eyebrow, styles["CoverEyebrow"]))
    story.append(Paragraph(agreement.get("title", "Agreement"), styles["CoverTitle"]))

    provider_name = provider.get("legal_name", "TBD")
    client_name = client.get("legal_name", "TBD")
    story.append(Paragraph(f"between <b>{html.escape(provider_name)}</b>", styles["CoverParties"]))
    story.append(Paragraph(f"and <b>{html.escape(client_name)}</b>", styles["CoverParties"]))
    story.append(Spacer(1, 0.55 * inch))

    # Two-column key terms chip panel
    def field(label: str, value: str) -> List:
        return [
            Paragraph(label, styles["CoverFieldLabel"]),
            Paragraph(html.escape(value or "TBD"), styles["CoverFieldValue"]),
        ]

    fields: List[List[List[Any]]] = [
        [field("CONTRACT ID", agreement.get("contract_id", "")),
         field("EFFECTIVE DATE", agreement.get("effective_date", "")),
         field("PROJECT", agreement.get("project_name", ""))],
    ]
    col_w = (available_width * 0.86) / 3.0
    chip = Table(fields, colWidths=[col_w] * 3, hAlign="CENTER")
    chip.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), pal["accent_soft"]),
        ("LINEABOVE", (0, 0), (-1, 0), 2, pal["accent"]),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(chip)
    story.append(Spacer(1, 0.7 * inch))

    disclaimer = (
        "Demonstration template only — not legal advice. Replace or review with qualified counsel "
        "before using for an actual engagement."
    )
    story.append(Paragraph(disclaimer, styles["CoverDisclaimer"]))
    story.append(PageBreak())
    return story


# ---------------------------------------------------------------------------
# Document build
# ---------------------------------------------------------------------------

def build_pdf(markdown: str, context: Dict[str, Dict[str, str]], out_path: Path,
              include_cover: bool = True) -> None:
    branding = context["branding"]
    pal = palette(branding)
    cover_enabled = include_cover and get_bool(branding, "cover_page_enabled", True)
    letterhead_enabled = get_bool(branding, "letterhead_enabled", True)

    left_margin = right_margin = 0.72 * inch
    if cover_enabled:
        top_margin = 0.82 * inch  # cover lays itself out; body uses compact header
    elif letterhead_enabled:
        top_margin = 1.30 * inch
    else:
        top_margin = 0.92 * inch
    bottom_margin = 0.82 * inch

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=LETTER,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin,
        title=context["agreement"].get("title", "Agreement"),
        author=context["provider"].get("legal_name", ""),
    )
    available_width = LETTER[0] - left_margin - right_margin
    styles = make_styles(pal)

    story: List[Any] = []
    if cover_enabled:
        story.extend(cover_page_flowables(context, styles, available_width, pal))
    story.extend(markdown_to_story(markdown, context, styles, available_width, pal))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.build(
        story,
        onFirstPage=page_drawer(context, pal, first_page=True, cover_first=cover_enabled),
        onLaterPages=page_drawer(context, pal, first_page=False, cover_first=cover_enabled),
    )


# ---------------------------------------------------------------------------
# Envelope
# ---------------------------------------------------------------------------

def draw_address_block(c: pdf_canvas.Canvas, lines: Sequence[str], x: float, y: float,
                       size: float = 11, leading: float = 14) -> None:
    c.setFont("Helvetica", size)
    for idx, line in enumerate(lines):
        c.drawString(x, y - idx * leading, line)


def build_envelope_pdf(context: Dict[str, Dict[str, str]], out_path: Path) -> None:
    width, height = 9.5 * inch, 4.125 * inch
    c = pdf_canvas.Canvas(str(out_path), pagesize=(width, height))
    c.setTitle("Printable Addressed Envelope")
    branding = context["branding"]
    envelope = context["envelope"]
    pal = palette(branding)

    if get_bool(branding, "watermark_enabled", True):
        draw_watermark(c, width, height, branding.get("watermark_text", ""))

    c.saveState()
    c.setStrokeColor(pal["border"])
    c.setLineWidth(0.5)
    c.rect(0.15 * inch, 0.15 * inch, width - 0.30 * inch, height - 0.30 * inch, stroke=1, fill=0)

    # Logo + brand on top-left
    draw_logo_badge(c, 0.42 * inch, height - 0.78 * inch, 0.5 * inch, branding, pal, on_dark=False)
    brand_name = branding.get("brand_name") or context["provider"].get("trade_name", "")
    c.setFillColor(pal["ink"])
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1.05 * inch, height - 0.42 * inch, brand_name)
    c.setFillColor(pal["muted"])
    c.setFont("Helvetica", 7.5)
    if branding.get("brand_tagline"):
        c.drawString(1.05 * inch, height - 0.56 * inch, branding["brand_tagline"])

    # Postage box
    c.setStrokeColor(pal["accent"])
    c.setFillColor(pal["white"])
    c.roundRect(width - 1.25 * inch, height - 0.82 * inch, 0.82 * inch, 0.46 * inch, 4, stroke=1, fill=0)
    c.setFillColor(pal["muted"])
    c.setFont("Helvetica", 7)
    c.drawCentredString(width - 0.84 * inch, height - 0.56 * inch, envelope.get("postage_box_text", "POSTAGE"))

    # Return address (smaller, below brand)
    if get_bool(envelope, "include_return_address", True):
        c.setFillColor(pal["muted"])
        c.setFont("Helvetica", 7.2)
        ret_lines = address_lines(context["provider"], include_name=False)
        for idx, line in enumerate(ret_lines):
            c.drawString(1.05 * inch, height - (0.82 + idx * 0.14) * inch, line)

    # Recipient block
    recipient_lines: List[str] = []
    attention = envelope.get("recipient_attention", "").strip()
    if attention:
        recipient_lines.append(attention)
    recipient_lines.extend(address_lines(context["client"], include_name=True))
    c.setFillColor(pal["ink"])
    draw_address_block(c, recipient_lines, 3.65 * inch, 2.25 * inch, size=11, leading=15)

    c.setFont("Helvetica", 6.5)
    c.setFillColor(pal["muted"])
    c.drawCentredString(width / 2, 0.32 * inch, "#10 envelope layout - print at 100% scale - demonstration addressing only")
    c.restoreState()
    c.showPage()
    c.save()


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> int:
    args = parse_args()
    config = read_config(args.config)
    context = build_context(config)
    template_path = resolve_path(args.template)
    out_path = resolve_path(args.out)
    markdown_out = resolve_path(args.markdown_out) if args.markdown_out else out_path.with_suffix(".md")
    envelope_out = resolve_path(args.envelope_out) if args.envelope_out else out_path.with_name("addressed_envelope.pdf")

    markdown = render_markdown(template_path, context)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.write_text(markdown, encoding="utf-8")
    build_pdf(markdown, context, out_path, include_cover=not args.no_cover)

    envelope_enabled = get_bool(context["branding"], "envelope_enabled", True)
    if envelope_enabled and not args.no_envelope:
        envelope_out.parent.mkdir(parents=True, exist_ok=True)
        build_envelope_pdf(context, envelope_out)
        print(f"Envelope PDF: {envelope_out}")

    print(f"Contract PDF: {out_path}")
    print(f"Filled Markdown: {markdown_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
