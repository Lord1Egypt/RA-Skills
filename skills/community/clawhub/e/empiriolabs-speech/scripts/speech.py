#!/usr/bin/env python3
"""Turn text into speech with EmpirioLabs AI and save the audio file.

Examples:
  python3 speech.py "Welcome to the weekly update." --out welcome.mp3
  python3 speech.py --text-file script.txt --voice Olivia --out narration.wav
  python3 speech.py "Bonjour tout le monde" --model tts-2 --language fr-FR --out bonjour.mp3
  python3 speech.py --list-models
  python3 speech.py --list-voices --model tts-2

Prints a JSON summary (model, voice, saved files, hosted URLs) to stdout. Progress goes to stderr.
Requires the EMPIRIOLABS_API_KEY environment variable. Python 3.8+, standard library only.
"""

from __future__ import annotations

import argparse
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import empiriolabs_api as api  # noqa: E402

ENDPOINT = "POST /v1/audio/speech"
VOICES_ENDPOINT = "GET /v1/voices"
REQUEST_TIMEOUT = 300.0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="speech.py",
        description="Turn text into speech with EmpirioLabs AI and save the audio.",
        epilog=(
            "When --model is omitted, a featured text-to-speech model from the live catalog is used.\n"
            "Speech is billed by input characters or tokens at the model's listed price.\n"
            "Keys: " + api.KEYS_URL + "\nDocs: " + api.DOCS_URL
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("text", nargs="?", help="Text to speak. Use --text-file for long scripts.")
    parser.add_argument("--text-file", metavar="PATH", help="Read the text from a UTF-8 file.")
    parser.add_argument("--model", help="Model id, for example tts-2. See --list-models.")
    parser.add_argument("--voice", help="Voice name or id for the chosen model. See --list-voices.")
    parser.add_argument("--language", help="Language or locale, for example en-US, on models that accept it.")
    parser.add_argument("--format", help="Audio format, for example mp3 or wav. Default: taken from --out.")
    parser.add_argument("--speed", type=float, help="Speaking rate, on models that accept it (1.0 is normal).")
    parser.add_argument("--param", action="append", metavar="KEY=VALUE",
                        help="Any other model parameter, for example --param temperature=0.8. Repeatable.")
    parser.add_argument("--out", help="Output file or directory. Default: the current directory.")
    parser.add_argument("--overwrite", action="store_true",
                        help="Replace existing files instead of adding a numeric suffix.")
    parser.add_argument("--no-download", action="store_true", help="Print the hosted URL without saving the file.")
    parser.add_argument("--timeout", type=float, default=600.0,
                        help="Seconds to wait if the audio is delivered as a job (default 600).")
    parser.add_argument("--list-models", action="store_true", help="List text-to-speech models with prices, then exit.")
    parser.add_argument("--list-voices", action="store_true",
                        help="List voices for --model (or the default model), then exit.")
    return parser


def read_text(args, parser):
    if args.text and args.text_file:
        parser.error("pass the text or --text-file, not both")
    if args.text_file:
        with open(os.path.expanduser(args.text_file), "r", encoding="utf-8") as handle:
            return handle.read().strip()
    return (args.text or "").strip()


def build_body(args, model_id, entry, text):
    spec = api.param_spec(entry, "input")
    limit = spec.get("max") if spec else None
    if isinstance(limit, (int, float)) and len(text) > limit:
        raise api.ApiError(
            model_id + " accepts up to " + str(int(limit)) + " characters per request and this text has "
            + str(len(text)) + ". Split it into parts or choose another model with --list-models.",
            exit_code=api.EXIT_USAGE,
        )
    body = {"model": model_id, "input": text}
    if args.voice:
        body["voice"] = args.voice
    if args.language:
        body["language"] = args.language
    if args.speed is not None:
        body["speed"] = args.speed
    extra = api.parse_params(args.param)
    if args.format:
        body["output_format"] = api.match_option(entry, "output_format", args.format) or args.format
    elif "output_format" not in extra and "format" not in extra:
        chosen = api.format_from_path(entry, args.out, names=("output_format", "format"))
        if chosen:
            body[chosen[0]] = chosen[1]
    body.update(extra)
    return body


def list_voices(args):
    model_id, entry = api.resolve_model(args.model, ENDPOINT, category="audio")
    if entry is not None and not api.supports(entry, VOICES_ENDPOINT):
        spec = api.param_spec(entry, "voice")
        options = (spec or {}).get("options") or []
        if options:
            for option in options:
                print(str(option))
            api.log(model_id + " voices from its catalog entry. Pass one with --voice.")
        else:
            api.log(model_id + " has no voice list. See " + str(entry.get("api_url") or api.DOCS_URL))
        return api.EXIT_OK
    query = {"model": model_id}
    if args.language:
        query["language"] = args.language
    payload = api.get_json("/voices?" + urllib.parse.urlencode(query))
    voices = payload.get("data") if isinstance(payload, dict) else payload
    for voice in voices or []:
        if not isinstance(voice, dict):
            print(str(voice))
            continue
        details = [str(voice.get(k)) for k in ("name", "gender", "language", "accent") if voice.get(k)]
        print(str(voice.get("id") or voice.get("voice_id") or voice.get("name")).ljust(28) + " " + ", ".join(details))
    api.log(str(len(voices or [])) + " voices for " + model_id + ". Pass one with --voice.")
    return api.EXIT_OK


def save_audio(args, resp, model_id):
    stem = api.default_stem("speech")
    if resp.content_type.startswith("audio/") or resp.content_type == "application/octet-stream":
        ext = api.extension_for(resp.content_type, fallback=".mp3")
        if args.no_download:
            raise api.ApiError("This model returns the audio directly, so there is no hosted URL. "
                               "Run without --no-download to save it.")
        path = api.write_bytes(api.target_path(args.out, stem, ext, 1, 1, args.overwrite), resp.body)
        api.log("Saved " + path)
        return [path], []
    payload = resp.json()
    items = api.media_items(payload)
    job_id = api.job_id_of(payload)
    if not items and job_id:
        api.log("Waiting for job " + job_id + " ...")
        payload = api.wait_for_job(job_id, timeout=args.timeout, label="Speech job")
        items = api.media_items(payload)
    if not items:
        raise api.ApiError("The request finished without returning audio.")
    urls = [item["url"] for item in items if item.get("url")]
    files = []
    if not args.no_download:
        files = api.save_items(items, args.out, stem, overwrite=args.overwrite, fallback_ext=".mp3")
        for path in files:
            api.log("Saved " + path)
    return files, urls


def run(args, parser):
    if args.list_models:
        api.print_model_list(api.list_models(), ENDPOINT, category="audio")
        return api.EXIT_OK
    if args.list_voices:
        api.api_key()
        return list_voices(args)
    text = read_text(args, parser)
    if not text:
        parser.error("text to speak is required (or pass --text-file, --list-models, or --list-voices)")
    api.api_key()
    model_id, entry = api.resolve_model(args.model, ENDPOINT, category="audio")
    body = build_body(args, model_id, entry, text)
    api.log("Synthesizing " + str(len(text)) + " characters with " + model_id + " ...")
    resp = api.request("POST", "/audio/speech", json_body=body, timeout=REQUEST_TIMEOUT, accept="*/*")
    files, urls = save_audio(args, resp, model_id)
    summary = {"model": model_id, "files": files, "urls": urls}
    if body.get("voice"):
        summary["voice"] = body["voice"]
    api.print_json(summary)
    return api.EXIT_OK


def main(argv=None):
    api.setup_console()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args, parser)
    except api.ApiError as exc:
        return api.fail(exc)
    except OSError as exc:
        return api.fail(api.ApiError("Could not read or write a file: " + str(exc)))
    except KeyboardInterrupt:
        api.log("Interrupted.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
