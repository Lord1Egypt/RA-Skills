#!/usr/bin/env python3
"""End-to-end WhatsApp content-creation workflow.

Pulls incoming WhatsApp requests, derives an image prompt (from text or by
transcribing an audio note), generates an image, and replies to the customer.
"""

import sys
from typing import Any, Dict, List, Optional

from generate_images import ImageGenerationError, generate_image
from transcribe import TranscriptionError, transcribe_audio
from wacli import WhatsAppClient


def _extract_prompt(message: Dict[str, Any]) -> Optional[str]:
    """Derive an image prompt from a message, transcribing audio when needed.

    Returns the prompt string, or ``None`` if no usable prompt could be built.
    """
    msg_type = message.get("type")
    content = message.get("content")

    if msg_type == "text":
        prompt = (content or "").strip()
        return prompt or None

    if msg_type == "audio":
        if not content:
            print("Audio message has no file path; skipping.")
            return None
        print(f"Transcribing audio file: {content}")
        try:
            prompt = transcribe_audio(content)
        except TranscriptionError as exc:
            print(f"Transcription failed: {exc}")
            return None
        caption = message.get("caption")
        if caption:
            prompt = f"{prompt} {caption}".strip()
        return prompt or None

    print(f"Unsupported message type: {msg_type!r}")
    return None


def process_whatsapp_request(message: Dict[str, Any]) -> bool:
    """Process a single incoming WhatsApp request end to end.

    Returns ``True`` on success, ``False`` if the request could not be handled.
    """
    sender = message.get("from")
    if not sender:
        print("Message missing sender; skipping.")
        return False

    print(f"Processing message from {sender}...")

    prompt = _extract_prompt(message)
    if not prompt:
        print("No prompt extracted from message")
        return False

    print(f"Extracted prompt: {prompt}")
    print("Generating image...")
    try:
        result = generate_image(prompt)
    except ImageGenerationError as exc:
        print(f"Failed to generate image: {exc}")
        return False

    print("Sending result back to customer...")
    wa_client = WhatsAppClient()
    caption = f"Here's your generated image!\nPrompt used: {result['revised_prompt']}"
    wa_client.send_message(sender, caption, result["image_path"])

    print("Request processed successfully!")
    return True


def process_all_unread() -> int:
    """Process all unread WhatsApp messages.

    Returns the number of messages processed successfully.
    """
    wa_client = WhatsAppClient()
    messages: List[Dict[str, Any]] = wa_client.list_messages()

    processed = 0
    for msg in messages:
        # In production, track read/unread status to avoid reprocessing.
        if process_whatsapp_request(msg):
            processed += 1

    print(f"Processed {processed}/{len(messages)} request(s) successfully.")
    return processed


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) == 2 and sys.argv[1] == "process-all":
        process_all_unread()
        return

    print("Content Creator Workflow")
    print("Usage:")
    print("  python workflow.py process-all - Process all unread requests")
    print("\nMake sure you have:")
    print("1. Set OPENAI_API_KEY environment variable")
    print("2. Logged into wacli with `python wacli.py login <your-token>`")


if __name__ == "__main__":
    main()
