#!/usr/bin/env python3
"""
YouTube Transcript Extractor

Fetches the transcript of a YouTube video from its URL and prints
the plain text. Optionally writes the result to a file.

Usage:
    python extract_youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
    python extract_youtube_transcript.py "https://youtu.be/VIDEO_ID" --lang zh-Hant en
    python extract_youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" --output transcript.txt
    python extract_youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" --list-langs
    python extract_youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" --cookies youtube_cookies.txt
"""

import argparse
import sys
from http.cookiejar import MozillaCookieJar
from urllib.parse import urlparse, parse_qs

import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    AgeRestricted,
    InvalidVideoId,
)


def extract_video_id(url: str) -> str:
    """
    Parse a YouTube video ID from common URL formats:
      - https://www.youtube.com/watch?v=VIDEO_ID
      - https://youtu.be/VIDEO_ID
      - https://www.youtube.com/embed/VIDEO_ID
      - https://www.youtube.com/live/VIDEO_ID
      - Raw video ID (11 chars, no slash)
    """
    url = url.strip()

    parsed = urlparse(url)

    # Raw video ID passed directly (no scheme)
    if not parsed.scheme and "/" not in url:
        return url

    host = parsed.netloc.lower().removeprefix("www.")

    if host in ("youtube.com", "m.youtube.com"):
        for prefix in ("/embed/", "/live/", "/shorts/"):
            if parsed.path.startswith(prefix):
                video_id = parsed.path.split(prefix, 1)[1].split("/")[0]
                if video_id:
                    return video_id
        # /watch?v=VIDEO_ID
        qs = parse_qs(parsed.query)
        ids = qs.get("v", [])
        if ids:
            return ids[0]

    elif host == "youtu.be":
        # youtu.be/VIDEO_ID
        video_id = parsed.path.lstrip("/").split("/")[0]
        if video_id:
            return video_id

    raise ValueError(
        f"Could not extract a video ID from the provided URL: {url}\n"
        "Supported formats:\n"
        "  https://www.youtube.com/watch?v=VIDEO_ID\n"
        "  https://youtu.be/VIDEO_ID\n"
        "  https://www.youtube.com/embed/VIDEO_ID\n"
        "  https://www.youtube.com/live/VIDEO_ID\n"
        "  https://www.youtube.com/shorts/VIDEO_ID"
    )


def format_transcript(transcript) -> str:
    """Join all snippet texts into a single readable string."""
    return " ".join(snippet.text for snippet in transcript)


def make_api(cookies: str | None) -> YouTubeTranscriptApi:
    """Instantiate the API, optionally with a Netscape cookies file."""
    if cookies:
        jar = MozillaCookieJar(cookies)
        jar.load(ignore_discard=True, ignore_expires=True)
        session = requests.Session()
        session.cookies = jar
        return YouTubeTranscriptApi(http_client=session)
    return YouTubeTranscriptApi()


def list_available_languages(video_id: str, cookies: str | None) -> None:
    """Print all available transcript languages for a video."""
    api = make_api(cookies)
    transcript_list = api.list(video_id)
    print(f"Available transcripts for video '{video_id}':\n")
    for t in transcript_list:
        kind = "auto-generated" if t.is_generated else "manual"
        print(f"  [{t.language_code}] {t.language} ({kind})")


def fetch_transcript(video_id: str, languages: list[str], cookies: str | None) -> str:
    """Fetch transcript text, trying preferred languages in order."""
    api = make_api(cookies)

    try:
        transcript = api.fetch(video_id, languages=languages)
    except NoTranscriptFound:
        # Fall back to any available transcript when preferred langs are absent
        transcript_list = api.list(video_id)
        transcript = transcript_list.find_transcript(
            [t.language_code for t in transcript_list]
        ).fetch()

    return format_transcript(transcript)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract the transcript of a YouTube video.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("url", help="YouTube video URL or video ID")
    parser.add_argument(
        "--lang",
        nargs="+",
        default=["en"],
        metavar="LANG",
        help="Language code(s) in order of preference (default: en). "
             "Example: --lang zh-Hant en",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Write transcript to FILE instead of (or in addition to) stdout",
    )
    parser.add_argument(
        "--list-langs",
        action="store_true",
        help="List all available transcript languages for the video and exit",
    )
    parser.add_argument(
        "--cookies",
        metavar="FILE",
        help="Path to a Netscape-format cookies file for YouTube authentication. "
             "Useful when requests are blocked on cloud/server IPs.",
    )

    args = parser.parse_args()

    # --- Step 1: extract video ID ---
    try:
        video_id = extract_video_id(args.url)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    # --- Step 2: list languages if requested ---
    if args.list_langs:
        try:
            list_available_languages(video_id, args.cookies)
        except VideoUnavailable:
            print(f"Error: Video '{video_id}' is unavailable.", file=sys.stderr)
            sys.exit(1)
        except Exception as exc:
            print(f"Error listing transcripts: {exc}", file=sys.stderr)
            sys.exit(1)
        return

    # --- Step 3: fetch transcript ---
    try:
        text = fetch_transcript(video_id, args.lang, args.cookies)
    except TranscriptsDisabled:
        print(
            f"Error: Transcripts/subtitles are disabled for video '{video_id}'.",
            file=sys.stderr,
        )
        sys.exit(1)
    except NoTranscriptFound:
        print(
            f"Error: No transcript found for video '{video_id}' "
            f"in requested language(s): {args.lang}.\n"
            f"Run with --list-langs to see what is available.",
            file=sys.stderr,
        )
        sys.exit(1)
    except VideoUnavailable:
        print(f"Error: Video '{video_id}' is unavailable.", file=sys.stderr)
        sys.exit(1)
    except AgeRestricted:
        print(
            f"Error: Video '{video_id}' is age-restricted. "
            "Authentication is required to access its transcript.",
            file=sys.stderr,
        )
        sys.exit(1)
    except InvalidVideoId:
        print(
            f"Error: '{video_id}' is not a valid YouTube video ID.",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)

    # --- Step 4: output ---
    print(text)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(text)
                fh.write("\n")
            print(f"\nTranscript saved to: {args.output}", file=sys.stderr)
        except OSError as exc:
            print(f"Error writing to file '{args.output}': {exc}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
