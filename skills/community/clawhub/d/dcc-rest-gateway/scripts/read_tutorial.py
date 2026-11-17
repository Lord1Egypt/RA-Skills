# /// script
# requires-python = ">=3.10"
# dependencies = ["yt-dlp[default]==2026.10.21"]
# ///
"""Collect private, timestamped tutorial evidence without an LLM or browser."""

from __future__ import annotations

import argparse
import contextlib
import copy
import hashlib
import json
import math
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

MAX_DOWNLOAD_BYTES = 512 * 1024 * 1024
MAX_CAPTION_BYTES = 2 * 1024 * 1024
MAX_CAPTION_TOTAL_BYTES = 6 * 1024 * 1024
MAX_LOG_BYTES = 1024 * 1024
MAX_TOOL_OUTPUT_BYTES = 64 * 1024
MAX_WALL_SECONDS = 300
LOCAL_MEDIA_OPTIONS = [
    "-protocol_whitelist",
    "file",
    "-format_whitelist",
    "mov,mp4,m4a,3gp,3g2,mj2,matroska,webm",
]


class BudgetExceeded(ValueError):
    """An explicit collection limit, rather than a provider availability result."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def source_extractor(url: str) -> str:
    """Restrict the top-level source, not every CDN request made by yt-dlp."""
    uri = urlsplit(url)
    if (
        uri.scheme != "https"
        or uri.username is not None
        or uri.password is not None
        or uri.port not in (None, 443)
        or uri.fragment
    ):
        raise ValueError(
            "Use one supported public HTTPS video URL without credentials or fragment"
        )
    host, path = uri.hostname, uri.path.rstrip("/")
    video_id = r"[A-Za-z0-9_-]{11}"
    query = parse_qs(uri.query)
    if host in ("youtube.com", "www.youtube.com", "m.youtube.com"):
        if (
            path == "/watch"
            and len(query.get("v", [])) == 1
            and re.fullmatch(video_id, query["v"][0])
        ) or re.fullmatch(r"/shorts/" + video_id, path):
            return "Youtube"
    elif host == "youtu.be" and re.fullmatch("/" + video_id, path):
        return "Youtube"
    elif host in ("bilibili.com", "www.bilibili.com", "m.bilibili.com"):
        if re.fullmatch(r"/video/(?:BV[A-Za-z0-9]{10}|av[0-9]+)", path):
            return "BiliBili"
    elif host in ("vimeo.com", "www.vimeo.com") and re.fullmatch(r"/[0-9]+", path):
        return "Vimeo"
    raise ValueError(
        "Supported sources are public YouTube, Bilibili and Vimeo video routes"
    )


class BoundedLog:
    """Keep a real UTF-8 byte cap even when a provider emits one giant write."""

    def __init__(self, path: Path):
        self.file = path.open("wb")
        self.written = 0
        self.exceeded = False

    def write(self, text: str) -> int:
        data = text.encode("utf-8", errors="replace")
        remaining = max(0, MAX_LOG_BYTES - self.written)
        retained = data[:remaining].decode("utf-8", errors="ignore").encode("utf-8")
        self.file.write(retained)
        self.written += len(retained)
        if len(data) > remaining:
            self.exceeded = True
            raise BudgetExceeded("Provider log exceeded the byte budget")
        return len(text)

    def flush(self) -> None:
        self.file.flush()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.file.close()


def check_download_size(progress: dict) -> None:
    """Enforce video bytes even when the server omits Content-Length."""
    if progress.get("downloaded_bytes", 0) > MAX_DOWNLOAD_BYTES:
        raise BudgetExceeded("Video download exceeded the byte budget")


def caption_paths(info: dict, output: Path, languages: list[str]) -> list[tuple]:
    tracks = []
    for language, track in (info.get("requested_subtitles") or {}).items():
        ext = track.get("ext", "")
        if language not in languages or not ext.isalnum():
            raise ValueError("Unexpected subtitle path from provider")
        path = output / ("source." + language + "." + ext)
        if path.resolve().parent != output.resolve():
            raise ValueError("Unexpected subtitle path from provider")
        tracks.append((language, track, path))
    inline = [
        len(track["data"].encode("utf-8")) for _, track, _ in tracks if "data" in track
    ]
    if (
        any(size > MAX_CAPTION_BYTES for size in inline)
        or sum(inline) > MAX_CAPTION_TOTAL_BYTES
    ):
        raise BudgetExceeded("Subtitle bytes exceeded the byte budget")
    return tracks


def discard_oversize_captions(output: Path) -> list[dict]:
    """Only our fresh directory's subtitle prefix; preserve the rejected sizes."""
    discarded = []
    for path in output.glob("source.*"):
        if (
            path.is_file()
            and not path.is_symlink()
            and path.stat().st_size > MAX_CAPTION_BYTES
        ):
            discarded.append({"path": path.name, "bytes": path.stat().st_size})
            path.unlink()
    return discarded


def run_tool(command: list[str], timeout: float = 60) -> str:
    """Bound tool output and lifetime; terminate only this held Popen on failure."""
    process = subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    data = bytearray()
    overflow = threading.Event()

    def drain():
        while chunk := process.stdout.read(4096):
            remaining = MAX_TOOL_OUTPUT_BYTES - len(data)
            data.extend(chunk[:remaining])
            if len(chunk) > remaining:
                overflow.set()
                if process.poll() is None:
                    process.kill()
                break

    thread = threading.Thread(target=drain, daemon=True)
    thread.start()
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        raise BudgetExceeded("Media tool exceeded its wall-clock budget") from None
    finally:
        thread.join(timeout=5)
        process.stdout.close()
    if overflow.is_set():
        raise BudgetExceeded("Media tool output exceeded the byte budget")
    text = data.decode("utf-8", errors="replace")
    if process.returncode:
        raise ValueError("Media tool failed: " + text)
    return text


def runtime_receipt(executable: str | None, flag: str) -> dict | None:
    if executable is None:
        return None
    return {
        "path": executable,
        "version": run_tool([executable, flag], timeout=10).splitlines()[0],
    }


def decoded_timestamp(text: str, stream: dict, start: float) -> dict:
    base = re.search(r"config in time_base:\s*([0-9]+/[0-9]+)", text)
    frame = re.search(r"\bn:\s*0\s+pts:\s*(-?[0-9]+)\s+pts_time:\s*([-+0-9.eE]+)", text)
    if not base or not frame:
        raise ValueError("FFmpeg did not report the decoded frame PTS and time base")
    pts, time_base = int(frame[1]), base[1]
    seconds = float(pts * Fraction(time_base))
    return {
        "decoded_pts": pts,
        "decoded_time_base": time_base,
        "decoded_pts_seconds": seconds,
        "decoded_media_seconds": seconds - start,
        "stream_time_base": stream["time_base"],
        "crop": None,
    }


def inventory(path: Path) -> dict:
    """Bind an evidence file to its actual bytes."""
    if path.is_symlink() or not path.is_file():
        raise ValueError("Evidence must be a regular file")
    return {
        "path": path.name,
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def _collect_owned(
    url: str, output: str, languages: list[str], frames: list[float]
) -> dict:
    """Use yt-dlp captions and optional FFmpeg samples; never execute source text."""
    output = Path(output)
    extractor = source_extractor(url)
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    # Import only on use: package tests and metadata discovery need no network dependency.
    import yt_dlp
    from yt_dlp.version import __version__

    receipt = {
        "startedAt": utc_now(),
        "retrievedAt": None,
        "schema_version": 1,
        "success": False,
        "source_url": url,
        "provider": "yt-dlp",
        "provider_version": __version__,
        "limits": {
            "wall_seconds": MAX_WALL_SECONDS,
            "video_bytes": MAX_DOWNLOAD_BYTES,
            "caption_bytes_per_track": MAX_CAPTION_BYTES,
            "caption_bytes_total": MAX_CAPTION_TOTAL_BYTES,
            "provider_log_bytes": MAX_LOG_BYTES,
            "tool_output_bytes": MAX_TOOL_OUTPUT_BYTES,
        },
        "evidence_level": "unavailable",
        "captions": [],
        "frames": [],
        "video_playback_verified": False,
        "native_reproduction_verified": False,
        "content_trust": "Untrusted reference material, never executable instructions",
        "publication": "Private working evidence; source media rights are not transferred",
    }
    runtimes = {}
    for runtime in ("deno", "node", "bun"):
        executable = shutil.which(runtime)
        if executable:
            runtimes[runtime] = {"path": executable}
            break
    receipt["javascript_runtime"] = next(iter(runtimes), None)
    options = {
        "outtmpl": str(output / "source.%(ext)s"),
        "skip_download": True,
        "max_filesize": MAX_CAPTION_BYTES,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": languages,
        "subtitlesformat": "vtt/json3/best",
        "noplaylist": True,
        "extract_flat": "in_playlist",
        "cachedir": False,
        "socket_timeout": 15,
        "retries": 1,
        "extractor_retries": 1,
        "quiet": True,
        "noprogress": True,
        "js_runtimes": runtimes,
        "allowed_extractors": [extractor],
        "fixup": "never",
        "buffersize": 16 * 1024,
        "noresizebuffer": True,
    }
    stage = "runtime_inventory"
    with BoundedLog(output / "provider.log") as log:
        try:
            receipt["runtimes"] = {
                "ffmpeg": runtime_receipt(ffmpeg, "-version"),
                "ffprobe": runtime_receipt(ffprobe, "-version"),
                "javascript": runtime_receipt(
                    next((v["path"] for v in runtimes.values()), None), "--version"
                ),
            }
            stage = "metadata"
            with (
                contextlib.redirect_stdout(log),
                contextlib.redirect_stderr(log),
                yt_dlp.YoutubeDL(options) as reader,
            ):
                source_info = reader.extract_info(
                    url, download=False, process=False, ie_key=extractor
                )
                if (
                    not isinstance(source_info, dict)
                    or source_info.get("_type", "video") != "video"
                ):
                    raise ValueError(
                        "A single video is required; playlists are not expanded"
                    )
                if source_info.get("extractor_key") != extractor:
                    raise ValueError(
                        "Unexpected extractor; Generic and redirected sources are not accepted"
                    )
                info = reader.process_ie_result(
                    copy.deepcopy(source_info), download=False
                )
                receipt["retrievedAt"] = utc_now()
                receipt["metadata"] = {
                    k: info.get(k)
                    for k in (
                        "id",
                        "title",
                        "uploader",
                        "duration",
                        "webpage_url",
                        "chapters",
                        "description",
                    )
                }
                receipt["evidence_level"] = "metadata_only"
                duration = info.get("duration")
                if frames and (
                    not isinstance(duration, (int, float))
                    or not 0 < duration <= 7200
                    or any(t >= duration for t in frames)
                ):
                    raise ValueError(
                        "Frame sampling requires a known duration up to two hours and times within it"
                    )
                stage = "captions"
                tracks = caption_paths(info, output, languages)
                caption_downloads = {}
                caption_budget_exceeded = False

                def check_caption_size(progress):
                    nonlocal caption_budget_exceeded
                    size = progress.get("downloaded_bytes", 0)
                    key = progress.get("filename", "subtitle")
                    caption_downloads[key] = max(size, caption_downloads.get(key, 0))
                    if (
                        size > MAX_CAPTION_BYTES
                        or sum(caption_downloads.values()) > MAX_CAPTION_TOTAL_BYTES
                    ):
                        caption_budget_exceeded = True
                        raise BudgetExceeded(
                            "Subtitle download exceeded the byte budget"
                        )

                reader.add_progress_hook(check_caption_size)
                reader.process_info(info)
                if caption_budget_exceeded:
                    raise BudgetExceeded("Subtitle download exceeded the byte budget")
                total_caption_bytes = 0
                for language, track, path in tracks:
                    if path.is_file():
                        size = path.stat().st_size
                        total_caption_bytes += size
                        if (
                            size > MAX_CAPTION_BYTES
                            or total_caption_bytes > MAX_CAPTION_TOTAL_BYTES
                        ):
                            raise BudgetExceeded(
                                "Subtitle files exceeded the byte budget"
                            )
                        row = inventory(path)
                        row.update(
                            language=language,
                            automatic=language not in (info.get("subtitles") or {}),
                        )
                        receipt["captions"].append(row)
                if receipt["captions"]:
                    receipt["evidence_level"] = "timestamped_captions"
                if frames:
                    stage = "video_download"
                    video_options = dict(
                        options,
                        outtmpl=str(output / "video.%(ext)s"),
                        skip_download=False,
                        writesubtitles=False,
                        writeautomaticsub=False,
                        format="best[height<=720][ext=mp4]/bestvideo[height<=720][ext=mp4]/best[height<=720][ext=webm]/bestvideo[height<=720][ext=webm]",
                        max_filesize=MAX_DOWNLOAD_BYTES,
                        progress_hooks=[check_download_size],
                    )
                    with yt_dlp.YoutubeDL(video_options) as video_reader:
                        video_info = video_reader.process_ie_result(
                            source_info, download=True
                        )
                        video = Path(video_reader.prepare_filename(video_info))
                    if (
                        video.resolve().parent != output.resolve()
                        or video.stat().st_size > MAX_DOWNLOAD_BYTES
                    ):
                        raise ValueError(
                            "Video path or size exceeded the download contract"
                        )
                    receipt["downloaded_video"] = inventory(video)
                    stage = "frame_sampling"
                    probe = json.loads(
                        run_tool(
                            [
                                ffprobe,
                                "-v",
                                "error",
                                *LOCAL_MEDIA_OPTIONS,
                                "-select_streams",
                                "v:0",
                                "-show_entries",
                                "stream=index,time_base,start_time:format=format_name,start_time",
                                "-of",
                                "json",
                                str(video),
                            ]
                        )
                    )
                    stream = probe["streams"][0]
                    start = float(
                        probe.get("format", {}).get(
                            "start_time", stream.get("start_time", 0)
                        )
                    )
                    receipt["media_probe"] = probe
                    for index, seconds in enumerate(frames):
                        image = output / f"frame-{index:02d}.png"
                        decoded = run_tool(
                            [
                                ffmpeg,
                                "-nostdin",
                                "-hide_banner",
                                "-nostats",
                                "-v",
                                "info",
                                "-copyts",
                                "-ss",
                                str(seconds),
                                *LOCAL_MEDIA_OPTIONS,
                                "-i",
                                str(video),
                                "-map",
                                "0:v:0",
                                "-vf",
                                "showinfo",
                                "-frames:v",
                                "1",
                                "-fps_mode",
                                "passthrough",
                                "-n",
                                str(image),
                            ]
                        )
                        if not image.is_file() or not image.stat().st_size:
                            raise ValueError("Requested frame was not produced")
                        receipt["frames"].append(
                            dict(
                                inventory(image),
                                requested_seconds=seconds,
                                **decoded_timestamp(decoded, stream, start),
                            )
                        )
                    receipt["evidence_level"] = (
                        "sampled_frames_and_captions"
                        if receipt["captions"]
                        else "sampled_frames_only"
                    )
                if log.exceeded:
                    raise BudgetExceeded("Provider log exceeded the byte budget")
                receipt["success"] = True
        except Exception as error:  # noqa: BLE001 - preserve arbitrary provider failures as evidence
            # Downloader hooks run after a write, so discard oversized owned partials.
            # An incomplete or oversized track is never accepted as raw evidence.
            discarded = discard_oversize_captions(output)
            if discarded:
                receipt["discarded_oversize_captions"] = discarded
                receipt["captions"] = [
                    row
                    for row in receipt["captions"]
                    if not any(row["path"] == item["path"] for item in discarded)
                ]
            # Provider errors can contain signed media URLs; retain details only in the private log.
            with contextlib.suppress(BudgetExceeded):
                print(str(error), file=log)
            receipt["error"] = {
                "stage": stage,
                "type": type(error).__name__,
                "details": "provider.log",
                **(
                    {"message": str(error)} if isinstance(error, BudgetExceeded) else {}
                ),
            }
    receipt["finishedAt"] = utc_now()
    receipt["captions_status"] = "available" if receipt["captions"] else "unavailable"
    (output / "evidence.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return receipt


def _windows_job(process):
    """Assign only our stdin-blocked worker; its future children inherit this job."""
    import ctypes
    from ctypes import wintypes

    class BasicLimit(ctypes.Structure):
        _fields_ = [
            ("process_time", ctypes.c_int64),
            ("job_time", ctypes.c_int64),
            ("flags", wintypes.DWORD),
            ("min_ws", ctypes.c_size_t),
            ("max_ws", ctypes.c_size_t),
            ("active", wintypes.DWORD),
            ("affinity", ctypes.c_size_t),
            ("priority", wintypes.DWORD),
            ("scheduling", wintypes.DWORD),
        ]

    class ExtendedLimit(ctypes.Structure):
        _fields_ = [
            ("basic", BasicLimit),
            ("io", ctypes.c_uint64 * 6),
            ("process_memory", ctypes.c_size_t),
            ("job_memory", ctypes.c_size_t),
            ("peak_process", ctypes.c_size_t),
            ("peak_job", ctypes.c_size_t),
        ]

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    kernel.CreateJobObjectW.restype = wintypes.HANDLE
    kernel.SetInformationJobObject.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    ]
    kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    job = kernel.CreateJobObjectW(None, None)
    if not job:
        raise ctypes.WinError(ctypes.get_last_error())
    limit = ExtendedLimit()
    limit.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    if not kernel.SetInformationJobObject(
        job, 9, ctypes.byref(limit), ctypes.sizeof(limit)
    ) or not kernel.AssignProcessToJobObject(job, wintypes.HANDLE(process._handle)):
        error = ctypes.WinError(ctypes.get_last_error())
        kernel.CloseHandle(job)
        raise error
    return lambda: kernel.CloseHandle(job)


def _supervise(command: list[str], payload: dict, timeout: float) -> None:
    """A hard deadline includes extractor calls, subtitles and all media tools."""
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=os.name != "nt",
    )
    close_job = None
    try:
        if os.name == "nt":
            close_job = _windows_job(process)
        process.communicate(json.dumps(payload).encode("utf-8"), timeout=timeout)
        if process.returncode:
            raise RuntimeError("Tutorial worker exited without a complete result")
    except subprocess.TimeoutExpired:
        raise BudgetExceeded(
            "Collection exceeded the overall wall-clock budget"
        ) from None
    finally:
        # Never inspect names or terminate unrelated PIDs. The worker blocks on stdin
        # until its ownership group/job has been assigned.
        if close_job is not None:
            close_job()
        elif os.name != "nt":
            with contextlib.suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGKILL)
        if process.poll() is None:
            process.kill()
        process.wait()
        if process.stdin:
            process.stdin.close()


def _run_worker(payload: dict, output: Path) -> None:
    bootstrap = (
        "import json,runpy,sys; "
        "m=runpy.run_path(sys.argv[1]); "
        "m['_collect_owned'](**json.load(sys.stdin))"
    )
    _supervise(
        [sys.executable, "-c", bootstrap, str(Path(__file__).resolve())],
        payload,
        MAX_WALL_SECONDS,
    )


def collect(url: str, output: Path, languages: list[str], frames: list[float]) -> dict:
    """Reserve fresh evidence, then run synchronous provider code in an owned worker."""
    source_extractor(url)
    if not 1 <= len(languages) <= 3 or any(
        not language
        or language.lower() == "all"
        or not language[0].isalpha()
        or len(language) > 20
        or any(
            c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
            for c in language
        )
        for language in languages
    ):
        raise ValueError("Choose one to three exact subtitle language codes")
    if len(frames) > 12 or any(not math.isfinite(t) or t < 0 for t in frames):
        raise ValueError("Choose at most twelve finite, nonnegative frame times")
    if frames and (shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None):
        raise ValueError("FFmpeg and ffprobe are required for requested frame samples")
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    fallback = {
        "schema_version": 1,
        "success": False,
        "source_url": url,
        "startedAt": utc_now(),
        "retrievedAt": None,
        "evidence_level": "unavailable",
        "captions": [],
        "frames": [],
        "captions_status": "unavailable",
        "video_playback_verified": False,
        "native_reproduction_verified": False,
    }
    evidence = output / "evidence.json"
    evidence.write_text(json.dumps(fallback, indent=2) + "\n", encoding="utf-8")
    try:
        _run_worker(
            {
                "url": url,
                "output": str(output),
                "languages": languages,
                "frames": frames,
            },
            output,
        )
        return json.loads(evidence.read_text(encoding="utf-8"))
    except (OSError, RuntimeError, ValueError) as error:
        # The worker may have been interrupted between a download write and hook.
        discarded = discard_oversize_captions(output)
        if discarded:
            fallback["discarded_oversize_captions"] = discarded
        fallback.update(
            finishedAt=utc_now(),
            error={
                "stage": "wall_clock"
                if isinstance(error, BudgetExceeded)
                else "worker",
                "type": type(error).__name__,
                "message": str(error),
            },
        )
        evidence.write_text(json.dumps(fallback, indent=2) + "\n", encoding="utf-8")
        return fallback


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="New private directory; existing paths are never overwritten",
    )
    parser.add_argument("--languages", default="en,zh-Hans,zh-Hant")
    parser.add_argument(
        "--frame",
        type=float,
        action="append",
        default=[],
        help="Opt in to a bounded video download and sample at these seconds",
    )
    args = parser.parse_args()
    try:
        receipt = collect(args.url, args.out, args.languages.split(","), args.frame)
    except (ImportError, OSError, ValueError) as error:
        print(json.dumps({"success": False, "error": str(error)}))
        return 1
    print(
        json.dumps(
            {
                "success": receipt["success"],
                "evidence_level": receipt["evidence_level"],
                "captions_status": receipt["captions_status"],
                "frame_count": len(receipt["frames"]),
                "receipt": str(args.out / "evidence.json"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if receipt["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
