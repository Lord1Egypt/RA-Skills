#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "typer>=0.12.0",
# ]
# ///
"""Gemini image & text generation via Corespeed AI Gateway."""

import json as json_lib
import mimetypes
import os
import sys
from pathlib import Path
from typing import Optional

import typer
from google import genai
from google.genai import types

app = typer.Typer(add_completion=False)


def _get_client(json_mode: bool = False) -> genai.Client:
    base_url = os.environ.get("CS_AI_GATEWAY_BASE_URL", "")
    api_token = os.environ.get("CS_AI_GATEWAY_API_TOKEN", "")
    if not base_url or not api_token:
        msg = "CS_AI_GATEWAY_BASE_URL and CS_AI_GATEWAY_API_TOKEN are required."
        if json_mode:
            typer.echo(json_lib.dumps({"ok": False, "error": msg}))
        else:
            typer.echo(f"Error: {msg}", err=True)
        raise typer.Exit(1)
    return genai.Client(
        api_key=api_token,
        http_options=types.HttpOptions(base_url=f"{base_url.rstrip('/')}/google-ai-studio"),
    )


@app.command()
def main(
    prompt: str = typer.Option(..., "--prompt", "-p", help="Text prompt"),
    filename: Path = typer.Option(..., "--filename", "-f", help="Output filename"),
    input: Optional[list[Path]] = typer.Option(None, "--input", "-i", help="Input image file(s)"),
    model: str = typer.Option("gemini-2.5-flash-image", "--model", "-m", help="Model name"),
    modalities: str = typer.Option("auto", help="Response type: auto, image, text, image+text"),
    json: bool = typer.Option(False, "--json", help="Output structured JSON for agent consumption"),
):
    """Generate images and text with Gemini via Corespeed AI Gateway."""
    client = _get_client(json_mode=json)
    filename.parent.mkdir(parents=True, exist_ok=True)

    is_image_output = filename.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".gif")

    # Determine response modalities
    if modalities == "auto":
        resp_mod = ["IMAGE", "TEXT"] if is_image_output else ["TEXT"]
    elif modalities == "image":
        resp_mod = ["IMAGE"]
    elif modalities == "text":
        resp_mod = ["TEXT"]
    else:
        resp_mod = ["IMAGE", "TEXT"]

    # Build content parts
    parts = []
    for fpath in input or []:
        if not fpath.exists():
            typer.echo(f"Error: Input file not found: {fpath}", err=True)
            raise typer.Exit(1)
        mime = mimetypes.guess_type(str(fpath))[0] or "application/octet-stream"
        data = fpath.read_bytes()
        parts.append(types.Part.from_bytes(data=data, mime_type=mime))
        typer.echo(f"Input: {fpath} ({mime}, {len(data)} bytes)")
    parts.append(types.Part.from_text(text=prompt))

    log = (lambda msg: None) if json else (lambda msg: typer.echo(msg))

    log(f"Model: {model}")
    log(f"Prompt: {prompt[:200]}")
    log(f"Modalities: {resp_mod}")
    log("Generating...")

    try:
        response = client.models.generate_content(
            model=model,
            contents=types.Content(role="user", parts=parts),
            config=types.GenerateContentConfig(response_modalities=resp_mod),
        )

        if not response.candidates or not response.candidates[0].content.parts:
            if json:
                typer.echo(json_lib.dumps({"ok": False, "error": "Empty response from model"}))
            else:
                typer.echo("Error: Empty response from model", err=True)
            raise typer.Exit(1)

        image_count = 0
        text_parts = []
        saved_files = []

        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                save_path = filename if image_count == 0 else (
                    filename.parent / f"{filename.stem}-{image_count + 1}{filename.suffix}"
                )
                save_path.write_bytes(part.inline_data.data)
                saved_files.append(str(save_path.resolve()))
                log(f"\nSaved: {save_path.resolve()}")
                log(f"MEDIA: {save_path.resolve()}")
                image_count += 1
            elif part.text:
                text_parts.append(part.text)

        if image_count == 0 and text_parts:
            text_content = "\n".join(text_parts)
            if is_image_output:
                if json:
                    typer.echo(json_lib.dumps({"ok": False, "error": "Model returned text instead of image", "text": text_content[:500]}))
                else:
                    typer.echo(f"Warning: Model returned text instead of image.", err=True)
                    typer.echo(f"Response: {text_content[:500]}", err=True)
                raise typer.Exit(1)
            filename.write_text(text_content, encoding="utf-8")
            saved_files.append(str(filename.resolve()))
            log(f"\nSaved: {filename.resolve()}")
            log(f"Text length: {len(text_content)} chars")
        elif text_parts:
            log(f"\nCaption: {' '.join(text_parts)[:300]}")

        um = response.usage_metadata
        tokens = {"prompt": um.prompt_token_count, "output": um.candidates_token_count, "total": um.total_token_count} if um else None

        if json:
            typer.echo(json_lib.dumps({
                "ok": True,
                "files": saved_files,
                "text": "\n".join(text_parts) if text_parts else None,
                "model": model,
                "tokens": tokens,
            }))
        else:
            if tokens:
                typer.echo(f"Tokens: prompt={tokens['prompt']}, output={tokens['output']}, total={tokens['total']}")

    except typer.Exit:
        raise
    except Exception as e:
        if json:
            typer.echo(json_lib.dumps({"ok": False, "error": str(e)}))
        else:
            typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
