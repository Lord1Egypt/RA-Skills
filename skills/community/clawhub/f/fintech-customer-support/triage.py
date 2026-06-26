#!/usr/bin/env python3
"""
triage.py — intent classifier for fintech-support-agent
Usage: python3 triage.py "<customer message>"
Prints a single intent label to stdout.
"""

import sys
import os
import json
import urllib.request
import urllib.error

INTENT_LABELS = [
    "TRANSFER_STATUS",
    "REFUND_REQUEST",
    "ACCOUNT_ISSUE",
    "KYC_GUIDANCE",
    "COMPLAINT",
    "UNKNOWN",
]

SYSTEM_PROMPT = """You are an intent classifier for a fintech customer support agent.

Given a customer message, return ONLY one of these exact labels — nothing else:
- TRANSFER_STATUS: customer asking about where their money is, transfer delay, payment status
- REFUND_REQUEST: customer wants money back, sent to wrong person, wants to cancel
- ACCOUNT_ISSUE: account suspended, blocked, restricted, can't log in, can't send
- KYC_GUIDANCE: identity verification, document upload, ID check, verification pending
- COMPLAINT: general frustration, escalation request, threatening to leave, unresolved problem
- UNKNOWN: message is unclear or does not match any category

Reply with only the label. No explanation. No punctuation. Just the label."""


def classify(message: str) -> str:
    api_key = os.environ.get("LLM_API_KEY", "")
    if not api_key:
        # Fallback: simple keyword matching when no LLM key is available
        return keyword_fallback(message)

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
        "max_tokens": 10,
        "temperature": 0,
    }

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
            label = data["choices"][0]["message"]["content"].strip().upper()
            if label in INTENT_LABELS:
                return label
            return "UNKNOWN"
    except (urllib.error.URLError, KeyError, json.JSONDecodeError):
        return keyword_fallback(message)


def keyword_fallback(message: str) -> str:
    """
    Simple keyword-based fallback when the LLM call fails or no key is set.
    Not a substitute for the LLM — use for testing only.
    """
    msg = message.lower()

    transfer_keywords = [
        "transfer", "sent", "money", "payment", "arrived", "received",
        "where is", "status", "pending", "delayed", "stuck", "not received",
        "transaction", "remittance", "sending", "not there", "not showing",
    ]
    refund_keywords = [
        "refund", "money back", "wrong person", "wrong account", "mistake",
        "cancel", "reverse", "sent by mistake", "wrong number",
    ]
    account_keywords = [
        "suspended", "blocked", "locked", "banned", "account", "can't send",
        "cannot send", "restricted", "frozen", "deactivated", "closed",
    ]
    kyc_keywords = [
        "verify", "verification", "kyc", "document", "id", "passport",
        "proof", "upload", "identity", "selfie", "photo id",
    ]
    complaint_keywords = [
        "complaint", "unhappy", "angry", "disgusting", "worst", "terrible",
        "fraud", "scam", "stolen", "refund denied", "no response", "escalate",
        "manager", "legal", "report", "never using", "leaving",
    ]

    scores = {
        "TRANSFER_STATUS": sum(1 for k in transfer_keywords if k in msg),
        "REFUND_REQUEST": sum(1 for k in refund_keywords if k in msg),
        "ACCOUNT_ISSUE": sum(1 for k in account_keywords if k in msg),
        "KYC_GUIDANCE": sum(1 for k in kyc_keywords if k in msg),
        "COMPLAINT": sum(1 for k in complaint_keywords if k in msg),
    }

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "UNKNOWN"
    return best


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 triage.py '<customer message>'", file=sys.stderr)
        sys.exit(1)

    message = " ".join(sys.argv[1:])
    print(classify(message))
