#!/usr/bin/env python3
"""
registration-scanner IMAP helper
Connects to an IMAP server, searches for registration-related emails,
and writes results to a JSON file.

Usage:
  python3 imap_scan.py \
    --host imap.mail.me.com \
    --port 993 \
    --user user@icloud.com \
    --password "app-specific-password" \
    --output /tmp/registration_scan_results.json

For Proton Mail Bridge (no SSL, local):
  python3 imap_scan.py \
    --host 127.0.0.1 \
    --port 1143 \
    --no-ssl \
    --user user@proton.me \
    --password "bridge-password" \
    --output /tmp/registration_scan_results.json
"""

import imaplib
import email
import json
import argparse
import ssl
import time
import sys
from email.header import decode_header
from datetime import datetime


SEARCH_SUBJECTS = [
    # English
    "welcome", "account created", "confirm your email", "verify your email",
    "verify your account", "activate your account", "successfully registered",
    "thanks for signing up", "thank you for registering", "you have subscribed",
    "subscription confirmed", "your account is ready", "complete your registration",
    # German
    "willkommen", "konto erstellt", "e-mail bestätigen", "registrierung bestätigen",
    "erfolgreich registriert", "anmeldung bestätigt", "danke für deine registrierung",
    "herzlich willkommen",
    # French
    "bienvenue", "compte créé", "confirmez votre adresse", "vérifiez votre e-mail",
    "activez votre compte", "inscription confirmée", "merci de votre inscription",
    # Spanish
    "bienvenido", "bienvenida", "cuenta creada", "confirma tu correo",
    "registro exitoso", "gracias por registrarte",
    # Italian
    "benvenuto", "benvenuta", "account creato", "conferma la tua email",
    "registrazione completata",
    # Portuguese
    "bem-vindo", "bem-vinda", "conta criada", "confirme o seu email",
    "registro confirmado",
    # Dutch
    "welkom", "account aangemaakt", "bevestig je e-mailadres",
    "registratie bevestigd",
    # Polish
    "witamy", "rejestracja potwierdzona",
    # Turkish
    "hoş geldiniz", "kayıt onaylandı",
]

SENDER_PATTERNS = ["noreply", "no-reply", "donotreply", "do-not-reply"]

EXCLUDE_SUBJECTS = [
    "password reset", "forgot password", "passwort vergessen",
    "invoice", "rechnung", "receipt", "order confirmation",
    "shipment", "delivery", "unsubscribe",
]


def decode_str(value):
    """Decode email header value to plain string."""
    if not value:
        return ""
    parts = decode_header(value)
    result = []
    for part, charset in parts:
        if isinstance(part, bytes):
            try:
                result.append(part.decode(charset or "utf-8", errors="replace"))
            except Exception:
                result.append(part.decode("latin-1", errors="replace"))
        else:
            result.append(part)
    return " ".join(result)


def extract_service_name(from_addr, subject):
    """Best-effort extraction of service name from sender or subject."""
    # Try sender domain first
    if "<" in from_addr:
        addr = from_addr.split("<")[1].rstrip(">").strip()
    else:
        addr = from_addr.strip()

    if "@" in addr:
        domain = addr.split("@")[1].lower()
        # Strip common prefixes
        parts = domain.split(".")
        if len(parts) >= 2:
            name = parts[-2]  # e.g. "spotify" from "mail.spotify.com"
            if name not in ("gmail", "yahoo", "hotmail", "outlook", "icloud",
                            "googlemail", "aol", "gmx", "web", "t-online"):
                return name.capitalize()

    # Fallback: try to parse from subject
    for skip in ["Re:", "Fwd:", "FW:", "[", "]"]:
        subject = subject.replace(skip, "").strip()
    return subject[:40] if subject else "Unknown"


def should_exclude(subject_lower):
    return any(excl in subject_lower for excl in EXCLUDE_SUBJECTS)


def connect_imap(host, port, user, password, use_ssl):
    """Connect and authenticate to IMAP server."""
    if use_ssl:
        context = ssl.create_default_context()
        imap = imaplib.IMAP4_SSL(host, port, ssl_context=context)
    else:
        imap = imaplib.IMAP4(host, port)
    imap.login(user, password)
    return imap


def search_imap(imap, query_bytes):
    """Run IMAP SEARCH and return list of message IDs."""
    try:
        status, data = imap.search(None, query_bytes)
        if status != "OK" or not data or not data[0]:
            return []
        return data[0].split()
    except Exception:
        return []


def fetch_email_headers(imap, msg_id):
    """Fetch From, Date, Subject headers for a message ID."""
    try:
        status, data = imap.fetch(msg_id, "(BODY.PEEK[HEADER.FIELDS (FROM DATE SUBJECT)])")
        if status != "OK" or not data or not data[0]:
            return None
        raw = data[0][1] if isinstance(data[0], tuple) else data[0]
        msg = email.message_from_bytes(raw)
        return {
            "from": decode_str(msg.get("From", "")),
            "date": decode_str(msg.get("Date", "")),
            "subject": decode_str(msg.get("Subject", "")),
        }
    except Exception:
        return None


def parse_date(date_str):
    """Parse email date string to ISO format, best effort."""
    from email.utils import parsedate_to_datetime
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return date_str[:10] if date_str else "Unknown"


def main():
    parser = argparse.ArgumentParser(description="IMAP Registration Scanner")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=993)
    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--no-ssl", action="store_true")
    args = parser.parse_args()

    use_ssl = not args.no_ssl
    print(f"[scanner] Connecting to {args.host}:{args.port} ({'SSL' if use_ssl else 'plain'})...")

    try:
        imap = connect_imap(args.host, args.port, args.user, args.password, use_ssl)
    except Exception as e:
        print(f"[scanner] ERROR: Could not connect – {e}", file=sys.stderr)
        sys.exit(1)

    imap.select("INBOX", readonly=True)
    print("[scanner] Connected. Starting search...")

    seen_ids = set()
    results = []

    # Search by subject keywords
    for term in SEARCH_SUBJECTS:
        query = f'SUBJECT "{term}"'.encode()
        msg_ids = search_imap(imap, query)
        for mid in msg_ids:
            if mid not in seen_ids:
                seen_ids.add(mid)
        time.sleep(0.3)

    # Search by sender patterns
    for pattern in SENDER_PATTERNS:
        query = f'FROM "{pattern}"'.encode()
        msg_ids = search_imap(imap, query)
        for mid in msg_ids:
            if mid not in seen_ids:
                seen_ids.add(mid)
        time.sleep(0.3)

    print(f"[scanner] Found {len(seen_ids)} candidate emails. Fetching headers...")

    # Fetch headers for all candidates
    service_map = {}  # service_name -> earliest entry

    for i, mid in enumerate(seen_ids):
        headers = fetch_email_headers(imap, mid)
        if not headers:
            continue

        subject = headers["subject"]
        subject_lower = subject.lower()

        if should_exclude(subject_lower):
            continue

        service = extract_service_name(headers["from"], subject)
        date_str = parse_date(headers["date"])

        entry = {
            "service": service,
            "date": date_str,
            "from": headers["from"],
            "subject": subject,
        }

        # Keep only oldest entry per service
        if service not in service_map:
            service_map[service] = entry
        else:
            if date_str < service_map[service]["date"]:
                service_map[service] = entry

        if i % 50 == 0 and i > 0:
            print(f"[scanner] Processed {i}/{len(seen_ids)} emails...")
        time.sleep(0.05)

    imap.logout()

    final = sorted(service_map.values(), key=lambda x: x["date"], reverse=True)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)

    print(f"[scanner] Done. {len(final)} unique services found → {args.output}")


if __name__ == "__main__":
    main()
