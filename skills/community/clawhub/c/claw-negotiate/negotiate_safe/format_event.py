#!/usr/bin/env python3
"""Format negotiation events as short Telegram messages.

User-facing cards use Telegram HTML formatting (`<b>`, `<code>`, `<pre>`) so
bold text renders cleanly without visible Markdown asterisks. Any user- or
model-supplied text that might contain `<`, `>`, or `&` is escaped via
`_escape_html` before being inserted into an HTML-formatted card.

Event schema reflects what the local turn helper emits:

  offer / counter / accept   (negotiation turns)
  outcome                    (local demo mode)
  signing                    (when awaiting cosign approval)
  confirm                    (our prepare step)
  authorized                 (our mint step)
  signed                     (synthesized by us after envelope=approved)
"""
from __future__ import annotations

import json
import sys
import html
from typing import Any
from urllib.parse import quote


# ──────────────────────────────────────────────────────────────
# Formatting helpers
# ──────────────────────────────────────────────────────────────


def fmt_dollars(n: float | int | None) -> str:
    """Smart-shorten dollar amounts without hiding negotiated precision."""
    if n is None:
        return "-"
    n = int(n)
    if n == 0:
        return "$0"
    sign = "-" if n < 0 else ""
    n = abs(n)
    if n >= 1_000_000:
        if n % 1_000_000 == 0:
            return f"{sign}${n // 1_000_000}M"
        if n % 10_000 == 0:
            millions = f"{n / 1_000_000:.2f}".rstrip("0").rstrip(".")
            return f"{sign}${millions}M"
        return f"{sign}${n:,}"
    if n >= 10_000 and n % 1000 == 0:
        return f"{sign}${n // 1000}K"
    return f"{sign}${n:,}"


def fmt_percent(d: float | None) -> str:
    if d is None:
        return "-"
    return f"{d * 100:.0f}%"


def _yn(flag: Any) -> str:
    return "yes" if flag else "no"


def _escape_html(s: str) -> str:
    """Escape text for Telegram HTML parse mode."""
    return html.escape(str(s), quote=False)


def _b(s: str) -> str:
    return f"<b>{_escape_html(s)}</b>"


def _code(s: str) -> str:
    return f"<code>{_escape_html(s)}</code>"


def _pre(s: str) -> str:
    return f"<pre>{_escape_html(s)}</pre>"


def _format_founder_identity(
    founder_name: str | None,
    founder_title: str | None,
    company_name: str | None,
) -> str | None:
    if founder_name and founder_title and company_name:
        return f"{founder_name}, {founder_title} of {company_name}"
    if founder_name and founder_title:
        return f"{founder_name}, {founder_title}"
    if founder_name and company_name:
        return f"{founder_name} of {company_name}"
    if founder_name:
        return founder_name
    return company_name or None


def _format_investor_identity(
    investor_name: str | None,
    investor_firm: str | None,
) -> str | None:
    if investor_name and investor_firm:
        return f"{investor_name} at {investor_firm}"
    return investor_name or investor_firm or None


_PARTY_ICON = {"founder": "\U0001f464", "investor": "\U0001f4bc"}  # 👤, 💼
_PLACEHOLDER_BOT_HANDLES = {"yourbot", "@yourbot"}


def _clean_bot_handle(value: Any) -> str:
    handle = str(value or "").strip()
    return "" if handle.lower() in _PLACEHOLDER_BOT_HANDLES else handle


def _format_check_bounds(c: dict[str, Any]) -> str | None:
    amount_min = c.get("investment_amount_min")
    amount_max = c.get("investment_amount_max")
    if amount_min is not None and amount_max is not None:
        return fmt_dollars(amount_min) + " – " + fmt_dollars(amount_max)
    amount = c.get("investment_amount")
    if amount is not None:
        return fmt_dollars(amount)
    return None


def _format_discount_bounds(c: dict[str, Any]) -> str | None:
    disc_min = c.get("discount_min")
    disc_max = c.get("discount_max", disc_min)
    if disc_min is None:
        return None
    if disc_max is None or disc_max == disc_min:
        return fmt_percent(disc_min)
    return fmt_percent(disc_min) + " – " + fmt_percent(disc_max)

# ──────────────────────────────────────────────────────────────
# Wrapper-side events
# ──────────────────────────────────────────────────────────────


def format_confirm(event: dict[str, Any]) -> str:
    c = event["constraints"]
    labels = {
        "required": "required",
        "preferred": "preferred",
        "indifferent": "no preference",
    }
    mfn_labels = {
        "required": "required",
        "preferred": "preferred",
        "indifferent": "no preference",
    }
    role = (c.get("role") or "founder").lower()
    role_label = "Founder" if role == "founder" else "Investor"
    role_icon = "\U0001f464" if role == "founder" else "\U0001f4bc"  # 👤 / 💼
    agent_label = f"{role_label} OpenClaw"

    founder_name = c.get("founder_name")
    founder_title = c.get("founder_title")
    company_name = c.get("company_name")
    investor_name = c.get("investor_name")
    investor_firm = c.get("investor_firm")

    # Build "You" and "Counterparty" lines based on the user's role. Show
    # only what was captured — omit missing pieces so the line stays clean.
    founder_line = _format_founder_identity(
        founder_name, founder_title, company_name,
    )
    investor_line = _format_investor_identity(investor_name, investor_firm)

    if role == "founder":
        you_line = founder_line
        counterparty_line = investor_line
        counterparty_label = "Investor"
    else:
        you_line = investor_line
        counterparty_line = founder_line
        counterparty_label = "Founder"

    identity_lines = [
        f"{role_icon} {_b(f'Review your {agent_label} authorization')}",
    ]
    if you_line or counterparty_line:
        identity_lines.append("")
    if you_line:
        identity_lines.append(f"{_b('You:')} {_escape_html(you_line)}")
    if counterparty_line:
        identity_lines.append(
            f"{_b(counterparty_label + ':')} {_escape_html(counterparty_line)}"
        )

    check_bounds = _format_check_bounds(c)
    discount_bounds = _format_discount_bounds(c)
    lines = [
        "\n".join(identity_lines),
        "",
        f"Your {agent_label} will only agree to:",
        "",
        f"• Valuation cap: {_b(fmt_dollars(c['valuation_cap_min']) + ' – ' + fmt_dollars(c['valuation_cap_max']))}",
    ]
    if check_bounds:
        lines.append(f"• Check size: {_b(check_bounds)}")
    lines.extend([
        f"• Discount: {_b(discount_bounds or fmt_percent(c['discount_min']))}",
        f"• Pro-rata rights: {_b(labels[c['pro_rata']])}",
        f"• MFN: {_b(mfn_labels[c['mfn']])}",
        "",
        "You will personally review and sign the final SAFE.",
        "",
        f"Reply {_code('GO')} to continue, or send edits.",
    ])
    return "\n".join(lines)


def format_authorized(event: dict[str, Any]) -> str:
    """Authorization card, framed user-first.

    Fires once after mint completes, before the first round. Shows the
    bounds in plain English so the user knows what their agent can and
    can't do. APOA is cited in a lightweight footer, not the headline —
    the concept earns its keep on the next screens (constraint
    violations, signed audit trail).
    """
    c = event.get("constraints") or {}
    cap_min = c.get("valuation_cap_min")
    cap_max = c.get("valuation_cap_max")
    disc_min = c.get("discount_min")
    discount_bounds = _format_discount_bounds(c)
    pro_rata = (c.get("pro_rata") or "indifferent").lower()
    mfn = (c.get("mfn") or "indifferent").lower()

    pr_labels = {
        "required": "required",
        "preferred": "preferred",
        "indifferent": "no preference",
    }
    ttl_hours = event.get("ttl_hours") or 1
    role = (c.get("role") or event.get("role") or "agent").strip().lower()
    agent_label = "Founder OpenClaw" if role == "founder" else (
        "Investor OpenClaw" if role == "investor" else "OpenClaw"
    )

    lines = [
        "\U0001f512 " + _b("Authorization set"),  # 🔒
        "",
        f"Your {agent_label} can now negotiate, but only within these limits:",
        "",
    ]
    if cap_min is not None and cap_max is not None:
        lines.append(
            f"• Valuation cap: {_b(fmt_dollars(cap_min) + ' – ' + fmt_dollars(cap_max))}"
        )
    check_bounds = _format_check_bounds(c)
    if check_bounds:
        lines.append(f"• Check size: {_b(check_bounds)}")
    if disc_min is not None:
        lines.append(f"• Discount: {_b(discount_bounds or fmt_percent(disc_min))}")
    lines.append(f"• Pro-rata rights: {_b(pr_labels.get(pro_rata, pro_rata))}")
    lines.append(f"• MFN: {_b(pr_labels.get(mfn, mfn))}")
    lines.extend([
        "",
        f"Valid for {ttl_hours} hour"
        f"{'s' if ttl_hours != 1 else ''}. Reply {_code('cancel')} anytime to revoke.",
        "",
        f"{_b('APOA constraint:')} every offer your {agent_label} makes is "
        "cryptographically bound to this authorization.",
    ])
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────
# Upstream events (from --json-events)
# ──────────────────────────────────────────────────────────────


def format_offer(
    event: dict[str, Any],
    constraints: dict[str, Any] | None = None,
) -> str:
    """Render an offer/counter/accept event.

    offer/counter → round card showing the party, rationale, and terms.
    accept        → celebration card ("🤝 Deal!") with agreed terms. The
                    accept event is the last event before signing, so this
                    is the user's big win-moment and should feel celebratory.
    """
    etype = event.get("type", "offer")
    if etype == "accept":
        return _format_accept(event)

    party_raw = (event.get("party") or "").lower()
    icon = _PARTY_ICON.get(party_raw, "")
    party = party_raw.capitalize() or "?"
    round_num = event.get("round", "?")
    try:
        offer_num = int(round_num) + 1
    except (TypeError, ValueError):
        offer_num = round_num

    terms = event.get("terms") or {}
    cap = terms.get("valuation_cap")
    amount = terms.get("investment_amount")
    discount = terms.get("discount_rate")

    mode = (constraints or {}).get("mode") if constraints else None
    agent_suffix = " OpenClaw"

    header_prefix = f"{icon} " if icon else ""
    header = f"{header_prefix}{_b(f'Offer {offer_num} — {party}{agent_suffix}')}"
    lines = [header]

    message = (event.get("message") or "").strip()
    if message:
        lines.extend(["", f'"{_escape_html(message)}"'])

    # PRIVACY: in two-party mode round cards land in the SHARED group
    # where the counterparty can read them. Each side's bounds are
    # private. Suppress the "your range" / "your min" annotations
    # entirely in two-party. Demo mode renders to the user's own DM,
    # so the hint is safe to keep there.
    if constraints and mode != "two_party":
        cap_min = constraints.get("valuation_cap_min")
        cap_max = constraints.get("valuation_cap_max")
        disc_min = constraints.get("discount_min")
        disc_max = constraints.get("discount_max", disc_min)
        cap_range = f" (your range: {fmt_dollars(cap_min)}–{fmt_dollars(cap_max)})" if cap_min is not None else ""
        if disc_min is not None and disc_max is not None and disc_max != disc_min:
            disc_range = f" (your range: {fmt_percent(disc_min)}–{fmt_percent(disc_max)})"
        else:
            disc_range = f" (your term: {fmt_percent(disc_min)})" if disc_min is not None else ""
    else:
        cap_range = disc_range = ""

    lines.extend([
        "",
        "Terms:",
        f"• Valuation cap: {_b(fmt_dollars(cap))}{_escape_html(cap_range)}",
    ])
    if amount is not None:
        lines.append(f"• Check size: {_b(fmt_dollars(amount))}")
    lines.extend([
        f"• Discount: {_b(fmt_percent(discount))}{_escape_html(disc_range)}",
        f"• Pro-rata rights: {_b(_yn(terms.get('pro_rata')))}",
        f"• MFN: {_b(_yn(terms.get('mfn')))}",
    ])

    return "\n".join(lines)


def _format_accept(event: dict[str, Any]) -> str:
    """Celebration card rendered on the accept event (fires before outcome).

    Pulling the celebration forward to the accept event (instead of waiting
    for outcome) eliminates the ~second-long delay upstream introduces
    between the two; user sees the deal land the instant it's struck.
    """
    terms = event.get("terms") or {}
    amount = terms.get("investment_amount")
    amount_line = (
        f"• Check size: {_b(fmt_dollars(amount))}\n"
        if amount is not None else ""
    )
    return (
        f"\U0001f91d {_b('Deal reached')}\n\n"  # 🤝
        "Both OpenClaws agreed to these terms:\n\n"
        f"• Valuation cap: {_b(fmt_dollars(terms.get('valuation_cap')))}\n"
        f"{amount_line}"
        f"• Discount: {_b(fmt_percent(terms.get('discount_rate')))}\n"
        f"• Pro-rata rights: {_b(_yn(terms.get('pro_rata')))}\n"
        f"• MFN: {_b(_yn(terms.get('mfn')))}\n\n"
        f"{_b('Next:')} each party will review and sign privately."
    )


def format_apoa_blocked_counterparty_offer(event: dict[str, Any]) -> str:
    role = (event.get("role") or "agent").strip().lower()
    label = "Founder OpenClaw" if role == "founder" else (
        "Investor OpenClaw" if role == "investor" else "OpenClaw"
    )
    return (
        f"\U0001f6e1 {_b('APOA blocked an out-of-bounds term')}\n\n"  # 🛡
        f"The latest counterparty offer was outside your authorization, so your {label} "
        "cannot accept it.\n\n"
        "Your OpenClaw will counter within your authorized terms or end the negotiation."
    )


def format_outcome(
    event: dict[str, Any],
    constraints: dict[str, Any] | None = None,
) -> str | None:
    """Render only failure outcomes.

    For `result=accepted`, return None so the caller skips it — the preceding
    `accept` event has already shown the full terms card with an "Accepted"
    header, and the upcoming `signing` event is the next clear action. Emitting
    a redundant "Deal!" card between them just adds a ~second of delay with no
    new information.

    For `result=max_rounds`, we're in a no-ZOPA case: the two parties' ranges
    didn't overlap. Spell that out in plain English so the user understands
    WHY we stopped and knows the next move is to revisit their bounds.
    """
    result = event.get("result")

    if result == "accepted":
        return None
    if result == "max_rounds":
        cap_min = (constraints or {}).get("valuation_cap_min") if constraints else None
        cap_max = (constraints or {}).get("valuation_cap_max") if constraints else None
        lines = [f"\U0001f937 {_b('No agreement reached')}"]  # 🤷
        if cap_min is not None and cap_max is not None:
            lines.append("")
            lines.append(
                "Your range and your counterparty's didn't overlap enough "
                "to close on terms."
            )
            lines.append(
                f"Your cap range was {_b(fmt_dollars(cap_min) + ' – ' + fmt_dollars(cap_max))}."
            )
        else:
            lines.append("")
            lines.append(
                "Your range and your counterparty's didn't overlap. "
                "No SAFE was executed."
            )
        return "\n".join(lines)
    if result == "rejected":
        return "Negotiation rejected. No agreement reached."
    return None


def format_propose_new_terms(event: dict[str, Any]) -> str:
    """Follow-up card pushed after a no-ZOPA outcome.

    Invites the user to try again with updated bounds. Kept intentionally
    short — the outcome card did the explaining; this one just points at
    the next action.
    """
    counterparty = (event.get("counterparty_label") or "").strip()
    if counterparty:
        with_line = f" with {counterparty}"
    else:
        with_line = ""
    return (
        f"\U0001f504 {_b('Try again?')}\n\n"  # 🔄
        f"Reply with updated terms and I'll start a new negotiation{with_line}. "
        "Example: \"Negotiate again, cap $15M-$25M, 15% discount.\""
    )


def format_signing(event: dict[str, Any]) -> str:
    approval_url = (event.get("approval_url") or "").strip()
    pending_id = event.get("pending_id") or ""

    if approval_url:
        # Do NOT escape the URL — Telegram auto-detects and links it. Adding
        # backslash escapes breaks the underscore in `pnd_XXX` when Telegram
        # hands the URL back to sshsign (observed: "Invalid pending ID").
        return (
            f"\u270d\ufe0f {_b('Review and sign')}\n\n"  # ✍️
            "Open the secure signing page below to review the final terms "
            "and draw your signature.\n\n"
            f"{_escape_html(approval_url)}\n\n"
            f"{_b('Do not share this link.')}"
        )
    if pending_id:
        return (
            "Awaiting your co-signature.\n\n"
            f"Approve from any terminal:\n{_code('ssh sshsign.dev approve --id ' + pending_id)}"
        )
    return "Awaiting your co-signature."


# ──────────────────────────────────────────────────────────────
# Post-envelope synthesized event
# ──────────────────────────────────────────────────────────────


def format_signed(event: dict[str, Any]) -> str:
    terms = event.get("terms") or {}
    cap = terms.get("valuation_cap")
    amount = terms.get("investment_amount")
    discount = terms.get("discount_rate")
    pro_rata = terms.get("pro_rata")
    mfn = terms.get("mfn")

    if cap is not None or discount is not None:
        lines = [
            f"\u2705 {_b('SAFE executed')}",
            "",
            "The signed SAFE is attached below.",
            "",
            f"{_b('Final terms:')}",
        ]
        if cap is not None:
            lines.append(f"• Valuation cap: {_b(fmt_dollars(cap))}")
        if amount is not None:
            lines.append(f"• Check size: {_b(fmt_dollars(amount))}")
        if discount is not None:
            lines.append(f"• Discount: {_b(fmt_percent(discount))}")
        if pro_rata is not None:
            lines.append(f"• Pro-rata rights: {_b(_yn(pro_rata))}")
        if mfn is not None:
            lines.append(f"• MFN: {_b(_yn(mfn))}")
        lines.append("")
        lines.append(
            "The cryptographic audit trail is available through sshsign."
        )
        return "\n".join(lines)
    return (
        f"\u2705 {_b('SAFE executed')}\n\n"
        "The cryptographic audit trail is available through sshsign."
    )


# ──────────────────────────────────────────────────────────────
# Dispatcher + CLI
# ──────────────────────────────────────────────────────────────


def format_profile(event: dict[str, Any]) -> str:
    """Render the user's saved identity (from env vars) as a chat card.

    Only shows lines for fields that are set — missing fields quietly
    disappear so the card doesn't advertise placeholders.
    """
    p = event.get("profile") or {}
    founder_name = (p.get("founder_name") or "").strip()
    founder_title = (p.get("founder_title") or "").strip()
    company_name = (p.get("company_name") or "").strip()
    investor_name = (p.get("investor_name") or "").strip()
    investor_firm = (p.get("investor_firm") or "").strip()

    has_founder = bool(founder_name or founder_title or company_name)
    has_investor = bool(investor_name or investor_firm)

    if not has_founder and not has_investor:
        return (
            "\U0001f464 Your profile is empty. "  # 👤
            "Say \"I'm Name, Title at Company\" to set it up."
        )

    lines = ["\U0001f464 " + _b("Your saved profile")]  # 👤

    if has_founder:
        lines.append("")
        lines.append(_b("Founder side") + " \U0001f464")  # 👤
        if founder_name:
            lines.append(f"• Name: {_b(founder_name)}")
        if founder_title:
            lines.append(f"• Title: {founder_title}")
        if company_name:
            lines.append(f"• Company: {company_name}")

    if has_investor:
        lines.append("")
        lines.append(_b("Investor side") + " \U0001f4bc")  # 💼
        if investor_name:
            lines.append(f"• Name: {_b(investor_name)}")
        if investor_firm:
            lines.append(f"• Firm: {investor_firm}")

    lines.append("")
    lines.append("To update, say something like: "
                 "\"Update my profile — I'm now Jane Smith, CFO of NewCo\".")
    return "\n".join(lines)


def format_invitation(event: dict[str, Any]) -> str:
    """Founder-side card shown after a two-party session is created.

    Inverted-invitation design: the founder doesn't know the
    investor's bot handle, so we cannot author a tap-to-join Telegram
    link. Instead, hand the founder a single copy-pasteable block
    that includes BOTH the session code and the founder's own bot
    handle. The investor's job is to paste this exact text to their
    own bot — the "via @<founder>" form is what the investor's parse
    layer extracts, with sshsign's metadata as the authoritative
    backstop.

    Required event fields: session_code, founder_bot_handle.
    Optional: expires_at, ttl_hours, counterparty_label.
    """
    code = (event.get("session_code") or "").strip()
    founder_bot = _clean_bot_handle(event.get("founder_bot_handle"))
    if founder_bot and not founder_bot.startswith("@"):
        founder_bot = "@" + founder_bot
    expires_at = event.get("expires_at") or ""
    ttl_h = event.get("ttl_hours") or 24
    counterparty = (event.get("counterparty_label") or "your investor").strip()

    # Pre-build the exact join template the investor should paste.
    # Including a placeholder line for "your terms" makes the
    # required edit obvious; the investor knows to swap it for their
    # own cap/discount/etc. without us having to explain.
    identity_fragment = ""
    investor_name = (event.get("investor_name") or "").strip()
    investor_firm = (event.get("investor_firm") or "").strip()
    if investor_name and investor_firm:
        identity_fragment = f"I am {investor_name} at {investor_firm}, "
    elif investor_name:
        identity_fragment = f"I am {investor_name}, "
    elif investor_firm:
        identity_fragment = f"I am at {investor_firm}, "

    if identity_fragment.endswith(", "):
        identity_fragment = identity_fragment[:-2] + "."
    join_intro = (
        f"Joining {code} via {founder_bot}, {identity_fragment}"
        if founder_bot
        else f"Joining {code} as investor, {identity_fragment}"
    ).strip()
    join_template = "\n\n".join([
        join_intro,
        "\n".join([
            "Cap: $X-$Y post.",
            "Check: $Z-$W.",
            "Pro rata: required / not required / no preference.",
            "Discount: V%",
        ]),
    ])

    invite_block = "\n\n".join([
        "Please join our SAFE negotiation.",
        "DM your investor agent on Telegram and paste:",
        join_template,
        "Replace $X, $Y, $Z, $W, V%, and the pro-rata preference with your investor-side limits.",
    ])

    first_name = counterparty.split()[0] if counterparty and counterparty != "your investor" else "your investor"

    lines = [
        f"✉️ {_b('Ready to invite ' + first_name)}",
        "",
        f"{_b('Send ' + counterparty + ' this message:')}",
        "",
        _pre(invite_block),
        "",
    ]
    # If founder_bot is empty we silently fall back to the generic
    # template above. The op-side warning that used to live here was
    # confusing to end users (it was meant for ops). Misconfig logs
    # to stderr from the call site instead.

    if expires_at:
        lines.append(
            f"I'll notify you when {first_name} joins. "
            f"The invitation is valid for {ttl_h} hours."
        )
    else:
        lines.append(f"I'll notify you when {first_name} joins.")
    lines.append("")
    lines.append(f"Reply {_code('cancel')} anytime to revoke.")
    return "\n".join(lines)


def _fmt_hhmm(total_seconds: float) -> str:
    """Render a duration as HH:MM (e.g., '23:47')."""
    total = max(0, int(total_seconds))
    hours = total // 3600
    minutes = (total % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"


def format_waiting(event: dict[str, Any]) -> str:
    """Periodic status card while the founder waits for their counterparty.

    Not fired on every poll — only when the wait has crossed a notable
    threshold (e.g., 1h, 6h, 12h elapsed) so the user doesn't get spammed.
    Shows a countdown to expiration so the user knows how much runway is
    left on the invitation.
    """
    elapsed_minutes = int(event.get("elapsed_minutes") or 0)
    remaining_hours = event.get("remaining_hours")
    lines = [
        f"\u23f3 Still waiting for your counterparty to join."  # ⏳
        f" ({elapsed_minutes} min elapsed)",
    ]
    if remaining_hours is not None:
        rem_seconds = float(remaining_hours) * 3600
        lines.append(
            f"Invitation expires in {_b(_fmt_hhmm(rem_seconds))}. "
            "Share the code soon."
        )
    return "\n".join(lines)


def format_counterparty_joined(event: dict[str, Any]) -> str:
    """Fires the moment the other OC joins the session — flips founder OC
    from waiting to active-negotiation mode."""
    who = (event.get("counterparty_label") or "your counterparty").strip()
    return f"\u2705 {who} joined. Starting the negotiation\u2026"  # ✅


def format_invitation_expired(event: dict[str, Any]) -> str:
    return (
        "\u23f0 Your invitation expired before anyone joined.\n\n"  # ⏰
        "Say \"negotiate my SAFE with \u2026\" again to create a new one."
    )


def format_session_expired(event: dict[str, Any]) -> str:
    """Mid-negotiation APOA/session expiration.

    Distinct from invitation_expired (which fires before the counterparty
    joins) — this one fires after things were in flight but the session
    ran out of time before both parties signed.
    """
    return (
        "\u23f0 " + _b("Authorization expired") + "\n\n"  # ⏰
        "No SAFE was executed. This mid-flight session is now closed because the APOA "
        "authorization expired before both parties signed.\n\n"
        "To continue, start a new SAFE negotiation with the same terms."
    )


def _who_label(event: dict[str, Any]) -> str:
    who = (event.get("by") or "").strip()
    return who or "The other party"


def _session_code(event: dict[str, Any]) -> str:
    return (event.get("session_code") or event.get("code") or "").strip()


def format_canceled_before_deal_initiator(event: dict[str, Any]) -> str:
    """You canceled — no agreement had been reached yet. Includes the
    session code so the user can confirm WHICH negotiation got
    canceled (especially when rapidly minting + canceling).
    """
    code = (event.get("session_code") or "").strip()
    code_line = f" {code}" if code else ""
    return (
        f"\u274c {_b('Negotiation' + code_line + ' canceled')}\n\n"  # ❌
        "No SAFE was executed. Your agent's authorization has been revoked."
    )


def format_canceled_before_deal_observer(event: dict[str, Any]) -> str:
    """Your counterparty canceled — no agreement had been reached yet."""
    who = _who_label(event)
    code = _session_code(event)
    header = f"Negotiation {code} canceled" if code else "Negotiation canceled"
    return (
        f"\u274c {_b(header)}\n\n"  # ❌
        f"{_escape_html(who)} stopped the negotiation before a deal was reached.\n\n"
        "No SAFE was executed."
    )


def format_canceled_after_deal_initiator(event: dict[str, Any]) -> str:
    """You revoked the agreed deal before either side signed."""
    return (
        f"\u274c {_b('Negotiation canceled')}\n\n"  # ❌
        "You revoked the agreed deal before signing.\n\n"
        "Your counterparty has been notified. No SAFE will be executed."
    )


def format_canceled_after_deal_observer(event: dict[str, Any]) -> str:
    who = _who_label(event)
    return (
        f"\u274c {_b('Negotiation canceled')}\n\n"  # ❌
        f"{_escape_html(who)} revoked the agreed deal before signing.\n\n"
        "No SAFE will be executed. The negotiation is closed."
    )


def format_rescinded_after_sign_initiator(event: dict[str, Any]) -> str:
    """You rescinded AFTER signing — your signature stays on record but
    the deal does not execute. Includes the session code so the user
    knows WHICH negotiation was rescinded.
    """
    code = (event.get("session_code") or "").strip()
    code_line = f" {code}" if code else ""
    return (
        f"\u26a0\ufe0f {_b('Negotiation' + code_line + ' rescinded after signing')}\n\n"  # ⚠
        "Your signature stays on record for audit purposes, "
        "but the SAFE will NOT execute. Your counterparty has been notified."
    )


def format_rescinded_after_sign_observer(event: dict[str, Any]) -> str:
    who = _who_label(event)
    return (
        f"\u26a0\ufe0f {_escape_html(who)} rescinded after signing.\n\n"  # ⚠
        "The SAFE will NOT execute. Their signature is on record but void for this deal."
    )


def format_cancel_completed_deal_refused(event: dict[str, Any]) -> str:
    """User tried to cancel an already-executed SAFE — not allowed."""
    code = _session_code(event)
    header = f"SAFE {code} already executed" if code else "SAFE already executed"
    return (
        f"\U0001f512 {_b(header)}\n\n"  # 🔒
        f"This negotiation is complete and can't be canceled with {_code('/cancel')}.\n\n"
        "To unwind it, both parties would need to sign a separate rescission agreement."
    )


def format_go_live(event: dict[str, Any]) -> str:
    """DM card pushed after two-party mint: instructs the founder to
    create a Telegram group with both bots + the investor, then paste
    `/bind INV-XXXXX` in the group.

    Design note: the code and the /bind payload are wrapped in backtick
    inline-code spans because Telegram surfaces long-press-to-copy
    (mobile) and click-to-copy (desktop) on inline code entities. Do NOT
    render `/bind INV-...` as a highlighted bot_command entity — tapping
    a highlighted /command re-sends it FROM THE CURRENT CHAT (the DM),
    which would re-trigger the go-live card in the DM instead of
    binding the group.
    """
    code = (event.get("session_code") or "").strip()
    founder_bot = (event.get("founder_bot") or "@AgenticPOA_bot").strip()
    investor_bot = (event.get("investor_bot") or "@AgenticPOAInvestor_bot").strip()
    counterparty = (event.get("counterparty_handle") or "").strip()

    members = [
        f"  • {founder_bot}  (me)",
        f"  • {investor_bot}  (your investor's agent)",
    ]
    if counterparty:
        members.append(f"  • {counterparty}  (your investor)")
    else:
        members.append("  • your investor (add their @username here)")

    bind_payload = f"/bind {code}" if code else "/bind INV-XXXXX"

    lines = [
        f"\U0001f3ac {_b('Want to see both OpenClaws negotiate in one chat?')}",  # 🎬
        "",
        "Create a new Telegram group with these three members:",
        "",
        *members,
        "",
        "Then paste this in the new group:",
        "",
        f"    {_code(bind_payload)}",
        "",
        f"<i>Or share the code</i> {_code(code)} <i>with your investor via any other "
        "channel to stick with DM-only mode.</i>",
    ]
    return "\n".join(lines)


def format_group_bound(event: dict[str, Any]) -> str:
    """Confirmation card posted IN the group after a successful /bind.
    Tells the founder and investor the venue is set up and what happens
    next."""
    code = (event.get("session_code") or "").strip()
    counterparty = (event.get("counterparty_label") or "your investor").strip()

    code_part = f" for {code}" if code else ""
    name = (counterparty.split()[0] if counterparty else "your counterparty")

    lines = [
        f"✅ {_b('Negotiation room ready' + code_part)}",  # ✅
        "",
        f"Both OpenClaws will post their offers here so you and {_escape_html(name)} "
        "can follow the rounds live.",
        "",
        f"{_b('Signing stays private.')} If a deal is reached, each party gets their own signing link in DM.",
    ]
    return "\n".join(lines)


def format_bind_wrong_user(event: dict[str, Any]) -> str:
    """Error reply when someone other than the session founder types /bind."""
    return (
        "⛔ Only the founder of this negotiation can bind it to a group.\n\n"  # ⛔
        "If you're the investor, ask the founder to paste /bind here instead."
    )


def format_bind_wrong_chat_type(event: dict[str, Any]) -> str:
    """Error reply when /bind is typed in a DM instead of a group."""
    return (
        "ℹ️ The `/bind` command only works in a group chat.\n\n"  # ℹ️
        "Create a new Telegram group with the two bots + your investor, "
        "then paste `/bind INV-XXXXX` there."
    )


def format_bind_unknown_code(event: dict[str, Any]) -> str:
    return (
        "❓ That code doesn't match a current negotiation. "  # ❓
        "Double-check the code with your founder."
    )


def format_bind_already_bound(event: dict[str, Any]) -> str:
    return (
        "⚠️ This negotiation is already bound to another group.\n\n"  # ⚠️
        "Cancel with `/cancel_negotiation` in your DM first "
        "if you need to start over."
    )


def format_active_negotiation_block(event: dict[str, Any]) -> str:
    """P7-5+ single-active-negotiation gate. Reject a new-mint attempt
    when there's already an in-flight negotiation on this bot. The
    descriptor identifies the conflict (an INV-XXXXX session code, or
    'a running negotiation' for demo mode).

    Critical: tells the user exactly how to free the slot — `cancel`
    the existing negotiation. The trigger word matches the SKILL.md
    A.7 cancel intent rule, so just typing `cancel` works without
    further qualification.
    """
    descriptor = (event.get("descriptor") or "an active negotiation").strip()
    return (
        f"⛔ {_b('Negotiation already in progress')}\n\n"  # ⛔
        f"You already have {_b(descriptor)} open.\n\n"
        f"Reply {_code('/cancel')} to stop it before starting a new negotiation."
    )


def format_founder_resumed(event: dict[str, Any]) -> str:
    """P7-5 orienting card. Posted in the group when an OC cron tick
    (or an in-process /bind fast path) picks up a waiting negotiation
    and is about to start streaming. Never starts with '/' (invariant
    enforced in tests to prevent any future self-trigger loops).
    """
    code = (event.get("session_code") or "").strip()
    return (
        f"⚡ {_b('Starting the negotiation')}\n\n"  # ⚡
        "The founder OpenClaw will post the first offer in a moment."
    )


def format_investor_waiting_for_founder(event: dict[str, Any]) -> str:
    """Investor-side, post-join: posted to investor's DM right after
    join completes, before the live group exists. Tells the investor
    the founder side is being prepared and what's about to happen.

    Inverted-invitation design: also surfaces the founder bot handle
    (pulled from sshsign session.metadata_public) so the investor
    knows whose agent they're waiting on.
    """
    founder_bot = _clean_bot_handle(event.get("founder_bot_handle"))
    if founder_bot and not founder_bot.startswith("@"):
        founder_bot = "@" + founder_bot
    if founder_bot:
        return (
            f"✅ {_b('Joined.')} Waiting for the founder OpenClaw.\n\n"  # ✅
            f"Founder OpenClaw: {_code(founder_bot)}\n\n"
            "They're setting up a Telegram group where the negotiation "
            "offers will stream live. You'll be invited to it shortly. "
            "No action needed from you — sit tight."
        )
    return (
        f"✅ {_b('Joined.')} Waiting for the founder OpenClaw.\n\n"  # ✅
        "They're setting up a Telegram group where the negotiation "
        "offers will stream live. You'll be invited to it shortly. "
        "No action needed from you — sit tight."
    )


def format_create_group_for_founder(event: dict[str, Any]) -> str:
    """Founder-side, post-investor-join: posted to founder's DM the
    moment the cron-driven scan picks up the joined session. Tells
    the founder how to create the live group, with BOTH bot handles
    pre-filled from sshsign session metadata.

    Asymmetric: only the founder gets a "create group" instruction.
    The investor's card is "wait" (above). This prevents both parties
    from racing to create separate groups.
    """
    code = (event.get("session_code") or "").strip()
    founder_bot = _clean_bot_handle(event.get("founder_bot_handle"))
    investor_bot = _clean_bot_handle(event.get("investor_bot_handle"))
    investor_label = (event.get("investor_label") or "your investor").strip()

    if founder_bot and not founder_bot.startswith("@"):
        founder_bot = "@" + founder_bot
    if investor_bot and not investor_bot.startswith("@"):
        investor_bot = "@" + investor_bot

    if not investor_bot:
        investor_bot = "(your investor's agent — handle not yet known)"

    bind_payload = f"/bind {code}" if code else "/bind INV-XXXXX"
    investor_first = investor_label.split()[0] if investor_label else "your investor"

    lines = [
        f"✅ {_b(investor_label + ' joined')}",  # ✅
        "",
        "Now bring everyone into the live negotiation group:",
        "",
        f"1. Create a Telegram group with you and {_escape_html(investor_first)}.",
        f"2. Add Founder OpenClaw: {_code(founder_bot)}",
        f"3. Add Investor OpenClaw: {_code(investor_bot)}",
        f"4. Paste in the group: {_code(bind_payload)}",
        "",
        "Both OpenClaws will post offers there. Signing stays private.",
    ]
    return "\n".join(lines)


def group_setup_reply_markup(event: dict[str, Any]) -> dict[str, Any] | None:
    """Inline buttons for the founder's group-setup card.

    Telegram supports startgroup deep links for adding a bot to a group and
    CopyTextButton for copying short commands. Do not include the INV code in
    the startgroup link: Telegram will echo that parameter back as
    `/start@bot INV-...` in the group, which can race the explicit /bind step.
    The text card remains complete on clients/transports that ignore
    reply_markup.
    """
    code = (event.get("session_code") or "").strip()
    bind_payload = f"/bind {code}" if code else "/bind INV-XXXXX"

    def bot_url(handle: str) -> str | None:
        handle = _clean_bot_handle(handle)
        if not handle or handle.startswith("("):
            return None
        handle = handle[1:] if handle.startswith("@") else handle
        if not handle:
            return None
        return f"https://t.me/{handle}?startgroup"

    founder_url = bot_url(event.get("founder_bot_handle") or "")
    investor_url = bot_url(event.get("investor_bot_handle") or "")
    handles = " ".join(
        h for h in (
            _clean_bot_handle(event.get("founder_bot_handle")),
            _clean_bot_handle(event.get("investor_bot_handle")),
        )
        if h
    )

    keyboard: list[list[dict[str, Any]]] = []
    if founder_url:
        keyboard.append([{"text": "Add founder OpenClaw", "url": founder_url}])
    if investor_url:
        keyboard.append([{"text": "Add investor OpenClaw", "url": investor_url}])
    if handles:
        keyboard.append([
            {"text": "Copy OpenClaw handles", "copy_text": {"text": handles}},
        ])
    keyboard.append([
        {"text": "Copy bind command", "copy_text": {"text": bind_payload}},
    ])
    return {"inline_keyboard": keyboard} if keyboard else None


def format_investor_waiting_heartbeat(event: dict[str, Any]) -> str:
    """Heartbeat card at ~15s if the founder's agent hasn't yet
    signaled streaming_at. Keeps the chat from feeling dead during
    the cron window. Posted at most once per wait.
    """
    return "⏳ Still waking the founder OpenClaw…"  # ⏳


def format_turn_heartbeat(event: dict[str, Any]) -> str:
    role = (event.get("role") or "agent").strip().lower()
    label = "Founder OC" if role == "founder" else (
        "Investor OC" if role == "investor" else "OC"
    )
    return (
        f"⏳ {_b(label + ' is drafting an offer…')}\n\n"
        "One moment while it works within the authorized terms."
    )


def format_turn_still_working(event: dict[str, Any]) -> str:
    role = (event.get("role") or "agent").strip().lower()
    label = "Founder OpenClaw" if role == "founder" else (
        "Investor OpenClaw" if role == "investor" else "OpenClaw"
    )
    return (
        f"⏳ {_b('Still working')}\n\n"
        f"{_escape_html(label)} is still reviewing the offer and drafting a compliant response."
    )


def format_investor_both_online(event: dict[str, Any]) -> str:
    """Posted the moment founder_streaming_at flips non-null on the
    session row. Bridges the ~1-2s gap between "founder's agent is
    up" and the first offer card arriving from upstream.
    """
    return (
        f"✅ {_b('Both OpenClaws are live')}\n\nStarting the negotiation now."  # ✅
    )


def format_investor_wake_timeout(event: dict[str, Any]) -> str:
    """180s bounded-poll timeout. Rare in practice (cron fires every
    30s), but surfaces clearly if the founder's droplet is offline or
    the cron job failed to install. Mentions the OC-restart hint so
    the user knows what to try first.
    """
    return (
        f"⏳ {_b('Still working')}\n\n"  # ⏳
        "If you know the founder, a quick nudge to them (sending any "
        "message to their bot) will force a retry. Otherwise the cron "
        "scan will keep trying — come back in a few minutes."
    )


def format_investor_session_ended(event: dict[str, Any]) -> str:
    """Terminal status detected during the investor's bounded poll.
    Not the primary cancellation notice (the canceling party's turn
    posts the authoritative card); this just tells the investor why
    streaming never started.
    """
    status = (event.get("status") or "ended").lower()
    pretty = {
        "canceled": "canceled",
        "rescinded": "canceled after signing",
        "rescinded_after_sign": "canceled after signing",
        "completed": "completed",
        "expired": "expired",
    }.get(status, status)
    return (
        f"ℹ️ Negotiation {pretty} before streaming started."  # ℹ️
    )


FORMATTERS = {
    "confirm": format_confirm,
    "authorized": format_authorized,
    "offer": format_offer,
    "counter": format_offer,
    "accept": format_offer,
    "outcome": format_outcome,
    "signing": format_signing,
    "signed": format_signed,
    "profile": format_profile,
    "invitation": format_invitation,
    "waiting": format_waiting,
    "counterparty_joined": format_counterparty_joined,
    "apoa_blocked_counterparty_offer": format_apoa_blocked_counterparty_offer,
    "invitation_expired": format_invitation_expired,
    "session_expired": format_session_expired,
    "canceled_before_deal_initiator": format_canceled_before_deal_initiator,
    "canceled_before_deal_observer": format_canceled_before_deal_observer,
    "canceled_after_deal_initiator": format_canceled_after_deal_initiator,
    "canceled_after_deal_observer": format_canceled_after_deal_observer,
    "rescinded_after_sign_initiator": format_rescinded_after_sign_initiator,
    "rescinded_after_sign_observer": format_rescinded_after_sign_observer,
    "cancel_completed_refused": format_cancel_completed_deal_refused,
    "propose_new_terms": format_propose_new_terms,
    "go_live": format_go_live,
    "group_bound": format_group_bound,
    "bind_wrong_user": format_bind_wrong_user,
    "bind_wrong_chat_type": format_bind_wrong_chat_type,
    "bind_unknown_code": format_bind_unknown_code,
    "bind_already_bound": format_bind_already_bound,
    "active_negotiation_block": format_active_negotiation_block,
    "founder_resumed": format_founder_resumed,
    # P7-5 investor-side UX
    "investor_waiting_for_founder": format_investor_waiting_for_founder,
    "create_group_for_founder": format_create_group_for_founder,
    "investor_waiting_heartbeat": format_investor_waiting_heartbeat,
    "turn_heartbeat": format_turn_heartbeat,
    "turn_still_working": format_turn_still_working,
    "investor_both_online": format_investor_both_online,
    "investor_wake_timeout": format_investor_wake_timeout,
    "investor_session_ended": format_investor_session_ended,
}


def format_event(
    event: dict[str, Any],
    constraints: dict[str, Any] | None = None,
) -> str | None:
    """Dispatch an event to the right formatter.

    Returns the formatted message body, or None if the event type is unknown
    or a known formatter decides to skip (e.g. unknown outcome.result).
    """
    kind = event.get("type")
    formatter = FORMATTERS.get(kind or "")
    if formatter is None:
        return None
    if formatter is format_offer:
        return format_offer(event, constraints)
    if formatter is format_outcome:
        return format_outcome(event, constraints)
    return formatter(event)


def main() -> int:
    try:
        event = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Invalid JSON: {e}\n")
        return 2

    if not isinstance(event, dict):
        sys.stderr.write("Event must be a JSON object\n")
        return 2

    output = format_event(event)
    if output is None:
        kind = event.get("type", "<missing>")
        sys.stderr.write(f"Unknown event type: {kind}. Known: {sorted(FORMATTERS)}\n")
        return 2

    sys.stdout.write(output)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
