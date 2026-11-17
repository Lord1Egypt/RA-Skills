#!/usr/bin/env python3
"""Read a PDF or an image with EmpirioLabs AI document OCR and return its text as Markdown.

Examples:
  python3 ocr.py ./invoice.pdf --out ./invoice.md
  python3 ocr.py https://example.com/paper.pdf --pages 0-2 --out paper.md   # the first three pages
  python3 ocr.py ./scan.png                       # print the Markdown
  python3 ocr.py ./report.pdf --json --out report.json
  python3 ocr.py --job-id JOB_ID --out long.md    # resume a long document's job
  python3 ocr.py --list-models

Prints the Markdown to stdout, or a JSON summary when --out is given. Progress goes to stderr.
Requires the EMPIRIOLABS_API_KEY environment variable. Python 3.8+, standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import empiriolabs_api as api  # noqa: E402

ENDPOINT = "POST /v1/ocr"
REQUEST_TIMEOUT = 600.0
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp", ".gif", ".avif"}


def build_parser():
    parser = argparse.ArgumentParser(
        prog="ocr.py",
        description="Read a PDF or an image (URL or local file) as Markdown with EmpirioLabs AI.",
        epilog=(
            "When --model is omitted, a document OCR model from the live catalog is used.\n"
            "OCR is billed per page at the model's listed price; check --list-models first.\n"
            "Keys: " + api.KEYS_URL + "\nDocs: " + api.DOCS_URL
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("source", nargs="?", help="https URL of the PDF or image, or a local file path.")
    parser.add_argument("--model", help="Model id. See --list-models.")
    parser.add_argument("--type", choices=("pdf", "image"),
                        help="What the source is, when its name does not end in .pdf or an image extension.")
    parser.add_argument("--pages", help="Pages of a PDF to read, counted from 0, for example 0-2 or 0,3,6.")
    parser.add_argument("--table-format", choices=("markdown", "html"), help="How tables are written.")
    parser.add_argument("--param", action="append", metavar="KEY=VALUE",
                        help="Any other model parameter, for example --param extract_header=true. Repeatable.")
    parser.add_argument("--out", help="Save the result here (.json saves the full result, anything else the Markdown).")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing --out file.")
    parser.add_argument("--json", action="store_true", help="Print the full result as JSON instead of Markdown.")
    parser.add_argument("--timeout", type=float, default=1800.0,
                        help="Seconds to wait for the job (default 1800). The job keeps running after a timeout.")
    parser.add_argument("--job-id", help="Wait for an earlier OCR job and print its result.")
    parser.add_argument("--list-models", action="store_true", help="List document OCR models with prices, then exit.")
    return parser


def source_kind(source, forced=None):
    """'pdf' or 'image', from --type or the name of the file."""
    if forced:
        return forced
    if source.startswith("data:"):
        return "pdf" if source.startswith("data:application/pdf") else "image"
    if source.startswith(("http://", "https://")):
        name = urllib.parse.urlsplit(source).path
    else:
        name = source
    suffix = os.path.splitext(name)[1].lower()
    if suffix == ".pdf":
        return "pdf"
    if suffix in IMAGE_SUFFIXES:
        return "image"
    if source.startswith(("http://", "https://")):
        return "pdf"
    raise api.ApiError("Cannot tell whether " + source + " is a PDF or an image. Pass --type pdf or --type image.",
                       exit_code=api.EXIT_USAGE)


def build_body(args, model_id):
    kind = source_kind(args.source, args.type)
    value = api.inline_file(args.source)
    if kind == "pdf":
        document = {"type": "document_url", "document_url": value}
    else:
        document = {"type": "image_url", "image_url": value}
    body = {"model": model_id, "document": document}
    if args.pages:
        body["pages"] = args.pages
    if args.table_format:
        body["table_format"] = args.table_format
    body.update(api.parse_params(args.param))
    return body


def markdown_of(result):
    """The pages' Markdown, in order, or None when the result holds none."""
    if not isinstance(result, dict):
        return None
    pages = result.get("pages")
    if not isinstance(pages, list):
        text = result.get("text") or result.get("markdown")
        return text if isinstance(text, str) else None
    parts = []
    for page in pages:
        if isinstance(page, dict) and isinstance(page.get("markdown"), str) and page["markdown"].strip():
            parts.append(page["markdown"].strip())
    return "\n\n".join(parts)


def finish(args, job, model_id, job_id):
    result = job.get("result") if isinstance(job, dict) and "result" in job else job
    text = markdown_of(result)
    if text is None and not args.json:
        api.log("No Markdown in the result; printing the full result.")
        args.json = True
    pages = result.get("pages") if isinstance(result, dict) else None
    if args.out:
        out = os.path.expanduser(args.out)
        if api.is_dir_target(out):
            path = api.target_path(out, api.default_stem("document"), ".json" if args.json else ".md", 1, 1,
                                   args.overwrite)
        else:
            path = os.path.abspath(out)
            if not args.overwrite:
                path = api.free_path(path)
        if path.lower().endswith(".json") or text is None:
            content = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            content = text
        api.write_bytes(path, (content.rstrip("\n") + "\n").encode("utf-8"))
        api.log("Saved " + path)
        api.print_json({"model": model_id, "job_id": job_id, "file": path,
                        "pages": len(pages) if isinstance(pages, list) else None,
                        "characters": len(text or "")})
    elif args.json:
        api.print_json(result)
    else:
        print(text, flush=True)
    return api.EXIT_OK


def run(args, parser):
    if args.list_models:
        api.print_model_list(api.list_models(), ENDPOINT)
        return api.EXIT_OK
    if args.job_id:
        api.api_key()
        job = api.wait_for_job(args.job_id, timeout=args.timeout, label="OCR job")
        return finish(args, job, job.get("model"), args.job_id)
    if not args.source:
        parser.error("a PDF or image URL or file path is required (or pass --job-id or --list-models)")
    api.api_key()
    model_id, _entry = api.resolve_model(args.model, ENDPOINT)
    body = build_body(args, model_id)
    api.log("Reading the document with " + model_id + " ...")
    payload = api.post_json("/ocr", body, timeout=REQUEST_TIMEOUT).json()
    job_id = api.job_id_of(payload)
    if not job_id:
        return finish(args, {"result": payload}, model_id, None)
    api.log("Job " + job_id + " accepted. Long documents can take a few minutes.")
    job = api.wait_for_job(job_id, timeout=args.timeout, label="OCR job")
    return finish(args, job, model_id, job_id)


def main(argv=None):
    api.setup_console()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args, parser)
    except api.JobTimeout as exc:
        code = api.fail(exc)
        api.log(api.resume_hint("ocr.py", exc.job_id, args.out))
        return code
    except api.ApiError as exc:
        return api.fail(exc)
    except OSError as exc:
        return api.fail(api.ApiError("Could not read or write a file: " + str(exc)))
    except KeyboardInterrupt:
        api.log("Interrupted. A submitted job keeps running; resume it with --job-id.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
