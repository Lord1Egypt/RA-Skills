#!/usr/bin/env python3
"""Generate a 3D model with EmpirioLabs AI, wait for it to finish, and save the file.

Examples:
  python3 model3d.py --image ./chair.png --out ./models/chair.glb
  python3 model3d.py --image https://example.com/shoe.png --resolution 512 --out shoe.glb
  python3 model3d.py "a low-poly wooden chair" --model MODEL_ID --out chair.glb
  python3 model3d.py --image ./chair.png --no-wait      # print the job id and return
  python3 model3d.py --job-id JOB_ID --out chair.glb    # resume an earlier job
  python3 model3d.py --list-models

Prints a JSON summary (model, job id, saved files, hosted URLs) to stdout. Progress goes to stderr.
Requires the EMPIRIOLABS_API_KEY environment variable. Python 3.8+, standard library only.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import empiriolabs_api as api  # noqa: E402

ENDPOINT = "POST /v1/3d/generations"
REQUEST_TIMEOUT = 300.0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="model3d.py",
        description="Generate a 3D model with EmpirioLabs AI, wait for the job, and save the file.",
        epilog=(
            "When --model is omitted, a featured 3D model from the live catalog is used.\n"
            "3D generation is billed per request at the model's listed price, and the price depends on\n"
            "the resolution; check --list-models first.\n"
            "Keys: " + api.KEYS_URL + "\nDocs: " + api.DOCS_URL
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("prompt", nargs="?", help="Description of the object, on models that take text.")
    parser.add_argument("--model", help="Model id. See --list-models.")
    parser.add_argument("--image", metavar="URL_OR_FILE",
                        help="Picture of the object: a public https URL or a local file.")
    parser.add_argument("--resolution", help="Detail level, for example 512 or 1024. Values depend on the model.")
    parser.add_argument("--param", action="append", metavar="KEY=VALUE",
                        help="Any other model parameter, for example --param seed=7. Repeatable.")
    parser.add_argument("--out", help="Output file or directory. Default: the current directory.")
    parser.add_argument("--overwrite", action="store_true",
                        help="Replace existing files instead of adding a numeric suffix.")
    parser.add_argument("--no-download", action="store_true", help="Print the hosted URL without saving the file.")
    parser.add_argument("--timeout", type=float, default=1800.0,
                        help="Seconds to wait for the job (default 1800). The job keeps running after a timeout.")
    parser.add_argument("--no-wait", action="store_true", help="Submit the job, print its id, and exit.")
    parser.add_argument("--job-id", help="Wait for an earlier 3D job and save its result.")
    parser.add_argument("--list-models", action="store_true", help="List 3D models with prices, then exit.")
    return parser


def check_inputs(args, entry):
    """Refuse a request the chosen model cannot run, before anything is billed."""
    if entry is None:
        return
    image = api.param_spec(entry, "image")
    prompt = api.param_spec(entry, "prompt")
    if args.image and image is None:
        raise api.ApiError(entry["id"] + " does not take an image. Pass a description instead.",
                           exit_code=api.EXIT_USAGE)
    if args.prompt and prompt is None:
        raise api.ApiError(entry["id"] + " builds the model from a picture and takes no description. "
                           "Pass --image, or choose a model that takes text with --list-models.",
                           exit_code=api.EXIT_USAGE)
    if not args.image and image is not None and (image.get("required") or prompt is None):
        raise api.ApiError(entry["id"] + " needs a picture of the object. Pass --image.",
                           exit_code=api.EXIT_USAGE)


def build_body(args, model_id, entry):
    body = {"model": model_id}
    if args.image:
        body["image"] = api.inline_file(args.image)
    if args.prompt:
        body["prompt"] = args.prompt
    if args.resolution:
        body["resolution"] = api.match_option(entry, "resolution", args.resolution) or args.resolution
    chosen = api.format_from_path(entry, args.out, names=("file_format", "format", "output_format"))
    if chosen:
        body[chosen[0]] = chosen[1]
    body.update(api.parse_params(args.param))
    return body


def finish(args, job, model_id, job_id):
    items = api.media_items(job)
    if not items:
        raise api.ApiError("Job " + str(job_id) + " finished without returning a 3D file.")
    urls = [item["url"] for item in items if item.get("url")]
    files = []
    if not args.no_download:
        files = api.save_items(items, args.out, api.default_stem("model"), overwrite=args.overwrite,
                               fallback_ext=".glb", timeout=600.0)
        for path in files:
            api.log("Saved " + path)
    api.print_json({"model": model_id, "job_id": job_id, "files": files, "urls": urls})
    return api.EXIT_OK


def run(args, parser):
    if args.list_models:
        api.print_model_list(api.list_models(), ENDPOINT)
        return api.EXIT_OK
    if args.job_id:
        api.api_key()
        job = api.wait_for_job(args.job_id, timeout=args.timeout, label="3D job")
        return finish(args, job, job.get("model"), args.job_id)
    if not args.prompt and not args.image:
        parser.error("--image or a description is required (or pass --job-id or --list-models)")
    api.api_key()
    model_id, entry = api.resolve_model(args.model, ENDPOINT)
    check_inputs(args, entry)
    body = build_body(args, model_id, entry)
    api.log("Submitting a 3D job to " + model_id + " ...")
    payload = api.post_json("/3d/generations", body, timeout=REQUEST_TIMEOUT).json()
    if api.media_items(payload):
        return finish(args, payload, model_id, api.job_id_of(payload))
    job_id = api.job_id_of(payload)
    if not job_id:
        raise api.ApiError("The service did not return a job id for this 3D request.")
    if args.no_wait:
        api.print_json({"model": model_id, "job_id": job_id, "status": payload.get("status") or "processing"})
        api.log(api.resume_hint("model3d.py", job_id, args.out))
        return api.EXIT_OK
    api.log("Job " + job_id + " accepted. 3D jobs usually take one to five minutes.")
    job = api.wait_for_job(job_id, timeout=args.timeout, label="3D job")
    return finish(args, job, model_id, job_id)


def main(argv=None):
    api.setup_console()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args, parser)
    except api.JobTimeout as exc:
        code = api.fail(exc)
        api.log(api.resume_hint("model3d.py", exc.job_id, args.out))
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
