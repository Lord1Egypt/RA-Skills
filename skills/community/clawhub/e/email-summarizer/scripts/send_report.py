#!/usr/bin/env python3
"""
send_report.py — Send a pre-built report file to an email address.

Sends an HTML file as the email body, with an optional Excel attachment.
Completely decoupled from report generation.

Usage:
  export EMAIL_USER=you@163.com
  export EMAIL_PASS=your-app-password

  # Send HTML + Excel attachment
  python3 send_report.py --html report.html --xlsx report.xlsx --to friend@example.com

  # Send only HTML body (no attachment)
  python3 send_report.py --html report.html --to friend@example.com

  # Omit --to to send to yourself (EMAIL_USER)
  python3 send_report.py --html report.html --xlsx report.xlsx

  # Custom subject
  python3 send_report.py --html report.html --subject "Weekly Contact Report"

Supported --preset values:
  163 (default) | qq | exmail | gmail | outlook

Environment variables:
  EMAIL_USER   Sender address (also the SMTP login)
  EMAIL_PASS   App password / authorization code
"""

import argparse, os, smtplib, sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.base      import MIMEBase
from email                import encoders

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _render import SMTP_MAP


def main():
    parser = argparse.ArgumentParser(
        description="Send a pre-built HTML report (+ optional xlsx) via SMTP.")
    parser.add_argument("--html",    required=True,
                        help="Path to the HTML report file (used as email body)")
    parser.add_argument("--xlsx",    default="",
                        help="Path to an Excel file to attach (optional)")
    parser.add_argument("--to",      default="",
                        help="Recipient address (default: EMAIL_USER)")
    parser.add_argument("--subject", default="",
                        help="Email subject (auto-generated from filename if omitted)")
    parser.add_argument("--preset",  default="163",
                        choices=list(SMTP_MAP.keys()),
                        help="SMTP preset (default: 163)")
    args = parser.parse_args()

    # ── Credentials ───────────────────────────────────────────────────────────
    email_user = os.environ.get("EMAIL_USER", "")
    email_pass = os.environ.get("EMAIL_PASS", "")
    if not email_user or not email_pass:
        print("ERROR: Set EMAIL_USER and EMAIL_PASS environment variables.", file=sys.stderr)
        sys.exit(1)

    recipient = args.to or email_user

    # ── Load HTML ─────────────────────────────────────────────────────────────
    if not os.path.isfile(args.html):
        print(f"ERROR: HTML file not found: {args.html}", file=sys.stderr)
        sys.exit(1)
    with open(args.html, "r", encoding="utf-8") as f:
        html_content = f.read()

    # ── Subject ───────────────────────────────────────────────────────────────
    subject = args.subject
    if not subject:
        base = os.path.splitext(os.path.basename(args.html))[0]
        now  = datetime.now().strftime("%Y-%m-%d")
        subject = f"Contact Profile Report — {base} ({now})"

    # ── Compose ───────────────────────────────────────────────────────────────
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"]    = email_user
    msg["To"]      = recipient

    body_part = MIMEMultipart("alternative")
    body_part.attach(MIMEText(html_content, "html", "utf-8"))
    msg.attach(body_part)

    if args.xlsx:
        if not os.path.isfile(args.xlsx):
            print(f"ERROR: Excel file not found: {args.xlsx}", file=sys.stderr)
            sys.exit(1)
        with open(args.xlsx, "rb") as f:
            xlsx_data = f.read()
        att = MIMEBase("application",
                       "vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        att.set_payload(xlsx_data)
        encoders.encode_base64(att)
        att.add_header("Content-Disposition", "attachment",
                       filename=os.path.basename(args.xlsx))
        msg.attach(att)
        print(f"[send] Attaching {os.path.basename(args.xlsx)}", file=sys.stderr)

    # ── Send ──────────────────────────────────────────────────────────────────
    host, port = SMTP_MAP.get(args.preset, ("smtp.163.com", 465))
    print(f"[send] Connecting to {host}:{port}…", file=sys.stderr)

    try:
        if port == 587:
            with smtplib.SMTP(host, port) as s:
                s.starttls()
                s.login(email_user, email_pass)
                s.sendmail(email_user, recipient, msg.as_bytes())
        else:
            with smtplib.SMTP_SSL(host, port) as s:
                s.login(email_user, email_pass)
                s.sendmail(email_user, recipient, msg.as_bytes())
    except smtplib.SMTPAuthenticationError:
        print("ERROR: SMTP authentication failed. "
              "Check EMAIL_USER / EMAIL_PASS and ensure SMTP is enabled.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    has_xlsx = f" + {os.path.basename(args.xlsx)}" if args.xlsx else ""
    print(f"[send] ✅ Sent to {recipient}  ({os.path.basename(args.html)}{has_xlsx})",
          file=sys.stderr)


if __name__ == "__main__":
    main()
