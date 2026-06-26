#!/usr/bin/env python3
"""
handlers.py — support skill handlers for fintech-support-agent

Usage:
  python3 handlers.py transfer_status --customer-id <id> [--ref <ref>]
  python3 handlers.py refund           --customer-id <id> --ref <ref>
  python3 handlers.py account_status  --customer-id <id>
  python3 handlers.py kyc_requirements --customer-id <id>
  python3 handlers.py escalate        --customer-id <id> --summary "<text>"
  python3 handlers.py weekly_digest

All handlers print structured plain-text output for the agent to read.
They never print raw JSON — the agent gets human-readable summaries.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Config from environment
# ---------------------------------------------------------------------------

API_BASE = os.environ.get("TRANSFER_API_BASE_URL", "").rstrip("/")
API_KEY = os.environ.get("TRANSFER_API_KEY", "")
ESCALATION_WEBHOOK = os.environ.get("ESCALATION_WEBHOOK_URL", "")
SUPPORT_EMAIL = os.environ.get("SUPPORT_EMAIL", "")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

# ---------------------------------------------------------------------------
# Memory helpers — lightweight JSON store in ~/.openclaw/memory/support/
# ---------------------------------------------------------------------------

MEMORY_DIR = Path.home() / ".openclaw" / "memory" / "support"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def load_customer_memory(customer_id: str) -> dict:
    path = MEMORY_DIR / f"{customer_id}.json"
    if path.exists():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_customer_memory(customer_id: str, data: dict) -> None:
    path = MEMORY_DIR / f"{customer_id}.json"
    existing = load_customer_memory(customer_id)
    existing.update(data)
    path.write_text(json.dumps(existing, indent=2))


def load_ticket_log() -> list:
    path = MEMORY_DIR / "ticket_log.json"
    if path.exists():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            return []
    return []


def append_ticket(entry: dict) -> None:
    log = load_ticket_log()
    log.append(entry)
    path = MEMORY_DIR / "ticket_log.json"
    path.write_text(json.dumps(log, indent=2))


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def api_get(path: str) -> dict | None:
    if not API_BASE or not API_KEY:
        return None
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        print(f"[API ERROR] GET {path}: {exc}", file=sys.stderr)
        return None


def api_post(path: str, payload: dict) -> dict | None:
    if not API_BASE or not API_KEY:
        return None
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers=HEADERS,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        print(f"[API ERROR] POST {path}: {exc}", file=sys.stderr)
        return None


def post_webhook(payload: dict) -> bool:
    if not ESCALATION_WEBHOOK:
        return False
    req = urllib.request.Request(
        ESCALATION_WEBHOOK,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.status < 300
    except urllib.error.URLError:
        return False


# ---------------------------------------------------------------------------
# Handler: transfer_status
# ---------------------------------------------------------------------------

def handle_transfer_status(customer_id: str, ref: str | None) -> None:
    """
    Look up a transfer and return a plain-language status summary.
    """
    if ref:
        data = api_get(f"/transfers/{ref}")
    elif customer_id:
        data = api_get(f"/customers/{customer_id}/transfers/latest")
    else:
        print("STATUS: MISSING_INFO")
        print("AGENT_NOTE: Need either a transaction reference or customer ID to look up the transfer.")
        return

    if data is None:
        print("STATUS: API_UNAVAILABLE")
        print("AGENT_NOTE: Could not reach the transfer API. Escalate to human.")
        return

    status = data.get("status", "UNKNOWN").upper()
    amount = data.get("amount")
    currency = data.get("currency", "")
    recipient = data.get("recipient_name", "the recipient")
    created_at = data.get("created_at", "")
    estimated_arrival = data.get("estimated_arrival", "")
    transfer_ref = data.get("reference", ref or "N/A")

    # Calculate age if created_at is provided
    age_hours = None
    if created_at:
        try:
            created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            age_hours = (datetime.now(timezone.utc) - created).total_seconds() / 3600
        except ValueError:
            pass

    print(f"TRANSFER_REF: {transfer_ref}")
    print(f"STATUS: {status}")

    if amount and currency:
        print(f"AMOUNT: {amount} {currency}")

    print(f"RECIPIENT: {recipient}")

    if estimated_arrival:
        print(f"ESTIMATED_ARRIVAL: {estimated_arrival}")

    if status == "COMPLETED":
        print("RESOLUTION: DELIVERED — funds have arrived with recipient.")

    elif status == "PENDING":
        if age_hours and age_hours > 24:
            print(f"DELAY_FLAG: Transfer has been pending for {age_hours:.0f} hours — exceeds normal processing time.")
            print("AGENT_NOTE: Recommend escalating to ops team for investigation.")
        else:
            print("RESOLUTION: IN_PROGRESS — transfer is being processed normally.")

    elif status == "FAILED":
        failure_reason = data.get("failure_reason", "No reason provided by the network.")
        print(f"FAILURE_REASON: {failure_reason}")
        print("AGENT_NOTE: Advise customer that funds will be returned within 3-5 business days.")

    elif status == "REFUNDED":
        print("RESOLUTION: Funds have been returned to the sender's account.")

    else:
        print("AGENT_NOTE: Status is non-standard. Check with ops team.")

    # Log to memory
    if customer_id:
        save_customer_memory(customer_id, {
            "last_transfer_ref": transfer_ref,
            "last_transfer_status": status,
            "last_checked": datetime.now(timezone.utc).isoformat(),
        })

    append_ticket({
        "type": "TRANSFER_STATUS",
        "customer_id": customer_id,
        "ref": transfer_ref,
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "resolved": status in ("COMPLETED", "REFUNDED"),
    })


# ---------------------------------------------------------------------------
# Handler: refund
# ---------------------------------------------------------------------------

def handle_refund(customer_id: str, ref: str) -> None:
    """
    Attempt a refund or recall, return outcome in plain language.
    """
    data = api_get(f"/transfers/{ref}")

    if data is None:
        print("STATUS: API_UNAVAILABLE")
        print("AGENT_NOTE: Could not reach the transfer API. Escalate to human.")
        return

    status = data.get("status", "UNKNOWN").upper()
    amount = data.get("amount")
    currency = data.get("currency", "")

    print(f"TRANSFER_REF: {ref}")
    print(f"CURRENT_STATUS: {status}")

    if status == "PENDING":
        # Attempt recall
        result = api_post(f"/transfers/{ref}/recall", {"reason": "customer_request"})
        if result and result.get("recalled"):
            print("OUTCOME: RECALL_SUCCESS")
            print("RESOLUTION: Transfer has been cancelled. Funds will return within 1-2 business days.")
        else:
            print("OUTCOME: RECALL_FAILED")
            print("AGENT_NOTE: Transfer could not be recalled — it may have already been picked up. Escalate.")

    elif status == "COMPLETED":
        # Log a dispute — we cannot directly refund delivered funds
        dispute = api_post(f"/transfers/{ref}/dispute", {
            "customer_id": customer_id,
            "reason": "customer_request",
        })
        dispute_ref = dispute.get("dispute_ref", "N/A") if dispute else "N/A"
        print("OUTCOME: DISPUTE_LOGGED")
        print(f"DISPUTE_REF: {dispute_ref}")
        print(
            "RESOLUTION: The transfer has already been delivered. A dispute has been "
            "logged with the receiving network. This process typically takes 5-10 business "
            "days and cannot be guaranteed — it depends on the recipient's provider."
        )

    elif status == "FAILED":
        print("OUTCOME: ALREADY_REFUNDED_OR_FAILED")
        print("RESOLUTION: This transfer failed and the funds are being returned automatically within 3-5 business days.")

    elif status == "REFUNDED":
        print("OUTCOME: ALREADY_REFUNDED")
        print("RESOLUTION: This transfer has already been refunded.")

    else:
        print(f"OUTCOME: UNKNOWN_STATUS ({status})")
        print("AGENT_NOTE: Cannot process refund — status is unrecognised. Escalate.")

    append_ticket({
        "type": "REFUND_REQUEST",
        "customer_id": customer_id,
        "ref": ref,
        "transfer_status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "resolved": status in ("FAILED", "REFUNDED"),
    })


# ---------------------------------------------------------------------------
# Handler: account_status
# ---------------------------------------------------------------------------

def handle_account_status(customer_id: str) -> None:
    """
    Check account status and return plain-language explanation.
    """
    data = api_get(f"/customers/{customer_id}/status")

    if data is None:
        print("STATUS: API_UNAVAILABLE")
        print("AGENT_NOTE: Could not reach the account API. Escalate to human.")
        return

    account_status = data.get("status", "UNKNOWN").upper()
    suspension_reason = data.get("suspension_reason", "").upper()
    kyc_pending = data.get("kyc_pending", False)
    restriction_detail = data.get("restriction_detail", "")

    print(f"ACCOUNT_STATUS: {account_status}")

    if account_status == "ACTIVE":
        print("RESOLUTION: Account is active and unrestricted. No issues found.")

    elif account_status in ("SUSPENDED", "RESTRICTED", "BLOCKED"):

        if suspension_reason in ("KYC_REQUIRED", "DOCUMENT_EXPIRED", "VERIFICATION_NEEDED") or kyc_pending:
            print("SUSPENSION_REASON: IDENTITY_VERIFICATION_REQUIRED")
            print("AGENT_NOTE: Switch to KYC_GUIDANCE flow — account will be reinstated once documents are verified.")

        elif suspension_reason in ("FRAUD", "AML", "COMPLIANCE", "RISK"):
            print("SUSPENSION_REASON: SECURITY_REVIEW")
            print(
                "RESOLUTION: Account is under a security review by the compliance team. "
                "Do not reveal the specific fraud signal. Tell the customer: "
                "'Your account has been flagged for a security review. "
                "Our compliance team will contact you within 48 hours with next steps.'"
            )
            print("AGENT_NOTE: Do not attempt to unblock. Route to compliance team only.")

        else:
            print(f"SUSPENSION_REASON: {suspension_reason or 'NOT_SPECIFIED'}")
            if restriction_detail:
                print(f"DETAIL: {restriction_detail}")
            print("AGENT_NOTE: Reason not classified. Escalate for manual review.")

    elif account_status == "CLOSED":
        print("RESOLUTION: This account has been permanently closed.")

    else:
        print(f"ACCOUNT_STATUS: {account_status}")
        print("AGENT_NOTE: Unrecognised status — escalate.")

    append_ticket({
        "type": "ACCOUNT_ISSUE",
        "customer_id": customer_id,
        "account_status": account_status,
        "suspension_reason": suspension_reason,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "resolved": account_status == "ACTIVE",
    })


# ---------------------------------------------------------------------------
# Handler: kyc_requirements
# ---------------------------------------------------------------------------

def handle_kyc_requirements(customer_id: str) -> None:
    """
    Return the specific documents this customer still needs to submit.
    """
    data = api_get(f"/customers/{customer_id}/kyc")

    if data is None:
        print("STATUS: API_UNAVAILABLE")
        print("AGENT_NOTE: Could not reach the KYC API. Provide generic guidance and escalate.")
        print("\nGENERIC_GUIDANCE:")
        print("  - Government-issued photo ID (passport, national ID, or driving licence)")
        print("  - Proof of address (utility bill or bank statement, dated within 3 months)")
        print("  - Selfie holding the ID document")
        print("  - File formats: PDF or JPEG, under 5MB each")
        return

    pending_docs = data.get("pending_documents", [])
    upload_url = data.get("upload_url", "")
    deadline = data.get("deadline", "")
    kyc_level = data.get("required_level", "")

    print(f"KYC_LEVEL_REQUIRED: {kyc_level or 'Standard'}")

    if not pending_docs:
        print("STATUS: KYC_COMPLETE — all documents have been received and verified.")
        return

    print(f"PENDING_DOCUMENTS ({len(pending_docs)} remaining):")
    for doc in pending_docs:
        doc_type = doc.get("type", "Unknown document")
        instructions = doc.get("instructions", "")
        print(f"  - {doc_type}")
        if instructions:
            print(f"    Instructions: {instructions}")

    print("\nFILE_REQUIREMENTS:")
    print("  - Format: PDF or JPEG (no Word docs, no screenshots of screenshots)")
    print("  - Size: Under 5MB per file")
    print("  - Quality: All text must be clearly readable")

    if upload_url:
        print(f"\nUPLOAD_URL: {upload_url}")
    else:
        print("\nUPLOAD_URL: Direct the customer to the Verify section in the app.")

    if deadline:
        print(f"\nDEADLINE: {deadline}")
        print("AGENT_NOTE: Mention the deadline clearly. Set a 24h follow-up cron.")

    print("\nFOLLOW_UP_CRON:")
    tomorrow = (datetime.now(timezone.utc) + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M UTC")
    print(f"  Schedule check at {tomorrow}: run account_status for {customer_id}")
    print("  If documents still not received: send proactive reminder to customer.")

    append_ticket({
        "type": "KYC_GUIDANCE",
        "customer_id": customer_id,
        "pending_docs": len(pending_docs),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "resolved": False,
    })


# ---------------------------------------------------------------------------
# Handler: escalate
# ---------------------------------------------------------------------------

def handle_escalate(customer_id: str, summary: str) -> None:
    """
    Create an escalation ticket, post to webhook, return case reference.
    """
    import hashlib
    import time

    case_ref = "ESC-" + hashlib.md5(
        f"{customer_id}{time.time()}".encode()
    ).hexdigest()[:8].upper()

    memory = load_customer_memory(customer_id)
    prior_issues = memory.get("ticket_history", [])

    payload = {
        "case_ref": case_ref,
        "customer_id": customer_id,
        "summary": summary,
        "prior_issues": prior_issues,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "priority": "HIGH" if any(
            word in summary.lower() for word in ["urgent", "large", "fraud", "scam", "all my money"]
        ) else "NORMAL",
        "source": "openclaw-fintech-support-agent",
    }

    webhook_sent = post_webhook(payload)

    print(f"CASE_REF: {case_ref}")
    print(f"PRIORITY: {payload['priority']}")
    print(f"WEBHOOK_SENT: {webhook_sent}")

    if webhook_sent:
        print("STATUS: ESCALATED — human agent has been notified.")
        print("EXPECTED_RESPONSE: 4 hours for NORMAL priority, 1 hour for HIGH priority.")
    else:
        print("STATUS: ESCALATION_WEBHOOK_FAILED")
        print(f"AGENT_NOTE: Post manually to {SUPPORT_EMAIL} with case ref {case_ref}.")

    # Tell the agent what to say to the customer
    print(f"\nCUSTOMER_MESSAGE:")
    print(
        f"I've flagged this for our senior support team. Someone will follow up with you "
        f"within {'1 hour' if payload['priority'] == 'HIGH' else '4 hours'}. "
        f"Your case reference is {case_ref}."
    )

    save_customer_memory(customer_id, {
        "last_escalation_ref": case_ref,
        "last_escalation_time": datetime.now(timezone.utc).isoformat(),
    })

    append_ticket({
        "type": "ESCALATION",
        "customer_id": customer_id,
        "case_ref": case_ref,
        "priority": payload["priority"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "resolved": False,
    })


# ---------------------------------------------------------------------------
# Handler: weekly_digest
# ---------------------------------------------------------------------------

def handle_weekly_digest() -> None:
    """
    Generate a plain-text weekly ops digest from the ticket log.
    """
    log = load_ticket_log()

    if not log:
        print("WEEKLY_DIGEST: No tickets recorded this week.")
        return

    # Filter to past 7 days
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    week_tickets = []
    for ticket in log:
        try:
            ts = datetime.fromisoformat(ticket["timestamp"].replace("Z", "+00:00"))
            if ts >= week_ago:
                week_tickets.append(ticket)
        except (KeyError, ValueError):
            continue

    total = len(week_tickets)
    if total == 0:
        print("WEEKLY_DIGEST: No tickets in the past 7 days.")
        return

    resolved = sum(1 for t in week_tickets if t.get("resolved", False))
    escalated = sum(1 for t in week_tickets if t.get("type") == "ESCALATION")

    type_counts: dict[str, int] = {}
    for t in week_tickets:
        ttype = t.get("type", "UNKNOWN")
        type_counts[ttype] = type_counts.get(ttype, 0) + 1

    top_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:3]

    # Find tickets open > 48h
    stale_cutoff = datetime.now(timezone.utc) - timedelta(hours=48)
    stale = []
    for t in week_tickets:
        if not t.get("resolved", False):
            try:
                ts = datetime.fromisoformat(t["timestamp"].replace("Z", "+00:00"))
                if ts < stale_cutoff:
                    stale.append(t)
            except (KeyError, ValueError):
                continue

    auto_resolution_rate = (resolved / total * 100) if total > 0 else 0
    escalation_rate = (escalated / total * 100) if total > 0 else 0

    week_start = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%d %b")
    week_end = datetime.now(timezone.utc).strftime("%d %b %Y")

    print(f"# Weekly support digest — {week_start} to {week_end}")
    print()
    print(f"Total tickets:          {total}")
    print(f"Auto-resolved:          {resolved} ({auto_resolution_rate:.0f}%)")
    print(f"Escalated to human:     {escalated} ({escalation_rate:.0f}%)")
    print()
    print("Top issue types:")
    for issue_type, count in top_types:
        print(f"  {issue_type:<25} {count} tickets")
    print()
    if stale:
        print(f"Open > 48h:             {len(stale)} tickets need attention")
        for t in stale[:5]:
            ts = t.get("timestamp", "")[:10]
            print(f"  - {t.get('type','?')} | customer {t.get('customer_id','?')} | opened {ts}")
    else:
        print("Open > 48h:             None — all tickets resolved or recently escalated.")

    print()
    print(f"SEND_TO: {SUPPORT_EMAIL}")


# ---------------------------------------------------------------------------
# CLI dispatch
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="fintech-support-agent handlers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("command", choices=[
        "transfer_status", "refund", "account_status",
        "kyc_requirements", "escalate", "weekly_digest",
    ])
    parser.add_argument("--customer-id", default="")
    parser.add_argument("--ref", default="")
    parser.add_argument("--summary", default="")

    args = parser.parse_args()

    if args.command == "transfer_status":
        handle_transfer_status(args.customer_id, args.ref or None)

    elif args.command == "refund":
        if not args.ref:
            print("ERROR: --ref is required for refund handler", file=sys.stderr)
            sys.exit(1)
        handle_refund(args.customer_id, args.ref)

    elif args.command == "account_status":
        handle_account_status(args.customer_id)

    elif args.command == "kyc_requirements":
        handle_kyc_requirements(args.customer_id)

    elif args.command == "escalate":
        if not args.summary:
            print("ERROR: --summary is required for escalate handler", file=sys.stderr)
            sys.exit(1)
        handle_escalate(args.customer_id, args.summary)

    elif args.command == "weekly_digest":
        handle_weekly_digest()


if __name__ == "__main__":
    main()
