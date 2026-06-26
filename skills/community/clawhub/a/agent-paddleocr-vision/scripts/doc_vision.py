#!/usr/bin/env python3
"""
Agent Vision - OCR as Agent's Eyes

Main entry point: orchestrates OCR extraction, document classification,
and action suggestion. Returns structured JSON for agent consumption.

Usage:
  Single file:
    python doc_vision.py --file-path <path> [--format json|text|pretty]
    python doc_vision.py --file-url <url> [--format json|text|pretty]

  Batch mode:
    python doc_vision.py --batch-dir <dir> [--output-dir <dir>] [--format json]
"""

import argparse
import json
import os
import sys
import time
import csv
import io
import traceback
from pathlib import Path
from typing import Any, Dict, Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add scripts directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from ocr_engine import parse_document  # our OCR wrapper, will support multi-backend later

# Remove template dependency — C方案: structured data only, no agent_prompt
# from templates import render_agent_prompt

# =============================================================================
# Retry wrapper
# =============================================================================

def parse_document_with_retry(file_path=None, file_url=None, file_type=None, max_retries=2):
    """Call parse_document with retry on 5xx errors."""
    last_err = None
    for attempt in range(max_retries + 1):
        try:
            return parse_document(file_path=file_path, file_url=file_url, file_type=file_type)
        except Exception as e:
            last_err = e
            err_str = str(e)
            if "500" in err_str or "502" in err_str or "503" in err_str or "timeout" in err_str.lower():
                if attempt < max_retries:
                    wait = 2 ** attempt
                    print(f"Retry {attempt+1}/{max_retries} after {wait}s: {err_str[:80]}", file=sys.stderr)
                    time.sleep(wait)
                    continue
            raise
    raise last_err
from classify import classify
from actions import suggest_actions, actions_to_dict


# =============================================================================
# Error Handling
# =============================================================================

def error_response(code: str, message: str) -> Dict[str, Any]:
    return {
        "ok": False,
        "error": {"code": code, "message": message},
        "document_type": None,
        "confidence": 0.0,
        "text": "",
        "pruned_result": None,
        "suggested_actions": [],
        "metadata": {},
    }


def format_pretty(result: Dict[str, Any]) -> str:
    """Format result as a pretty human-readable summary."""
    lines = []
    lines.append("=" * 60)
    lines.append("  Agent Vision — Document Analysis Result")
    lines.append("=" * 60)

    if not result.get("ok"):
        lines.append(f"  ERROR: {result.get('error', {}).get('message', 'Unknown')}")
        lines.append("=" * 60)
        return "\n".join(lines)

    lines.append(f"  Type:       {result.get('document_type', '?')}")
    lines.append(f"  Confidence: {result.get('confidence', 0):.0%}")
    lines.append(f"  Pages:      {result.get('metadata', {}).get('pages', '?')}")
    lines.append(f"  Backend:    {result.get('metadata', {}).get('backend', '?')}")
    lines.append("-" * 60)

    # Text preview (first 300 chars)
    text = result.get("text", "")
    if text:
        preview = text[:300].replace("\n", " ")
        if len(text) > 300:
            preview += "..."
        lines.append(f"  Text: {preview}")
        lines.append("-" * 60)

    # Extracted fields
    fields = result.get("extracted_fields", {})
    if fields:
        lines.append("  Extracted Fields:")
        for k, v in fields.items():
            lines.append(f"    {k}: {v}")
        lines.append("-" * 60)

    # Suggested actions
    actions = result.get("suggested_actions", [])
    if actions:
        lines.append("  Suggested Actions:")
        for i, a in enumerate(actions[:5], 1):
            params_str = ""
            if a.get("parameters"):
                params_str = " | " + ", ".join(f"{k}={v}" for k, v in a["parameters"].items() if v)
            lines.append(f"    {i}. [{a.get('confidence', 0):.0%}] {a.get('description', a.get('action', '?'))}{params_str}")
        lines.append("-" * 60)

    # Top action
    top = result.get("top_action")
    if top:
        lines.append(f"  Top Action: {top}")

    # Searchable PDF
    pdf = result.get("searchable_pdf")
    if pdf:
        lines.append(f"  Searchable PDF: {pdf}")

    lines.append("=" * 60)
    return "\n".join(lines)


def results_to_csv(results: List[Dict[str, Any]]) -> str:
    """Convert list of results to CSV string."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["file", "type", "confidence", "top_action", "text_preview", "error"])
    for r in results:
        src = r.get("metadata", {}).get("source", "?")
        writer.writerow([
            src,
            r.get("document_type", ""),
            f"{r.get('confidence', 0):.2f}",
            r.get("top_action", ""),
            (r.get("text", "") or "")[:100].replace("\n", " "),
            r.get("error", {}).get("message", "") if not r.get("ok") else "",
        ])
    return output.getvalue()


def process_single_file(
    file_path: Optional[str] = None,
    file_url: Optional[str] = None,
    file_type: Optional[int] = None,
    output_format: str = "pretty",
    output_path: Optional[Path] = None,
    make_searchable_pdf: bool = False,
) -> Dict[str, Any]:
    """
    Process a single document and return the result dict.
    Also write output if output_path is provided.
    """
    if not file_path and not file_url:
        return error_response("INPUT_ERROR", "file_path or file_url required")

    # OCR (with retry on 5xx/timeout)
    try:
        ocr_result = parse_document_with_retry(file_path=file_path, file_url=file_url, file_type=file_type)
    except Exception as e:
        return error_response("OCR_ERROR", f"OCR failed: {e}")

    if not ocr_result.get("ok", False):
        return error_response("OCR_ERROR", ocr_result.get("error", {}).get("message", "Unknown OCR error"))

    text = ocr_result.get("text", "")
    pruned_result = ocr_result.get("result", {})

    # Classify
    try:
        classification = classify(text)
    except Exception as e:
        return error_response("CLASSIFY_ERROR", f"Classification failed: {e}")

    doc_type = classification.doc_type
    confidence = classification.confidence

    # Actions
    try:
        actions = suggest_actions(
            doc_type=doc_type,
            text=text,
            metadata={
                "pages": len(pruned_result.get("layoutParsingResults", [])) if isinstance(pruned_result, dict) else 0,
                "backend": os.getenv("OCR_BACKEND", "auto"),
            },
            pruned_result=pruned_result,
        )
        actions_dict = actions_to_dict(actions)
    except Exception as e:
        actions_dict = []
        # Log but continue
        print(f"Warning: action suggestion failed: {e}", file=sys.stderr)

    # Extract structured fields from all action parameters
    extracted_fields = {}
    for a in actions:
        if a.parameters:
            for k, v in a.parameters.items():
                if v and k not in extracted_fields:
                    extracted_fields[k] = v

    # Build response (C方案: structured data only, no agent_prompt)
    response = {
        "ok": True,
        "document_type": doc_type,
        "confidence": confidence,
        "text": text,
        "pruned_result": pruned_result,
        "suggested_actions": actions_dict,
        "extracted_fields": extracted_fields,
        "top_action": actions[0].name if actions else None,
        "metadata": {
            "pages": len(pruned_result.get("layoutParsingResults", [])) if isinstance(pruned_result, dict) else 0,
            "backend": os.getenv("OCR_BACKEND", "auto"),
            "source": file_path or file_url,
        },
    }

    # Write to file if requested
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            if output_format == "text":
                f.write(text)
            elif output_format == "csv":
                f.write(results_to_csv([response]))
            else:
                json.dump(response, f, ensure_ascii=False, indent=2)
        print(f"Saved: {output_path}", file=sys.stderr)

    # Optionally generate searchable PDF
    if make_searchable_pdf:
        pdf_out = (output_path or Path("output")).with_suffix(".searchable.pdf")
        try:
            from make_searchable_pdf import make_searchable_pdf
            input_file = Path(file_path) if file_path else None
            if input_file and input_file.exists():
                # Pass the full OCR result (contains layoutParsingResults) to enable bbox-based text placement
                success = make_searchable_pdf(input_file, pruned_result, pdf_out)
                if success:
                    print(f"Searchable PDF: {pdf_out}", file=sys.stderr)
                    response["searchable_pdf"] = str(pdf_out)
        except ImportError:
            print("Warning: make_searchable_pdf module not available. Install reportlab, pdf2image, pillow.", file=sys.stderr)
        except Exception as e:
            print(f"Warning: searchable PDF generation failed: {e}", file=sys.stderr)

    return response


# =============================================================================
# Main
# =============================================================================

def batch_mode(args):
    """Process all files in a directory (parallel)."""
    batch_dir = Path(args.batch_dir)
    if not batch_dir.exists():
        print(f"Error: batch directory not found: {batch_dir}", file=sys.stderr)
        sys.exit(1)

    exts = {".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}
    files = [p for p in batch_dir.iterdir() if p.is_file() and p.suffix.lower() in exts]
    if not files:
        print(f"No supported files found in {batch_dir} (extensions: {', '.join(exts)})", file=sys.stderr)
        sys.exit(1)

    workers = max(1, args.workers or 3)
    print(f"Batch processing {len(files)} files with {workers} workers...", file=sys.stderr)

    results = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        future_map = {
            pool.submit(
                process_single_file,
                file_path=str(fp),
                file_type=0 if fp.suffix.lower() == ".pdf" else 1,
                output_format="json",
                output_path=None,
            ): fp for fp in files
        }
        for fut in as_completed(future_map):
            fp = future_map[fut]
            try:
                res = fut.result()
            except Exception as e:
                res = error_response("BATCH_ERROR", str(e))
            res["source_file"] = fp.name
            if "metadata" not in res:
                res["metadata"] = {}
            res["metadata"]["source"] = str(fp)
            results.append(res)

    summary = {
        "batch_summary": {
            "total": len(results),
            "success": sum(1 for r in results if r.get("ok")),
            "failed": sum(1 for r in results if not r.get("ok")),
            "by_type": {},
        },
        "results": results,
    }

    for r in results:
        if r.get("ok"):
            dotype = r.get("document_type", "unknown")
            summary["batch_summary"]["by_type"][dotype] = summary["batch_summary"]["by_type"].get(dotype, 0) + 1

    # Output summary
    if args.format == "csv":
        print(results_to_csv(results))
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=2))

    # Optional per-file JSON
    if args.output_dir:
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        for r in results:
            safe_name = Path(r.get("source_file", "result")).stem + ".json"
            out_path = out_dir / safe_name
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(r, f, ensure_ascii=False, indent=2)
        print(f"Individual results written to: {out_dir}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Agent Vision - OCR with agent actions")
    parser.add_argument("--file-path", help="Local file path")
    parser.add_argument("--file-url", help="Remote URL")
    parser.add_argument("--file-type", type=int, choices=[0, 1], help="0=PDF, 1=image (override)")
    parser.add_argument("--output", help="Output file path (single file mode)")
    parser.add_argument("--stdout", action="store_true", help="Print JSON to stdout (single file)")
    parser.add_argument("--format", choices=["json", "text", "pretty", "csv"], default="pretty", help="Output format (single/batch)")
    parser.add_argument("--pretty", action="store_true", help="Pretty print JSON (single file)")

    # Batch mode
    parser.add_argument("--batch-dir", help="Directory containing documents to process in batch")
    parser.add_argument("--output-dir", help="Output directory for batch results (one JSON per file)")
    parser.add_argument("--workers", type=int, default=3, help="Parallel workers for batch mode")

    # Searchable PDF
    parser.add_argument("--make-searchable-pdf", action="store_true", help="Generate searchable PDF (requires reportlab, pypdf, pillow)")

    args = parser.parse_args()

    # Batch mode
    if args.batch_dir:
        batch_mode(args)
        return

    # Single file mode
    if not args.file_path and not args.file_url:
        print(json.dumps(error_response("INPUT_ERROR", "file_path or file_url required"), ensure_ascii=False))
        sys.exit(1)

    response = process_single_file(
        file_path=args.file_path,
        file_url=args.file_url,
        file_type=args.file_type,
        output_format=args.format,
        output_path=Path(args.output) if args.output else None,
        make_searchable_pdf=args.make_searchable_pdf,
    )

    # Output to stdout by default if no --output
    if args.stdout or not args.output:
        if args.format == "text":
            print(response.get("text", ""))
        elif args.format == "pretty" or args.pretty:
            print(format_pretty(response))
        elif args.format == "csv":
            print(results_to_csv([response]))
        else:
            print(json.dumps(response, ensure_ascii=False))


if __name__ == "__main__":
    main()
