#!/usr/bin/env python3
"""Fword: Convert LaTeX back to Word (.docx) with original style recovery.

Usage:
    python back.py input.tex [output.docx] [--reference-doc TEMPLATE.docx]

Uses the .fword/ workspace (created during initial conversion) to recover
the original document's styles, fonts, headers/footers, and page layout.
"""

import argparse
import sys
from pathlib import Path

import pypandoc
from rich.console import Console

from workspace import get_reference_doc, get_workspace, record_conversion

console = Console()


def main():
    parser = argparse.ArgumentParser(description="Convert LaTeX back to Word")
    parser.add_argument("input", help="Input .tex file")
    parser.add_argument("output", nargs="?", default=None, help="Output .docx file")
    parser.add_argument("--reference-doc", default=None, help="Reference .docx for styles")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        console.print(f"[bold red]Error:[/] File not found: {input_path}")
        sys.exit(1)
    if input_path.suffix.lower() not in (".tex", ".latex"):
        console.print(f"[bold red]Error:[/] Expected .tex file, got: {input_path.suffix}")
        sys.exit(1)

    output_path = Path(args.output) if args.output else input_path.with_suffix(".docx")
    reference_doc = Path(args.reference_doc) if args.reference_doc else None

    # Find workspace
    workspace = get_workspace(input_path.parent)
    if workspace:
        console.print(f"[bold blue]→[/] Found workspace: {workspace}")
        if reference_doc is None:
            reference_doc = get_reference_doc(workspace)
            if reference_doc:
                console.print("  Using original document as style reference")
    else:
        console.print("[bold yellow]![/] No .fword workspace found — styles may differ from original")

    # Convert
    console.print("[bold blue]→[/] Converting LaTeX → Word")
    pandoc_args = ["--wrap=none"]
    if reference_doc:
        pandoc_args.append(f"--reference-doc={reference_doc}")

    pypandoc.convert_file(
        str(input_path),
        "docx",
        extra_args=pandoc_args,
        outputfile=str(output_path),
    )

    if workspace:
        record_conversion(workspace, "latex2docx", input_path.name, output_path.name)

    console.print(f"[bold green]✓[/] Output: {output_path}")


if __name__ == "__main__":
    main()
