#!/usr/bin/env python3
"""
analyze.py — Universal media analysis script for CLIProxyAPI

Usage:
  python3 analyze.py image.jpg "question"
  python3 analyze.py doc.pdf "summary"
  python3 analyze.py img1.jpg img2.jpg "compare"
  python3 analyze.py --stream image.jpg "describe"
  python3 analyze.py --system "you are an expert" image.jpg "question"
  python3 analyze.py --max-tokens 4096 doc.pdf "analysis"
  python3 analyze.py --model claude-opus-4-6 image.jpg "question"

Supported file types:
  Images:    .jpg/.jpeg, .png, .gif, .webp
  Documents: .pdf
  URLs:      http:// and https:// (referenced directly as image URL)

Configuration via env vars:
  CLIPROXY_URL    Endpoint URL (default: http://localhost:8317/v1/messages)
  CLIPROXY_MODEL  Model (default: claude-sonnet-4-6)

⚠️  System prompts are always sent as an array (CLIProxy requirement).
    String notation is silently ignored by the proxy.
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Standaard configuratie
DEFAULT_ENDPOINT = "http://localhost:8317/v1/messages"
DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_MAX_TOKENS = 1024

# Media type mapping op extensie
IMAGE_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def detect_media_type(path: str) -> str:
    """Bepaal media type op basis van bestandsextensie."""
    ext = Path(path).suffix.lower()
    if ext in IMAGE_TYPES:
        return IMAGE_TYPES[ext]
    if ext == ".pdf":
        return "application/pdf"
    # Fallback: probeer via mimetypes module
    mime, _ = mimetypes.guess_type(path)
    if mime:
        return mime
    raise ValueError(f"Onbekende bestandsextensie: {ext} — ondersteund: jpg/jpeg/png/gif/webp/pdf")


def load_file_as_base64(path: str) -> str:
    """Laad een bestand en codeer als base64 string."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_content_block(file_path: str) -> dict:
    """
    Maak een content block voor een bestand.
    Ondersteunt: afbeeldingen (base64), PDFs (base64 document), URLs (image url).
    """
    # URL: directe referentie (alleen voor afbeeldingen — document URL werkt niet)
    if file_path.startswith("http://") or file_path.startswith("https://"):
        return {
            "type": "image",
            "source": {
                "type": "url",
                "url": file_path,
            },
        }

    # Lokaal bestand
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Bestand niet gevonden: {file_path}")

    media_type = detect_media_type(file_path)
    data = load_file_as_base64(file_path)

    if media_type == "application/pdf":
        # PDFs als document type (enige geldige document media type)
        return {
            "type": "document",
            "source": {
                "type": "base64",
                "media_type": "application/pdf",
                "data": data,
            },
        }
    elif media_type.startswith("image/"):
        # Afbeeldingen als image type
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": data,
            },
        }
    else:
        raise ValueError(
            f"Niet ondersteund media type: {media_type}\n"
            f"Ondersteund: afbeeldingen (jpg/png/gif/webp) en PDFs.\n"
            f"Workarounds:\n"
            f"  - Office bestanden: converteer naar PDF\n"
            f"  - Audio: gebruik Whisper voor transcriptie\n"
            f"  - Tekst: kopieer de inhoud direct in je vraag"
        )


def stream_response(resp) -> str:
    """Verwerk SSE streaming response, print naar stdout, retourneer volledige tekst."""
    full_text = ""
    for line in resp:
        line = line.decode("utf-8").rstrip()
        if not line.startswith("data: "):
            continue
        data_str = line[6:]
        if data_str == "[DONE]":
            break
        try:
            event = json.loads(data_str)
        except json.JSONDecodeError:
            continue

        event_type = event.get("type", "")

        if event_type == "content_block_delta":
            delta = event.get("delta", {})
            if delta.get("type") == "text_delta":
                chunk = delta.get("text", "")
                print(chunk, end="", flush=True)
                full_text += chunk
        elif event_type == "message_stop":
            break

    print()  # Newline na streaming
    return full_text


def analyze(
    files: list,
    question: str,
    system: str = None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    model: str = None,
    endpoint: str = None,
    stream: bool = False,
) -> str:
    """
    Analyseer een of meerdere bestanden met een vraag.

    Args:
        files:      Lijst van bestandspaden of URLs
        question:   De vraag of instructie
        system:     Optionele system prompt (wordt als array verstuurd — CLIProxy vereiste)
        max_tokens: Maximum output tokens
        model:      Model override (default: CLIPROXY_MODEL env var of claude-sonnet-4-6)
        endpoint:   Endpoint URL override (default: CLIPROXY_URL env var)
        stream:     Gebruik SSE streaming output

    Returns:
        De gegenereerde tekst als string
    """
    # Configuratie
    actual_endpoint = endpoint or os.environ.get("CLIPROXY_URL", DEFAULT_ENDPOINT)
    actual_model = model or os.environ.get("CLIPROXY_MODEL", DEFAULT_MODEL)

    # Bouw content blocks
    content = []
    for f in files:
        content.append(build_content_block(f))
    content.append({"type": "text", "text": question})

    # Bouw request payload
    payload = {
        "model": actual_model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": content}],
    }

    # System prompt — ALTIJD array-notatie (string wordt silently genegeerd door CLIProxy)
    if system:
        payload["system"] = [{"type": "text", "text": system}]

    # Streaming flag
    if stream:
        payload["stream"] = True

    # HTTP request
    req = urllib.request.Request(
        actual_endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": "dummy",  # CLIProxy gebruikt eigen auth
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            if stream:
                return stream_response(resp)
            else:
                response_data = json.loads(resp.read())
                return response_data["content"][0]["text"]

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_body)
            error_msg = error_json.get("error", {}).get("message", error_body)
        except json.JSONDecodeError:
            error_msg = error_body
        raise RuntimeError(f"HTTP {e.code}: {error_msg}") from e

    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Kan endpoint niet bereiken: {actual_endpoint}\n"
            f"Fout: {e.reason}\n"
            f"Controleer of CLIProxyAPI draait en CLIPROXY_URL correct is."
        ) from e


def main():
    parser = argparse.ArgumentParser(
        description="Analyseer afbeeldingen en PDFs via CLIProxyAPI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Voorbeelden:
  python3 analyze.py image.jpg "Wat staat er op deze foto?"
  python3 analyze.py document.pdf "Geef een samenvatting"
  python3 analyze.py img1.jpg img2.jpg "Vergelijk deze afbeeldingen"
  python3 analyze.py --stream image.jpg "Beschrijf in detail"
  python3 analyze.py --system "Je bent een medisch expert" scan.jpg "Wat zie je?"
  python3 analyze.py --max-tokens 4096 rapport.pdf "Uitgebreide analyse"
  python3 analyze.py https://example.com/photo.jpg "Beschrijf"

Env vars:
  CLIPROXY_URL    Endpoint URL (default: http://localhost:8317/v1/messages)
  CLIPROXY_MODEL  Model (default: claude-sonnet-4-6)
        """,
    )

    parser.add_argument(
        "--stream",
        action="store_true",
        help="Gebruik SSE streaming (output verschijnt direct)",
    )
    parser.add_argument(
        "--system",
        type=str,
        default=None,
        help="System prompt (wordt als array verstuurd)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=DEFAULT_MAX_TOKENS,
        help=f"Maximum output tokens (default: {DEFAULT_MAX_TOKENS})",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model override (default: CLIPROXY_MODEL of claude-sonnet-4-6)",
    )
    parser.add_argument(
        "--url",
        type=str,
        default=None,
        dest="endpoint",
        help="Endpoint URL override (default: CLIPROXY_URL)",
    )
    parser.add_argument(
        "args",
        nargs="+",
        help="[bestand1.jpg] [bestand2.pdf] ... [vraag]",
    )

    parsed = parser.parse_args()

    # Splits args: alles behalve het laatste is een bestand/URL, laatste is de vraag
    if len(parsed.args) < 2:
        parser.error(
            "Geef minimaal één bestand en een vraag op.\n"
            "Gebruik: analyze.py [--opties] bestand.jpg 'vraag'"
        )

    files = parsed.args[:-1]
    question = parsed.args[-1]

    try:
        result = analyze(
            files=files,
            question=question,
            system=parsed.system,
            max_tokens=parsed.max_tokens,
            model=parsed.model,
            endpoint=parsed.endpoint,
            stream=parsed.stream,
        )
        if not parsed.stream:
            print(result)
    except (RuntimeError, FileNotFoundError, ValueError) as e:
        print(f"Fout: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
