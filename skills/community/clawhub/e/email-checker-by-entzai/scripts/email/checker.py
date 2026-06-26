#!/usr/bin/env python3
"""
Email Checker - Checks unread emails in Inbox and sends report.
Uses AppleScript for reliable detection of unread status.

CHANGELOG:
  v3 (portability update):
  - All hardcoded values moved to config/settings.json
  - call_lm_studio() renamed to call_llm() (provider-agnostic)
  - LLM can be disabled via settings.json ("provider": "none")
  - get_unread_emails.scpt now receives account_id as CLI arg
  - Run setup.sh to create settings.json

  v2 (LM Studio update):
  - Replaced Ollama API with LM Studio / vLLM OpenAI-compatible API
  - call_ollama() renamed to call_lm_studio() and rewritten for
    OpenAI /v1/chat/completions format
  - Increased thread history from 5 → 10 messages
  - Increased per-message content capture from 800 → 2000 chars

  v1 (original rewrite):
  - Added get_thread_history() : fetches previous messages in the same
    thread from Mail.app via AppleScript
  - Replaced generate_contextual_draft() : now builds a structured prompt
    and sends it to the LLM
"""

import subprocess
import urllib.request      # stdlib — no pip needed to call the REST API
import urllib.error
from datetime import datetime
from pathlib import Path
import json
import re

SCRIPT_DIR    = Path(__file__).parent.resolve()
WORKSPACE_DIR = SCRIPT_DIR.parent.parent
LOG_DIR       = WORKSPACE_DIR / "logs"
TEMP_DIR      = WORKSPACE_DIR / "temp"

LOG_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE    = LOG_DIR  / "email_check.log"
EMAILS_FILE = TEMP_DIR / "recent_emails.json"

# ─────────────────────────────────────────────────────────────────────────────
# Config loading — all values come from config/settings.json.
# Run setup.sh to create it.
# ─────────────────────────────────────────────────────────────────────────────
CONFIG_FILE = WORKSPACE_DIR / "config" / "settings.json"


def load_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Config not found at {CONFIG_FILE}. Run setup.sh first."
        )
    return json.loads(CONFIG_FILE.read_text())


CONFIG = load_config()

LLM_BASE_URL     = CONFIG["llm"]["base_url"]
LLM_API_KEY      = CONFIG["llm"]["api_key"]
LLM_MODEL        = CONFIG["llm"]["model"]
LLM_MAX_TOKENS   = CONFIG["llm"]["max_tokens"]
LLM_TIMEOUT      = CONFIG["llm"]["timeout"]
LLM_ENABLED      = CONFIG["llm"].get("provider", "") != "none"
MAIL_ACCOUNT_ID  = CONFIG["mail"]["account_id"]
REPORT_RECIPIENT = CONFIG["user"]["report_email"]
TRUSTED_SENDERS  = CONFIG["user"]["trusted_senders"]
USER_NAME        = CONFIG["user"]["name"]
BOT_NAME         = CONFIG["user"]["bot_name"]


def log(message):
    """Write to log file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


# ─────────────────────────────────────────────────────────────────────────────
# get_unread_emails
# ─────────────────────────────────────────────────────────────────────────────
def get_unread_emails():
    """Get unread emails from Inbox using AppleScript (includes content)."""
    script_path = SCRIPT_DIR / "get_unread_emails.scpt"

    result = subprocess.run(
        ['osascript', str(script_path), MAIL_ACCOUNT_ID],
        capture_output=True, text=True
    )
    output = result.stdout.strip()

    if 'NO_UNREAD_EMAILS' in output or not output:
        log("No unread messages found in inbox")
        return []

    # Parse AppleScript output: sender|subject|||content (blocks split by |||)
    emails = []
    for block in output.split('|||'):
        if '|' in block:
            parts   = block.split('|', 2)
            sender  = parts[0].strip()
            subject = parts[1].strip() if len(parts) > 1 else "No Subject"
            content = parts[2].strip() if len(parts) > 2 else ""
            emails.append({
                'sender':  sender,
                'subject': subject,
                'content': content[:500],   # first 500 chars for the preview
                'date':    datetime.now().isoformat()
            })

    log(f"Found {len(emails)} unread email(s)")
    return emails


# ─────────────────────────────────────────────────────────────────────────────
# analyze_email
# ─────────────────────────────────────────────────────────────────────────────
def analyze_email(sender, subject, content=""):
    """Analyze an email and determine if it's important."""
    importance_score  = 0
    priority_keywords = {
        "urgent":          3,
        "asap":            3,
        "emergency":       3,
        "immediate":       3,
        "critical":        3,
        "review":          2,
        "approve":         2,
        "feedback":        2,
        "action required": 2,
        "respond":         1
    }

    subject_lower = (subject or "").lower()
    content_lower = (content or "").lower()
    sender_lower  = (sender  or "").lower()

    for keyword, score in priority_keywords.items():
        if keyword in subject_lower or keyword in content_lower:
            importance_score += score

    for known in TRUSTED_SENDERS:
        if known in sender_lower:
            importance_score += 2

    if importance_score >= 5:
        priority       = "HIGH"
        needs_response = True
    elif importance_score >= 2:
        priority       = "MEDIUM"
        needs_response = False
    else:
        priority       = "LOW"
        needs_response = False

    triggered_keywords = [
        k for k in priority_keywords
        if k in subject_lower or k in content_lower
    ]

    return {
        "priority":           priority,
        "score":              importance_score,
        "needs_response":     needs_response,
        "important_keywords": triggered_keywords
    }


# ─────────────────────────────────────────────────────────────────────────────
# get_thread_history
# ─────────────────────────────────────────────────────────────────────────────
def get_thread_history(subject, sender, max_messages=10):
    """
    Fetch previous messages in the same email thread from Mail.app.

    Args:
        subject     : Subject of the current email (normalised internally)
        sender      : Sender of the current email
        max_messages: Max prior messages to return (default 10)

    Returns:
        List of dicts [{"sender": ..., "subject": ..., "content": ...}]
        sorted oldest-first. Empty list on failure or no history.
    """

    # ── Normalise subject ─────────────────────────────────────────────────────
    # Strip leading bracket tags e.g. [EXTERNAL], [BULK], [SPAM]
    # then strip reply/forward prefixes repeatedly until none remain,
    # then strip trailing symbols/punctuation.
    base_subject = subject.strip()
    base_subject = re.sub(r'^\[[^\]]*\]\s*', '', base_subject)  # [TAG] prefix
    while True:
        stripped = re.sub(r'^(re|fwd|fw|aw|sv|ant)\s*:\s*', '', base_subject, flags=re.IGNORECASE).strip()
        if stripped == base_subject:
            break
        base_subject = stripped
    base_subject = re.sub(r'[\s\W]+$', '', base_subject).strip()  # trailing symbols

    if not base_subject:
        log("Thread history: subject normalised to empty, skipping")
        return []

    # ── Escape for safe injection into AppleScript string literal ─────────────
    safe_subject = base_subject.replace('"', '\\"')

    # ── AppleScript: search INBOX for matching thread messages ─────────────────
    applescript = f'''
    tell application "Mail"
        set targetSubject to "{safe_subject}"
        set inboxAccount to account id "{MAIL_ACCOUNT_ID}"
        set inboxFolder to mailbox "INBOX" of inboxAccount
        set allMessages to every message of inboxFolder

        set matchedMessages to {{}}

        repeat with msg in allMessages
            set msgSubject to subject of msg
            if msgSubject contains targetSubject then
                set msgContent to text 1 thru (min of 2000 and (count characters of (content of msg))) of (content of msg)
                set msgEntry to (sender of msg) & "|||" & msgSubject & "|||" & msgContent
                set end of matchedMessages to msgEntry
            end if
        end repeat

        set AppleScript's text item delimiters to "<<<MSG>>>"
        set resultText to matchedMessages as text
        set AppleScript's text item delimiters to ""
        return resultText
    end tell
    '''

    try:
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True, text=True,
            timeout=30
        )

        raw = result.stdout.strip()
        if not raw:
            log(f"Thread history: no prior messages found for '{base_subject}'")
            return []

        thread = []
        for block in raw.split('<<<MSG>>>'):
            block = block.strip()
            if not block:
                continue
            parts = block.split('|||', 2)
            if len(parts) == 3:
                thread.append({
                    "sender":  parts[0].strip(),
                    "subject": parts[1].strip(),
                    "content": parts[2].strip()
                })

        thread = thread[-max_messages:]

        log(f"Thread history: found {len(thread)} prior message(s) for '{base_subject}'")
        return thread

    except subprocess.TimeoutExpired:
        log("Thread history: AppleScript timed out, continuing without thread context")
        return []
    except Exception as e:
        log(f"Thread history: failed ({e}), continuing without thread context")
        return []


# ─────────────────────────────────────────────────────────────────────────────
# call_llm  (was call_lm_studio in v2, call_ollama in v1)
# ─────────────────────────────────────────────────────────────────────────────
def call_llm(prompt, model=None, timeout=None):
    """
    Send a prompt to the configured LLM and return generated text.

    Uses the OpenAI-compatible /v1/chat/completions endpoint.
    Provider, URL, key, and model come from config/settings.json.

    Args:
        prompt  : Full prompt string (sent as a single user message)
        model   : Model ID override (defaults to LLM_MODEL)
        timeout : Seconds before giving up (defaults to LLM_TIMEOUT)

    Returns:
        str : The model's response text, or empty string on any failure.
    """
    model   = model   or LLM_MODEL
    timeout = timeout or LLM_TIMEOUT

    url = f"{LLM_BASE_URL}/chat/completions"

    payload = json.dumps({
        "model":      model,
        "messages":   [{"role": "user", "content": prompt}],
        "max_tokens": LLM_MAX_TOKENS,
        "stream":     False
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {LLM_API_KEY}",
            "User-Agent":    "OpenClawBot/1.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            # Strip <think>...</think> reasoning block if present
            if "</think>" in content:
                content = content.split("</think>", 1)[1]
            return content.strip()

    except urllib.error.URLError as e:
        log(f"LLM connection failed ({e}). Check {LLM_BASE_URL} is reachable.")
        return ""
    except (KeyError, IndexError) as e:
        log(f"LLM response format unexpected: {e}")
        return ""
    except json.JSONDecodeError as e:
        log(f"LLM returned invalid JSON: {e}")
        return ""
    except Exception as e:
        log(f"LLM call failed unexpectedly: {e}")
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# generate_contextual_draft
# ─────────────────────────────────────────────────────────────────────────────
def generate_contextual_draft(sender, subject, content):
    """
    Generate a contextual draft reply using the configured LLM.
    Fetches thread history first so the model has full conversation context.

    Returns immediately with a placeholder if LLM_ENABLED is False.
    """

    if not LLM_ENABLED:
        return "[LLM disabled — no draft generated. Set provider in settings.json to enable.]"

    # ── Extract clean display name ────────────────────────────────────────────
    if '<' in sender:
        sender_name = sender.split('<')[0].strip()
    else:
        sender_name = sender.strip()
    if not sender_name:
        sender_name = "there"

    # ── Fetch thread history ──────────────────────────────────────────────────
    log(f"Fetching thread history for: {subject}")
    thread_history = get_thread_history(subject, sender)

    # ── Build thread context block for the prompt ─────────────────────────────
    if thread_history:
        history_lines = ["Previous messages in this thread (oldest first):"]
        history_lines.append("─" * 40)
        for i, msg in enumerate(thread_history, 1):
            history_lines.append(f"[Message {i}]")
            history_lines.append(f"From: {msg['sender']}")
            history_lines.append(f"Subject: {msg['subject']}")
            history_lines.append(f"Content:\n{msg['content']}")
            history_lines.append("")
        thread_context = "\n".join(history_lines)
    else:
        thread_context = "This appears to be the start of a new thread (no prior messages found)."

    # ── Build the full prompt ─────────────────────────────────────────────────
    prompt = f"""You are {BOT_NAME}, an AI email assistant for {USER_NAME}.
Your job is to draft a reply on {USER_NAME}'s behalf to the email below.

About {USER_NAME}:
- Values concise, friendly, and professional communication
- Signs off as "{USER_NAME}" in personal emails, or "{BOT_NAME} 🤖" when acting autonomously

{thread_context}

─────────────────────────────────────────
Current email to reply to:
From: {sender} ({sender_name})
Subject: {subject}
Content:
{content}
─────────────────────────────────────────

Instructions:
- Read the thread history carefully and reply to THIS specific email in context.
- If the thread has prior messages, acknowledge or build on what was already discussed.
- If there is no thread history, respond appropriately for a first contact.
- Keep the reply concise (2–5 sentences is usually enough unless more detail is warranted).
- Match the tone of the incoming email: casual if they are casual, formal if they are formal.
- DO NOT use filler phrases like "I hope this email finds you well" or "Thanks for reaching out".
- DO NOT start with "I" as the very first word of the reply.
- End with a natural sign-off followed by "{BOT_NAME} 🤖" on its own line.
- Output ONLY the email body text. No explanations, no metadata, no subject line.

Draft reply:"""

    log(f"Calling LLM ({LLM_MODEL}) for draft reply to: {subject}")
    draft = call_llm(prompt)

    if not draft:
        log(f"LLM returned empty for '{subject}', using fallback draft")
        draft = (
            f"Hi {sender_name},\n\n"
            f"Received your message about '{subject}'. "
            f"I'll follow up with a proper reply shortly.\n\n"
            f"{BOT_NAME} 🤖\n\n"
            f"[NOTE: LLM was unavailable — this is a placeholder draft]"
        )

    log(f"Draft generated for: {subject}")
    return draft


# ─────────────────────────────────────────────────────────────────────────────
# mark_emails_as_read
# ─────────────────────────────────────────────────────────────────────────────
def mark_emails_as_read():
    """Mark all unread emails in inbox as read using AppleScript."""
    script = f'''tell application "Mail"
        set inboxAccount to account id "{MAIL_ACCOUNT_ID}"
        set inboxFolder to mailbox "INBOX" of inboxAccount

        set unreadMessages to every message of inboxFolder whose read status is false

        if (count of unreadMessages) > 0 then
            repeat with msg in unreadMessages
                set read status of msg to true
            end repeat
            return count of unreadMessages & " email(s) marked as read"
        else
            return "No emails to mark as read"
        end if
    end tell'''

    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True, text=True,
            timeout=30
        )
        log(f"Marked as read: {result.stdout.strip()}")
        return True
    except subprocess.TimeoutExpired:
        log("mark_emails_as_read: osascript timed out after 30s")
        return False
    except Exception as e:
        log(f"Failed to mark emails as read: {e}")
        return False


# ─────────────────────────────────────────────────────────────────────────────
# format_report
# ─────────────────────────────────────────────────────────────────────────────
def format_report(emails_data):
    """Format the email report."""
    report = []
    report.append("=" * 60)
    report.append(f"EMAIL CHECK REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 60)
    report.append("")

    if not emails_data:
        report.append("No unread emails found in inbox.")
        return "\n".join(report)

    report.append(f"Total unread messages: {len(emails_data)}")
    report.append("")

    high_priority   = []
    medium_priority = []
    low_priority    = []

    for email in emails_data:
        analysis = analyze_email(
            email.get("sender",  "Unknown"),
            email.get("subject", "No Subject"),
            email.get("content", "")
        )
        email["analysis"] = analysis

        if analysis["priority"] == "HIGH":
            high_priority.append(email)
        elif analysis["priority"] == "MEDIUM":
            medium_priority.append(email)
        else:
            low_priority.append(email)

    # ── HIGH priority ──────────────────────────────────────────────────────────
    if high_priority:
        report.append("⚠️  HIGH PRIORITY EMAILS (Action Required)")
        report.append("-" * 40)

        for email in high_priority:
            sender  = email.get("sender",  "Unknown")
            subject = email.get("subject", "No Subject")
            content = email.get("content", "")

            report.append(f"\nFrom: {sender}")
            report.append(f"Subject: {subject}")
            report.append(f"Impact Score: {email['analysis']['score']}/15")

            if email['analysis']['important_keywords']:
                report.append(f"Triggered keywords: {', '.join(email['analysis']['important_keywords'])}")

            if content:
                report.append("\nEmail Preview:")
                report.append("-" * 20)
                report.append(content[:300] + "..." if len(content) > 300 else content)

            report.append("\nDraft Response:")
            report.append("-" * 20)
            draft = generate_contextual_draft(sender, subject, content)
            report.append(draft)

        report.append("")

    # ── MEDIUM priority ────────────────────────────────────────────────────────
    if medium_priority:
        report.append("⚠️  MEDIUM PRIORITY EMAILS")
        report.append("-" * 40)

        for email in medium_priority:
            sender  = email.get("sender",  "Unknown")
            subject = email.get("subject", "No Subject")
            content = email.get("content", "")

            report.append(f"\nFrom: {sender}")
            report.append(f"Subject: {subject}")

            if content:
                report.append("Preview:")
                report.append(content[:150] + "..." if len(content) > 150 else content)

        report.append("")

    # ── LOW priority ───────────────────────────────────────────────────────────
    if low_priority:
        report.append("✅ LOW PRIORITY EMAILS")
        report.append("-" * 40)

        for email in low_priority:
            sender  = email.get("sender",  "Unknown")
            subject = email.get("subject", "No Subject")
            content = email.get("content", "")

            report.append(f"\nFrom: {sender}")
            report.append(f"Subject: {subject}")

            if content:
                report.append("Preview:")
                report.append(content[:150] + "..." if len(content) > 150 else content)

        report.append("")

    report.append("=" * 60)
    return "\n".join(report)


# ─────────────────────────────────────────────────────────────────────────────
# send_email_report
# ─────────────────────────────────────────────────────────────────────────────
def send_email_report(report_content):
    """Send email report."""
    subject = f"OpenClaw Email Check Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    report_file = TEMP_DIR / "email_report.txt"
    report_file.write_text(report_content, encoding="utf-8")

    applescript = f'''tell application "Mail"
        set reportContent to do shell script "cat {report_file}"
        set newMessage to make new outgoing message with properties {{subject:"{subject}", content:reportContent}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{REPORT_RECIPIENT}"}}
        end tell
        send newMessage
    end tell'''

    try:
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True, text=True,
            timeout=30
        )
        if result.returncode != 0:
            log(f"send_email_report: osascript error: {result.stderr.strip()}")
            return False
        log(f"Email report sent to {REPORT_RECIPIENT}")
        return True
    except subprocess.TimeoutExpired:
        log("send_email_report: osascript timed out after 30s")
        return False
    except Exception as e:
        log(f"Failed to send email: {e}")
        return False


# ─────────────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    """Main execution function."""
    log("Starting email check...")

    emails = get_unread_emails()

    if not emails:
        report = format_report([])
        print(report)
        return report

    report = format_report(emails)

    with open(EMAILS_FILE, "w") as f:
        json.dump(
            [
                {
                    "sender":   e.get("sender"),
                    "subject":  e.get("subject"),
                    "priority": e.get("analysis", {}).get("priority")
                }
                for e in emails
            ],
            f, indent=2
        )

    log("Email check completed")

    send_email_report(report)
    mark_emails_as_read()

    print(report)
    return report


if __name__ == "__main__":
    main()
