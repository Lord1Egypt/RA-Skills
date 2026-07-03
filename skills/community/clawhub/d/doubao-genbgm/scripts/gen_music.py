#!/usr/bin/env python3
"""
Doubao Music Generation Script: Supports vocal song (GenSong) and instrumental BGM (GenBGM) generation.

Usage (generate BGM):
  python3 gen_music.py --mode bgm --text "Cafe light music, piano and guitar, relaxing and healing" --duration 60

Usage (generate song from prompt):
  python3 gen_music.py --mode song --prompt "A song about the starry sky" --genre "Pop" --mood "Dreamy/Ethereal"

Usage (generate song from lyrics):
  python3 gen_music.py --mode song --lyrics-file my_lyrics.txt --genre "Folk" --gender Female

Authentication: Set VOLC_ACCESS_KEY and VOLC_SECRET_KEY in .env file
Dependencies: pip install requests
"""

import argparse
import hashlib
import hmac
import json
import os
import sys
import time
import datetime

try:
    import requests
except ImportError:
    print("Error: requests is not installed, please run: pip install requests", file=sys.stderr)
    sys.exit(1)


# ─── .env Loading ────────────────────────────────────────────────────────────

def load_dotenv():
    """Load environment variables from .env file (script directory first, then parent directory). Does not overwrite existing environment variables."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, ".env"),
        os.path.join(script_dir, "..", ".env"),
    ]
    for path in candidates:
        path = os.path.normpath(path)
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = value
            break


# ─── Volcano Engine Signing ──────────────────────────────────────────────────

SERVICE = "imagination"
REGION = "cn-beijing"
HOST = "open.volcengineapi.com"
API_VERSION = "2024-08-12"


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _hmac_sha256(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def build_auth_headers(access_key: str, secret_key: str, action: str, body: dict) -> dict:
    """Build Volcano Engine HMAC-SHA256 signature headers."""
    now = datetime.datetime.utcnow()
    x_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_str = now.strftime("%Y%m%d")

    body_bytes = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    body_hash = _sha256_hex(body_bytes)

    # Canonical URI & Query
    uri = "/"
    query_string = f"Action={action}&Version={API_VERSION}"

    # Canonical Headers
    signed_headers = "content-type;host;x-content-sha256;x-date"
    canonical_headers = (
        f"content-type:application/json\n"
        f"host:{HOST}\n"
        f"x-content-sha256:{body_hash}\n"
        f"x-date:{x_date}\n"
    )

    canonical_request = "\n".join([
        "POST",
        uri,
        query_string,
        canonical_headers,
        signed_headers,
        body_hash,
    ])

    credential_scope = f"{date_str}/{REGION}/{SERVICE}/request"
    string_to_sign = "\n".join([
        "HMAC-SHA256",
        x_date,
        credential_scope,
        _sha256_hex(canonical_request.encode("utf-8")),
    ])

    signing_key = _hmac_sha256(
        _hmac_sha256(
            _hmac_sha256(
                _hmac_sha256(secret_key.encode("utf-8"), date_str),
                REGION,
            ),
            SERVICE,
        ),
        "request",
    )
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    authorization = (
        f"HMAC-SHA256 Credential={access_key}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, "
        f"Signature={signature}"
    )

    return {
        "Content-Type": "application/json",
        "Host": HOST,
        "X-Date": x_date,
        "X-Content-Sha256": body_hash,
        "Authorization": authorization,
    }


def call_api(access_key: str, secret_key: str, action: str, body: dict) -> dict:
    url = f"https://{HOST}/?Action={action}&Version={API_VERSION}"
    headers = build_auth_headers(access_key, secret_key, action, body)
    body_bytes = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

    resp = requests.post(url, headers=headers, data=body_bytes, timeout=30)
    if resp.status_code != 200:
        print(f"Error: HTTP {resp.status_code}\n{resp.text}", file=sys.stderr)
        sys.exit(1)
    return resp.json()


# ─── Task Submission ──────────────────────────────────────────────────────────

def submit_bgm(access_key: str, secret_key: str, args) -> str:
    body = {"Text": args.text}

    if args.duration:
        body["Duration"] = args.duration
    if args.version:
        body["Version"] = args.version
    if args.rewrite:
        body["EnableInputRewrite"] = True
    if args.callback:
        body["CallbackURL"] = args.callback

    # Segments (v5.0 structured segments)
    if args.segments:
        try:
            body["Segments"] = json.loads(args.segments)
        except json.JSONDecodeError as e:
            print(f"Error: --segments JSON format invalid: {e}", file=sys.stderr)
            sys.exit(1)

    action = "GenBGM" if args.billing == "prepaid" else "GenBGMForTime"
    print(f"Submitting BGM generation task (Action={action})...")
    print(f"  Description: {args.text}")
    if args.duration:
        print(f"  Duration: {args.duration}s")

    result = call_api(access_key, secret_key, action, body)
    return _extract_task_id(result)


def submit_song(access_key: str, secret_key: str, args) -> str:
    body = {}

    # Text input: prompt or lyrics
    if args.lyrics:
        body["Lyrics"] = args.lyrics
        print(f"  Lyrics: {args.lyrics[:50]}{'...' if len(args.lyrics) > 50 else ''}")
    elif args.prompt:
        body["Prompt"] = args.prompt
        print(f"  Prompt: {args.prompt}")
    else:
        print("Error: --mode song requires --prompt or --lyrics / --lyrics-file", file=sys.stderr)
        sys.exit(1)

    if args.model_version:
        body["ModelVersion"] = args.model_version
    if args.genre:
        body["Genre"] = args.genre
    if args.genre_extra:
        body["GenreExtra"] = args.genre_extra
    if args.mood:
        body["Mood"] = args.mood
    if args.gender:
        body["Gender"] = args.gender
    if args.timbre:
        body["Timbre"] = args.timbre
    if args.duration:
        body["Duration"] = args.duration
    if args.lang:
        body["Lang"] = args.lang
    if args.format:
        body["VodFormat"] = args.format
    if args.key:
        body["Key"] = args.key
    if args.kmode:
        body["Kmode"] = args.kmode
    if args.tempo:
        body["Tempo"] = args.tempo
    if args.instrument:
        body["Instrument"] = args.instrument
    if args.scene:
        body["Scene"] = args.scene
    if args.callback:
        body["CallbackURL"] = args.callback
    if args.skip_copy_check:
        body["SkipCopyCheck"] = True

    action = "GenSongV4" if args.billing == "prepaid" else "GenSongForTime"
    print(f"Submitting song generation task (Action={action})...")

    result = call_api(access_key, secret_key, action, body)
    return _extract_task_id(result)


def _extract_task_id(result: dict) -> str:
    code = result.get("Code", -1)
    if code != 0:
        msg = result.get("Message", "")
        err = result.get("ResponseMetadata", {}).get("Error") or {}
        print(f"Error: Submission failed Code={code} Message={msg} Error={err}", file=sys.stderr)
        sys.exit(1)
    task_id = result["Result"]["TaskID"]
    wait = result["Result"].get("PredictedWaitTime", 0)
    print(f"Task submitted, TaskID: {task_id} (estimated wait {wait}s)")
    return task_id


# ─── Task Polling and Download ────────────────────────────────────────────────

STATUS_MAP = {
    0: "Waiting",
    1: "Processing",
    2: "Success",
    3: "Failed",
}


def poll_task(access_key: str, secret_key: str, task_id: str, poll_interval: int) -> dict:
    """Poll task status (Action=QuerySong), returns Result data.
    Status codes: 0=Waiting, 1=Processing, 2=Success, 3=Failed.
    """
    body = {"TaskID": task_id}
    print(f"\nPolling task status (interval {poll_interval} seconds)...")

    while True:
        time.sleep(poll_interval)
        result = call_api(access_key, secret_key, "QuerySong", body)

        code = result.get("Code", -1)
        if code != 0:
            print(f"Query error: Code={code} Message={result.get('Message', '')}, retrying...",
                  file=sys.stderr)
            continue

        task = result.get("Result", {})
        status = task.get("Status", -1)
        progress = task.get("Progress", 0)
        print(f"Status: {STATUS_MAP.get(status, status)} (progress {progress}%)")

        if status == 2:
            return task
        elif status == 3:
            failure = task.get("FailureReason") or {}
            reason = failure.get("Msg", "Unknown reason")
            fcode = failure.get("Code", "")
            print(f"Task failed: {reason} (Code={fcode})", file=sys.stderr)
            if fcode == 300061 or "Plagiarized" in str(reason):
                print("Tip: Lyrics triggered copyright check, try modifying the lyrics or add --skip-copy-check",
                      file=sys.stderr)
            sys.exit(1)
        # status 0/1 -> continue polling


def download_audio(audio_url: str, output_path: str):
    """Download audio file to local path."""
    print(f"\nDownloading audio to: {output_path}")
    resp = requests.get(audio_url, timeout=120, stream=True)
    if resp.status_code != 200:
        print(f"Error: Download failed HTTP {resp.status_code}", file=sys.stderr)
        sys.exit(1)
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    size = os.path.getsize(output_path)
    print(f"Download complete: {output_path} ({size / 1024:.1f} KB)")


# ─── CLI ───────────────────────────────────────────────────────────────────────

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Doubao Music Generation: Vocal song (song) or instrumental BGM (bgm)"
    )

    # Mode
    parser.add_argument("--mode", choices=["bgm", "song"], default="bgm",
                        help="Generation mode: bgm=instrumental, song=vocal song (default: bgm)")
    parser.add_argument("--billing", choices=["prepaid", "postpaid"], default="postpaid",
                        help="Billing method: prepaid=prepaid, postpaid=postpaid (default: postpaid)")

    # BGM parameters
    bgm_group = parser.add_argument_group("BGM parameters (--mode bgm)")
    bgm_group.add_argument("--text", help="BGM description (required)")
    bgm_group.add_argument("--version", default="v5.0",
                           help="Model version (default: v5.0)")
    bgm_group.add_argument("--rewrite", action="store_true",
                           help="Enable automatic prompt rewrite")
    bgm_group.add_argument("--segments",
                           help='Structured segments JSON (v5.0 only), e.g.: \'[{"Name":"verse","Duration":20}] \'')

    # Song parameters
    song_group = parser.add_argument_group("Song parameters (--mode song)")
    song_input = song_group.add_mutually_exclusive_group()
    song_input.add_argument("--prompt", help="Prompt (choose one of --lyrics or --prompt)")
    song_input.add_argument("--lyrics", help="Lyrics text")
    song_group.add_argument("--lyrics-file", help="Read lyrics from file")
    song_group.add_argument("--model-version", default="v4.3",
                            choices=["v4.0", "v4.3", "v5.0"],
                            help="Song model version (default: v4.3)")
    song_group.add_argument("--genre", help="Primary genre (e.g. Pop / Folk / Electronic)")
    song_group.add_argument("--genre-extra", help="Secondary genres, comma-separated (v4.3)")
    song_group.add_argument("--mood", help="Mood (e.g. Happy / Dreamy/Ethereal)")
    song_group.add_argument("--gender", choices=["Male", "Female"], help="Vocal gender")
    song_group.add_argument("--timbre", help="Timbre (e.g. Warm / Husky)")
    song_group.add_argument("--lang",
                            help="Language (Chinese/English/Cantonese/Instrumental/Non-vocal etc.)")
    song_group.add_argument("--key",
                            choices=["A", "A#", "B", "C", "C#", "Cb", "D", "D#", "E", "F", "F#", "G", "Ab"],
                            help="Key (v4.3)")
    song_group.add_argument("--kmode", choices=["Major", "Minor"], help="Mode (v4.3)")
    song_group.add_argument("--tempo",
                            choices=["Grave", "Largo", "Adagio", "Andante", "Moderato", "Allegro", "Vivace", "Presto"],
                            help="Tempo (v4.3)")
    song_group.add_argument("--instrument", help="Instruments, comma-separated, up to 5 (v4.3)")
    song_group.add_argument("--scene", help="Scenes, comma-separated, up to 3 (v4.3)")
    song_group.add_argument("--skip-copy-check", action="store_true",
                            help="Disable lyrics copyright check")

    # Common parameters
    parser.add_argument("--duration", type=int,
                        help="Audio duration in seconds; BGM: [30,120], Song: [30,240]")
    parser.add_argument("--format", choices=["wav", "mp3"], default="mp3",
                        help="Output audio format (default: mp3)")
    parser.add_argument("--output", default="output.mp3",
                        help="Output file path (default: output.mp3)")
    parser.add_argument("--callback", help="Task completion callback URL (optional)")
    parser.add_argument("--poll-interval", type=int, default=5,
                        help="Polling interval in seconds (default: 5)")

    args = parser.parse_args()

    # Read credentials (.env first, then environment variables)
    access_key = os.environ.get("VOLC_ACCESS_KEY")
    secret_key = os.environ.get("VOLC_SECRET_KEY")
    if not access_key or not secret_key:
        print("Error: VOLC_ACCESS_KEY / VOLC_SECRET_KEY not set", file=sys.stderr)
        print("Please configure them in the .env file:", file=sys.stderr)
        print("  VOLC_ACCESS_KEY=your_access_key", file=sys.stderr)
        print("  VOLC_SECRET_KEY=your_secret_key", file=sys.stderr)
        sys.exit(1)

    # Handle --lyrics-file
    if args.lyrics_file:
        if not os.path.isfile(args.lyrics_file):
            print(f"Error: Lyrics file not found: {args.lyrics_file}", file=sys.stderr)
            sys.exit(1)
        with open(args.lyrics_file, encoding="utf-8") as f:
            args.lyrics = f.read().strip()

    # Parameter validation
    if args.mode == "bgm" and not args.text:
        print("Error: --mode bgm requires --text", file=sys.stderr)
        sys.exit(1)
    if args.mode == "song" and not args.prompt and not args.lyrics:
        print("Error: --mode song requires --prompt or --lyrics / --lyrics-file", file=sys.stderr)
        sys.exit(1)

    # Fix output extension
    output = args.output
    if args.format == "mp3" and not output.endswith(".mp3"):
        output = os.path.splitext(output)[0] + ".mp3"
    elif args.format == "wav" and not output.endswith(".wav"):
        output = os.path.splitext(output)[0] + ".wav"

    # Submit task
    if args.mode == "bgm":
        task_id = submit_bgm(access_key, secret_key, args)
    else:
        task_id = submit_song(access_key, secret_key, args)

    # Poll for result
    task = poll_task(access_key, secret_key, task_id, args.poll_interval)

    # Get audio URL (in SongDetail.AudioUrl)
    song_detail = task.get("SongDetail") or {}
    audio_url = song_detail.get("AudioUrl", "")
    if not audio_url:
        print(f"Error: Audio URL not found in task result, full result:\n{json.dumps(task, ensure_ascii=False, indent=2)}",
              file=sys.stderr)
        sys.exit(1)

    print(f"\nGeneration successful!")
    print(f"Audio URL: {audio_url}")
    if song_detail.get("Duration"):
        print(f"Audio duration: {song_detail['Duration']:.1f}s")

    # Download audio
    download_audio(audio_url, output)


if __name__ == "__main__":
    main()
