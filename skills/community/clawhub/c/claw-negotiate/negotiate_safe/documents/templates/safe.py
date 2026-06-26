"""YC Post-Money SAFE template. Generates a deterministic PDF."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from fpdf import FPDF

from .base import DocumentTemplate

FONT_DIR = Path(__file__).parent.parent / "fonts"

# Color palette
TEAL = (0, 150, 143)       # Primary accent
DARK = (28, 28, 30)        # Near-black for headings
BODY = (60, 60, 67)        # Dark gray for body text
LIGHT = (142, 142, 147)    # Light gray for secondary text
RULE = (229, 229, 234)     # Hairline rules
WHITE = (255, 255, 255)
TABLE_BG = (248, 248, 250)  # Subtle alternating row background


def _font_dir() -> Path:
    return FONT_DIR


def _setup_fonts(pdf: FPDF) -> None:
    """Register Inter font family if available, fall back to Helvetica."""
    font_dir = _font_dir()
    if (font_dir / "Inter-Regular.ttf").exists():
        pdf.add_font("Inter", "", str(font_dir / "Inter-Regular.ttf"))
        pdf.add_font("Inter", "B", str(font_dir / "Inter-Bold.ttf"))
        pdf.add_font("Inter", "I", str(font_dir / "Inter-Italic.ttf"))
        if (font_dir / "Inter-Light.ttf").exists():
            pdf.add_font("InterLight", "", str(font_dir / "Inter-Light.ttf"))
        if (font_dir / "Inter-Medium.ttf").exists():
            pdf.add_font("InterMedium", "", str(font_dir / "Inter-Medium.ttf"))


def _font(pdf: FPDF, weight: str = "", size: float = 10) -> None:
    """Set font with fallback. weight: '', 'B', 'I', 'light', 'medium'."""
    if weight == "light" and "InterLight" in pdf.fonts:
        pdf.set_font("InterLight", "", size)
    elif weight == "medium" and "InterMedium" in pdf.fonts:
        pdf.set_font("InterMedium", "", size)
    elif "Inter" in pdf.fonts:
        pdf.set_font("Inter", weight if weight in ("", "B", "I") else "", size)
    else:
        pdf.set_font("Helvetica", weight if weight in ("", "B", "I") else "", size)


def _color(pdf: FPDF, rgb: tuple) -> None:
    pdf.set_text_color(*rgb)


def _draw_color(pdf: FPDF, rgb: tuple) -> None:
    pdf.set_draw_color(*rgb)


def _fill_color(pdf: FPDF, rgb: tuple) -> None:
    pdf.set_fill_color(*rgb)


def _sanitize_text(text: str) -> str:
    """Replace Unicode characters that Helvetica (fallback font) can't render."""
    if not text:
        return text
    replacements = {
        "\u2014": "--",   # em dash
        "\u2013": "-",    # en dash
        "\u2018": "'",    # left single quote
        "\u2019": "'",    # right single quote
        "\u201c": '"',    # left double quote
        "\u201d": '"',    # right double quote
        "\u2026": "...",  # ellipsis
        "\u2022": "*",    # bullet
        "\u00a0": " ",    # non-breaking space
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def _rule(pdf: FPDF, y: float | None = None) -> None:
    """Draw a subtle horizontal rule."""
    _draw_color(pdf, RULE)
    yy = y if y is not None else pdf.get_y()
    pdf.line(pdf.l_margin, yy, pdf.w - pdf.r_margin, yy)


class SAFETemplate(DocumentTemplate):
    """
    YC Post-Money SAFE document template.

    Standard SAFE templates from Y Combinator (ycombinator.com/documents).
    SAFE template generation inspired by Praful Mathur's SAFE-CLI-Signer
    (github.com/prafulfillment/SAFE-CLI-Signer).
    """

    REQUIRED_FIELDS = [
        "valuation_cap",
        "discount_rate",
        "pro_rata",
        "date",
        "investment_amount",
    ]

    REQUIRED_PARTIES = {
        "founder": ["company", "name", "title"],
        "investor": ["name"],
    }

    # Layout constants
    MARGIN_LEFT = 22
    MARGIN_RIGHT = 22
    MARGIN_TOP = 25

    def validate_terms(self) -> tuple[bool, str]:
        for field in self.REQUIRED_FIELDS:
            if field not in self.terms:
                return False, f"Missing required field: {field}"

        for party, fields in self.REQUIRED_PARTIES.items():
            if party not in self.parties:
                return False, f"Missing required party: {party}"
            for f in fields:
                if f not in self.parties[party]:
                    return False, f"Missing '{f}' in {party} party info"

        return True, ""

    def generate_pdf(self, output_path: str) -> str:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=25)
        pdf.creation_date = datetime(2025, 1, 1, tzinfo=timezone.utc)
        _setup_fonts(pdf)
        self._render_safe_content(pdf)
        pdf.output(output_path)
        return self._hash_file(output_path)

    def _section_header(self, pdf: FPDF, title: str) -> None:
        _font(pdf, "B", 11)
        _color(pdf, DARK)
        pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        _rule(pdf)
        pdf.ln(3)
        _font(pdf, "", 9.5)
        _color(pdf, BODY)

    def _subsection(self, pdf: FPDF, title: str) -> None:
        _font(pdf, "medium", 9.5)
        _color(pdf, DARK)
        pdf.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        _font(pdf, "", 9.5)
        _color(pdf, BODY)

    @staticmethod
    def _wrap_unbroken_value(value: str, chunk_size: int = 32) -> str:
        """Insert line breaks into long tokens such as SHA-256 hashes."""
        value = str(value or "")
        if not value or any(ch.isspace() for ch in value) or len(value) <= chunk_size:
            return value
        return "\n".join(
            value[i:i + chunk_size]
            for i in range(0, len(value), chunk_size)
        )

    def _key_value(
        self,
        pdf: FPDF,
        key: str,
        value: str,
        key_width: int = 55,
        *,
        wrap_unbroken: bool = False,
    ) -> float:
        value = self._wrap_unbroken_value(value) if wrap_unbroken else str(value or "")
        line_h = 5
        row_h = max(6, line_h * max(1, value.count("\n") + 1))
        x = pdf.get_x()
        y = pdf.get_y()

        _font(pdf, "medium", 9)
        _color(pdf, LIGHT)
        pdf.cell(key_width, 6, key)
        _font(pdf, "", 9.5)
        _color(pdf, DARK)
        pdf.set_xy(x + key_width, y)
        pdf.multi_cell(
            pdf.w - pdf.r_margin - (x + key_width),
            line_h,
            value,
            new_x="LMARGIN",
            new_y="NEXT",
        )
        if pdf.get_y() < y + row_h:
            pdf.set_y(y + row_h)
        _color(pdf, BODY)
        return row_h

    def _body_text(self, pdf: FPDF, text: str) -> None:
        _font(pdf, "", 9.5)
        _color(pdf, BODY)
        pdf.multi_cell(0, 5, text)

    @staticmethod
    def _format_timestamp(ts: str) -> str:
        if not ts:
            return ""
        try:
            dt = datetime.fromisoformat(ts)
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except (ValueError, TypeError):
            return str(ts)

    @staticmethod
    def _format_time_short(ts: str) -> str:
        if not ts:
            return ""
        try:
            dt = datetime.fromisoformat(ts)
            return dt.strftime("%H:%M:%S")
        except (ValueError, TypeError):
            return ""

    # ──────────────────────────────────────────────────────────
    # Executed document (SAFE + audit trail + certificate)
    # ──────────────────────────────────────────────────────────

    def append_execution_page(
        self,
        pdf_path: str,
        signers: list[dict] | None = None,
        doc_hash: str = "",
        negotiation_history: list[dict] | None = None,
        negotiation_id: str = "",
        elapsed_seconds: float | None = None,
    ) -> str:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=25)
        pdf.set_left_margin(self.MARGIN_LEFT)
        pdf.set_right_margin(self.MARGIN_RIGHT)
        _setup_fonts(pdf)

        self._render_safe_content(pdf, signers=signers)

        if negotiation_history:
            self._render_audit_trail(
                pdf, negotiation_history, negotiation_id, elapsed_seconds,
            )

        self._render_certificate(
            pdf, signers or [], doc_hash, negotiation_id,
        )

        pdf.output(pdf_path)
        return self._hash_file(pdf_path)

    def _page_title(self, pdf: FPDF, title: str) -> None:
        """Render a page title matching the Signature Page style."""
        pdf.ln(10)
        _font(pdf, "light", 20)
        _color(pdf, DARK)
        pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(3)
        _draw_color(pdf, TEAL)
        center_x = pdf.w / 2
        pdf.line(center_x - 20, pdf.get_y(), center_x + 20, pdf.get_y())
        pdf.ln(8)

    def _card_with_teal_bar(self, pdf: FPDF, card_h: float) -> float:
        """Draw a gray card with teal left border. Returns card_y."""
        card_y = pdf.get_y()
        _fill_color(pdf, TABLE_BG)
        pdf.rect(pdf.l_margin, card_y, pdf.w - pdf.l_margin - pdf.r_margin, card_h, style="F")
        _fill_color(pdf, TEAL)
        pdf.rect(pdf.l_margin, card_y, 2.5, card_h, style="F")
        return card_y

    def _render_certificate(
        self,
        pdf: FPDF,
        signers: list[dict],
        doc_hash: str,
        negotiation_id: str,
    ) -> None:
        pdf.add_page()

        self._page_title(pdf, "Certificate of Execution")

        _font(pdf, "light", 9)
        _color(pdf, LIGHT)
        num_signers = len(signers)
        if num_signers > 1:
            desc = (
                "This certificate attests that the preceding SAFE agreement has been "
                "cryptographically signed by all parties and executed via sshsign."
            )
        else:
            desc = (
                "This certificate attests that the preceding SAFE agreement has been "
                "cryptographically signed and executed via sshsign."
            )
        pdf.multi_cell(0, 4.5, desc)
        pdf.ln(4)

        # Document details card with teal bar
        row_h = 6
        card_h = 8 + row_h  # Signatories
        if doc_hash:
            card_h += max(row_h, 5 * (doc_hash.count("\n") + 2))
        if negotiation_id:
            card_h += row_h

        card_y = self._card_with_teal_bar(pdf, card_h)
        pdf.ln(4)

        indent = 8
        pdf.set_left_margin(self.MARGIN_LEFT + indent)
        pdf.set_x(self.MARGIN_LEFT + indent)

        if doc_hash:
            self._key_value(pdf, "Document SHA-256", doc_hash, key_width=50, wrap_unbroken=True)
        if negotiation_id:
            self._key_value(pdf, "Negotiation ID", negotiation_id, key_width=50)
        self._key_value(pdf, "Signatories", str(num_signers), key_width=50)

        pdf.set_left_margin(self.MARGIN_LEFT)
        pdf.set_y(card_y + card_h + 5)

        # Render each signer's block
        for i, signer in enumerate(signers):
            role = signer.get("role", f"Party {i + 1}")
            key_id = signer.get("key_id", "")
            signature_block = signer.get("signature", "")
            signature_image = signer.get("signature_image")
            audit_tx_id = signer.get("audit_tx_id")
            pending_id = signer.get("pending_id", "")

            # Signer header
            self._section_header(pdf, role.capitalize())

            # Signer details
            self._key_value(pdf, "Signing Key", key_id, key_width=45)
            if audit_tx_id:
                self._key_value(pdf, "Audit TX", str(audit_tx_id), key_width=45)
            if pending_id:
                self._key_value(pdf, "Pending ID", pending_id, key_width=45)
            pdf.ln(2)

            # SSH Signature block with teal bar
            if signature_block:
                _font(pdf, "medium", 8)
                _color(pdf, DARK)
                pdf.cell(0, 5, "SSH Signature", new_x="LMARGIN", new_y="NEXT")
                pdf.ln(1)

                sig_lines = signature_block.strip().split("\n")
                sig_h = len(sig_lines) * 3.5 + 6
                sig_y = self._card_with_teal_bar(pdf, sig_h)
                pdf.ln(3)

                indent = 8
                pdf.set_left_margin(self.MARGIN_LEFT + indent)
                pdf.set_x(self.MARGIN_LEFT + indent)

                pdf.set_font("Courier", "", 5.5)
                _color(pdf, BODY)
                for line in sig_lines:
                    pdf.cell(0, 3.5, line, new_x="LMARGIN", new_y="NEXT")

                pdf.set_left_margin(self.MARGIN_LEFT)
                pdf.set_y(sig_y + sig_h + 3)

            # Note if handwritten signature is on the signature page
            if signature_image:
                _font(pdf, "light", 7)
                _color(pdf, LIGHT)
                pdf.cell(0, 4, "Handwritten signature appears on the Signature Page", new_x="LMARGIN", new_y="NEXT")
                pdf.ln(2)

            # Separator between signers (not after last)
            if i < num_signers - 1:
                pdf.ln(3)
                _rule(pdf)
                pdf.ln(5)

        # Footer
        pdf.ln(3)
        _font(pdf, "light", 7.5)
        _color(pdf, LIGHT)
        pdf.cell(
            0, 5,
            "Verify this document at sshsign.dev  |  Generated by APOA Negotiate",
            new_x="LMARGIN", new_y="NEXT", align="C",
        )

    # ──────────────────────────────────────────────────────────
    # Audit trail
    # ──────────────────────────────────────────────────────────

    def _render_audit_trail(
        self,
        pdf: FPDF,
        history: list[dict],
        negotiation_id: str = "",
        elapsed_seconds: float | None = None,
    ) -> None:
        pdf.add_page()

        self._page_title(pdf, "Negotiation Audit Trail")

        _font(pdf, "light", 9)
        _color(pdf, LIGHT)
        pdf.multi_cell(0, 4.5, (
            "Complete record of the negotiation between the parties. Each offer was "
            "validated against the proposing agent's APOA authorization constraints "
            "and logged to an immutable Merkle tree via sshsign/immudb."
        ))
        pdf.ln(4)

        # Summary card with teal left border
        # Count rows to calculate card height
        row_h = 6
        num_rows = 1  # Total Offers (always)
        if negotiation_id:
            num_rows += 1
        if elapsed_seconds is not None:
            num_rows += 1
        if history:
            if history[0].get("timestamp"):
                num_rows += 1  # Started
            if history[-1].get("timestamp"):
                num_rows += 1  # Completed

        card_h = num_rows * row_h + 8  # rows + padding

        _fill_color(pdf, TABLE_BG)
        card_y = pdf.get_y()
        pdf.rect(pdf.l_margin, card_y, pdf.w - pdf.l_margin - pdf.r_margin, card_h, style="F")

        _fill_color(pdf, TEAL)
        pdf.rect(pdf.l_margin, card_y, 2.5, card_h, style="F")
        pdf.ln(4)

        indent = 8
        pdf.set_left_margin(self.MARGIN_LEFT + indent)
        pdf.set_x(self.MARGIN_LEFT + indent)

        if negotiation_id:
            self._key_value(pdf, "Negotiation ID", negotiation_id, key_width=45)
        self._key_value(pdf, "Total Offers", str(len(history)), key_width=45)
        if elapsed_seconds is not None:
            self._key_value(pdf, "Duration", f"{elapsed_seconds:.1f} seconds", key_width=45)

        if history:
            first_ts = history[0].get("timestamp", "")
            last_ts = history[-1].get("timestamp", "")
            if first_ts:
                self._key_value(pdf, "Started", self._format_timestamp(first_ts), key_width=45)
            if last_ts:
                self._key_value(pdf, "Completed", self._format_timestamp(last_ts), key_width=45)

        pdf.set_left_margin(self.MARGIN_LEFT)
        pdf.set_y(card_y + card_h + 5)  # Position cursor after the card

        # Offer summary table
        self._section_header(pdf, "Offer Summary")
        pdf.ln(2)

        # Table header
        _font(pdf, "medium", 7)
        _color(pdf, LIGHT)
        col_w = [12, 20, 16, 28, 14, 18, 18, 0]
        headers = ["Round", "Party", "Type", "Cap", "Disc.", "Pro-Rata", "TX", "Time"]
        aligns = ["L", "L", "L", "R", "R", "R", "R", "R"]
        for i, (h, w) in enumerate(zip(headers, col_w)):
            if w == 0:
                pdf.cell(0, 5, h, align=aligns[i])
            else:
                pdf.cell(w, 5, h, align=aligns[i])
        pdf.cell(0, 5, "", new_x="LMARGIN", new_y="NEXT")

        _rule(pdf)
        pdf.ln(2)

        # Table rows with alternating backgrounds
        prev_terms: dict = {}
        for idx, entry in enumerate(history):
            round_num = entry.get("round", "")
            party = entry.get("from", "")
            offer_type = entry.get("type", "")
            terms = entry.get("terms", {})
            tx = entry.get("immudb_tx", "")
            ts = self._format_time_short(entry.get("timestamp", ""))

            # Alternating row background
            if idx % 2 == 1:
                _fill_color(pdf, TABLE_BG)
                pdf.rect(pdf.l_margin, pdf.get_y(), pdf.w - pdf.l_margin - pdf.r_margin, 5, style="F")

            _font(pdf, "", 7.5)
            _color(pdf, DARK)

            pdf.cell(12, 5, str(round_num))
            pdf.cell(20, 5, party)

            if offer_type in ("accept", "reject"):
                _font(pdf, "B", 7.5)
                _color(pdf, TEAL)
                pdf.cell(16, 5, offer_type)
                _color(pdf, DARK)
                _font(pdf, "", 7.5)
                pdf.cell(28, 5, "")
                pdf.cell(14, 5, "")
                pdf.cell(18, 5, "")
            else:
                pdf.cell(16, 5, offer_type)

                cap = terms.get("valuation_cap", 0)
                cap_changed = prev_terms and cap != prev_terms.get("valuation_cap")
                if cap_changed:
                    _color(pdf, TEAL)
                    _font(pdf, "B", 7.5)
                pdf.cell(28, 5, f"${cap:,.0f}", align="R")
                if cap_changed:
                    _color(pdf, DARK)
                    _font(pdf, "", 7.5)

                disc = terms.get("discount_rate", 0)
                disc_changed = prev_terms and disc != prev_terms.get("discount_rate")
                if disc_changed:
                    _color(pdf, TEAL)
                    _font(pdf, "B", 7.5)
                pdf.cell(14, 5, f"{disc:.0%}", align="R")
                if disc_changed:
                    _color(pdf, DARK)
                    _font(pdf, "", 7.5)

                pr = terms.get("pro_rata", False)
                pr_changed = prev_terms and pr != prev_terms.get("pro_rata")
                if pr_changed:
                    _color(pdf, TEAL)
                    _font(pdf, "B", 7.5)
                pdf.cell(18, 5, "Yes" if pr else "No", align="R")
                if pr_changed:
                    _color(pdf, DARK)
                    _font(pdf, "", 7.5)

            _color(pdf, LIGHT)
            _font(pdf, "", 6.5)
            pdf.cell(18, 5, str(tx) if tx is not None and tx != 0 else "", align="R")
            pdf.cell(0, 5, ts, align="R")
            pdf.cell(0, 5, "", new_x="LMARGIN", new_y="NEXT")

            _color(pdf, DARK)
            if terms:
                prev_terms = terms

        pdf.ln(6)

        # Negotiation transcript
        self._section_header(pdf, "Negotiation Transcript")

        for entry in history:
            round_num = entry.get("round", "")
            party = entry.get("from", "")
            offer_type = entry.get("type", "")
            message = entry.get("message", "")
            ts = self._format_timestamp(entry.get("timestamp", ""))

            if not message:
                continue

            # Round header
            _font(pdf, "medium", 8.5)
            _color(pdf, DARK)
            label = f"Round {round_num}  --  {party.capitalize()}"
            pdf.cell(0, 5, label)

            if ts:
                _font(pdf, "light", 6.5)
                _color(pdf, LIGHT)
                pdf.cell(0, 5, ts, align="R")
            pdf.cell(0, 5, "", new_x="LMARGIN", new_y="NEXT")

            # Offer type pill
            _font(pdf, "medium", 7)
            _color(pdf, TEAL)
            pdf.cell(0, 4, offer_type, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)

            # Message
            _font(pdf, "I", 8.5)
            _color(pdf, BODY)
            pdf.multi_cell(0, 4.5, f'"{_sanitize_text(message)}"')
            _color(pdf, DARK)
            pdf.ln(4)

    # ──────────────────────────────────────────────────────────
    # SAFE content pages
    # ──────────────────────────────────────────────────────────

    def _render_safe_content(self, pdf: FPDF, signers: list[dict] | None = None) -> None:
        pdf.set_left_margin(self.MARGIN_LEFT)
        pdf.set_right_margin(self.MARGIN_RIGHT)
        pdf.add_page()

        company = _sanitize_text(self.parties["founder"]["company"])
        investor_name = _sanitize_text(self.parties["investor"]["name"])
        investor_firm = _sanitize_text(self.parties["investor"].get("firm", ""))
        investor_label = investor_firm or investor_name
        founder_name = _sanitize_text(self.parties["founder"]["name"])
        founder_title = _sanitize_text(self.parties["founder"]["title"])
        cap = self.terms["valuation_cap"]
        discount = self.terms["discount_rate"]
        pro_rata = self.terms["pro_rata"]
        mfn = self.terms.get("mfn", False)
        amount = self.terms["investment_amount"]
        date = self.terms["date"]
        amount_display = f"${amount:,.0f}"

        # Title block
        pdf.ln(8)
        _font(pdf, "light", 28)
        _color(pdf, DARK)
        pdf.cell(0, 14, "SAFE", new_x="LMARGIN", new_y="NEXT", align="C")

        _font(pdf, "light", 11)
        _color(pdf, LIGHT)
        pdf.cell(
            0, 7,
            "Simple Agreement for Future Equity",
            new_x="LMARGIN", new_y="NEXT", align="C",
        )
        pdf.ln(3)

        # Teal accent line under title
        _draw_color(pdf, TEAL)
        center_x = pdf.w / 2
        pdf.line(center_x - 25, pdf.get_y(), center_x + 25, pdf.get_y())
        pdf.ln(8)

        # Preamble
        self._body_text(pdf, (
            f"THIS CERTIFIES THAT in exchange for the payment by "
            f"{investor_label} (the \"Investor\") of "
            f"{amount_display} (the \"Purchase Amount\") "
            f"on or about {date}, {company} "
            f"(the \"Company\"), hereby issues to the Investor the right to certain shares "
            f"of the Company's Capital Stock, subject to the terms described below."
        ))
        pdf.ln(6)

        # Key Terms card
        _fill_color(pdf, TABLE_BG)
        card_y = pdf.get_y()
        pdf.rect(pdf.l_margin, card_y, pdf.w - pdf.l_margin - pdf.r_margin, 46, style="F")

        # Teal left border on the card
        _fill_color(pdf, TEAL)
        pdf.rect(pdf.l_margin, card_y, 2.5, 46, style="F")
        pdf.ln(3)

        # Indent content past the teal bar
        indent = 8
        pdf.set_left_margin(self.MARGIN_LEFT + indent)
        pdf.set_x(self.MARGIN_LEFT + indent)

        _font(pdf, "medium", 8)
        _color(pdf, LIGHT)
        pdf.cell(0, 5, "KEY TERMS", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        self._key_value(pdf, "Valuation Cap", f"${cap:,.0f}")
        self._key_value(pdf, "Discount Rate", f"{discount:.0%}")
        self._key_value(pdf, "Pro-Rata Rights", "Included" if pro_rata else "Not Included")
        self._key_value(pdf, "Most Favored Nation", "Included" if mfn else "Not Included")
        self._key_value(pdf, "Purchase Amount", amount_display)
        self._key_value(pdf, "Date", date)

        # Restore margin
        pdf.set_left_margin(self.MARGIN_LEFT)
        pdf.ln(6)

        # Sections
        self._section_header(pdf, "Section 1: Events")

        self._subsection(pdf, "1(a) Equity Financing")
        self._body_text(pdf, (
            "If there is an Equity Financing before the termination of this Safe, on the "
            "initial closing of such Equity Financing, this Safe will automatically convert "
            "into the number of shares of Safe Preferred Stock equal to the Purchase Amount "
            "divided by either (i) the Safe Price or (ii) the Discount Price, whichever "
            "calculation results in a greater number of shares of Safe Preferred Stock."
        ))
        pdf.ln(4)

        self._subsection(pdf, "1(b) Liquidity Event")
        self._body_text(pdf, (
            "If there is a Liquidity Event before the termination of this Safe, this Safe "
            "will automatically be entitled (subject to the liquidation priority set forth in "
            "Section 1(d) below) to receive a portion of Proceeds, due and payable to the "
            "Investor immediately prior to, or concurrent with, the consummation of such "
            "Liquidity Event."
        ))
        pdf.ln(4)

        self._subsection(pdf, "1(c) Dissolution Event")
        self._body_text(pdf, (
            "If there is a Dissolution Event before the termination of this Safe, the "
            "Investor will automatically be entitled (subject to the liquidation priority "
            "set forth in Section 1(d) below) to receive a portion of Proceeds equal to the "
            "Purchase Amount, due and payable to the Investor immediately prior to the "
            "consummation of the Dissolution Event."
        ))
        pdf.ln(6)

        self._section_header(pdf, "Section 2: Definitions")
        self._body_text(pdf, (
            f"\"Safe Price\" means the price per share equal to the Post-Money Valuation Cap "
            f"divided by the Company Capitalization."
        ))
        pdf.ln(3)
        self._body_text(pdf, (
            f"\"Discount Price\" means the price per share of the Standard Preferred Stock "
            f"sold in the Equity Financing multiplied by the Discount Rate "
            f"({1.0 - discount:.0%} of the price per share)."
        ))
        pdf.ln(3)
        self._body_text(pdf, f"\"Post-Money Valuation Cap\" means ${cap:,.0f}.")
        pdf.ln(6)

        self._section_header(pdf, "Section 3: Company Representations")
        self._body_text(pdf, (
            "(a) The Company is a corporation duly organized, validly existing, and in good "
            "standing under the laws of its state of incorporation, and has the power and "
            "authority to own, lease, and operate its properties and carry on its business "
            "as now conducted."
        ))
        pdf.ln(3)
        self._body_text(pdf, (
            "(b) The execution, delivery, and performance by the Company of this Safe is "
            "within the power of the Company and has been duly authorized by all necessary "
            "actions on the part of the Company."
        ))
        pdf.ln(6)

        self._section_header(pdf, "Section 4: Investor Representations")
        self._body_text(pdf, (
            "(a) The Investor has full legal capacity, power, and authority to execute and "
            "deliver this Safe and to perform its obligations hereunder."
        ))
        pdf.ln(3)
        self._body_text(pdf, (
            "(b) The Investor is an accredited investor as such term is defined in Rule 501 "
            "of Regulation D under the Securities Act."
        ))
        pdf.ln(6)

        self._section_header(pdf, "Section 5: Miscellaneous")
        self._body_text(pdf, (
            "(a) Any provision of this Safe may be amended, waived, or modified by written "
            "consent of the Company and the Investor."
        ))
        pdf.ln(3)
        self._body_text(pdf, (
            "(b) Any notice required or permitted by this Safe will be deemed sufficient "
            "when delivered personally or sent by email to the relevant address listed on "
            "the signature page."
        ))
        pdf.ln(3)
        self._body_text(pdf, (
            "(c) This Safe shall be governed by and construed under the laws of the State of "
            "Delaware, United States, without regard to conflicts of law provisions."
        ))
        pdf.ln(3)
        self._body_text(pdf, (
            "(d) In the event that any provision of this Safe is determined to be invalid, "
            "illegal, or unenforceable, the remaining provisions shall continue in full "
            "force and effect."
        ))
        pdf.ln(8)

        next_section = 6

        if pro_rata:
            self._section_header(pdf, f"Section {next_section}: Pro-Rata Rights")
            self._body_text(pdf, (
                "The Investor shall have a pro-rata right to participate in subsequent "
                "Equity Financing rounds of the Company, on the same terms and conditions "
                "as other investors in such round, up to an amount sufficient to maintain "
                "the Investor's percentage ownership of the Company."
            ))
            pdf.ln(8)
            next_section += 1

        if mfn:
            self._section_header(pdf, f"Section {next_section}: Most Favored Nation")
            self._body_text(pdf, (
                "If the Company issues any subsequent Simple Agreements for Future Equity "
                "or convertible securities (each a \"Subsequent Instrument\") with terms more "
                "favorable to the holder of such Subsequent Instrument than the terms of this "
                "Safe, the Company shall promptly notify the Investor and, at the Investor's "
                "election, amend this Safe to reflect such more favorable terms. More favorable "
                "terms include, without limitation, a lower valuation cap, a higher discount "
                "rate, or additional rights not included in this Safe."
            ))
            pdf.ln(3)
            self._body_text(pdf, (
                "This provision shall terminate upon the earliest of: (i) the initial closing "
                "of an Equity Financing, (ii) a Liquidity Event, or (iii) a Dissolution Event."
            ))
            pdf.ln(8)

        # Signature page
        pdf.add_page()
        pdf.ln(10)

        _font(pdf, "light", 20)
        _color(pdf, DARK)
        pdf.cell(0, 10, "Signature Page", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(3)

        _draw_color(pdf, TEAL)
        center_x = pdf.w / 2
        pdf.line(center_x - 20, pdf.get_y(), center_x + 20, pdf.get_y())
        pdf.ln(12)

        # Helper to find a signer's handwritten image
        def _get_hw_sig(role: str) -> str | None:
            if not signers:
                return None
            for s in signers:
                if s.get("role") == role and s.get("signature_image"):
                    return s["signature_image"]
            return None

        # Company signature block
        _font(pdf, "medium", 8)
        _color(pdf, LIGHT)
        pdf.cell(0, 5, "COMPANY", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
        _font(pdf, "B", 11)
        _color(pdf, DARK)
        pdf.cell(0, 7, company, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)

        founder_hw = _get_hw_sig("founder")
        if founder_hw:
            self._embed_signature_image(pdf, founder_hw)
        else:
            pdf.ln(5)
            _draw_color(pdf, RULE)
            pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + 80, pdf.get_y())

        pdf.ln(2)
        _font(pdf, "", 9)
        _color(pdf, BODY)
        pdf.cell(0, 5, f"{founder_name},  {founder_title}", new_x="LMARGIN", new_y="NEXT")
        _font(pdf, "light", 8)
        _color(pdf, LIGHT)
        pdf.cell(0, 5, date, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(12)

        # Investor signature block
        _font(pdf, "medium", 8)
        _color(pdf, LIGHT)
        pdf.cell(0, 5, "INVESTOR", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
        _font(pdf, "B", 11)
        _color(pdf, DARK)
        pdf.cell(0, 7, investor_label, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)

        investor_hw = _get_hw_sig("investor")
        if investor_hw:
            self._embed_signature_image(pdf, investor_hw)
        else:
            pdf.ln(5)
            _draw_color(pdf, RULE)
            pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + 80, pdf.get_y())

        pdf.ln(2)
        _font(pdf, "", 9)
        _color(pdf, BODY)
        pdf.cell(0, 5, investor_name, new_x="LMARGIN", new_y="NEXT")
        _font(pdf, "light", 8)
        _color(pdf, LIGHT)
        pdf.cell(0, 5, date, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(16)

        # Footer
        _font(pdf, "light", 7.5)
        _color(pdf, LIGHT)
        pdf.cell(
            0, 5,
            "Generated by APOA Negotiate  |  Signatures verified via sshsign",
            new_x="LMARGIN", new_y="NEXT", align="C",
        )

    def _embed_signature_image(self, pdf: FPDF, image_b64: str) -> None:
        """Embed a base64-encoded handwritten signature image."""
        img_data = image_b64
        if "," in img_data:
            img_data = img_data.split(",", 1)[1]

        img_bytes = base64.b64decode(img_data)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp.write(img_bytes)
            tmp_path = tmp.name

        try:
            pdf.image(tmp_path, x=pdf.l_margin, w=80, h=25)
            pdf.ln(26)
        finally:
            Path(tmp_path).unlink(missing_ok=True)
