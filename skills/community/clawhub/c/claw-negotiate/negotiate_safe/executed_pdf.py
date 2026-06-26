"""Local executed SAFE PDF generation.

This module keeps the OpenClaw skill self-contained. It deliberately uses only
the Python standard library so a fresh skill install can produce an executed
artifact without cloning the separate negotiate engine.
"""
from __future__ import annotations

import hashlib
import json
import os
import shlex
import subprocess
import base64
import binascii
import struct
import zlib
from datetime import datetime, timezone
from pathlib import Path

from minting import identity_value
from upstream import ssh_history, synthesize_offer_event


def _money(value: object, *, decimals: bool = False) -> str:
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return str(value or "")
    if decimals:
        return f"${amount:,.2f}"
    return f"${amount:,.0f}"


def _percent(value: object) -> str:
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return str(value or "")
    if amount.is_integer():
        return f"{int(amount)}%"
    return f"{amount:g}%"


def _yes_no(value: object) -> str:
    return "Yes" if bool(value) else "No"


def _wrap(text: str, width: int = 86) -> list[str]:
    words = str(text or "").split()
    if not words:
        return [""]
    lines: list[str] = []
    current = ""
    for word in words:
        if len(word) > width:
            if current:
                lines.append(current)
                current = ""
            for i in range(0, len(word), width):
                lines.append(word[i : i + width])
            continue
        candidate = f"{current} {word}".strip()
        if len(candidate) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _maybe_load_cfg(mint: dict, role: str) -> dict:
    path = mint.get(f"{role}_config_path", "")
    return _load_json(Path(path)) if path else {}


def _pick(
    *,
    configs: list[tuple[dict, str]],
    constraints: dict,
    constraint_key: str,
    env_key: str,
    default: str,
    field: str = "",
) -> str:
    for cfg, key in configs:
        value = identity_value(cfg.get(key), field=field)
        if value:
            return value
    value = identity_value(
        constraints.get(constraint_key),
        field=field,
        drop_placeholders=False,
    )
    if value:
        return value
    return identity_value(os.environ.get(env_key), field=field) or default


def _run_ssh_json(host: str, args: list[str], runner=subprocess.run) -> dict:
    remote_cmd = " ".join(shlex.quote(a) for a in args)
    result = runner(
        ["ssh", host, remote_cmd],
        capture_output=True,
        text=True,
        timeout=20,
    )
    if result.returncode != 0:
        return {"error": (result.stderr or result.stdout or "ssh command failed").strip()}
    try:
        data = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        return {"error": "invalid sshsign JSON response"}
    return data if isinstance(data, dict) else {"value": data}


def _history(output_dir: Path, negotiation_id: str, sshsign_host: str) -> list[dict]:
    rows = ssh_history(negotiation_id, sshsign_host=sshsign_host) or []
    events: list[dict] = []
    for row in rows:
        event = synthesize_offer_event(row)
        if not event:
            continue
        event = dict(event)
        event["audit_tx"] = row.get("immudb_tx") or row.get("audit_tx_id")
        event["created_at"] = row.get("created_at") or row.get("timestamp")
        events.append(event)
    return events


def _agreed_terms(events: list[dict]) -> dict:
    for event in reversed(events):
        if event.get("type") == "accept" and isinstance(event.get("terms"), dict):
            return dict(event["terms"])
    return dict(events[-1].get("terms") or {}) if events else {}


def _history_elapsed_seconds(events: list[dict]) -> float | None:
    parsed = []
    for event in events:
        raw = event.get("created_at")
        if not raw:
            continue
        text = str(raw).replace("Z", "+00:00")
        try:
            parsed.append(datetime.fromisoformat(text))
        except ValueError:
            continue
    if len(parsed) < 2:
        return None
    return max(0.0, (max(parsed) - min(parsed)).total_seconds())


def _pending_ids(output_dir: Path, negotiation_id: str) -> dict[str, str]:
    ids: dict[str, str] = {}
    for role in ("founder", "investor"):
        path = output_dir / f"{negotiation_id}_{role}_pending.txt"
        try:
            pending_id = path.read_text(encoding="utf-8").strip()
        except OSError:
            pending_id = ""
        if pending_id:
            ids[role] = pending_id
    return ids


def _collect_signers(
    output_dir: Path,
    negotiation_id: str,
    parties: dict,
    sshsign_host: str,
) -> list[dict]:
    signers: list[dict] = []
    for role, pending_id in _pending_ids(output_dir, negotiation_id).items():
        envelope = _run_ssh_json(sshsign_host, ["get-envelope", "--id", pending_id])
        env = envelope.get("envelope") if isinstance(envelope.get("envelope"), dict) else {}
        if role == "founder":
            label = parties["founder"]["name"]
            org = parties["founder"]["company"]
            title = parties["founder"]["title"]
        else:
            label = parties["investor"]["name"]
            org = parties["investor"]["firm"]
            title = "Investor"
        signers.append({
            "role": role.capitalize(),
            "name": label,
            "title": title,
            "organization": org,
            "pending_id": pending_id,
            "status": envelope.get("status", ""),
            "key_id": envelope.get("key_id", ""),
            "signature": envelope.get("signature", ""),
            "signature_image": env.get("signature_image", ""),
            "envelope_hash": envelope.get("envelope_hash", ""),
            "image_hash": env.get("image_hash", ""),
            "captured_at": env.get("captured_at", ""),
        })
    return signers


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def _png_to_pdf_rgb(png_b64: str) -> tuple[int, int, bytes] | None:
    """Return (width, height, zlib-compressed RGB bytes) for common PNGs.

    The sshsign signature pad emits RGBA PNG data URLs. We flatten alpha onto
    white and embed the result directly as a PDF Image XObject, avoiding heavy
    runtime dependencies for public OpenClaw skill installs.
    """
    if not png_b64:
        return None
    if "," in png_b64 and png_b64.startswith("data:"):
        png_b64 = png_b64.split(",", 1)[1]
    try:
        data = base64.b64decode(png_b64, validate=True)
    except (ValueError, binascii.Error):  # type: ignore[name-defined]
        return None
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return None

    pos = 8
    width = height = bit_depth = color_type = 0
    idat = bytearray()
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos : pos + 4])[0]
        chunk_type = data[pos + 4 : pos + 8]
        chunk = data[pos + 8 : pos + 8 + length]
        pos += 12 + length
        if chunk_type == b"IHDR" and len(chunk) >= 13:
            width, height, bit_depth, color_type = struct.unpack(">IIBB", chunk[:10])
        elif chunk_type == b"IDAT":
            idat.extend(chunk)
        elif chunk_type == b"IEND":
            break

    channels_by_type = {0: 1, 2: 3, 6: 4}
    channels = channels_by_type.get(color_type)
    if not width or not height or bit_depth != 8 or not channels:
        return None
    row_len = width * channels
    try:
        raw = zlib.decompress(bytes(idat))
    except zlib.error:
        return None
    expected = (row_len + 1) * height
    if len(raw) < expected:
        return None

    rows: list[bytearray] = []
    offset = 0
    previous = bytearray(row_len)
    for _ in range(height):
        filter_type = raw[offset]
        offset += 1
        row = bytearray(raw[offset : offset + row_len])
        offset += row_len
        for i in range(row_len):
            left = row[i - channels] if i >= channels else 0
            up = previous[i]
            up_left = previous[i - channels] if i >= channels else 0
            if filter_type == 1:
                row[i] = (row[i] + left) & 0xFF
            elif filter_type == 2:
                row[i] = (row[i] + up) & 0xFF
            elif filter_type == 3:
                row[i] = (row[i] + ((left + up) // 2)) & 0xFF
            elif filter_type == 4:
                row[i] = (row[i] + _paeth(left, up, up_left)) & 0xFF
            elif filter_type != 0:
                return None
        rows.append(row)
        previous = row

    pixels: list[tuple[int, int, int]] = []
    for row in rows:
        for x in range(width):
            i = x * channels
            if color_type == 0:
                gray = row[i]
                pixels.append((gray, gray, gray))
            elif color_type == 2:
                pixels.append((row[i], row[i + 1], row[i + 2]))
            else:
                r, g, b, a = row[i], row[i + 1], row[i + 2], row[i + 3]
                inv = 255 - a
                pixels.append((
                    (r * a + 255 * inv) // 255,
                    (g * a + 255 * inv) // 255,
                    (b * a + 255 * inv) // 255,
                ))

    marked = [
        (idx % width, idx // width)
        for idx, (r, g, b) in enumerate(pixels)
        if min(r, g, b) < 245
    ]
    if marked:
        pad = 10
        min_x = max(0, min(x for x, _y in marked) - pad)
        max_x = min(width - 1, max(x for x, _y in marked) + pad)
        min_y = max(0, min(y for _x, y in marked) - pad)
        max_y = min(height - 1, max(y for _x, y in marked) + pad)
    else:
        min_x, min_y, max_x, max_y = 0, 0, width - 1, height - 1

    cropped_width = max_x - min_x + 1
    cropped_height = max_y - min_y + 1
    rgb = bytearray()
    for y in range(min_y, max_y + 1):
        start = y * width
        for x in range(min_x, max_x + 1):
            rgb.extend(pixels[start + x])
    return cropped_width, cropped_height, zlib.compress(bytes(rgb), level=9)


class _SimplePDF:
    def __init__(self) -> None:
        self.pages: list[list[str]] = []
        self.images: list[tuple[int, int, bytes]] = []
        self._new_page()

    def _new_page(self) -> None:
        self.pages.append([])

    def new_page(self) -> None:
        self._new_page()

    @staticmethod
    def _escape(text: str) -> str:
        text = text.encode("latin-1", "replace").decode("latin-1")
        return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    def command(self, text: str) -> None:
        self.pages[-1].append(text)

    def text(self, x: float, y: float, text: str = "", *, size: int = 10, bold: bool = False, font: str = "") -> None:
        page = self.pages[-1]
        font_name = font or ("F2" if bold else "F1")
        page.append(f"BT /{font_name} {size} Tf {x:.1f} {y:.1f} Td ({self._escape(text)}) Tj ET")

    def rect(self, x: float, y: float, w: float, h: float, *, gray: float = 0.96) -> None:
        self.command(f"{gray:.3f} g {x:.1f} {y:.1f} {w:.1f} {h:.1f} re f 0 g")

    def stroke_rect(self, x: float, y: float, w: float, h: float, *, gray: float = 0.82) -> None:
        self.command(f"{gray:.3f} G {x:.1f} {y:.1f} {w:.1f} {h:.1f} re S 0 G")

    def rule(self, x: float, y: float, w: float, *, gray: float = 0.65) -> None:
        self.command(f"{gray:.3f} G {x:.1f} {y:.1f} m {x + w:.1f} {y:.1f} l S 0 G")

    def line(self, text: str = "", *, size: int = 10, bold: bool = False) -> None:
        page = self.pages[-1]
        content_lines = len([cmd for cmd in page if cmd.startswith("BT ")])
        if content_lines >= 44:
            self._new_page()
            page = self.pages[-1]
            content_lines = 0
        self.text(54, 760 - content_lines * 16, text, size=size, bold=bold)

    def gap(self) -> None:
        self.line("")

    def add_image(self, png_b64: str, *, x: float, y: float, w: float, h: float) -> bool:
        image = _png_to_pdf_rgb(png_b64)
        if not image:
            return False
        self.images.append(image)
        name = f"Im{len(self.images)}"
        self.command(f"q {w:.1f} 0 0 {h:.1f} {x:.1f} {y:.1f} cm /{name} Do Q")
        return True

    def write(self, path: Path) -> None:
        objects: list[bytes] = [
            b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [%s] /Count %d >>",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>",
        ]
        image_obj_ids: list[int] = []
        for width, height, compressed in self.images:
            image_obj_ids.append(len(objects) + 1)
            objects.append(
                b"<< /Type /XObject /Subtype /Image "
                b"/Width " + str(width).encode() + b" /Height " + str(height).encode() + b" "
                b"/ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /FlateDecode "
                b"/Length " + str(len(compressed)).encode() + b" >>\nstream\n"
                + compressed
                + b"\nendstream"
            )
        page_obj_ids: list[int] = []
        for page in self.pages:
            content = ("\n".join(page) + "\n").encode("latin-1", "replace")
            content_obj_id = len(objects) + 1
            objects.append(b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"endstream")
            page_obj_id = len(objects) + 1
            xobject = b" ".join(
                f"/Im{i} {obj_id} 0 R".encode()
                for i, obj_id in enumerate(image_obj_ids, start=1)
            )
            objects.append(
                b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                b"/Resources << /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R >> "
                b"/XObject << " + xobject + b" >> >> "
                b"/Contents " + str(content_obj_id).encode() + b" 0 R >>"
            )
            page_obj_ids.append(page_obj_id)
        kids = b" ".join(f"{obj_id} 0 R".encode() for obj_id in page_obj_ids)
        objects[1] = objects[1] % (kids, len(page_obj_ids))

        out = bytearray(b"%PDF-1.4\n")
        offsets = [0]
        for index, obj in enumerate(objects, start=1):
            offsets.append(len(out))
            out.extend(f"{index} 0 obj\n".encode())
            out.extend(obj)
            out.extend(b"\nendobj\n")
        xref = len(out)
        out.extend(f"xref\n0 {len(objects) + 1}\n".encode())
        out.extend(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            out.extend(f"{offset:010d} 00000 n \n".encode())
        out.extend(
            f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n".encode()
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(bytes(out))


def _document_hash(negotiation_id: str, terms: dict, parties: dict, events: list[dict]) -> str:
    payload = {
        "negotiation_id": negotiation_id,
        "terms": terms,
        "parties": parties,
        "events": events,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _template_discount(value: object) -> float:
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return 0.0
    return amount / 100.0 if amount > 1 else amount


def _template_history(events: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for event in events:
        terms = dict(event.get("terms") or {})
        if "discount_rate" in terms:
            terms["discount_rate"] = _template_discount(terms.get("discount_rate"))
        row = {
            "round": event.get("round", 0),
            "from": event.get("party", ""),
            "type": event.get("type", ""),
            "terms": terms,
            "message": event.get("message", ""),
            "immudb_tx": event.get("audit_tx", ""),
            "timestamp": event.get("created_at", ""),
        }
        rows.append(row)
    return rows


def _render_with_apoa_template(
    *,
    pdf_path: Path,
    terms: dict,
    parties: dict,
    signers: list[dict],
    doc_hash: str,
    events: list[dict],
    negotiation_id: str,
    elapsed: float | None,
) -> bool:
    try:
        from negotiate_safe.documents.templates.safe import SAFETemplate
    except Exception:
        try:
            from documents.templates.safe import SAFETemplate
        except Exception:
            return False

    template_terms = dict(terms)
    template_terms["discount_rate"] = _template_discount(template_terms.get("discount_rate"))
    template_signers = []
    for signer in signers:
        template_signer = dict(signer)
        template_signer["role"] = str(template_signer.get("role", "")).lower()
        template_signers.append(template_signer)

    try:
        template = SAFETemplate(template_terms, parties)
        ok, _error = template.validate_terms()
        if not ok:
            return False
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        template.append_execution_page(
            str(pdf_path),
            signers=template_signers,
            doc_hash=doc_hash,
            negotiation_history=_template_history(events),
            negotiation_id=negotiation_id,
            elapsed_seconds=elapsed,
        )
    except Exception:
        return False
    return pdf_path.exists()


def finalize_executed_pdf(
    output_dir: Path,
    pending_id: str,
    sshsign_host: str,
) -> Path | None:
    mint = _load_json(output_dir / "mint.json")
    config = _load_json(output_dir / "config.json")
    constraints = config.get("constraints") or {}
    negotiation_id = mint.get("negotiation_id") or ""
    if not negotiation_id:
        return None

    founder_cfg = _maybe_load_cfg(mint, "founder")
    investor_cfg = _maybe_load_cfg(mint, "investor")
    parties = {
        "founder": {
            "company": _pick(
                configs=[(founder_cfg, "company_name")],
                constraints=constraints,
                constraint_key="company_name",
                env_key="COMPANY_NAME",
                default="Company",
                field="company",
            ),
            "name": _pick(
                configs=[(founder_cfg, "name"), (founder_cfg, "founder_name")],
                constraints=constraints,
                constraint_key="founder_name",
                env_key="FOUNDER_NAME",
                default="Founder",
            ),
            "title": _pick(
                configs=[(founder_cfg, "title")],
                constraints=constraints,
                constraint_key="founder_title",
                env_key="FOUNDER_TITLE",
                default="",
            ),
        },
        "investor": {
            "name": _pick(
                configs=[(investor_cfg, "name"), (investor_cfg, "investor_name")],
                constraints=constraints,
                constraint_key="investor_name",
                env_key="INVESTOR_NAME",
                default="Investor",
            ),
            "firm": _pick(
                configs=[(investor_cfg, "firm"), (investor_cfg, "investor_firm")],
                constraints=constraints,
                constraint_key="investor_firm",
                env_key="INVESTOR_FIRM",
                default="",
            ),
        },
    }

    events = _history(output_dir, negotiation_id, sshsign_host)
    terms = _agreed_terms(events)
    if not terms:
        return None
    terms.setdefault("investment_amount", founder_cfg.get("investment_amount") or investor_cfg.get("investment_amount") or 0)
    terms["date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    signers = _collect_signers(output_dir, negotiation_id, parties, sshsign_host)
    if not signers:
        return None
    doc_hash = _document_hash(negotiation_id, terms, parties, events)
    elapsed = _history_elapsed_seconds(events)

    config_anchor = mint.get("founder_config_path") or mint.get("investor_config_path") or ""
    neg_dir = Path(config_anchor).parent if config_anchor else output_dir
    pdf_path = neg_dir / "output" / f"{negotiation_id}_executed.pdf"
    if _render_with_apoa_template(
        pdf_path=pdf_path,
        terms=terms,
        parties=parties,
        signers=signers,
        doc_hash=doc_hash,
        events=events,
        negotiation_id=negotiation_id,
        elapsed=elapsed,
    ):
        return pdf_path

    pdf = _SimplePDF()

    def center_title(title: str, subtitle: str = "") -> None:
        x = max(54, 306 - len(title) * 5.6)
        pdf.text(x, 720, title, size=24)
        if subtitle:
            pdf.text(max(54, 306 - len(subtitle) * 2.8), 692, subtitle, size=11)
        pdf.command("0.000 0.600 0.560 RG 224.0 674.0 m 388.0 674.0 l S 0 G")

    def footer(text: str) -> None:
        pdf.text(max(54, 306 - len(text) * 2.2), 54, text, size=8)

    def paragraph(y: float, text: str, *, width: int = 102, size: int = 10, italic: bool = False) -> float:
        for line in _wrap(text, width):
            pdf.text(65, y, line, size=size, font="F1")
            y -= 13
        return y

    def section(y: float, title: str, body: str) -> float:
        pdf.text(65, y, title, size=12, bold=True)
        pdf.rule(65, y - 8, 482, gray=0.86)
        y -= 24
        return paragraph(y, body, width=104)

    def kv_box(y: float, rows: list[tuple[str, str]], *, x: float = 65, w: float = 482, stripe: bool = True) -> float:
        h = 25 + len(rows) * 19
        pdf.rect(x, y - h, w, h, gray=0.965)
        if stripe:
            pdf.command(f"0.000 0.600 0.560 rg {x:.1f} {y - h:.1f} 7.0 {h:.1f} re f 0 g")
        yy = y - 22
        for label, value in rows:
            pdf.text(x + 26, yy, label, size=9)
            pdf.text(x + 184, yy, value, size=9, bold=True)
            yy -= 19
        return y - h - 24

    def event_dt(event: dict) -> datetime | None:
        raw = event.get("created_at")
        if not raw:
            return None
        try:
            return datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
        except ValueError:
            return None

    investor_line = parties["investor"]["name"]
    if parties["investor"]["firm"]:
        investor_line += f" at {parties['investor']['firm']}"

    center_title("SAFE", "Simple Agreement for Future Equity")
    opening = (
        f"THIS CERTIFIES THAT in exchange for the payment by {investor_line} "
        f"(the \"Investor\") of {_money(terms.get('investment_amount'))} (the "
        f"\"Purchase Amount\") on or about {terms['date']}, {parties['founder']['company']} "
        f"(the \"Company\"), hereby issues to the Investor the right to certain shares "
        "of the Company's Capital Stock, subject to the terms described below."
    )
    y = paragraph(642, opening, width=108)
    y = kv_box(y - 10, [
        ("KEY TERMS", ""),
        ("Valuation Cap", _money(terms.get("valuation_cap"))),
        ("Discount Rate", _percent(terms.get("discount_rate"))),
        ("Pro-Rata Rights", "Included" if terms.get("pro_rata") else "Not Included"),
        ("Most Favored Nation", "Included" if terms.get("mfn") else "Not Included"),
        ("Purchase Amount", _money(terms.get("investment_amount"))),
        ("Date", terms["date"]),
    ])
    y = section(y, "Section 1: Events", "1(a) Equity Financing. If there is an Equity Financing before the termination of this Safe, this Safe will automatically convert into the number of shares of Safe Preferred Stock equal to the Purchase Amount divided by the Safe Price or the Discount Price, whichever calculation results in a greater number of shares. 1(b) Liquidity Event. If there is a Liquidity Event before the termination of this Safe, this Safe will automatically be entitled to receive a portion of Proceeds. 1(c) Dissolution Event. If there is a Dissolution Event before the termination of this Safe, the Investor will be entitled to receive the Purchase Amount immediately prior to the consummation of the Dissolution Event.")
    section(y, "Section 2: Definitions", f"\"Safe Price\" means the price per share equal to the Post-Money Valuation Cap divided by the Company Capitalization. \"Discount Price\" means the price per share of the Standard Preferred Stock sold in the Equity Financing multiplied by the Discount Rate. \"Post-Money Valuation Cap\" means {_money(terms.get('valuation_cap'))}.")

    pdf.new_page()
    y = 720
    y = section(y, "Section 3: Company Representations", "The Company is a corporation duly organized, validly existing, and in good standing under the laws of its state of incorporation, and has the power and authority to own, lease, and operate its properties and carry on its business as now conducted. The execution, delivery, and performance by the Company of this Safe is within the power of the Company and has been duly authorized by all necessary actions on the part of the Company.")
    y = section(y - 12, "Section 4: Investor Representations", "The Investor has full legal capacity, power, and authority to execute and deliver this Safe and to perform its obligations hereunder. The Investor is an accredited investor as such term is defined in Rule 501 of Regulation D under the Securities Act.")
    y = section(y - 12, "Section 5: Miscellaneous", "Any provision of this Safe may be amended, waived, or modified by written consent of the Company and the Investor. Any notice required or permitted by this Safe will be deemed sufficient when delivered personally or sent by email to the relevant address listed on the signature page. This Safe shall be governed by and construed under the laws of the State of Delaware, United States, without regard to conflict of laws provisions.")
    section(y - 12, "Section 6: Pro-Rata Rights", "The Investor shall have a pro-rata right to participate in subsequent Equity Financing rounds on the same terms and conditions as other investors in such round, up to an amount sufficient to maintain the Investor's percentage ownership of the Company." if terms.get("pro_rata") else "The Investor shall not receive contractual pro-rata participation rights under this Safe.")

    pdf.new_page()
    center_title("Signature Page")
    founder_signer = next((s for s in signers if s["role"].lower() == "founder"), signers[0])
    investor_signer = next((s for s in signers if s["role"].lower() == "investor"), signers[-1])
    pdf.text(65, 630, "COMPANY", size=9)
    pdf.text(65, 606, parties["founder"]["company"], size=12, bold=True)
    pdf.add_image(founder_signer.get("signature_image", ""), x=95, y=510, w=160, h=80)
    pdf.text(65, 420, f"{parties['founder']['name']}, {parties['founder']['title']}".rstrip(", "), size=9)
    pdf.text(65, 402, terms["date"], size=8)
    pdf.text(65, 350, "INVESTOR", size=9)
    pdf.text(65, 326, parties["investor"]["firm"] or parties["investor"]["name"], size=12, bold=True)
    pdf.add_image(investor_signer.get("signature_image", ""), x=95, y=230, w=160, h=80)
    pdf.text(65, 140, parties["investor"]["name"], size=9)
    pdf.text(65, 122, terms["date"], size=8)
    footer("Generated by APOA Negotiate  |  Signatures verified via sshsign")

    pdf.new_page()
    center_title("Negotiation Audit Trail")
    y = paragraph(642, "Complete record of the negotiation between the parties. Each offer was validated against the proposing agent's APOA authorization constraints and logged to an immutable Merkle tree via sshsign/immudb.", width=108, size=9)
    first_dt = next((event_dt(e) for e in events if event_dt(e)), None)
    last_dt = next((event_dt(e) for e in reversed(events) if event_dt(e)), None)
    y = kv_box(y - 10, [
        ("Negotiation ID", negotiation_id),
        ("Total Offers", str(len(events))),
        ("Duration", f"{elapsed:.1f} seconds" if elapsed is not None else ""),
        ("Started", first_dt.strftime("%Y-%m-%d %H:%M:%S UTC") if first_dt else ""),
        ("Completed", last_dt.strftime("%Y-%m-%d %H:%M:%S UTC") if last_dt else ""),
    ])
    pdf.text(65, y, "Offer Summary", size=12, bold=True)
    pdf.rule(65, y - 8, 482, gray=0.86)
    y -= 30
    headers = [("Round", 65), ("Party", 100), ("Type", 160), ("Cap", 250), ("Disc.", 306), ("Pro-Rata", 348), ("TX", 420), ("Time", 486)]
    for label, x in headers:
        pdf.text(x, y, label, size=7)
    y -= 13
    for event in events[:9]:
        terms_text = event.get("terms") or {}
        dt = event_dt(event)
        values = [
            (str(event.get("round", "")), 65),
            (str(event.get("party", "")), 100),
            (str(event.get("type", "")), 160),
            (_money(terms_text.get("valuation_cap")), 250),
            (_percent(terms_text.get("discount_rate")), 306),
            ("Yes" if terms_text.get("pro_rata") else "No", 348),
            (str(event.get("audit_tx") or ""), 420),
            (dt.strftime("%H:%M:%S") if dt else "", 486),
        ]
        for value, x in values:
            pdf.text(x, y, value, size=7, bold=value in {"accept"})
        y -= 13
    y -= 18
    pdf.text(65, y, "Negotiation Transcript", size=12, bold=True)
    pdf.rule(65, y - 8, 482, gray=0.86)
    y -= 28
    for event in events:
        if y < 90:
            pdf.new_page()
            y = 730
        dt = event_dt(event)
        pdf.text(65, y, f"Round {event.get('round', '')} -- {str(event.get('party', '')).capitalize()}", size=9)
        if dt:
            pdf.text(430, y, dt.strftime("%Y-%m-%d %H:%M:%S UTC"), size=7)
        y -= 12
        pdf.text(65, y, str(event.get("type", "")), size=7, bold=True)
        y -= 13
        message = event.get("message") or ""
        if message:
            for line in _wrap(f"\"{message}\"", 112):
                pdf.text(65, y, line, size=8)
                y -= 11
        y -= 10

    pdf.new_page()
    center_title("Certificate of Execution")
    y = paragraph(642, "This certificate attests that the preceding SAFE agreement has been cryptographically signed by all parties and executed via sshsign.", width=108, size=9)
    y = kv_box(y - 10, [
        ("Document SHA-256", doc_hash[:32]),
        ("", doc_hash[32:]),
        ("Negotiation ID", negotiation_id),
        ("Signatories", str(len(signers))),
    ])
    for signer in signers:
        if y < 180:
            pdf.new_page()
            y = 720
        pdf.text(65, y, signer["role"], size=12, bold=True)
        pdf.rule(65, y - 8, 482, gray=0.86)
        y -= 28
        pdf.text(65, y, "Signing Key", size=9)
        pdf.text(195, y, signer["key_id"], size=9)
        y -= 18
        pdf.text(65, y, "Pending ID", size=9)
        pdf.text(195, y, signer["pending_id"], size=9)
        y -= 28
        pdf.text(65, y, "SSH Signature", size=8)
        y -= 12
        block_h = 76
        pdf.rect(65, y - block_h, 482, block_h, gray=0.965)
        pdf.command(f"0.000 0.600 0.560 rg 65.0 {y - block_h:.1f} 7.0 {block_h:.1f} re f 0 g")
        yy = y - 17
        for line in str(signer.get("signature") or "").splitlines()[:6]:
            pdf.text(90, yy, line[:82], size=5, font="F3")
            yy -= 10
        y -= block_h + 22
        pdf.text(65, y, "Handwritten signature appears on the Signature Page", size=7)
        y -= 34
    footer("Verify this document at sshsign.dev  |  Generated by APOA Negotiate")
    pdf.write(pdf_path)
    return pdf_path if pdf_path.exists() else None
