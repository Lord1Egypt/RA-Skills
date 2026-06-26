#!/usr/bin/env python3
"""
AI Code Review Service
Integrates:
- Code review analysis
- OpenAI Whisper API for voice note transcription
- Discord notifications
- Health monitoring
- ClawHub skill management
"""
import html
import logging
import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

from openai import OpenAI
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuration from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
CLAWHUB_API_URL = os.getenv("CLAWHUB_API_URL", "https://api.clawhub.com/v1")

# Allowed diff URL schemes to prevent SSRF
ALLOWED_DIFF_SCHEMES = {"https", "http"}
# Base directory for voice note files to prevent path traversal
VOICE_NOTE_BASE_DIR = Path(os.getenv("VOICE_NOTE_BASE_DIR", "/tmp/voice_notes")).resolve()
# Request timeout in seconds
REQUEST_TIMEOUT = 30

_client: Optional[OpenAI] = None


def _get_openai_client() -> OpenAI:
    """Lazily initialize and return the OpenAI client."""
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def _validate_diff_url(url: str) -> None:
    """Validate that a diff URL is safe to fetch (prevents SSRF)."""
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_DIFF_SCHEMES:
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}' for diff URL. Allowed: {ALLOWED_DIFF_SCHEMES}")
    hostname = parsed.hostname or ""
    # Block internal/private network addresses
    if hostname in ("localhost", "127.0.0.1", "0.0.0.0", "::1") or hostname.startswith("10.") or hostname.startswith("192.168.") or hostname.startswith("172."):
        if not os.getenv("ALLOW_INTERNAL_DIFF_URLS"):
            raise ValueError(f"Diff URL points to internal address '{hostname}', which is blocked for security")
    if not hostname:
        raise ValueError("Diff URL has no hostname")


def _validate_voice_note_path(file_path: str) -> Path:
    """Validate and resolve voice note path to prevent path traversal."""
    resolved = Path(file_path).resolve()
    if not str(resolved).startswith(str(VOICE_NOTE_BASE_DIR)):
        raise ValueError(f"Voice note path '{file_path}' is outside the allowed directory '{VOICE_NOTE_BASE_DIR}'")
    if not resolved.is_file():
        raise FileNotFoundError(f"Voice note file not found: {resolved}")
    return resolved


def _escape_discord_content(text: str) -> str:
    """Escape Discord markdown special characters to prevent injection."""
    return text.replace("@", "@\u200b").replace("<", "&lt;").replace(">", "&gt;")


def transcribe_voice_note(audio_file_path: str) -> str:
    """Transcribe voice note from code review meetings using Whisper API."""
    client = _get_openai_client()
    resolved_path = _validate_voice_note_path(audio_file_path)

    with open(resolved_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
    logger.info("Transcribed voice note: %s (%d chars)", audio_file_path, len(transcription.text))
    return transcription.text


def send_discord_notification(message: str, embed: Optional[Dict] = None) -> bool:
    """Send code review notification to Discord channel."""
    if not DISCORD_WEBHOOK_URL:
        logger.warning("Discord webhook URL not configured, skipping notification")
        return False

    payload = {"content": _escape_discord_content(message)}
    if embed:
        # Sanitize embed text fields
        safe_embed = json.loads(
            json.dumps(embed).replace("@", "@\u200b")
        )
        payload["embeds"] = [safe_embed]

    try:
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=REQUEST_TIMEOUT,
        )
        success = response.status_code == 204
        if not success:
            logger.warning("Discord notification failed: HTTP %d - %s", response.status_code, response.text[:200])
        return success
    except requests.RequestException as exc:
        logger.error("Discord notification error: %s", exc)
        return False


def analyze_code_changes(diff_content: str) -> Dict:
    """Analyze code changes for potential issues and improvements."""
    if not diff_content or not diff_content.strip():
        return {
            "issues_found": 0,
            "suggestions": [],
            "approval": "skipped",
            "summary": "No diff content provided — review skipped.",
        }

    # TODO: Replace with actual LLM-based code review logic
    return {
        "issues_found": 0,
        "suggestions": [],
        "approval": "pending_manual_review",
        "summary": "Automated analysis not yet implemented — manual review required.",
    }


def process_pull_request(pr_number: int, diff_url: str, voice_note_path: Optional[str] = None) -> Dict:
    """Process a full pull request code review."""
    # 1. Fetch diff content with validation
    diff_content = ""
    if diff_url:
        _validate_diff_url(diff_url)
        try:
            resp = requests.get(diff_url, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            diff_content = resp.text
        except requests.RequestException as exc:
            logger.error("Failed to fetch diff for PR #%d: %s", pr_number, exc)
            return {
                "issues_found": 0,
                "suggestions": [],
                "approval": "error",
                "summary": f"Failed to fetch diff: {exc}",
            }

    # 2. Analyze code changes
    review_result = analyze_code_changes(diff_content)

    # 3. Transcribe voice note if provided
    if voice_note_path:
        try:
            transcription = transcribe_voice_note(voice_note_path)
            review_result["voice_note_transcription"] = transcription
        except (ValueError, FileNotFoundError) as exc:
            logger.warning("Voice note skipped for PR #%d: %s", pr_number, exc)
        except Exception as exc:
            logger.error("Voice note transcription failed for PR #%d: %s", pr_number, exc)

    # 4. Send notification to Discord
    embed = {
        "title": f"Code Review Completed for PR #{pr_number}",
        "description": html.escape(review_result["summary"]),
        "color": 0x00FF00 if review_result["approval"] == "approved" else 0xFF0000,
        "fields": [
            {"name": "Status", "value": html.escape(review_result["approval"].capitalize()), "inline": True},
            {"name": "Issues Found", "value": str(review_result["issues_found"]), "inline": True},
            {"name": "Suggestions", "value": str(len(review_result["suggestions"])), "inline": True},
        ],
    }
    send_discord_notification(
        message=f"New code review completed for PR #{pr_number}",
        embed=embed,
    )

    logger.info("PR #%d review complete: %s", pr_number, review_result["approval"])
    return review_result


def publish_skill(skill_path: str, version: str) -> bool:
    """Publish a skill to ClawHub."""
    if not skill_path or not version:
        raise ValueError("skill_path and version are required")
    # TODO: Implement ClawHub publish logic via API
    logger.info("Skill publish requested: path=%s version=%s (not yet implemented)", skill_path, version)
    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: code_review_service.py <pr_number> <diff_url> [voice_note_path]")
        sys.exit(1)

    try:
        pr = int(sys.argv[1])
        url = sys.argv[2]
        voice = sys.argv[3] if len(sys.argv) > 3 else None
        result = process_pull_request(pr_number=pr, diff_url=url, voice_note_path=voice)
        print(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error("Invalid input: %s", e)
        sys.exit(1)
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        sys.exit(2)