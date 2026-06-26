# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Music generation using Volcengine Imagination API.
Supports: vocal songs (GenSong), instrumental BGM (GenBGM), lyrics (GenLyrics).
Ref: https://www.volcengine.com/docs/84992
Auth: HMAC-SHA256 signature with AK/SK.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
import time
from datetime import datetime, timezone
from functools import reduce
from typing import Any, Dict, Optional

import requests

API_HOST = "open.volcengineapi.com"
API_BASE = f"https://{API_HOST}"
API_VERSION = "2024-08-12"
REGION = "cn-beijing"
SERVICE = "imagination"

POLL_INTERVAL = 10
MAX_WAIT_SECONDS = 300
TASK_STATUS_SUCCESS = 2
TASK_STATUS_FAILED = 3


class VolcEngineApiClient:
    """Volcengine API client with HMAC-SHA256 signature authentication."""

    def __init__(self, ak: str, sk: str):
        self.ak = ak
        self.sk = sk

    def request(self, action: str, body: dict, method: str = "POST") -> dict:
        url = f"{API_BASE}/?Action={action}&Version={API_VERSION}"
        json_body = "" if method == "GET" else json.dumps(body, ensure_ascii=False)
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        body_hash = hashlib.sha256(json_body.encode()).hexdigest()

        headers_to_sign = {
            "content-type": "application/json; charset=utf-8",
            "host": API_HOST,
            "x-content-sha256": body_hash,
            "x-date": ts,
        }
        signed_keys = sorted(headers_to_sign.keys())
        canonical_headers = "".join(
            f"{k}:{headers_to_sign[k]}\n" for k in signed_keys
        )
        signed_headers = ";".join(signed_keys)

        canonical_request = (
            f"{method}\n/\n"
            f"Action={action}&Version={API_VERSION}\n"
            f"{canonical_headers}\n{signed_headers}\n{body_hash}"
        )

        credential_scope = f"{ts[:8]}/{REGION}/{SERVICE}/request"
        string_to_sign = (
            f"HMAC-SHA256\n{ts}\n{credential_scope}\n"
            f"{hashlib.sha256(canonical_request.encode()).hexdigest()}"
        )

        signing_key = reduce(
            lambda key, msg: hmac.new(key, msg.encode(), hashlib.sha256).digest(),
            [ts[:8], REGION, SERVICE, "request"],
            self.sk.encode(),
        )
        signature = hmac.new(
            signing_key, string_to_sign.encode(), hashlib.sha256
        ).hexdigest()

        req_headers = {
            k.title().replace("X-C", "X-c"): v
            for k, v in headers_to_sign.items()
        }
        req_headers["Authorization"] = (
            f"HMAC-SHA256 Credential={self.ak}/{credential_scope}, "
            f"SignedHeaders={signed_headers}, Signature={signature}"
        )

        if method == "GET":
            resp = requests.get(url, headers=req_headers, timeout=30)
        else:
            resp = requests.post(
                url, headers=req_headers, data=json_body.encode(), timeout=30
            )

        if resp.status_code != 200:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text}")
        return resp.json()


def _get_client() -> VolcEngineApiClient:
    ak = os.getenv("VOLCENGINE_ACCESS_KEY", "").strip()
    sk = os.getenv("VOLCENGINE_SECRET_KEY", "").strip()
    if not ak or not sk:
        raise PermissionError(
            "VOLCENGINE_ACCESS_KEY and VOLCENGINE_SECRET_KEY must be set in environment variables. "
            "Obtain from: Volcengine Console → Account → Key Management → Create Key"
        )
    return VolcEngineApiClient(ak, sk)


def _get_song_action(mode: str, billing: str) -> str:
    actions = {
        ("song", "prepaid"): "GenSongV4",
        ("song", "postpaid"): "GenSongForTime",
        ("bgm", "prepaid"): "GenBGM",
        ("bgm", "postpaid"): "GenBGMForTime",
    }
    return actions[(mode, billing)]


def _poll_task(
    client: VolcEngineApiClient,
    task_id: str,
    max_wait: int = MAX_WAIT_SECONDS,
) -> dict:
    """Poll QuerySong until task completes or timeout."""
    polls = 0
    max_polls = max_wait // POLL_INTERVAL

    while polls < max_polls:
        time.sleep(POLL_INTERVAL)
        polls += 1
        resp = client.request("QuerySong", {"TaskID": task_id})
        result = resp.get("Result", {})
        status = result.get("Status")

        print(
            f"Polling [{polls}/{max_polls}] TaskID={task_id} Status={status}",
            file=sys.stderr,
        )

        if status == TASK_STATUS_SUCCESS:
            return result
        if status == TASK_STATUS_FAILED:
            failure = result.get("FailureReason", {})
            raise RuntimeError(
                f"Task failed: code={failure.get('Code')}, msg={failure.get('Msg')}"
            )

    raise TimeoutError(
        f"Task {task_id} still running after {max_wait}s. "
        f"Query manually: python scripts/music_generate.py query --task-id {task_id}"
    )


def generate_song(
    client: VolcEngineApiClient,
    billing: str = "postpaid",
    lyrics: Optional[str] = None,
    prompt: Optional[str] = None,
    model_version: str = "v4.3",
    genre: Optional[str] = None,
    mood: Optional[str] = None,
    gender: Optional[str] = None,
    timbre: Optional[str] = None,
    duration: Optional[int] = None,
    key: Optional[str] = None,
    kmode: Optional[str] = None,
    tempo: Optional[str] = None,
    instrument: Optional[str] = None,
    genre_extra: Optional[str] = None,
    scene: Optional[str] = None,
    lang: Optional[str] = None,
    vod_format: Optional[str] = None,
    max_wait: int = MAX_WAIT_SECONDS,
) -> dict:
    if not lyrics and not prompt:
        return {"status": "error", "error": "Either --lyrics or --prompt must be provided"}

    body: Dict[str, Any] = {"ModelVersion": model_version}
    if lyrics:
        body["Lyrics"] = lyrics
    if prompt:
        body["Prompt"] = prompt
    if genre:
        body["Genre"] = genre
    if mood:
        body["Mood"] = mood
    if gender:
        body["Gender"] = gender
    if timbre:
        body["Timbre"] = timbre
    if duration:
        body["Duration"] = duration
    if key:
        body["Key"] = key
    if kmode:
        body["Kmode"] = kmode
    if tempo:
        body["Tempo"] = tempo
    if instrument:
        body["Instrument"] = instrument
    if genre_extra:
        body["GenreExtra"] = genre_extra
    if scene:
        body["Scene"] = scene
    if lang:
        body["Lang"] = lang
    if vod_format:
        body["VodFormat"] = vod_format

    action = _get_song_action("song", billing)
    resp = client.request(action, body)
    task_id = resp.get("Result", {}).get("TaskID")
    if not task_id:
        return {"status": "error", "error": f"No TaskID returned: {resp}"}

    print(f"Song task submitted: TaskID={task_id}", file=sys.stderr)

    try:
        result = _poll_task(client, task_id, max_wait)
    except TimeoutError as e:
        return {"status": "timeout", "mode": "song", "task_id": task_id, "error": str(e)}

    detail = result.get("SongDetail", {})
    return {
        "status": "success",
        "mode": "song",
        "task_id": task_id,
        "audio_url": detail.get("AudioUrl"),
        "duration": detail.get("Duration"),
        "lyrics": detail.get("Lyrics"),
        "genre": detail.get("Genre"),
        "mood": detail.get("Mood"),
        "gender": detail.get("Gender"),
        "error": None,
    }


def generate_bgm(
    client: VolcEngineApiClient,
    text: str,
    billing: str = "postpaid",
    duration: Optional[int] = None,
    version: str = "v5.0",
    segments: Optional[str] = None,
    enable_input_rewrite: bool = False,
    max_wait: int = MAX_WAIT_SECONDS,
) -> dict:
    if not text:
        return {"status": "error", "error": "--text is required and cannot be empty"}

    body: Dict[str, Any] = {
        "Text": text,
        "Version": version,
        "EnableInputRewrite": enable_input_rewrite,
    }
    if duration:
        body["Duration"] = duration
    if segments:
        try:
            body["Segments"] = json.loads(segments)
        except json.JSONDecodeError:
            return {"status": "error", "error": f"Failed to parse segments JSON: {segments}"}

    action = _get_song_action("bgm", billing)
    resp = client.request(action, body)
    task_id = resp.get("Result", {}).get("TaskID")
    if not task_id:
        return {"status": "error", "error": f"No TaskID returned: {resp}"}

    print(f"BGM task submitted: TaskID={task_id}", file=sys.stderr)

    try:
        result = _poll_task(client, task_id, max_wait)
    except TimeoutError as e:
        return {"status": "timeout", "mode": "bgm", "task_id": task_id, "error": str(e)}

    detail = result.get("SongDetail", {})
    return {
        "status": "success",
        "mode": "bgm",
        "task_id": task_id,
        "audio_url": detail.get("AudioUrl"),
        "duration": detail.get("Duration"),
        "prompt": detail.get("Prompt"),
        "error": None,
    }


def generate_lyrics(
    client: VolcEngineApiClient,
    prompt: str,
    genre: Optional[str] = None,
    mood: Optional[str] = None,
    gender: Optional[str] = None,
    model_version: Optional[str] = None,
) -> dict:
    if not prompt:
        return {"status": "error", "error": "--prompt is required and cannot be empty"}

    body: Dict[str, Any] = {"Prompt": prompt}
    if genre:
        body["Genre"] = genre
    if mood:
        body["Mood"] = mood
    if gender:
        body["Gender"] = gender
    if model_version:
        body["ModelVersion"] = model_version

    resp = client.request("GenLyrics", body)
    result = resp.get("Result", {})
    return {
        "status": "success",
        "mode": "lyrics",
        "task_id": result.get("TaskID"),
        "lyrics": result.get("Lyrics"),
        "genre": result.get("Genre"),
        "mood": result.get("Mood"),
        "gender": result.get("Gender"),
        "error": None,
    }


def query_task(client: VolcEngineApiClient, task_id: str) -> dict:
    resp = client.request("QuerySong", {"TaskID": task_id})
    result = resp.get("Result", {})
    status = result.get("Status")
    detail = result.get("SongDetail", {})
    failure = result.get("FailureReason")

    status_map = {0: "waiting", 1: "processing", 2: "success", 3: "failed"}
    return {
        "status": status_map.get(status, f"unknown({status})"),
        "mode": "query",
        "task_id": task_id,
        "audio_url": detail.get("AudioUrl"),
        "duration": detail.get("Duration"),
        "lyrics": detail.get("Lyrics"),
        "genre": detail.get("Genre"),
        "mood": detail.get("Mood"),
        "failure_reason": failure,
        "error": None,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Music generation using Volcengine Imagination API"
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # --- song ---
    song_parser = subparsers.add_parser("song", help="Generate vocal song")
    song_parser.add_argument("--lyrics", help="Lyrics with structure tags")
    song_parser.add_argument("--prompt", help="Text prompt (Chinese, 5-700 chars)")
    song_parser.add_argument(
        "--model-version", default="v4.3", choices=["v4.0", "v4.3"]
    )
    song_parser.add_argument("--genre", help="Music genre")
    song_parser.add_argument("--mood", help="Music mood")
    song_parser.add_argument("--gender", choices=["Female", "Male"])
    song_parser.add_argument("--timbre", help="Vocal timbre")
    song_parser.add_argument("--duration", type=int, help="Duration in seconds [30-240]")
    song_parser.add_argument("--key", help="Musical key (v4.3)")
    song_parser.add_argument("--kmode", choices=["Major", "Minor"], help="Key mode (v4.3)")
    song_parser.add_argument("--tempo", help="Tempo (v4.3)")
    song_parser.add_argument("--instrument", help="Instruments, comma-separated (v4.3)")
    song_parser.add_argument("--genre-extra", help="Secondary genres, comma-separated, max 2 (v4.3)")
    song_parser.add_argument("--scene", help="Scene tags, comma-separated (v4.3)")
    song_parser.add_argument("--lang", choices=["Chinese", "English", "Instrumental/Non-vocal"])
    song_parser.add_argument("--vod-format", choices=["wav", "mp3"])
    song_parser.add_argument(
        "--billing", default="postpaid", choices=["prepaid", "postpaid"]
    )
    song_parser.add_argument(
        "--timeout", type=int, default=MAX_WAIT_SECONDS, help="Max wait seconds"
    )

    # --- bgm ---
    bgm_parser = subparsers.add_parser("bgm", help="Generate instrumental BGM")
    bgm_parser.add_argument("--text", required=True, help="BGM description")
    bgm_parser.add_argument("--duration", type=int, help="Duration in seconds [30-120]")
    bgm_parser.add_argument("--version", default="v5.0", help="Model version")
    bgm_parser.add_argument(
        "--segments",
        help='JSON array of segments, e.g. \'[{"Name":"verse","Duration":20}]\'',
    )
    bgm_parser.add_argument("--enable-input-rewrite", action="store_true")
    bgm_parser.add_argument(
        "--billing", default="postpaid", choices=["prepaid", "postpaid"]
    )
    bgm_parser.add_argument(
        "--timeout", type=int, default=MAX_WAIT_SECONDS, help="Max wait seconds"
    )

    # --- lyrics ---
    lyrics_parser = subparsers.add_parser("lyrics", help="Generate lyrics")
    lyrics_parser.add_argument("--prompt", required=True, help="Lyrics prompt (Chinese)")
    lyrics_parser.add_argument("--genre", help="Music genre")
    lyrics_parser.add_argument("--mood", help="Music mood")
    lyrics_parser.add_argument("--gender", choices=["Female", "Male"])
    lyrics_parser.add_argument("--model-version", default=None)

    # --- query ---
    query_parser = subparsers.add_parser("query", help="Query task status")
    query_parser.add_argument("--task-id", required=True, help="Task ID to query")

    args = parser.parse_args()

    try:
        client = _get_client()
    except PermissionError as e:
        print(
            json.dumps({"status": "error", "error": str(e)}, indent=2, ensure_ascii=False)
        )
        sys.exit(1)

    try:
        if args.mode == "song":
            result = generate_song(
                client,
                billing=args.billing,
                lyrics=args.lyrics,
                prompt=args.prompt,
                model_version=args.model_version,
                genre=args.genre,
                mood=args.mood,
                gender=args.gender,
                timbre=args.timbre,
                duration=args.duration,
                key=args.key,
                kmode=args.kmode,
                tempo=args.tempo,
                instrument=args.instrument,
                genre_extra=args.genre_extra,
                scene=args.scene,
                lang=args.lang,
                vod_format=args.vod_format,
                max_wait=args.timeout,
            )
        elif args.mode == "bgm":
            result = generate_bgm(
                client,
                text=args.text,
                billing=args.billing,
                duration=args.duration,
                version=args.version,
                segments=args.segments,
                enable_input_rewrite=args.enable_input_rewrite,
                max_wait=args.timeout,
            )
        elif args.mode == "lyrics":
            result = generate_lyrics(
                client,
                prompt=args.prompt,
                genre=args.genre,
                mood=args.mood,
                gender=args.gender,
                model_version=args.model_version,
            )
        elif args.mode == "query":
            result = query_task(client, args.task_id)
        else:
            result = {"status": "error", "error": f"Unknown mode: {args.mode}"}
    except Exception as e:
        result = {"status": "error", "error": str(e)}

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("status") in ("success",) else 1)


if __name__ == "__main__":
    main()
