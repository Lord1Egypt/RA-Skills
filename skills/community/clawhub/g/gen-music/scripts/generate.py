#!/usr/bin/env python3
"""Submit text-to-music jobs to a local ACE-Step API and save the outputs."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import base64
from pathlib import Path
from typing import Any


SKILL_NAME = "gen-music"
DEFAULT_BASE_URL = "http://127.0.0.1:8001"
DEFAULT_MODEL = "acestep/acestep-v15-turbo"
DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def load_skill_config() -> dict[str, Any]:
    candidates = [
        Path.home() / ".openclaw" / "openclaw.json",
        Path("/data/.clawdbot/openclaw.json"),
    ]
    for path in candidates:
        payload = read_json(path)
        if not isinstance(payload, dict):
            continue
        skills = payload.get("skills")
        if not isinstance(skills, dict):
            continue
        entries = skills.get("entries")
        if isinstance(entries, dict):
            entry = entries.get(SKILL_NAME)
            if isinstance(entry, dict):
                return entry
        entry = skills.get(SKILL_NAME)
        if isinstance(entry, dict):
            return entry
    return {}


def expand_optional_path(value: str | None) -> Path | None:
    if not value:
        return None
    return Path(value).expanduser()


def default_out_dir(config: dict[str, Any]) -> Path:
    configured = config.get("outputDir")
    if isinstance(configured, str) and configured.strip():
        base = Path(configured).expanduser()
    else:
        preferred = Path.home() / "Projects" / "tmp" / "ace-step"
        base = preferred if preferred.parent.is_dir() else Path("./tmp/ace-step")
    timestamp = dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return base / timestamp


def request_text(
    method: str,
    url: str,
    payload: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 60,
) -> str:
    body = None
    request_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": DEFAULT_USER_AGENT,
    }
    if headers:
        request_headers.update(headers)
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, method=method, headers=request_headers, data=body)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed ({exc.code}): {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"{method} {url} failed: {exc.reason}") from exc


def request_json(
    method: str,
    url: str,
    payload: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    raw = request_text(method, url, payload=payload, headers=headers, timeout=timeout)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{method} {url} returned non-JSON response: {raw[:200]}") from exc
    if not isinstance(parsed, dict):
        raise RuntimeError(f"{method} {url} returned unexpected JSON payload: {parsed}")
    return parsed


def check_health(base_url: str, headers: dict[str, str]) -> None:
    raw = request_text("GET", f"{base_url}/health", headers=headers, timeout=30).strip()
    if not raw:
        return
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        print(f"ACE-Step health: {raw}")
        return
    if not isinstance(payload, dict):
        return
    health_data = payload.get("data")
    if isinstance(health_data, dict):
        print(f"ACE-Step: {health_data.get('service', 'unknown')} loaded={health_data.get('loaded_model', 'unknown')}")


def extract_task_id(payload: dict[str, Any]) -> str:
    data = payload.get("data")
    if not isinstance(data, dict):
        raise RuntimeError(f"Unexpected release_task payload: {payload}")
    task_id = data.get("task_id")
    if not isinstance(task_id, str) or not task_id:
        raise RuntimeError(f"Missing task_id in release_task payload: {payload}")
    return task_id


def parse_result_entries(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, str) and value.strip():
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return []
        if isinstance(parsed, list):
            return [item for item in parsed if isinstance(item, dict)]
    return []


def is_success(result_item: dict[str, Any], entries: list[dict[str, Any]]) -> bool:
    if result_item.get("status") == 1:
        return True
    return any(entry.get("status") == 1 or entry.get("stage") == "succeeded" for entry in entries)


def is_failure(result_item: dict[str, Any], entries: list[dict[str, Any]]) -> bool:
    if result_item.get("status") == 2:
        return True
    return any(entry.get("status") == 2 or entry.get("stage") in {"failed", "error"} for entry in entries)


def poll_result(
    base_url: str,
    task_id: str,
    headers: dict[str, str],
    interval: float,
    timeout: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    deadline = time.time() + timeout
    last_progress = ""
    while time.time() < deadline:
        payload = request_json(
            "POST",
            f"{base_url}/query_result",
            payload={"task_id_list": [task_id]},
            headers=headers,
            timeout=max(60, int(interval) + 10),
        )
        data = payload.get("data")
        if not isinstance(data, list) or not data or not isinstance(data[0], dict):
            raise RuntimeError(f"Unexpected query_result payload: {payload}")
        item = data[0]
        entries = parse_result_entries(item.get("result"))
        progress = item.get("progress_text")
        if isinstance(progress, str) and progress and progress != last_progress:
            print(progress)
            last_progress = progress
        if is_success(item, entries):
            return item, entries
        if is_failure(item, entries):
            raise RuntimeError(json.dumps(item, ensure_ascii=False))
        time.sleep(interval)
    raise RuntimeError(f"Timed out waiting for task {task_id}")


def build_chat_messages(prompt: str, lyrics: str, duration: float) -> list[dict[str, str]]:
    lines = [
        "Generate music audio only.",
        f"Prompt: {prompt}",
        f"Target duration: {int(duration)} seconds.",
    ]
    if lyrics:
        lines.append(f"Lyrics:\n{lyrics}")
    return [{"role": "user", "content": "\n".join(lines)}]


def data_url_to_bytes(value: str) -> tuple[bytes, str]:
    match = re.match(r"^data:([^;,]+);base64,(.+)$", value, re.DOTALL)
    if not match:
        raise RuntimeError("Unsupported audio URL format in chat completion response.")
    content_type = match.group(1).strip().lower()
    payload = match.group(2).strip()
    try:
        raw = base64.b64decode(payload, validate=True)
    except ValueError as exc:
        raise RuntimeError("Invalid base64 audio payload in chat completion response.") from exc
    return raw, content_type


def suffix_from_content_type(content_type: str) -> str:
    mapping = {
        "audio/mpeg": ".mp3",
        "audio/mp3": ".mp3",
        "audio/wav": ".wav",
        "audio/x-wav": ".wav",
        "audio/flac": ".flac",
        "audio/aac": ".aac",
        "audio/ogg": ".ogg",
        "audio/opus": ".opus",
        "audio/mp4": ".m4a",
    }
    return mapping.get(content_type, ".mp3")


def generate_via_chat_completions(
    base_url: str,
    headers: dict[str, str],
    prompt: str,
    lyrics: str,
    duration: float,
    model: str,
    out_dir: Path,
) -> tuple[str, list[Path], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    submit_payload = {
        "model": model or DEFAULT_MODEL,
        "messages": build_chat_messages(prompt, lyrics, duration),
    }
    response = request_json(
        "POST",
        f"{base_url}/v1/chat/completions",
        payload=submit_payload,
        headers=headers,
        timeout=300,
    )
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
        raise RuntimeError(f"Unexpected chat completions payload: {response}")
    message = choices[0].get("message")
    if not isinstance(message, dict):
        raise RuntimeError(f"Missing message in chat completions payload: {response}")
    audio_items = message.get("audio")
    if not isinstance(audio_items, list) or not audio_items or not isinstance(audio_items[0], dict):
        raise RuntimeError(f"Missing audio payload in chat completions response: {response}")
    audio_url = audio_items[0].get("audio_url")
    if not isinstance(audio_url, dict):
        raise RuntimeError(f"Missing audio_url in chat completions response: {response}")
    data_url = audio_url.get("url")
    if not isinstance(data_url, str) or not data_url:
        raise RuntimeError(f"Missing audio url in chat completions response: {response}")

    raw_audio, content_type = data_url_to_bytes(data_url)
    suffix = suffix_from_content_type(content_type)
    out_dir.mkdir(parents=True, exist_ok=True)
    destination = out_dir / f"01{suffix}"
    destination.write_bytes(raw_audio)

    content_value = message.get("content", "")
    content_text = content_value if isinstance(content_value, str) else json.dumps(content_value, ensure_ascii=False)
    result_item = {
        "status": 1,
        "progress_text": "completed",
        "provider": "chat_completions",
        "content": content_text,
    }
    entries = [
        {
            "status": 1,
            "stage": "succeeded",
            "provider": "chat_completions",
            "file": str(destination),
            "content_type": content_type,
        }
    ]
    task_id = str(response.get("id") or f"chatcmpl-{int(time.time())}")
    return task_id, [destination], submit_payload, result_item, entries


def local_source_path(file_value: str) -> Path | None:
    if not file_value:
        return None
    parsed = urllib.parse.urlparse(file_value)
    if parsed.scheme in {"http", "https"}:
        query = urllib.parse.parse_qs(parsed.query)
        local_path = query.get("path", [None])[0]
        return expand_optional_path(local_path)
    if parsed.path == "/v1/audio":
        query = urllib.parse.parse_qs(parsed.query)
        local_path = query.get("path", [None])[0]
        return expand_optional_path(local_path)
    if file_value.startswith("/v1/audio?path="):
        query = urllib.parse.parse_qs(parsed.query)
        local_path = query.get("path", [None])[0]
        return expand_optional_path(local_path)
    path = expand_optional_path(file_value)
    if path and path.exists():
        return path
    return None


def download_file(url: str, destination: Path, headers: dict[str, str]) -> None:
    request_headers = {"User-Agent": DEFAULT_USER_AGENT}
    request_headers.update(headers)
    req = urllib.request.Request(url, headers=request_headers)
    with urllib.request.urlopen(req, timeout=300) as resp:
        with destination.open("wb") as handle:
            shutil.copyfileobj(resp, handle)


def save_outputs(
    entries: list[dict[str, Any]],
    base_url: str,
    out_dir: Path,
    headers: dict[str, str],
) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    for index, entry in enumerate(entries, start=1):
        file_value = entry.get("file")
        if not isinstance(file_value, str) or not file_value:
            continue
        source_path = local_source_path(file_value)
        suffix = Path(source_path.name).suffix if source_path else Path(urllib.parse.urlparse(file_value).path).suffix
        suffix = suffix or ".mp3"
        destination = out_dir / f"{index:02d}{suffix}"
        if source_path and source_path.exists():
            shutil.copy2(source_path, destination)
        else:
            url = file_value
            if file_value.startswith("/"):
                url = f"{base_url}{file_value}"
            download_file(url, destination, headers)
        saved.append(destination)
    return saved


def build_headers(api_key: str | None) -> dict[str, str]:
    headers: dict[str, str] = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be >= 1")
    return parsed


def duration_seconds(value: str) -> float:
    parsed = float(value)
    if parsed < 10 or parsed > 600:
        raise argparse.ArgumentTypeError("must be between 10 and 600 seconds")
    return parsed


def parse_args() -> argparse.Namespace:
    config = load_skill_config()
    parser = argparse.ArgumentParser(description="Generate music through a local ACE-Step API.")
    parser.add_argument("prompt", nargs="?", help="Prompt describing the song.")
    parser.add_argument("--prompt", dest="prompt_flag", help="Prompt describing the song.")
    parser.add_argument("--lyrics", default="", help="Inline lyrics.")
    parser.add_argument("--lyrics-file", default="", help="Path to a lyrics text file.")
    parser.add_argument("--duration", type=duration_seconds, default=float(config.get("defaultDuration", 30)), help="Audio duration in seconds (10-600).")
    parser.add_argument("--batch-size", type=positive_int, default=int(config.get("batchSize", 1)), help="How many variants to request.")
    parser.add_argument("--thinking", action="store_true", help="Enable LM-assisted planning/codes generation.")
    parser.add_argument("--model", default=str(config.get("model", DEFAULT_MODEL)).strip(), help="Optional model override.")
    parser.add_argument("--sample-mode", default=str(config.get("sampleMode", "text2music")), help="Sample mode to pass to ACE-Step.")
    parser.add_argument("--format", default=str(config.get("audioFormat", "mp3")), help="Output audio format.")
    parser.add_argument("--base-url", default="", help="ACE-Step API base URL.")
    parser.add_argument("--api-key", default="", help="Optional API key.")
    parser.add_argument("--out-dir", default="", help="Directory to copy final files into.")
    parser.add_argument("--poll-interval", type=float, default=float(config.get("pollInterval", 5)), help="Polling interval in seconds.")
    parser.add_argument("--timeout", type=positive_int, default=int(config.get("timeout", 1800)), help="Overall timeout in seconds.")
    args = parser.parse_args()
    args.skill_config = config
    return args


def resolve_prompt(args: argparse.Namespace) -> str:
    prompt = (args.prompt_flag or args.prompt or "").strip()
    if not prompt:
        raise RuntimeError("Missing prompt. Pass it positionally or with --prompt.")
    return prompt


def resolve_lyrics(args: argparse.Namespace) -> str:
    if args.lyrics_file:
        return Path(args.lyrics_file).expanduser().read_text(encoding="utf-8").strip()
    return args.lyrics.strip()


def write_manifest(
    out_dir: Path,
    task_id: str,
    saved_files: list[Path],
    submit_payload: dict[str, Any],
    result_item: dict[str, Any],
    entries: list[dict[str, Any]],
) -> None:
    manifest = {
        "task_id": task_id,
        "saved_files": [str(path) for path in saved_files],
        "submit_payload": submit_payload,
        "result_item": result_item,
        "entries": entries,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    args = parse_args()
    config = args.skill_config
    prompt = resolve_prompt(args)
    lyrics = resolve_lyrics(args)
    base_url = (
        args.base_url.strip()
        or os.environ.get("ACESTEP_API_BASE_URL", "").strip()
        or str(config.get("baseUrl", "")).strip()
        or DEFAULT_BASE_URL
    ).rstrip("/")
    api_key = (
        args.api_key.strip()
        or os.environ.get("ACESTEP_API_KEY", "").strip()
        or str(config.get("apiKey", "")).strip()
        or ""
    )
    out_dir = (
        Path(args.out_dir).expanduser()
        if args.out_dir
        else expand_optional_path(os.environ.get("ACESTEP_OUTPUT_DIR"))
        or default_out_dir(config)
    )
    headers = build_headers(api_key)

    check_health(base_url, headers)

    submit_payload: dict[str, Any] = {
        "prompt": prompt,
        "lyrics": lyrics,
        "audio_duration": args.duration,
        "sample_mode": args.sample_mode,
        "batch_size": args.batch_size,
        "thinking": args.thinking,
        "audio_format": args.format,
    }
    if args.model:
        submit_payload["model"] = args.model

    try:
        created = request_json(
            "POST",
            f"{base_url}/release_task",
            payload=submit_payload,
            headers=headers,
            timeout=60,
        )
        task_id = extract_task_id(created)
        print(f"task_id={task_id}")

        result_item, entries = poll_result(
            base_url=base_url,
            task_id=task_id,
            headers=headers,
            interval=args.poll_interval,
            timeout=args.timeout,
        )

        saved_files = save_outputs(entries, base_url, out_dir, headers)
    except RuntimeError as exc:
        if "release_task failed (404)" not in str(exc):
            raise
        print("ACE-Step: /release_task unavailable, falling back to /v1/chat/completions")
        task_id, saved_files, submit_payload, result_item, entries = generate_via_chat_completions(
            base_url=base_url,
            headers=headers,
            prompt=prompt,
            lyrics=lyrics,
            duration=args.duration,
            model=args.model,
            out_dir=out_dir,
        )
        print(f"task_id={task_id}")

    write_manifest(out_dir, task_id, saved_files, submit_payload, result_item, entries)

    if not saved_files:
        eprint("Generation succeeded but no output files were saved.")
        return 1

    print(f"out_dir={out_dir}")
    for path in saved_files:
        print(path)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        eprint("Interrupted.")
        raise SystemExit(130)
    except Exception as exc:
        eprint(str(exc))
        raise SystemExit(1)
