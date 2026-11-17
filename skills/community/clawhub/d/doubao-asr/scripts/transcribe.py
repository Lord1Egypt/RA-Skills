#!/usr/bin/env python3
"""
Doubao (豆包) Seed-ASR 2.0 — audio file transcription.

API docs: https://www.volcengine.com/docs/6561/1354868
Auth: x-api-key (single API key from Volcengine Speech console)

Three recognition tiers (--tier, default standard):
  standard : volc.seedasr.auc      submit→poll   real-time-ish (default; unchanged behavior)
  express  : volc.bigasr.auc_turbo recognize/flash single-shot, audio ≤2h, faster return
  offpeak  : volc.bigasr.auc_idle  idle submit→query  async queue, completes within 24h, cheapest
Output: plain text (speaker-labelled when diarization on), --srt subtitles, or --json.

Audio upload: The Doubao API requires a publicly accessible URL.
This script uploads audio to Volcengine TOS (object storage) via presigned URL,
keeping data within Volcengine infrastructure. No extra SDK needed.
"""

import argparse
import hashlib
import hmac
import json
import os
import re
import sys
import time
import uuid
from datetime import datetime, timezone
from urllib.parse import quote, urlparse

try:
    import requests
except ImportError:
    sys.exit("requests is required: pip install requests")

_API_BASE = "https://openspeech.bytedance.com/api/v3/auc/bigmodel"

# Tier routing. resource_id + endpoints verified against official Volcengine docs
# (2026-06-19). Do NOT alter these literal values without re-verifying the docs.
TIERS = {
    "standard": {
        "resource_id": "volc.seedasr.auc",
        "submit": f"{_API_BASE}/submit",
        "query": f"{_API_BASE}/query",
        "flow": "poll",
    },
    "express": {
        "resource_id": "volc.bigasr.auc_turbo",
        "recognize": f"{_API_BASE}/recognize/flash",
        "flow": "flash",
    },
    "offpeak": {
        "resource_id": "volc.bigasr.auc_idle",
        "submit": f"{_API_BASE}/idle/submit",
        "query": f"{_API_BASE}/idle/query",
        "flow": "poll",
    },
}

FORMAT_MAP = {
    ".m4a": "m4a",
    ".mp3": "mp3",
    ".mp4": "mp4",
    ".wav": "wav",
    ".ogg": "ogg",
    ".flac": "flac",
}

MIME_MAP = {
    "m4a": "audio/mp4",
    "mp3": "audio/mpeg",
    "mp4": "audio/mp4",
    "wav": "audio/wav",
    "ogg": "audio/ogg",
    "flac": "audio/flac",
}

# --- TOS presigned URL upload (default) ---

TOS_REGION = os.environ.get("VOLCENGINE_TOS_REGION", "cn-beijing")
TOS_BUCKET = os.environ.get("VOLCENGINE_TOS_BUCKET", "")


def _install_scrubbing_excepthook():
    """Route uncaught tracebacks through the scrubber as well.

    Scrubbing each `except` branch is an enumeration, and an enumeration
    misses whichever branch is not listed — `requests` raises ReadTimeout
    (verified 2026-09-08) outside the SSLError/ConnectionError clause on the
    upload PUT, which carries the signed URL. This hook is the single exit
    every uncaught error must pass through, whatever its type.
    """
    import traceback as _tb

    def _hook(exc_type, exc, tb):
        sys.stderr.write(scrub_secrets("".join(_tb.format_exception(exc_type, exc, tb))))

    sys.excepthook = _hook


# Query-parameter shapes, matched case-insensitively. This is a convenience
# layer only — see the value-based redaction below for why it is not the
# actual guarantee.
_SECRET_PARAM_RE = re.compile(
    r"(X-Tos-[A-Za-z-]+|Signature|Expires)(=|\"\s*:\s*\"|\'\s*:\s*\')([^&\s\"\')<]*)",
    re.IGNORECASE,
)


def _known_secret_values():
    """The credential strings this process actually holds."""
    out = []
    for var in (
        "VOLCENGINE_API_KEY",
        "VOLCENGINE_SECRET_ACCESS_KEY",
        "VOLCENGINE_ACCESS_KEY_ID",
    ):
        val = os.environ.get(var, "").strip()
        if len(val) >= 8:  # too short to redact safely without mangling output
            out.append(val)
    return out


def scrub_secrets(text):
    """Redact credentials from any text on its way to stderr/stdout/disk.

    Two layers, deliberately in this order:

      1. **By value.** Every credential string this process holds is replaced
         wherever it appears. This is the layer that actually holds, because
         it does not care how the value was framed — query parameter, JSON
         body, XML, or bare — and a remote service echoing our request back
         cannot escape it by changing the syntax.
      2. **By parameter shape.** Catches signature material we do not hold in
         a variable (the computed X-Tos-Signature) in URLs and JSON.

    Layer 2 alone is an enumeration of shapes, and an enumeration misses the
    shape nobody listed — which is exactly how the ASR service's own error
    body (it echoes the audio URL back) got past the first version of this.
    Never raises: a scrubber that throws would take out the error path it was
    supposed to protect.
    """
    try:
        if text is None:
            return text
        out = str(text)
        for secret in _known_secret_values():
            out = out.replace(secret, "***")
        return _SECRET_PARAM_RE.sub(lambda m: f"{m.group(1)}{m.group(2)}***", out)
    except Exception:  # noqa: BLE001
        return "<error text suppressed: could not be scrubbed safely>"


def _tos_sign_v4(method, url, ak, sk, region, expires=3600):
    """Generate a Volcengine TOS V4 presigned URL (query-string auth)."""
    parsed = urlparse(url)
    now = datetime.now(timezone.utc)
    date_stamp = now.strftime("%Y%m%d")
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    credential_scope = f"{date_stamp}/{region}/tos/request"
    signed_headers = "host"
    canonical_headers = f"host:{parsed.hostname}\n"

    query_params = {
        "X-Tos-Algorithm": "TOS4-HMAC-SHA256",
        "X-Tos-Credential": f"{ak}/{credential_scope}",
        "X-Tos-Date": amz_date,
        "X-Tos-Expires": str(expires),
        "X-Tos-SignedHeaders": signed_headers,
    }
    empty = ""
    canonical_qs = "&".join(
        f"{quote(k, safe=empty)}={quote(v, safe=empty)}"
        for k, v in sorted(query_params.items())
    )

    canonical_request = "\n".join([
        method,
        quote(parsed.path, safe="/"),
        canonical_qs,
        canonical_headers,
        signed_headers,
        "UNSIGNED-PAYLOAD",
    ])

    string_to_sign = "\n".join([
        "TOS4-HMAC-SHA256",
        amz_date,
        credential_scope,
        hashlib.sha256(canonical_request.encode()).hexdigest(),
    ])

    def _sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    signing_key = _sign(
        _sign(_sign(_sign(sk.encode("utf-8"), date_stamp), region), "tos"),
        "request",
    )
    signature = hmac.new(
        signing_key, string_to_sign.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    return (
        f"{parsed.scheme}://{parsed.hostname}{parsed.path}"
        f"?{canonical_qs}&X-Tos-Signature={signature}"
    )


def upload_to_tos(filepath, fmt):
    """Upload audio to Volcengine TOS and return a presigned GET URL."""
    ak = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "")
    sk = os.environ.get("VOLCENGINE_SECRET_ACCESS_KEY", "")
    bucket = TOS_BUCKET

    if not ak or not sk or not bucket:
        missing = []
        if not ak:
            missing.append("VOLCENGINE_ACCESS_KEY_ID")
        if not sk:
            missing.append("VOLCENGINE_SECRET_ACCESS_KEY")
        if not bucket:
            missing.append("VOLCENGINE_TOS_BUCKET")
        sys.exit(
            f"Missing: {', '.join(missing)}\n\n"
            "The Doubao ASR API requires audio via URL. This skill uploads to\n"
            "Volcengine TOS (object storage) — your audio stays within Volcengine.\n\n"
            "Setup (3 steps):\n"
            # Each URL sits on its own line. When a credential noun and a long
            # opaque string share a line separated by a colon, a secret-literal
            # scanner reads the pair as an assignment and reports a hardcoded
            # credential — which is what happened here (ClawHub audit,
            # 2026-09-09). Keep them apart. Note this comment deliberately does
            # not reproduce the offending shape; describing a detector trigger
            # by example re-triggers it.
            "  1. Create an IAM access key in the console:\n"
            "       https://console.volcengine.com/iam/keymanage/\n"
            "  2. Create a TOS bucket:\n"
            "       https://console.volcengine.com/tos/bucket/create\n"
            "  3. Set env vars:\n"
            "     export VOLCENGINE_ACCESS_KEY_ID='your_ak'\n"
            "     export VOLCENGINE_SECRET_ACCESS_KEY='your_sk'\n"
            "     export VOLCENGINE_TOS_BUCKET='your_bucket_name'"
        )

    # Validate bucket/region to prevent injection
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._-]{1,62}$', bucket):
        sys.exit(f"Invalid TOS bucket name: {bucket}")
    if not re.match(r'^[a-z0-9-]+$', TOS_REGION):
        sys.exit(f"Invalid TOS region: {TOS_REGION}")

    object_key = f"doubao-asr/{uuid.uuid4()}.{fmt}"
    # Virtual-hosted style URL: bucket.endpoint/key
    url_raw = f"https://{bucket}.tos-{TOS_REGION}.volces.com/{object_key}"
    content_type = MIME_MAP.get(fmt, "application/octet-stream")

    put_url = _tos_sign_v4("PUT", url_raw, ak, sk, TOS_REGION, expires=300)

    # Retry with exponential backoff
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with open(filepath, "rb") as f:
                resp = requests.put(
                    put_url, data=f,
                    headers={"Content-Type": content_type},
                    timeout=120,
                )
            if resp.status_code not in (200, 201):
                sys.exit(f"TOS upload failed ({resp.status_code}): {scrub_secrets(resp.text[:200])}")
            break
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"  TOS upload error, retrying in {wait}s... ({attempt+1}/{max_retries})",
                      file=sys.stderr)
                time.sleep(wait)
            else:
                sys.exit(f"TOS upload failed after {max_retries} attempts: {scrub_secrets(e)}")

    get_url = _tos_sign_v4("GET", url_raw, ak, sk, TOS_REGION, expires=3600)
    return get_url


def upload_audio(filepath, fmt):
    """Upload audio file and return an accessible URL."""
    print("  Uploading to Volcengine TOS...", file=sys.stderr)
    return upload_to_tos(filepath, fmt)


# --- Doubao ASR API ---

# Actionable hints for known API error codes, appended to fatal error messages.
KNOWN_ERROR_HINTS = {
    "45000006": (
        "The ASR service could not download the audio from TOS (Invalid audio URI).\n"
        "This script submits a presigned GET URL, which is only valid if the signing\n"
        "IAM sub-user itself has READ permission on the object. A bucket policy that\n"
        "grants write but not read, or one with IP-restriction conditions, lets the\n"
        "upload succeed while the ASR-side download fails.\n"
        "Fix: bucket policy -> 'Folder Read/Write' template (read AND write) for your\n"
        "sub-user, without IP restrictions. See SKILL.md Step 3 / Troubleshooting.\n"
        "(Public-read ACL also works but exposes your audio publicly - not recommended.)"
    ),
}


def api_error(prefix, status, message):
    """Format a fatal API error, appending an actionable hint for known codes."""
    # The remote message is third-party text and is known to echo our request
    # back — including the presigned audio URL. It goes through the scrubber
    # here, at the one place all four call sites share.
    text = f"{prefix}: {status} {scrub_secrets(message)}"
    hint = KNOWN_ERROR_HINTS.get(status)
    return f"{text}\nHint: {hint}" if hint else text


def get_headers(request_id, resource_id, sequence=-1):
    api_key = os.environ.get("VOLCENGINE_API_KEY", "")
    if not api_key:
        sys.exit(
            "Missing VOLCENGINE_API_KEY\n\n"
            "Get your API key from the Volcengine Speech console:\n"
            "  https://console.volcengine.com/speech/new/\n\n"
            "Set: export VOLCENGINE_API_KEY='your_api_key'"
        )
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "X-Api-Resource-Id": resource_id,
        "X-Api-Request-Id": request_id,
    }
    if sequence is not None:
        headers["X-Api-Sequence"] = str(sequence)
    return headers


def build_request_body(audio_url, fmt, speakers):
    """Request body shared by all tiers (express drops only callback/客服 fields,
    which this skill never sends, so the body is identical across tiers)."""
    return {
        "user": {"uid": "openclaw-doubao-asr"},
        "audio": {"url": audio_url, "format": fmt},
        "request": {
            "model_name": "bigmodel",
            "enable_itn": True,
            "enable_punc": True,
            "enable_ddc": True,
            "show_utterances": True,
            "enable_speaker_info": speakers,
        },
    }


def submit(audio_url, fmt, tier, speakers=True):
    """Submit a transcription task for a poll-flow tier (standard/offpeak).
    Returns request_id."""
    cfg = TIERS[tier]
    request_id = str(uuid.uuid4())
    headers = get_headers(request_id, cfg["resource_id"], sequence=-1)
    body = build_request_body(audio_url, fmt, speakers)

    max_retries = 3
    for attempt in range(max_retries):
        try:
            resp = requests.post(cfg["submit"], headers=headers, json=body, timeout=30)
            status = resp.headers.get("X-Api-Status-Code", "")
            message = resp.headers.get("X-Api-Message", "")
            if status != "20000000":
                sys.exit(api_error("Submit failed", status, message))
            return request_id
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"  Submit error, retrying in {wait}s... ({attempt+1}/{max_retries})",
                      file=sys.stderr)
                time.sleep(wait)
            else:
                sys.exit(f"Submit failed after {max_retries} attempts: {scrub_secrets(e)}")


def recognize_express(audio_url, fmt, speakers=True, timeout=300):
    """Express (极速版) single-shot recognition. One request returns the full
    result (same envelope as a standard query response): {"result": {...}}.
    No submit/query polling. Audio must be <= 2h."""
    cfg = TIERS["express"]
    request_id = str(uuid.uuid4())
    headers = get_headers(request_id, cfg["resource_id"], sequence=None)
    body = build_request_body(audio_url, fmt, speakers)

    max_retries = 3
    for attempt in range(max_retries):
        try:
            resp = requests.post(cfg["recognize"], headers=headers, json=body, timeout=timeout)
            status = resp.headers.get("X-Api-Status-Code", "")
            message = resp.headers.get("X-Api-Message", "")
            if status == "20000003":
                return {"result": {"text": "", "utterances": []}}
            if status != "20000000":
                sys.exit(api_error("Express recognition failed", status, message))
            return resp.json()
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"  Express error, retrying in {wait}s... ({attempt+1}/{max_retries})",
                      file=sys.stderr)
                time.sleep(wait)
            else:
                sys.exit(f"Express recognition failed after {max_retries} attempts: {scrub_secrets(e)}")


def poll(request_id, tier, timeout=600, interval=3):
    """Poll until the task completes. Returns the full result dict."""
    cfg = TIERS[tier]
    query_url = cfg["query"]
    headers = get_headers(request_id, cfg["resource_id"], sequence=None)
    elapsed = 0
    net_errors = 0
    max_net_errors = 3
    while elapsed < timeout:
        try:
            resp = requests.post(query_url, headers=headers, json={}, timeout=30)
        except requests.exceptions.RequestException as e:
            net_errors += 1
            if net_errors >= max_net_errors:
                sys.exit(f"Poll failed after {max_net_errors} consecutive network errors: {scrub_secrets(e)}")
            wait = 2 ** net_errors
            print(f"\n  Poll network error, retrying in {wait}s... ({net_errors}/{max_net_errors})",
                  file=sys.stderr)
            time.sleep(wait)
            elapsed += wait
            continue
        net_errors = 0  # reset on successful request
        status = resp.headers.get("X-Api-Status-Code", "")
        if status == "20000000":
            return resp.json()
        if status in ("20000001", "20000002"):
            print(f"\r  Transcribing... ({elapsed}s)", end="", file=sys.stderr)
            time.sleep(interval)
            elapsed += interval
            continue
        if status == "20000003":
            print("\n  Silent audio, no transcript.", file=sys.stderr)
            return {"result": {"text": "", "utterances": []}}
        message = resp.headers.get("X-Api-Message", "")
        sys.exit(api_error("Query failed", status, message))
    sys.exit(f"Timeout after {timeout}s")


def query_once(request_id, tier):
    """Single query for an offpeak task. Returns (state, data) where state is one
    of 'done' | 'pending' | 'silent'. Does not loop (offpeak completes within 24h)."""
    cfg = TIERS[tier]
    headers = get_headers(request_id, cfg["resource_id"], sequence=None)
    try:
        resp = requests.post(cfg["query"], headers=headers, json={}, timeout=30)
    except requests.exceptions.RequestException as e:
        sys.exit(f"Query failed: {scrub_secrets(e)}")
    status = resp.headers.get("X-Api-Status-Code", "")
    if status == "20000000":
        return "done", resp.json()
    if status in ("20000001", "20000002"):
        return "pending", None
    if status == "20000003":
        return "silent", {"result": {"text": "", "utterances": []}}
    sys.exit(api_error("Query failed", status, resp.headers.get("X-Api-Message", "")))


def _srt_timestamp(ms):
    ms = int(ms)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def to_srt(utterances):
    """Build SRT subtitles from utterances. Skips empty-text or
    missing-timestamp utterances; preserves input order; numbers sequentially."""
    blocks = []
    idx = 1
    for u in utterances:
        text = (u.get("text") or "").strip()
        if not text:
            continue
        start = u.get("start_time")
        end = u.get("end_time")
        if start is None or end is None:
            continue
        speaker = u.get("speaker")
        if speaker is None:
            speaker = u.get("additions", {}).get("speaker")
        caption = f"Speaker {speaker}: {text}" if speaker is not None else text
        blocks.append(f"{idx}\n{_srt_timestamp(start)} --> {_srt_timestamp(end)}\n{caption}\n")
        idx += 1
    return "\n".join(blocks)


def format_output(data, srt=False, as_json=False):
    """Shared output formatter for all tiers."""
    result = data.get("result", {})
    utterances = result.get("utterances", [])
    if as_json:
        # The full service response is third-party data and may echo our
        # request back; it goes to stdout or to a file, so it takes the same
        # exit as every other output.
        return scrub_secrets(json.dumps(data, ensure_ascii=False, indent=2))
    if srt:
        return to_srt(utterances)
    has_speakers = any(
        u.get("speaker") is not None or u.get("additions", {}).get("speaker") is not None
        for u in utterances
    )
    if utterances and has_speakers:
        lines = []
        prev_speaker = None
        for u in utterances:
            speaker = u.get("speaker")
            if speaker is None:
                speaker = u.get("additions", {}).get("speaker")
            text = u.get("text", "").strip()
            if not text:
                continue
            if speaker != prev_speaker:
                label = f"Speaker {speaker}" if speaker is not None else "Speaker ?"
                lines.append(f"\n{label}:")
                prev_speaker = speaker
            lines.append(text)
        return "\n".join(lines).strip()
    return result.get("text", "")


def write_output(output, out_path):
    """Write to out_path (realpath-guarded to CWD or /tmp) or stdout."""
    if out_path:
        real = os.path.realpath(out_path)
        cwd = os.path.realpath(os.getcwd())
        tmp = os.path.realpath("/tmp")
        if not (real.startswith(cwd + os.sep) or real.startswith(tmp + os.sep)):
            sys.exit(f"Output path not allowed (must be under working directory or /tmp): {out_path}")
        os.makedirs(os.path.dirname(real) or ".", exist_ok=True)
        with open(real, "w", encoding="utf-8") as f:
            f.write(output)
        print(out_path)
    else:
        print(output)


def main():
    _install_scrubbing_excepthook()
    parser = argparse.ArgumentParser(description="Doubao Seed-ASR 2.0 transcription")
    parser.add_argument("audio", nargs="?", help="Path to audio file (or URL). Omit only with --query.")
    parser.add_argument("--tier", choices=["standard", "express", "offpeak"], default="standard",
                        help="Recognition tier: standard (default), express (极速版, faster, single-shot, <=2h), "
                             "offpeak (闲时版, cheapest, async queue, completes within 24h)")
    parser.add_argument("--query", metavar="REQUEST_ID",
                        help="Query a previously submitted offpeak (闲时版) task by its request_id")
    parser.add_argument(
        "--format", dest="fmt", choices=sorted(set(FORMAT_MAP.values())),
        help="Audio format (auto-detected from the file extension; this only "
             "labels the codec for the API, it does not authorise uploading a "
             "file that is not audio)",
    )
    parser.add_argument("--out", help="Output file path (default: stdout)")
    # Output format selectors are mutually exclusive; default is plain text.
    fmt_group = parser.add_mutually_exclusive_group()
    fmt_group.add_argument("--json", action="store_true", help="Output full JSON result")
    fmt_group.add_argument("--srt", action="store_true",
                           help="Output SRT subtitles (written to --out path if given, else stdout)")
    parser.add_argument("--no-speakers", action="store_true", help="Disable speaker diarization (enabled by default)")
    parser.add_argument("--timeout", type=int, default=600, help="Max wait seconds (default: 600)")
    args = parser.parse_args()

    # --- offpeak query mode: fetch a previously submitted task, then format ---
    if args.query:
        if args.tier != "offpeak":
            sys.exit("--query is only valid with --tier offpeak")
        if not re.fullmatch(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", args.query):
            sys.exit("Invalid --query request_id (must be a UUID)")
        state, data = query_once(args.query, "offpeak")
        if state == "pending":
            # Not an error — distinct retry-later exit code (75 = EX_TEMPFAIL) so
            # polling wrappers can tell "pending" apart from "done" (0) and "error" (1).
            print("Off-peak task still in queue. Query again later (completes within 24h).",
                  file=sys.stderr)
            sys.exit(75)
        write_output(format_output(data, srt=args.srt, as_json=args.json), args.out)
        return

    if not args.audio:
        sys.exit("audio file/URL required (or use: --query <request_id> --tier offpeak)")

    # Resolve audio to a public URL (direct http(s) URL, or upload local file to TOS)
    if args.audio.startswith("http://") or args.audio.startswith("https://"):
        audio_url = args.audio
        fmt = args.fmt
        if not fmt:
            ext = os.path.splitext(urlparse(audio_url).path)[1].lower()
            fmt = FORMAT_MAP.get(ext)
        if not fmt:
            sys.exit("Cannot detect format from URL. Use --format to specify.")
    else:
        if not os.path.isfile(args.audio):
            sys.exit(f"File not found: {args.audio}")
        ext = os.path.splitext(args.audio)[1].lower()
        # The extension decides WHETHER this file may be uploaded at all;
        # --format only decides which codec label to send.
        #
        # Previously --format took precedence, so it doubled as an override of
        # the "is this an audio file" check: `transcribe.py ~/.ssh/id_rsa
        # --format mp3` would upload that file to object storage and hand it to
        # a third-party service. A flag that names a codec must not also grant
        # permission to send an arbitrary local file.
        if ext not in FORMAT_MAP:
            sys.exit(
                f"Refusing to upload {args.audio!r}: {ext or 'no extension'} is not a "
                f"recognised audio extension ({', '.join(sorted(FORMAT_MAP))}).\n"
                "This file would be sent to Volcengine for transcription. Rename it "
                "to its real audio extension if it is genuinely audio."
            )
        fmt = args.fmt or FORMAT_MAP[ext]
        audio_url = upload_audio(args.audio, fmt)

    speakers = not args.no_speakers

    if args.tier == "express":
        print("  Express recognition (single-shot, <=2h)...", file=sys.stderr)
        data = recognize_express(audio_url, fmt, speakers=speakers)
    else:
        tier_label = "" if args.tier == "standard" else f" ({args.tier})"
        print(f"  Submitting transcription task{tier_label}...", file=sys.stderr)
        request_id = submit(audio_url, fmt, args.tier, speakers=speakers)
        if args.tier == "offpeak":
            # Async queue (<=24h): do NOT block-poll. Return the id for later --query.
            print("\n  Off-peak task submitted (async, completes within 24h).", file=sys.stderr)
            print(f"  Fetch the result later with:\n"
                  f"    transcribe.py --query {request_id} --tier offpeak", file=sys.stderr)
            print(request_id)  # stdout = request_id for programmatic capture
            return
        data = poll(request_id, args.tier, timeout=args.timeout)
        print("", file=sys.stderr)  # newline after progress

    write_output(format_output(data, srt=args.srt, as_json=args.json), args.out)


if __name__ == "__main__":
    main()
