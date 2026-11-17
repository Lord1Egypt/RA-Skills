#!/usr/bin/env python3
"""Generate a video with EmpirioLabs AI, wait for it to finish, and save it.

Examples:
  python3 video.py "a paper boat drifting down a rainy street" --out boat.mp4
  python3 video.py "the camera slowly pushes in" --image https://example.com/still.png --out push.mp4
  python3 video.py "waves at sunset" --model hunyuan-video-1-5 --resolution 480p --duration 5 --out waves.mp4
  python3 video.py "city timelapse" --no-wait          # print the job id and return
  python3 video.py --job-id JOB_ID --out city.mp4      # resume an earlier job
  python3 video.py --list-models

Prints a JSON summary (model, job id, saved files, hosted URLs) to stdout. Progress goes to stderr.
Requires the EMPIRIOLABS_API_KEY environment variable. Python 3.8+, standard library only.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import empiriolabs_api as api  # noqa: E402

ENDPOINT = "POST /v1/videos/generations"
REQUEST_TIMEOUT = 120.0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="video.py",
        description="Generate a video with EmpirioLabs AI, wait for the job, and save the file.",
        epilog=(
            "When --model is omitted, a featured video model from the live catalog is used.\n"
            "Video is billed per clip or per second of output at the model's listed price; check\n"
            "--list-models before long or high-resolution runs.\n"
            "Keys: " + api.KEYS_URL + "\nDocs: " + api.DOCS_URL
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("prompt", nargs="?", help="Description of the video to create.")
    parser.add_argument("--model", help="Model id, for example hunyuan-video-1-5. See --list-models.")
    parser.add_argument("--image", action="append", metavar="URL",
                        help="Public https URL of a start image (image-to-video). Repeat to pass reference images.")
    parser.add_argument("--duration", type=int, help="Length in seconds. Supported values depend on the model.")
    parser.add_argument("--resolution", help="Output resolution, for example 480p, 720p, or 1080p.")
    parser.add_argument("--aspect-ratio", help="Output aspect ratio, for example 16:9 or 9:16.")
    parser.add_argument("--audio", dest="audio", action="store_true", default=None,
                        help="Also generate an audio track, on models that support it.")
    parser.add_argument("--no-audio", dest="audio", action="store_false", help="Ask for a silent clip.")
    parser.add_argument("--param", action="append", metavar="KEY=VALUE",
                        help="Any other model parameter, for example --param seed=7. Repeatable.")
    parser.add_argument("--out", help="Output file or directory. Default: the current directory.")
    parser.add_argument("--overwrite", action="store_true",
                        help="Replace existing files instead of adding a numeric suffix.")
    parser.add_argument("--no-download", action="store_true", help="Print the hosted URL without saving the file.")
    parser.add_argument("--timeout", type=float, default=1800.0,
                        help="Seconds to wait for the job (default 1800). The job keeps running after a timeout.")
    parser.add_argument("--no-wait", action="store_true", help="Submit the job, print its id, and exit.")
    parser.add_argument("--job-id", help="Wait for an earlier video job and save its result.")
    parser.add_argument("--list-models", action="store_true", help="List video models with prices, then exit.")
    return parser


def check_images(images):
    for value in images or []:
        if not value.startswith(("http://", "https://")):
            raise api.ApiError(
                "--image needs a public https URL. To animate a local picture, publish it first; the "
                "empiriolabs-image skill prints a hosted URL for every image it creates.",
                exit_code=api.EXIT_USAGE,
            )


def build_body(args, model_id):
    body = {"model": model_id}
    if args.prompt:
        body["prompt"] = args.prompt
    images = args.image or []
    if len(images) == 1:
        body["image"] = images[0]
    elif images:
        body["images"] = images
    if args.duration is not None:
        body["duration"] = args.duration
    if args.resolution:
        body["resolution"] = args.resolution
    if args.aspect_ratio:
        body["aspect_ratio"] = args.aspect_ratio
    if args.audio is not None:
        body["generate_audio"] = args.audio
    body.update(api.parse_params(args.param))
    return body


def finish(args, job, model_id, job_id):
    items = api.media_items(job)
    if not items:
        raise api.ApiError("Job " + str(job_id) + " finished without returning a video.")
    urls = [item["url"] for item in items if item.get("url")]
    files = []
    if not args.no_download:
        files = api.save_items(items, args.out, api.default_stem("video"), overwrite=args.overwrite,
                               fallback_ext=".mp4", timeout=600.0)
        for path in files:
            api.log("Saved " + path)
    summary = {"model": model_id, "job_id": job_id, "files": files, "urls": urls}
    api.print_json(summary)
    return api.EXIT_OK


def run(args, parser):
    if args.list_models:
        api.print_model_list(api.list_models(), ENDPOINT, category="video")
        return api.EXIT_OK
    if args.job_id:
        api.api_key()
        job = api.wait_for_job(args.job_id, timeout=args.timeout, label="Video job")
        return finish(args, job, job.get("model"), args.job_id)
    if not args.prompt and not args.image:
        parser.error("a prompt or --image is required (or pass --job-id or --list-models)")
    check_images(args.image)
    api.api_key()
    model_id, _entry = api.resolve_model(args.model, ENDPOINT, category="video")
    body = build_body(args, model_id)
    api.log("Submitting a video job to " + model_id + " ...")
    payload = api.post_json("/videos/generations", body, timeout=REQUEST_TIMEOUT).json()
    if api.media_items(payload):
        return finish(args, payload, model_id, api.job_id_of(payload))
    job_id = api.job_id_of(payload)
    if not job_id:
        raise api.ApiError("The service did not return a job id for this video request.")
    if args.no_wait:
        api.print_json({"model": model_id, "job_id": job_id, "status": payload.get("status") or "processing"})
        api.log(api.resume_hint("video.py", job_id, args.out))
        return api.EXIT_OK
    api.log("Job " + job_id + " accepted. Video jobs usually take one to fifteen minutes.")
    job = api.wait_for_job(job_id, timeout=args.timeout, label="Video job")
    return finish(args, job, model_id, job_id)


def main(argv=None):
    api.setup_console()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args, parser)
    except api.JobTimeout as exc:
        code = api.fail(exc)
        api.log(api.resume_hint("video.py", exc.job_id, args.out))
        return code
    except api.ApiError as exc:
        return api.fail(exc)
    except KeyboardInterrupt:
        api.log("Interrupted. A submitted job keeps running; resume it with --job-id.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
