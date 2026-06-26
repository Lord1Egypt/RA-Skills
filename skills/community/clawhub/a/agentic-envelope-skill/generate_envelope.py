#!/usr/bin/env python3
"""Generate a branded printable #10 addressed envelope PDF.

Reads [provider], [client], [branding], and [envelope] sections from one or
more INI files. Later config files override earlier ones.
"""

from __future__ import annotations

import argparse
import configparser
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas as pdf_canvas

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = BASE_DIR / "config.ini"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a branded #10 envelope PDF.")
    parser.add_argument("--config", nargs="+", default=[str(DEFAULT_CONFIG)])
    parser.add_argument("--out", default=str(BASE_DIR / "output" / "addressed_envelope.pdf"))
    parser.add_argument("--recipient-attention", default=None)
    parser.add_argument("--postage-box-text", default=None)
    parser.add_argument("--no-return-address", action="store_true")
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
        "ink": colors.HexColor("#0F172A"),
        "white": colors.white,
    }


def resolve_logo_path(branding: Dict[str, str]) -> Path | None:
    raw = (branding.get("logo_path") or "").strip()
    if not raw:
        return None
    path = resolve_path(raw)
    return path if path.exists() else None


def draw_logo_badge(
    c: pdf_canvas.Canvas,
    x: float,
    y: float,
    size: float,
    branding: Dict[str, str],
    pal: Dict[str, colors.Color],
) -> None:
    logo = resolve_logo_path(branding)
    if logo:
        try:
            c.drawImage(ImageReader(str(logo)), x, y, width=size, height=size, preserveAspectRatio=True, mask="auto")
            return
        except Exception:
            pass

    monogram = (branding.get("logo_monogram") or "CT").strip()[:3] or "CT"
    c.saveState()
    c.setFillColor(pal["accent"])
    c.roundRect(x, y, size, size, size * 0.18, stroke=0, fill=1)
    c.setFillColor(pal["white"])
    font_size = size * (0.50 if len(monogram) <= 2 else 0.38)
    c.setFont("Helvetica-Bold", font_size)
    c.drawCentredString(x + size / 2.0, y + size / 2.0 - font_size * 0.36, monogram)
    c.restoreState()


def draw_watermark(c: pdf_canvas.Canvas, width: float, height: float, text: str) -> None:
    if not text.strip():
        return
    c.saveState()
    c.translate(width / 2.0, height / 2.0)
    c.rotate(16)
    c.setFillColor(colors.Color(0.1, 0.1, 0.1, alpha=0.08))
    c.setFont("Helvetica-Bold", 42)
    c.drawCentredString(0, -12, text.strip())
    c.restoreState()


def draw_address_block(
    c: pdf_canvas.Canvas,
    lines: Sequence[str],
    x: float,
    y: float,
    size: float = 11,
    leading: float = 14,
) -> None:
    c.setFont("Helvetica", size)
    for idx, line in enumerate(lines):
        c.drawString(x, y - idx * leading, line)


def build_context(config: configparser.ConfigParser) -> Dict[str, Dict[str, str]]:
    context = {
        "provider": section_dict(config, "provider"),
        "client": section_dict(config, "client"),
        "branding": section_dict(config, "branding"),
        "envelope": section_dict(config, "envelope"),
    }

    for section in ["provider", "client"]:
        for key in ["legal_name", "trade_name", "address_line1", "address_line2", "city", "state", "postal_code", "country"]:
            context[section].setdefault(key, "TBD")
    for key, value in {
        "logo_path": "assets/logo.png",
        "logo_monogram": "CT",
        "brand_name": context["provider"].get("trade_name", "CompleteTech"),
        "brand_tagline": "",
        "accent_color": "#1E3A8A",
        "accent_color_dark": "#0F172A",
        "accent_color_soft": "#EEF2FF",
        "muted_color": "#64748B",
        "border_color": "#E2E8F0",
        "watermark_enabled": "no",
        "watermark_text": "DEMO DRAFT",
    }.items():
        context["branding"].setdefault(key, value)
    for key, value in {
        "recipient_attention": "",
        "postage_box_text": "POSTAGE",
        "include_return_address": "yes",
        "footer_note": "#10 envelope layout - print at 100% scale - demonstration addressing only",
    }.items():
        context["envelope"].setdefault(key, value)

    return context


def build_envelope_pdf(context: Dict[str, Dict[str, str]], out_path: Path) -> None:
    width, height = 9.5 * inch, 4.125 * inch
    c = pdf_canvas.Canvas(str(out_path), pagesize=(width, height))
    c.setTitle("Printable Addressed Envelope")
    c.setAuthor(context["branding"].get("brand_name", "CompleteTech"))

    branding = context["branding"]
    envelope = context["envelope"]
    pal = palette(branding)

    if get_bool(branding, "watermark_enabled", False):
        draw_watermark(c, width, height, branding.get("watermark_text", ""))

    c.saveState()
    c.setStrokeColor(pal["border"])
    c.setLineWidth(0.5)
    c.rect(0.15 * inch, 0.15 * inch, width - 0.30 * inch, height - 0.30 * inch, stroke=1, fill=0)

    draw_logo_badge(c, 0.42 * inch, height - 0.78 * inch, 0.5 * inch, branding, pal)
    brand_name = branding.get("brand_name") or context["provider"].get("trade_name", "")
    c.setFillColor(pal["ink"])
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1.05 * inch, height - 0.42 * inch, brand_name)
    c.setFillColor(pal["muted"])
    c.setFont("Helvetica", 7.5)
    if branding.get("brand_tagline"):
        c.drawString(1.05 * inch, height - 0.56 * inch, branding["brand_tagline"])

    c.setStrokeColor(pal["accent"])
    c.setFillColor(pal["white"])
    c.roundRect(width - 1.25 * inch, height - 0.82 * inch, 0.82 * inch, 0.46 * inch, 4, stroke=1, fill=0)
    c.setFillColor(pal["muted"])
    c.setFont("Helvetica", 7)
    c.drawCentredString(width - 0.84 * inch, height - 0.56 * inch, envelope.get("postage_box_text", "POSTAGE"))

    if get_bool(envelope, "include_return_address", True):
        c.setFillColor(pal["muted"])
        c.setFont("Helvetica", 7.2)
        ret_lines = address_lines(context["provider"], include_name=False)
        for idx, line in enumerate(ret_lines):
            c.drawString(1.05 * inch, height - (0.82 + idx * 0.14) * inch, line)

    recipient_lines: List[str] = []
    attention = envelope.get("recipient_attention", "").strip()
    if attention:
        recipient_lines.append(attention)
    recipient_lines.extend(address_lines(context["client"], include_name=True))
    c.setFillColor(pal["ink"])
    draw_address_block(c, recipient_lines, 3.65 * inch, 2.25 * inch, size=11, leading=15)

    footer = envelope.get("footer_note", "").strip()
    if footer:
        c.setFont("Helvetica", 6.5)
        c.setFillColor(pal["muted"])
        c.drawCentredString(width / 2, 0.32 * inch, footer)

    c.restoreState()
    c.showPage()
    c.save()


def main() -> int:
    args = parse_args()
    config = read_config(args.config)
    context = build_context(config)

    if args.recipient_attention is not None:
        context["envelope"]["recipient_attention"] = args.recipient_attention
    if args.postage_box_text is not None:
        context["envelope"]["postage_box_text"] = args.postage_box_text
    if args.no_return_address:
        context["envelope"]["include_return_address"] = "no"

    out_path = resolve_path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    build_envelope_pdf(context, out_path)
    print(f"Envelope PDF: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
