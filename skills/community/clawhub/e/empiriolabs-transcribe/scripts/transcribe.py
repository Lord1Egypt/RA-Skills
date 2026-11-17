#!/usr/bin/env python3
"""Transcribe an audio or video file to text with EmpirioLabs AI.

Examples:
  python3 transcribe.py https://example.com/interview.mp3
  python3 transcribe.py meeting.m4a --out meeting.txt
  python3 transcribe.py https://example.com/talk.mp4 --model deepgram-nova-3 --diarize --out talk.json
  python3 transcribe.py --job-id JOB_ID          # resume an earlier job
  python3 transcribe.py --list-models

Prints the transcript to stdout. With --out, saves it (plain text, or the full result
when the path ends in .json) and prints a JSON summary instead. Progress goes to stderr.
Requires the EMPIRIOLABS_API_KEY environment variable. Python 3.8+, standard library only.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import empiriolabs_api as api  # noqa: E402

ENDPOINT = "POST /v1/audio/transcriptions"
REQUEST_TIMEOUT = 600.0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="transcribe.py",
        description="Transcribe an audio or video file (URL or local path) with EmpirioLabs AI.",
        epilog=(
            "When --model is omitted, a featured transcription model from the live catalog is used.\n"
            "Transcription is billed by audio length at the model's listed price.\n"
            "Keys: " + api.KEYS_URL + "\nDocs: " + api.DOCS_URL
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("source", nargs="?", help="https URL of the audio or video file, or a local file path.")
    parser.add_argument("--model", help="Model id, for example whisper-large-v3-turbo. See --list-models.")
    parser.add_argument("--language", help="Spoken language hint, for example en, on models that accept it.")
    parser.add_argument("--diarize", action="store_true", help="Label speakers, on models that support it.")
    parser.add_argument("--param", action="append", metavar="KEY=VALUE",
                        help="Any other model parameter, for example --param smart_format=true. Repeatable.")
    parser.add_argument("--out", help="Save the transcript here (.json saves the full result).")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing --out file.")
    parser.add_argument("--json", action="store_true", help="Print the full result as JSON instead of plain text.")
    parser.add_argument("--timeout", type=float, default=1800.0,
                        help="Seconds to wait for the job (default 1800). The job keeps running after a timeout.")
    parser.add_argument("--no-wait", action="store_true", help="Submit the job, print its id, and exit.")
    parser.add_argument("--job-id", help="Wait for an earlier transcription job and print its result.")
    parser.add_argument("--list-models", action="store_true", help="List transcription models with prices, then exit.")
    return parser


def submit(args, model_id):
    extra = api.parse_params(args.param)
    if args.source.startswith(("http://", "https://")):
        body = {"model": model_id, "file_url": args.source}
        if args.language:
            body["language"] = args.language
        if args.diarize:
            body["diarize"] = True
        body.update(extra)
        return api.post_json("/audio/transcriptions", body, timeout=REQUEST_TIMEOUT)
    path = os.path.expanduser(args.source)
    if not os.path.isfile(path):
        raise api.ApiError("File not found: " + args.source + ". Pass an https URL or the path of a local file.",
                           exit_code=api.EXIT_USAGE)
    fields = [("model", model_id)]
    if args.language:
        fields.append(("language", args.language))
    if args.diarize:
        fields.append(("diarize", "true"))
    for key, value in extra.items():
        fields.append((key, value if isinstance(value, str) else json.dumps(value)))
    with open(path, "rb") as handle:
        payload = handle.read()
    ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
    data, content_type = api.encode_multipart(fields, [("file", os.path.basename(path), ctype, payload)])
    api.log("Uploading " + os.path.basename(path) + " (" + str(len(payload) // 1024) + " KB) ...")
    return api.request("POST", "/audio/transcriptions", data=data, content_type=content_type,
                       timeout=REQUEST_TIMEOUT)


def transcript_text(result):
    if isinstance(result, str):
        return result
    if not isinstance(result, dict):
        return None
    text = result.get("text") or result.get("transcript")
    if isinstance(text, str):
        return text
    segments = result.get("segments")
    if isinstance(segments, list):
        parts = [s.get("text", "").strip() for s in segments if isinstance(s, dict) and s.get("text")]
        if parts:
            return " ".join(parts)
    return None


def finish(args, job, model_id, job_id):
    result = job.get("result") if isinstance(job, dict) and "result" in job else job
    text = transcript_text(result)
    if text is None and not args.json:
        api.log("No plain-text transcript in the result; printing the full result.")
        args.json = True
    if args.out:
        out = os.path.expanduser(args.out)
        if api.is_dir_target(out):
            ext = ".json" if args.json else ".txt"
            path = api.target_path(out, api.default_stem("transcript"), ext, 1, 1, args.overwrite)
        else:
            path = os.path.abspath(out)
            if not args.overwrite:
                path = api.free_path(path)
        if path.lower().endswith(".json"):
            content = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            content = text if text is not None else json.dumps(result, indent=2, ensure_ascii=False)
        api.write_bytes(path, (content.rstrip("\n") + "\n").encode("utf-8"))
        api.log("Saved " + path)
        summary = {"model": model_id, "job_id": job_id, "file": path,
                   "characters": len(text or "")}
        if isinstance(result, dict):
            for key in ("language", "duration"):
                if result.get(key) is not None:
                    summary[key] = result[key]
        api.print_json(summary)
    elif args.json:
        api.print_json(result)
    else:
        print(text, flush=True)
    return api.EXIT_OK


def run(args, parser):
    if args.list_models:
        api.print_model_list(api.list_models(), ENDPOINT, category="transcription")
        return api.EXIT_OK
    if args.job_id:
        api.api_key()
        job = api.wait_for_job(args.job_id, timeout=args.timeout, label="Transcription job")
        return finish(args, job, job.get("model"), args.job_id)
    if not args.source:
        parser.error("an audio or video URL or file path is required (or pass --job-id or --list-models)")
    api.api_key()
    model_id, _entry = api.resolve_model(args.model, ENDPOINT, category="transcription")
    api.log("Transcribing with " + model_id + " ...")
    payload = submit(args, model_id).json()
    job_id = api.job_id_of(payload)
    if not job_id:
        if transcript_text(payload) is not None:
            return finish(args, {"result": payload}, model_id, None)
        raise api.ApiError("The service did not return a job id for this transcription.")
    if args.no_wait:
        api.print_json({"model": model_id, "job_id": job_id, "status": payload.get("status") or "processing"})
        api.log(api.resume_hint("transcribe.py", job_id, args.out))
        return api.EXIT_OK
    job = api.wait_for_job(job_id, timeout=args.timeout, label="Transcription job")
    return finish(args, job, model_id, job_id)


def main(argv=None):
    api.setup_console()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args, parser)
    except api.JobTimeout as exc:
        code = api.fail(exc)
        api.log(api.resume_hint("transcribe.py", exc.job_id, args.out))
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
