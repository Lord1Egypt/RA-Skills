#!/usr/bin/env python3
"""Fword: Convert Word (.docx) to clean LaTeX.

Usage:
    python convert.py input.docx [output.tex] [--raw] [-p PROVIDER] [--model MODEL]

Supported providers: anthropic, openai, qwen, kimi, minimax, deepseek, zhipu
"""

import argparse
import sys
from pathlib import Path

import pypandoc
from rich.console import Console

from ai_refiner import PROVIDERS, refine_latex
from workspace import create_workspace, record_conversion

console = Console()


def extract_metadata(docx_path: Path) -> dict:
    """Extract document metadata from docx."""
    try:
        from docx import Document
        doc = Document(str(docx_path))
        props = doc.core_properties
        return {
            "title": props.title or "",
            "author": props.author or "",
        }
    except Exception:
        return {}


def docx_to_latex_raw(docx_path: Path, media_dir: Path | None = None) -> str:
    """Convert docx to raw LaTeX via Pandoc."""
    if media_dir is None:
        media_dir = docx_path.parent / "media"
    args = [
        "--standalone",
        "--wrap=none",
        f"--extract-media={media_dir}",
    ]
    return pypandoc.convert_file(str(docx_path), "latex", extra_args=args)


def main():
    parser = argparse.ArgumentParser(description="Convert Word to LaTeX")
    parser.add_argument("input", help="Input .docx file")
    parser.add_argument("output", nargs="?", default=None, help="Output .tex file")
    parser.add_argument("--raw", action="store_true", help="Pandoc only, skip AI refinement")
    parser.add_argument(
        "-p", "--provider",
        choices=list(PROVIDERS.keys()),
        default="anthropic",
        help="AI provider",
    )
    parser.add_argument("--model", default=None, help="AI model (default: provider's default)")
    parser.add_argument("--api-key", default=None, help="API key (or set provider's env var)")
    parser.add_argument("--base-url", default=None, help="Custom API base URL")
    parser.add_argument("--keep-intermediate", action="store_true", help="Save raw pandoc output")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        console.print(f"[bold red]Error:[/] File not found: {input_path}")
        sys.exit(1)
    if input_path.suffix.lower() not in (".docx", ".doc"):
        console.print(f"[bold red]Error:[/] Expected .docx file, got: {input_path.suffix}")
        sys.exit(1)

    output_path = Path(args.output) if args.output else input_path.with_suffix(".tex")

    provider_info = PROVIDERS.get(args.provider, {})
    model_name = args.model or provider_info.get("default_model", "?")

    # Stage 0: Workspace
    console.print(f"[bold blue]→[/] Reading: {input_path.name}")
    console.print(f"  Provider: {args.provider} | Model: {model_name}")
    workspace = create_workspace(input_path, output_dir=output_path.parent)
    console.print(f"  Workspace: {workspace}")

    metadata = extract_metadata(input_path)
    if metadata.get("title"):
        console.print(f"  Title: {metadata['title']}")

    # Stage 1: Pandoc
    console.print("[bold blue]→[/] Stage 1: Pandoc conversion (docx → raw LaTeX)")
    raw_latex = docx_to_latex_raw(input_path)
    console.print(f"  Raw output: {len(raw_latex)} chars, {raw_latex.count(chr(10))} lines")

    if args.keep_intermediate:
        raw_path = input_path.with_suffix(".raw.tex")
        raw_path.write_text(raw_latex, encoding="utf-8")
        console.print(f"  Saved intermediate: {raw_path}")

    # Stage 2: AI refinement
    if args.raw:
        console.print("[bold yellow]![/] Skipping AI refinement (--raw)")
        result = raw_latex
    else:
        console.print("[bold blue]→[/] Stage 2: AI refinement")
        result = refine_latex(
            raw_latex,
            metadata,
            provider=args.provider,
            model=args.model,
            api_key=args.api_key,
            base_url=args.base_url,
        )

    # Output
    output_path.write_text(result, encoding="utf-8")
    record_conversion(workspace, "docx2latex", input_path.name, output_path.name)
    console.print(f"[bold green]✓[/] Output: {output_path}")
    console.print(f"  {len(result)} chars, {result.count(chr(10))} lines")
    console.print(f"  [dim]Use 'python back.py {output_path.name}' to convert back to Word[/dim]")


if __name__ == "__main__":
    main()
