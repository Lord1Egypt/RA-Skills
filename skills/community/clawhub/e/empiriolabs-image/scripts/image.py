#!/usr/bin/env python3
"""Generate or edit images with EmpirioLabs AI and save them to a path you choose.

Examples:
  python3 image.py "a lighthouse at dawn, watercolor" --out ./images/
  python3 image.py "make the sky stormy" --image photo.jpg --out stormy.png
  python3 image.py "a red bicycle" --model flux-2-klein-4b --aspect-ratio 16:9 --out bike.webp
  python3 image.py --list-models

Prints a JSON summary (model, saved files, hosted URLs) to stdout. Progress goes to stderr.
Requires the EMPIRIOLABS_API_KEY environment variable. Python 3.8+, standard library only.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import empiriolabs_api as api  # noqa: E402

ENDPOINT = "POST /v1/images/generations"
REQUEST_TIMEOUT = 330.0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="image.py",
        description="Generate or edit images with EmpirioLabs AI and save them locally.",
        epilog=(
            "When --model is omitted, a featured image model from the live catalog is used.\n"
            "Each request is billed to your EmpirioLabs AI account at the model's listed price.\n"
            "Keys: " + api.KEYS_URL + "\nDocs: " + api.DOCS_URL
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("prompt", nargs="?", help="What to create, or the change to make when --image is given.")
    parser.add_argument("--model", help="Model id, for example flux-2-klein-4b. See --list-models.")
    parser.add_argument("--image", action="append", metavar="URL_OR_PATH",
                        help="Image to edit or use as a reference (https URL or local file). Repeat for several.")
    parser.add_argument("--aspect-ratio", help="Output aspect ratio, for example 1:1, 16:9, or 9:16.")
    parser.add_argument("--size", help="Output size such as 1024x1024, on models that accept it.")
    parser.add_argument("-n", "--count", type=int, help="Number of images to create. Each image is billed.")
    parser.add_argument("--param", action="append", metavar="KEY=VALUE",
                        help="Any other model parameter, for example --param seed=42. Repeatable.")
    parser.add_argument("--out", help="Output file or directory. Default: the current directory.")
    parser.add_argument("--overwrite", action="store_true",
                        help="Replace existing files instead of adding a numeric suffix.")
    parser.add_argument("--no-download", action="store_true", help="Print the hosted URLs without saving files.")
    parser.add_argument("--timeout", type=float, default=600.0,
                        help="Seconds to wait for a queued image job (default 600).")
    parser.add_argument("--job-id", help="Wait for an earlier image job and save its result.")
    parser.add_argument("--list-models", action="store_true", help="List image models with prices, then exit.")
    return parser


def build_body(args, model_id, entry):
    body = {"model": model_id, "prompt": args.prompt, "sync": True, "response_format": "url"}
    if args.aspect_ratio:
        body["aspect_ratio"] = args.aspect_ratio
    if args.size:
        body["size"] = args.size
    if args.count:
        if args.count < 1:
            raise api.ApiError("--count must be 1 or more.", exit_code=api.EXIT_USAGE)
        body["num_images"] = args.count
    if args.image:
        body["image"] = [api.inline_file(value) for value in args.image]
    extra = api.parse_params(args.param)
    if not any(name in extra for name in ("format", "output_format")):
        chosen = api.format_from_path(entry, args.out)
        if chosen:
            body[chosen[0]] = chosen[1]
    body.update(extra)
    return body


def finish(args, payload, model_id, job_id):
    items = api.media_items(payload)
    if not items:
        raise api.ApiError("The request finished without returning an image. Adjust the prompt and try again.")
    urls = [item["url"] for item in items if item.get("url")]
    files = []
    if not args.no_download:
        files = api.save_items(items, args.out, api.default_stem("image"), overwrite=args.overwrite,
                               fallback_ext=".png")
        for path in files:
            api.log("Saved " + path)
    summary = {"model": model_id, "files": files, "urls": urls}
    if job_id:
        summary["job_id"] = job_id
    api.print_json(summary)
    return api.EXIT_OK


def run(args, parser):
    if args.list_models:
        feature = "image_editing" if args.image else None
        api.print_model_list(api.list_models(), ENDPOINT, category="image", feature=feature)
        return api.EXIT_OK
    if args.job_id:
        api.api_key()
        job = api.wait_for_job(args.job_id, timeout=args.timeout, label="Image job")
        return finish(args, job, job.get("model"), args.job_id)
    if not args.prompt:
        parser.error("a prompt is required (or pass --job-id or --list-models)")
    api.api_key()
    feature = "image_editing" if args.image else None
    model_id, entry = api.resolve_model(args.model, ENDPOINT, category="image", feature=feature)
    body = build_body(args, model_id, entry)
    api.log(("Editing" if args.image else "Generating") + " with " + model_id + " ...")
    payload = api.post_json("/images/generations", body, timeout=REQUEST_TIMEOUT).json()
    job_id = api.job_id_of(payload)
    if not api.media_items(payload) and job_id:
        api.log("The image is still rendering. Waiting for job " + job_id + " ...")
        payload = api.wait_for_job(job_id, timeout=args.timeout, label="Image job")
    return finish(args, payload, model_id, job_id)


def main(argv=None):
    api.setup_console()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args, parser)
    except api.JobTimeout as exc:
        code = api.fail(exc)
        api.log(api.resume_hint("image.py", exc.job_id, args.out))
        return code
    except api.ApiError as exc:
        return api.fail(exc)
    except KeyboardInterrupt:
        api.log("Interrupted.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
