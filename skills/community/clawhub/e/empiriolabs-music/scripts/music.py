#!/usr/bin/env python3
"""Generate music or sound effects with EmpirioLabs AI, wait for the result, and save the audio file.

Examples:
  python3 music.py "an upbeat synthwave track with a driving bassline" --duration 30 --out ./audio/track.mp3
  python3 music.py "a gentle folk song about rain" --lyrics-file ./lyrics.txt --out song.mp3
  python3 music.py "footsteps on gravel, then a door closing" --model MODEL_ID --duration 5 --out steps.wav
  python3 music.py "a film score that swells slowly" --no-wait      # print the job id and return
  python3 music.py --job-id JOB_ID --out score.mp3                  # resume an earlier job
  python3 music.py --list-models

Prints a JSON summary (model, job id, saved files, hosted URLs) to stdout. Progress goes to stderr.
Requires the EMPIRIOLABS_API_KEY environment variable. Python 3.8+, standard library only.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import empiriolabs_api as api  # noqa: E402

ENDPOINT = "POST /v1/audio/generations"
REQUEST_TIMEOUT = 600.0
DURATION_NAMES = ("audio_duration", "duration")
FORMAT_NAMES = ("format", "output_format", "response_format")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="music.py",
        description="Generate music or sound effects with EmpirioLabs AI and save the audio file.",
        epilog=(
            "When --model is omitted, a featured music model from the live catalog is used.\n"
            "Audio is billed per generated second or per request at the model's listed price; check\n"
            "--list-models before long runs.\n"
            "Keys: " + api.KEYS_URL + "\nDocs: " + api.DOCS_URL
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("prompt", nargs="?", help="Description of the music or the sound.")
    parser.add_argument("--model", help="Model id. See --list-models.")
    parser.add_argument("--lyrics", help="Lyrics to sing, on models that take them.")
    parser.add_argument("--lyrics-file", metavar="FILE", help="Read the lyrics from a text file.")
    parser.add_argument("--duration", type=float, help="Length in seconds. Supported values depend on the model.")
    parser.add_argument("--param", action="append", metavar="KEY=VALUE",
                        help="Any other model parameter, for example --param seed=7. Repeatable.")
    parser.add_argument("--out", help="Output file or directory. Default: the current directory.")
    parser.add_argument("--overwrite", action="store_true",
                        help="Replace existing files instead of adding a numeric suffix.")
    parser.add_argument("--no-download", action="store_true", help="Print the hosted URL without saving the file.")
    parser.add_argument("--timeout", type=float, default=1800.0,
                        help="Seconds to wait for the job (default 1800). The job keeps running after a timeout.")
    parser.add_argument("--no-wait", action="store_true", help="Submit the job, print its id, and exit.")
    parser.add_argument("--job-id", help="Wait for an earlier audio job and save its result.")
    parser.add_argument("--list-models", action="store_true", help="List music and sound models with prices, then exit.")
    return parser


def read_lyrics(args):
    if args.lyrics and args.lyrics_file:
        raise api.ApiError("Pass --lyrics or --lyrics-file, not both.", exit_code=api.EXIT_USAGE)
    if not args.lyrics_file:
        return args.lyrics
    path = os.path.expanduser(args.lyrics_file)
    if not os.path.isfile(path):
        raise api.ApiError("Lyrics file not found: " + args.lyrics_file, exit_code=api.EXIT_USAGE)
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read().strip()


def duration_name(entry):
    """The parameter the model uses for the length of the audio."""
    for name in DURATION_NAMES:
        if api.param_spec(entry, name) is not None:
            return name
    return DURATION_NAMES[-1]


def build_body(args, model_id, entry, lyrics):
    body = {"model": model_id, "prompt": args.prompt}
    if lyrics:
        if entry is not None and api.param_spec(entry, "lyrics") is None:
            raise api.ApiError(model_id + " does not take lyrics. Choose a model that does with --list-models, "
                               "or describe the song in the prompt.", exit_code=api.EXIT_USAGE)
        body["lyrics"] = lyrics
    if args.duration is not None:
        seconds = int(args.duration) if float(args.duration).is_integer() else args.duration
        body[duration_name(entry)] = seconds
    chosen = api.format_from_path(entry, args.out, names=FORMAT_NAMES)
    if chosen:
        body[chosen[0]] = chosen[1]
    body.update(api.parse_params(args.param))
    return body


def finish(args, job, model_id, job_id):
    items = api.media_items(job)
    if not items:
        raise api.ApiError("Job " + str(job_id) + " finished without returning audio.")
    urls = [item["url"] for item in items if item.get("url")]
    files = []
    if not args.no_download:
        files = api.save_items(items, args.out, api.default_stem("audio"), overwrite=args.overwrite,
                               fallback_ext=".mp3", timeout=600.0)
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
        job = api.wait_for_job(args.job_id, timeout=args.timeout, label="Audio job")
        return finish(args, job, job.get("model"), args.job_id)
    if not args.prompt:
        parser.error("a description of the music or sound is required (or pass --job-id or --list-models)")
    lyrics = read_lyrics(args)
    api.api_key()
    model_id, entry = api.resolve_model(args.model, ENDPOINT)
    body = build_body(args, model_id, entry, lyrics)
    api.log("Submitting an audio job to " + model_id + " ...")
    payload = api.post_json("/audio/generations", body, timeout=REQUEST_TIMEOUT).json()
    if api.media_items(payload):
        return finish(args, payload, model_id, api.job_id_of(payload))
    job_id = api.job_id_of(payload)
    if not job_id:
        raise api.ApiError("The service did not return a job id for this audio request.")
    if args.no_wait:
        api.print_json({"model": model_id, "job_id": job_id, "status": payload.get("status") or "processing"})
        api.log(api.resume_hint("music.py", job_id, args.out))
        return api.EXIT_OK
    api.log("Job " + job_id + " accepted. Audio jobs usually take under five minutes.")
    job = api.wait_for_job(job_id, timeout=args.timeout, label="Audio job")
    return finish(args, job, model_id, job_id)


def main(argv=None):
    api.setup_console()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args, parser)
    except api.JobTimeout as exc:
        code = api.fail(exc)
        api.log(api.resume_hint("music.py", exc.job_id, args.out))
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
