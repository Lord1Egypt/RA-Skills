"""YouTube collector with transcript-first strategy."""

from __future__ import annotations

import logging
import os
import re
import subprocess
import tempfile

import requests

from datapulse.core.models import MediaType, SourceType
from datapulse.core.security import get_secret, has_secret
from datapulse.core.utils import clean_text, generate_excerpt

from .base import BaseCollector, ParseResult

logger = logging.getLogger("datapulse.parsers.youtube")


class YouTubeCollector(BaseCollector):
    name = "youtube"
    source_type = SourceType.YOUTUBE
    reliability = 0.9
    tier = 2
    setup_hint = "pip install youtube-transcript-api; set GROQ_API_KEY for Whisper fallback"
    preferred_languages = ["en", "zh-Hans", "zh", "ja", "ko", "de", "fr", "es"]
    max_metadata_bytes = 2_000_000

    def check(self) -> dict[str, str | bool]:
        try:
            import youtube_transcript_api  # noqa: F401
            has_transcript = True
        except ImportError:
            has_transcript = False
        has_groq = has_secret("GROQ_API_KEY")
        if not has_transcript and not has_groq:
            return {"status": "warn", "message": "youtube-transcript-api missing and no GROQ_API_KEY", "available": False}
        parts = []
        if has_transcript:
            parts.append("transcript-api")
        if has_groq:
            parts.append("groq-whisper")
        return {"status": "ok", "message": f"backends: {', '.join(parts)}", "available": True}

    def can_handle(self, url: str) -> bool:
        return "youtube.com" in (url.lower()) or "youtu.be" in url.lower()

    def parse(self, url: str) -> ParseResult:
        video_id = self._extract_video_id(url)
        if not video_id:
            return ParseResult.failure(url, "Cannot extract YouTube video ID.")

        title, author, description = self._fetch_metadata(url)
        transcript, transcript_lang = self._fetch_transcript(video_id)
        flags = []
        if transcript:
            flags.extend(["transcript", "youtube-transcript-api"])
            content = transcript
            if transcript_lang:
                flags.append(f"lang:{transcript_lang}")
        else:
            logger.info("No transcript available for %s, try Whisper fallback via yt-dlp", video_id)
            whisper = self._fallback_whisper(url)
            if whisper:
                flags.extend(["whisper", "groq"])
                content = whisper
            else:
                flags.append("metadata-only")
                content = description or ""

        if not content:
            return ParseResult.failure(url, "No YouTube content extracted")

        extra: dict[str, object] = {"video_id": video_id, "lang": transcript_lang if transcript else "", "has_transcript": bool(transcript)}
        if description:
            chapters = self._parse_chapters(description)
            if chapters:
                extra["chapters"] = chapters

        return ParseResult(
            url=url,
            title=title or f"YouTube Video ({video_id})",
            content=clean_text(content),
            author=author,
            excerpt=generate_excerpt(content),
            source_type=self.source_type,
            media_type=MediaType.VIDEO.value,
            tags=["youtube", "video", "transcript" if "transcript" in flags else "metadata"],
            confidence_flags=flags,
            extra=extra,
        )

    @staticmethod
    def _parse_chapters(description: str) -> list[dict[str, object]]:
        """Parse YouTube chapters from video description.

        Matches patterns like:
        - 0:00 Intro
        - 1:23 - Main Topic
        - 1:02:30 Deep Dive
        """
        pattern = re.compile(r"^(\d{1,2}:\d{2}(?::\d{2})?)\s*[-–—]?\s*(.+)$", re.MULTILINE)
        chapters: list[dict[str, object]] = []
        for m in pattern.finditer(description):
            timestamp = m.group(1)
            title = m.group(2).strip()
            parts = timestamp.split(":")
            if len(parts) == 3:
                seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            else:
                seconds = int(parts[0]) * 60 + int(parts[1])
            chapters.append({"timestamp": timestamp, "seconds": seconds, "title": title})
        return chapters

    def _extract_video_id(self, url: str) -> str:
        if "youtu.be" in url:
            return url.split("/")[-1].split("?")[0]
        m = re.search(r"[?&]v=([a-zA-Z0-9_-]{6,})", url)
        if m:
            return m.group(1)
        m = re.search(r"/embed/([a-zA-Z0-9_-]{6,})", url)
        if m:
            return m.group(1)
        m = re.search(r"/shorts/([a-zA-Z0-9_-]{6,})", url)
        if m:
            return m.group(1)
        return ""

    def _fetch_metadata(self, url: str) -> tuple[str, str, str]:
        try:
            with requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"},
                timeout=20,
                allow_redirects=True,
                stream=True,
            ) as resp:
                resp.raise_for_status()
                body = bytearray()
                for chunk in resp.iter_content(chunk_size=8192):
                    if not chunk:
                        continue
                    body.extend(chunk)
                    if len(body) > self.max_metadata_bytes:
                        raise ValueError("YouTube page too large")
                text = body.decode(resp.encoding or resp.apparent_encoding or "utf-8", errors="replace")

            from bs4 import BeautifulSoup

            soup = BeautifulSoup(text, "lxml")
            title = ""
            og_title = soup.find("meta", property="og:title")
            if og_title:
                title = str(og_title.get("content", "")).strip()  # type: ignore[union-attr]
            if not title:
                title = soup.title.get_text(strip=True) if soup.title else ""
            author = ""
            og_author = soup.find("link", attrs={"itemprop": "name"})
            if og_author:
                author = str(og_author.get("content", "")).strip()  # type: ignore[union-attr]
            if not author:
                og_chan = soup.find("meta", property="og:video:tag")
                author = str(og_chan.get("content", "")) if og_chan else ""  # type: ignore[union-attr]
            desc = ""
            og_desc = soup.find("meta", property="og:description")
            if og_desc:
                desc = str(og_desc.get("content", "")).strip()  # type: ignore[union-attr]
            return title, author, desc
        except Exception:
            return "", "", ""

    def _fetch_transcript(self, video_id: str) -> tuple[str, str]:
        try:
            from youtube_transcript_api import YouTubeTranscriptApi

            api = YouTubeTranscriptApi()
            transcript_list = api.list(video_id)
            transcript = None
            lang = ""
            for candidate in self.preferred_languages:
                try:
                    transcript = transcript_list.find_manually_created_transcript([candidate])
                    lang = candidate
                    break
                except Exception:
                    continue
            if transcript is None:
                for candidate in self.preferred_languages:
                    try:
                        transcript = transcript_list.find_generated_transcript([candidate])
                        lang = f"{candidate} (auto)"
                        break
                    except Exception:
                        continue
            if transcript is None:
                entries = list(transcript_list)
                if entries:
                    transcript = entries[0]
                    lang = transcript.language_code

            if transcript is None:
                return "", ""

            segments = transcript.fetch()
            lines = [getattr(s, "text", "") for s in segments]
            text = " ".join(line for line in lines if line)
            return (clean_text(text), lang)
        except Exception as exc:
            logger.warning("Transcript failed for %s: %s", video_id, exc)
            return "", ""

    def _fallback_whisper(self, url: str) -> str:
        api_key = get_secret("GROQ_API_KEY")
        if not api_key:
            return ""

        with tempfile.TemporaryDirectory() as tmp:
            output = os.path.join(tmp, "audio.%(ext)s")
            cmd = [
                "yt-dlp",
                "-x",
                "--audio-format",
                "m4a",
                "--audio-quality",
                "5",
                "-o",
                output,
                "--no-playlist",
                url,
            ]
            try:
                subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            except Exception:
                return ""

            audio_file = ""
            for name in os.listdir(tmp):
                if name.startswith("audio."):
                    audio_file = os.path.join(tmp, name)
                    break
            if not audio_file or not os.path.exists(audio_file):
                return ""

            if os.path.getsize(audio_file) > 25 * 1024 * 1024:
                return ""

            with open(audio_file, "rb") as f:
                files = {"file": (os.path.basename(audio_file), f, "audio/mp4")}
                payload = {"model": "whisper-large-v3", "response_format": "text"}
                headers = {"Authorization": f"Bearer {api_key}"}
                try:
                    response = requests.post(
                        "https://api.groq.com/openai/v1/audio/transcriptions",
                        headers=headers,
                        files=files,
                        data=payload,
                        timeout=120,
                    )
                    if response.status_code == 200:
                        return clean_text(response.text)
                except Exception:
                    return ""
        return ""
