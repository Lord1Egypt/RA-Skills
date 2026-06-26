#!/usr/bin/env python3
"""Tests for fetch-podcast.py."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
spec = importlib.util.spec_from_file_location("fetch_podcast", SCRIPTS_DIR / "fetch-podcast.py")
fetch_podcast = importlib.util.module_from_spec(spec)
sys.modules["fetch_podcast"] = fetch_podcast
spec.loader.exec_module(fetch_podcast)


def utc(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


class TestPodcastPlatformInference(unittest.TestCase):
    def test_infers_youtube_platform(self):
        self.assertEqual(
            fetch_podcast.infer_platform("https://www.youtube.com/playlist?list=abc"),
            "youtube",
        )
        self.assertEqual(
            fetch_podcast.infer_platform("https://youtu.be/videoid"),
            "youtube",
        )

    def test_infers_rss_platform_for_non_youtube_url(self):
        self.assertEqual(
            fetch_podcast.infer_platform("https://example.com/feed.xml"),
            "rss",
        )

    def test_infers_xiaoyuzhou_platform(self):
        self.assertEqual(
            fetch_podcast.infer_platform(
                "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940"
            ),
            "xiaoyuzhou",
        )
        self.assertEqual(
            fetch_podcast.infer_platform(
                "https://xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940"
            ),
            "xiaoyuzhou",
        )

    def test_extracts_xiaoyuzhou_podcast_id(self):
        self.assertEqual(
            fetch_podcast.extract_xiaoyuzhou_podcast_id(
                "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940"
            ),
            "686a1832222ae2de21fea940",
        )

    def test_extracts_xiaoyuzhou_podcast_id_with_query_and_fragment(self):
        self.assertEqual(
            fetch_podcast.extract_xiaoyuzhou_podcast_id(
                "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940?foo=bar#frag"
            ),
            "686a1832222ae2de21fea940",
        )

    def test_extract_xiaoyuzhou_podcast_id_rejects_non_podcast_url(self):
        self.assertEqual(
            fetch_podcast.extract_xiaoyuzhou_podcast_id(
                "https://www.xiaoyuzhoufm.com/episode/69f441cd5390b7cc928acdcc"
            ),
            "",
        )

    def test_extract_xiaoyuzhou_podcast_id_rejects_empty_podcast_path(self):
        url = "https://www.xiaoyuzhoufm.com/podcast/"
        self.assertEqual(fetch_podcast.extract_xiaoyuzhou_podcast_id(url), "")
        self.assertEqual(fetch_podcast.infer_platform(url), "rss")

    def test_extract_xiaoyuzhou_podcast_id_rejects_extra_path_segments(self):
        self.assertEqual(
            fetch_podcast.extract_xiaoyuzhou_podcast_id(
                "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940/extra"
            ),
            "",
        )


class TestPodcastDateParsing(unittest.TestCase):
    def test_parse_podcast_date_iso(self):
        parsed = fetch_podcast.parse_podcast_date("2026-05-04T20:05:00Z")
        self.assertEqual(parsed.isoformat(), "2026-05-04T20:05:00+00:00")

    def test_parse_podcast_date_rfc2822(self):
        parsed = fetch_podcast.parse_podcast_date("Mon, 04 May 2026 20:05:00 +0000")
        self.assertEqual(parsed.isoformat(), "2026-05-04T20:05:00+00:00")


class TestPodcastRssParsing(unittest.TestCase):
    def test_parse_rss_episodes(self):
        rss = """<?xml version="1.0"?>
<rss><channel>
<item>
  <title>Episode One</title>
  <guid>episode-one</guid>
  <link>https://example.com/episodes/1</link>
  <pubDate>Mon, 04 May 2026 20:05:00 +0000</pubDate>
</item>
<item>
  <title>Old Episode</title>
  <guid>old-episode</guid>
  <link>https://example.com/episodes/old</link>
  <pubDate>Mon, 01 Jan 2024 20:05:00 +0000</pubDate>
</item>
</channel></rss>"""
        source = {
            "id": "test-podcast",
            "name": "Test Podcast",
            "topics": ["llm"],
            "url": "https://example.com/feed.xml",
        }
        cutoff = utc("2026-05-01T00:00:00Z")

        episodes = fetch_podcast.parse_rss_episodes(rss, source, cutoff)

        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0]["title"], "Episode One")
        self.assertEqual(episodes[0]["guid"], "episode-one")
        self.assertEqual(episodes[0]["link"], "https://example.com/episodes/1")
        self.assertEqual(episodes[0]["topics"], ["llm"])
        self.assertEqual(episodes[0]["show_name"], "Test Podcast")
        self.assertEqual(episodes[0]["platform"], "rss")
        self.assertEqual(episodes[0]["transcript_status"], "disabled")

    def test_feedparser_path_scans_full_feed_before_limiting(self):
        old_entries = [
            {
                "title": f"Older Episode {index}",
                "id": f"older-{index}",
                "link": f"https://example.com/episodes/older-{index}",
                "published": f"Mon, {index + 1:02d} May 2026 20:05:00 +0000",
            }
            for index in range(fetch_podcast.MAX_EPISODES_PER_SOURCE)
        ]
        newest_entry = {
            "title": "Newest Episode",
            "id": "newest",
            "link": "https://example.com/episodes/newest",
            "published": "Sun, 31 May 2026 20:05:00 +0000",
        }

        class FakeFeedparser:
            @staticmethod
            def parse(_content):
                return type("Feed", (), {"entries": old_entries + [newest_entry]})()

        source = {
            "id": "test-podcast",
            "name": "Test Podcast",
            "topics": ["llm"],
            "url": "https://example.com/feed.xml",
        }
        cutoff = utc("2026-05-01T00:00:00Z")

        with patch.object(fetch_podcast, "HAS_FEEDPARSER", True):
            with patch.object(fetch_podcast, "feedparser", FakeFeedparser, create=True):
                episodes = fetch_podcast.parse_rss_episodes("", source, cutoff)

        self.assertEqual(len(episodes), fetch_podcast.MAX_EPISODES_PER_SOURCE)
        self.assertEqual(episodes[0]["guid"], "newest")
        self.assertNotIn("older-0", {episode["guid"] for episode in episodes})


class TestPodcastSourceLoading(unittest.TestCase):
    def test_load_podcast_sources_filters_enabled_podcast_sources(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            defaults = Path(tmpdir) / "defaults"
            defaults.mkdir()
            sources_path = defaults / "sources.json"
            sources_path.write_text(
                json.dumps(
                    {
                        "sources": [
                            {
                                "id": "rss-source",
                                "type": "rss",
                                "name": "RSS",
                                "enabled": True,
                                "priority": False,
                                "url": "https://example.com/rss.xml",
                                "topics": ["llm"],
                            },
                            {
                                "id": "podcast-source",
                                "type": "podcast",
                                "name": "Podcast",
                                "enabled": True,
                                "priority": False,
                                "url": "https://example.com/feed.xml",
                                "topics": ["llm"],
                            },
                            {
                                "id": "disabled-podcast",
                                "type": "podcast",
                                "name": "Disabled",
                                "enabled": False,
                                "priority": False,
                                "url": "https://example.com/disabled.xml",
                                "topics": ["llm"],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            sources = fetch_podcast.load_podcast_sources(defaults, None)

            self.assertEqual([s["id"] for s in sources], ["podcast-source"])


class TestOpenCliHelpers(unittest.TestCase):
    @patch.dict("os.environ", {"OPENCLI_BIN": "/custom/opencli"})
    def test_resolve_opencli_bin_from_env(self):
        self.assertEqual(fetch_podcast.resolve_opencli_bin(), "/custom/opencli")

    @patch.dict("os.environ", {}, clear=True)
    @patch("shutil.which", return_value="/usr/local/bin/opencli")
    def test_resolve_opencli_bin_from_path(self, _which):
        self.assertEqual(fetch_podcast.resolve_opencli_bin(), "/usr/local/bin/opencli")

    @patch.dict("os.environ", {}, clear=True)
    @patch("shutil.which", return_value=None)
    def test_resolve_opencli_bin_returns_none_when_missing(self, _which):
        self.assertIsNone(fetch_podcast.resolve_opencli_bin())

    @patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["opencli"],
            returncode=0,
            stdout='[{"eid":"episode-one"}]',
            stderr="",
        ),
    )
    def test_run_opencli_json_parses_stdout(self, run):
        payload = fetch_podcast.run_opencli_json(
            "/usr/local/bin/opencli",
            ["xiaoyuzhou", "podcast-episodes", "pid", "--limit", "20", "-f", "json"],
        )

        self.assertEqual(payload, [{"eid": "episode-one"}])
        self.assertEqual(run.call_args.args[0][0], "/usr/local/bin/opencli")
        self.assertIn("-f", run.call_args.args[0])
        self.assertIn("json", run.call_args.args[0])
        self.assertTrue(run.call_args.kwargs["capture_output"])
        self.assertTrue(run.call_args.kwargs["text"])
        self.assertEqual(run.call_args.kwargs["timeout"], 90)

    @patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["opencli"],
            returncode=78,
            stdout="",
            stderr="Missing Xiaoyuzhou credentials. Expected /Users/test/.opencli/xiaoyuzhou.json",
        ),
    )
    def test_run_opencli_json_raises_on_nonzero_exit(self, _run):
        with self.assertRaises(RuntimeError) as context:
            fetch_podcast.run_opencli_json(
                "/usr/local/bin/opencli",
                ["xiaoyuzhou", "podcast-episodes", "pid", "-f", "json"],
            )

        self.assertIn("Missing Xiaoyuzhou credentials", str(context.exception))

    @patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["opencli"],
            returncode=66,
            stdout="",
            stderr="No results found",
        ),
    )
    def test_run_opencli_json_returns_empty_list_on_empty_result_exit(self, _run):
        payload = fetch_podcast.run_opencli_json(
            "/usr/local/bin/opencli",
            ["xiaoyuzhou", "podcast-episodes", "pid", "-f", "json"],
        )

        self.assertEqual(payload, [])

    @patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["opencli"],
            returncode=0,
            stdout="{not-json",
            stderr="",
        ),
    )
    def test_run_opencli_json_raises_on_invalid_json(self, _run):
        with self.assertRaises(RuntimeError) as context:
            fetch_podcast.run_opencli_json(
                "/usr/local/bin/opencli",
                ["xiaoyuzhou", "podcast-episodes", "pid", "-f", "json"],
            )

        self.assertIn("valid JSON", str(context.exception))


class TestYoutubeMetadataNormalization(unittest.TestCase):
    def setUp(self):
        self.source = {
            "id": "training-data-podcast",
            "name": "Training Data",
            "url": "https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8",
            "topics": ["llm", "ai-agent"],
            "transcript": {"enabled": True, "backend": "auto"},
        }
        self.cutoff = utc("2026-05-01T00:00:00Z")

    def test_normalizes_youtube_entries_from_ytdlp(self):
        payload = {
            "entries": [
                {
                    "id": "abc123",
                    "title": "Waymo Autonomy",
                    "webpage_url": "https://www.youtube.com/watch?v=abc123",
                    "timestamp": 1777925100,
                    "duration": 3600,
                },
                {
                    "id": "old123",
                    "title": "Old Episode",
                    "webpage_url": "https://www.youtube.com/watch?v=old123",
                    "timestamp": 1700000000,
                },
            ]
        }

        episodes = fetch_podcast.normalize_youtube_metadata(payload, self.source, self.cutoff)

        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0]["title"], "Waymo Autonomy")
        self.assertEqual(episodes[0]["guid"], "youtube:abc123")
        self.assertEqual(episodes[0]["link"], "https://www.youtube.com/watch?v=abc123")
        self.assertEqual(episodes[0]["platform"], "youtube")
        self.assertEqual(episodes[0]["duration_seconds"], 3600)
        self.assertEqual(episodes[0]["transcript_status"], "missing")

    def test_reconstructs_link_for_flat_youtube_entry(self):
        payload = {
            "entries": [
                {
                    "id": "abc123",
                    "title": "Flat Entry",
                    "url": "abc123",
                    "timestamp": 1777925100,
                },
            ]
        }

        episodes = fetch_podcast.normalize_youtube_metadata(payload, self.source, self.cutoff)

        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0]["link"], "https://www.youtube.com/watch?v=abc123")

    def test_normalizes_youtube_entries_newest_first_before_limit(self):
        payload = {
            "entries": [
                {
                    "id": "older",
                    "title": "Older Episode",
                    "webpage_url": "https://www.youtube.com/watch?v=older",
                    "upload_date": "20260502",
                },
                {
                    "id": "newer",
                    "title": "Newer Episode",
                    "webpage_url": "https://www.youtube.com/watch?v=newer",
                    "upload_date": "20260504",
                },
            ]
        }

        episodes = fetch_podcast.normalize_youtube_metadata(payload, self.source, self.cutoff)

        self.assertEqual(
            [episode["guid"] for episode in episodes],
            ["youtube:newer", "youtube:older"],
        )

    def test_normalizes_youtube_entries_deduplicates_playlist_edges(self):
        payload = {
            "entries": [
                {
                    "id": "same",
                    "title": "Same Episode",
                    "webpage_url": "https://www.youtube.com/watch?v=same",
                    "upload_date": "20260504",
                },
                {
                    "id": "same",
                    "title": "Same Episode Duplicate",
                    "webpage_url": "https://www.youtube.com/watch?v=same",
                    "upload_date": "20260504",
                },
            ]
        }

        episodes = fetch_podcast.normalize_youtube_metadata(payload, self.source, self.cutoff)

        self.assertEqual([episode["guid"] for episode in episodes], ["youtube:same"])


    @patch("fetch_podcast.run_ytdlp_video_metadata")
    def test_hydrates_flat_youtube_entry_dates_before_normalization(self, run_video_metadata):
        run_video_metadata.return_value = {
            "id": "abc123",
            "title": "Hydrated Episode",
            "webpage_url": "https://www.youtube.com/watch?v=abc123",
            "upload_date": "20260504",
            "duration": 1800,
        }
        payload = {
            "entries": [
                {
                    "id": "abc123",
                    "title": "Flat Episode",
                    "url": "abc123",
                },
            ]
        }

        hydrated = fetch_podcast.hydrate_youtube_metadata(payload, "/usr/local/bin/yt-dlp")
        episodes = fetch_podcast.normalize_youtube_metadata(hydrated, self.source, self.cutoff)

        run_video_metadata.assert_called_once_with(
            "/usr/local/bin/yt-dlp",
            "https://www.youtube.com/watch?v=abc123",
        )
        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0]["title"], "Hydrated Episode")
        self.assertEqual(episodes[0]["date"], "2026-05-04T00:00:00+00:00")
        self.assertEqual(episodes[0]["duration_seconds"], 1800)

    @patch("fetch_podcast.run_ytdlp_video_metadata")
    def test_hydrates_date_only_youtube_entry_before_hour_cutoff(self, run_video_metadata):
        run_video_metadata.return_value = {
            "id": "abc123",
            "title": "Hydrated Date Only Episode",
            "webpage_url": "https://www.youtube.com/watch?v=abc123",
            "timestamp": 1777925100,
        }
        payload = {
            "entries": [
                {
                    "id": "abc123",
                    "title": "Date Only Episode",
                    "webpage_url": "https://www.youtube.com/watch?v=abc123",
                    "upload_date": "20260504",
                },
            ]
        }

        hydrated = fetch_podcast.hydrate_youtube_metadata(payload, "/usr/local/bin/yt-dlp")
        episodes = fetch_podcast.normalize_youtube_metadata(
            hydrated,
            self.source,
            utc("2026-05-04T12:00:00Z"),
        )

        run_video_metadata.assert_called_once_with(
            "/usr/local/bin/yt-dlp",
            "https://www.youtube.com/watch?v=abc123",
        )
        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0]["date"], "2026-05-04T20:05:00+00:00")

    @patch("fetch_podcast.run_ytdlp_video_metadata")
    def test_skips_hydration_for_precise_youtube_timestamp(self, run_video_metadata):
        payload = {
            "entries": [
                {
                    "id": "abc123",
                    "title": "Timestamped Episode",
                    "webpage_url": "https://www.youtube.com/watch?v=abc123",
                    "timestamp": 1777925100,
                },
            ]
        }

        hydrated = fetch_podcast.hydrate_youtube_metadata(payload, "/usr/local/bin/yt-dlp")

        run_video_metadata.assert_not_called()
        self.assertEqual(hydrated["entries"][0]["title"], "Timestamped Episode")

    @patch("fetch_podcast.run_ytdlp_video_metadata")
    def test_hydrates_tail_playlist_window_before_normalization(self, run_video_metadata):
        run_video_metadata.return_value = {
            "id": "tail",
            "title": "Tail Window Episode",
            "webpage_url": "https://www.youtube.com/watch?v=tail",
            "upload_date": "20260531",
        }
        entries = [
            {
                "id": f"head-{index}",
                "title": f"Head Episode {index}",
                "webpage_url": f"https://www.youtube.com/watch?v=head-{index}",
                "timestamp": 1777665900,
            }
            for index in range(fetch_podcast.MAX_EPISODES_PER_SOURCE)
        ]
        entries.append(
            {
                "id": "tail",
                "title": "Flat Tail Episode",
                "url": "tail",
            }
        )

        hydrated = fetch_podcast.hydrate_youtube_metadata(
            {"entries": entries},
            "/usr/local/bin/yt-dlp",
        )
        episodes = fetch_podcast.normalize_youtube_metadata(hydrated, self.source, self.cutoff)

        run_video_metadata.assert_called_once_with(
            "/usr/local/bin/yt-dlp",
            "https://www.youtube.com/watch?v=tail",
        )
        self.assertEqual(episodes[0]["guid"], "youtube:tail")


class TestXiaoyuzhouMetadataNormalization(unittest.TestCase):
    def setUp(self):
        self.source = {
            "id": "whynottv-podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "platform": "xiaoyuzhou",
            "topics": ["podcast"],
            "transcript": {"enabled": False},
        }
        self.cutoff = utc("2026-01-01T00:00:00Z")

    def test_normalizes_xiaoyuzhou_episode_rows(self):
        rows = [
            {
                "eid": "69f441cd5390b7cc928acdcc",
                "title": "Danfei Xu",
                "duration": "137:23",
                "plays": 11915,
                "date": "2026-05-01",
            },
        ]

        episodes = fetch_podcast.normalize_xiaoyuzhou_metadata(rows, self.source, self.cutoff)

        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0]["title"], "Danfei Xu")
        self.assertEqual(
            episodes[0]["link"],
            "https://www.xiaoyuzhoufm.com/episode/69f441cd5390b7cc928acdcc",
        )
        self.assertEqual(episodes[0]["guid"], "xiaoyuzhou:69f441cd5390b7cc928acdcc")
        self.assertEqual(episodes[0]["date"], "2026-05-01T00:00:00+00:00")
        self.assertEqual(episodes[0]["platform"], "xiaoyuzhou")
        self.assertEqual(episodes[0]["show_name"], "WhynotTV Podcast")
        self.assertEqual(episodes[0]["transcript_status"], "disabled")

    def test_filters_xiaoyuzhou_rows_older_than_cutoff(self):
        rows = [
            {"eid": "old", "title": "Old Episode", "date": "2025-12-31"},
            {"eid": "new", "title": "New Episode", "date": "2026-01-01"},
        ]

        episodes = fetch_podcast.normalize_xiaoyuzhou_metadata(rows, self.source, self.cutoff)

        self.assertEqual([episode["guid"] for episode in episodes], ["xiaoyuzhou:new"])

    def test_includes_xiaoyuzhou_rows_on_cutoff_calendar_date(self):
        rows = [
            {"eid": "same-day", "title": "Same Day Episode", "date": "2026-05-01"},
        ]

        episodes = fetch_podcast.normalize_xiaoyuzhou_metadata(
            rows,
            self.source,
            utc("2026-05-01T12:00:00Z"),
        )

        self.assertEqual([episode["guid"] for episode in episodes], ["xiaoyuzhou:same-day"])
        self.assertEqual(episodes[0]["date"], "2026-05-01T00:00:00+00:00")

    def test_filters_xiaoyuzhou_full_timestamps_before_hour_cutoff(self):
        rows = [
            {
                "eid": "too-old",
                "title": "Too Old Episode",
                "date": "2026-05-01T10:59:59Z",
            },
            {
                "eid": "new-enough",
                "title": "New Enough Episode",
                "date": "2026-05-01T11:00:00Z",
            },
        ]

        episodes = fetch_podcast.normalize_xiaoyuzhou_metadata(
            rows,
            self.source,
            utc("2026-05-01T11:00:00Z"),
        )

        self.assertEqual([episode["guid"] for episode in episodes], ["xiaoyuzhou:new-enough"])

    def test_normalizes_xiaoyuzhou_rows_newest_first(self):
        rows = [
            {"eid": "older", "title": "Older", "date": "2026-05-01"},
            {"eid": "newer", "title": "Newer", "date": "2026-05-03"},
        ]

        episodes = fetch_podcast.normalize_xiaoyuzhou_metadata(rows, self.source, self.cutoff)

        self.assertEqual(
            [episode["guid"] for episode in episodes],
            ["xiaoyuzhou:newer", "xiaoyuzhou:older"],
        )

    def test_normalize_xiaoyuzhou_metadata_rejects_non_list_payload(self):
        with self.assertRaises(RuntimeError):
            fetch_podcast.normalize_xiaoyuzhou_metadata({"eid": "one"}, self.source, self.cutoff)

    def test_skips_duplicate_and_malformed_xiaoyuzhou_rows(self):
        rows = [
            {"eid": "same", "title": "First Episode", "date": "2026-05-01"},
            {"eid": "same", "title": "Duplicate Episode", "date": "2026-05-02"},
            {"eid": "", "title": "Missing ID", "date": "2026-05-03"},
            {"eid": "missing-title", "date": "2026-05-04"},
            ["not", "a", "row"],
        ]

        episodes = fetch_podcast.normalize_xiaoyuzhou_metadata(rows, self.source, self.cutoff)

        self.assertEqual([episode["title"] for episode in episodes], ["First Episode"])


class TestTranscriptBackend(unittest.TestCase):
    def setUp(self):
        self.source = {
            "id": "training-data-podcast",
            "name": "Training Data",
            "url": "https://www.youtube.com/playlist?list=listid",
            "topics": ["llm"],
            "transcript": {
                "enabled": True,
                "backend": "auto",
                "languages": ["en", "zh"],
            },
        }
        self.episode = {
            "title": "Episode",
            "link": "https://www.youtube.com/watch?v=abc123",
            "date": "2026-05-04T20:05:00+00:00",
            "guid": "youtube:abc123",
            "topics": ["llm"],
            "show_name": "Training Data",
            "platform": "youtube",
            "transcript_status": "missing",
        }

    def xiaoyuzhou_source(self):
        return {
            "id": "whynottv-podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "topics": ["podcast"],
            "transcript": {
                "enabled": True,
                "backend": "opencli",
            },
        }

    def xiaoyuzhou_episode(self):
        return {
            "title": "Danfei Xu",
            "link": "https://www.xiaoyuzhoufm.com/episode/69f441cd5390b7cc928acdcc",
            "date": "2026-05-01T00:00:00+00:00",
            "guid": "xiaoyuzhou:69f441cd5390b7cc928acdcc",
            "topics": ["podcast"],
            "show_name": "WhynotTV Podcast",
            "platform": "xiaoyuzhou",
            "transcript_status": "missing",
        }

    @patch("fetch_podcast.resolve_ytdlp_bin", return_value=None)
    def test_transcript_backend_unavailable_keeps_episode(self, _resolve):
        result = fetch_podcast.enrich_episode_transcript(self.episode.copy(), self.source, {}, no_cache=True)

        self.assertEqual(result["transcript_status"], "backend_unavailable")
        self.assertIn("transcript_error", result)
        self.assertNotIn("transcript", result)

    @patch("fetch_podcast.run_ytdlp_transcript")
    @patch("fetch_podcast.resolve_ytdlp_bin", return_value="/usr/local/bin/yt-dlp")
    def test_transcript_success_attaches_text(self, _resolve, run_transcript):
        run_transcript.return_value = {
            "status": "ok",
            "transcript": "Speaker 1 | 00:00 - 00:05 Hello world.",
        }

        result = fetch_podcast.enrich_episode_transcript(self.episode.copy(), self.source, {}, no_cache=True)

        self.assertEqual(result["transcript_status"], "ok")
        self.assertEqual(result["transcript"], "Speaker 1 | 00:00 - 00:05 Hello world.")

    @patch("fetch_podcast.run_opencli_json")
    @patch("fetch_podcast.resolve_opencli_bin", return_value="/usr/local/bin/opencli")
    def test_opencli_transcript_success_attaches_text(self, _resolve, run_opencli):
        def write_absolute_transcript(_opencli_bin, args, **_kwargs):
            output_dir = Path(args[args.index("--output") + 1])
            text_file = output_dir / "transcript.txt"
            text_file.write_text("Segment one.\nSegment two.\n", encoding="utf-8")
            return [
                {
                    "status": "success",
                    "segments": "2",
                    "text_file": str(text_file),
                }
            ]

        run_opencli.side_effect = write_absolute_transcript

        result = fetch_podcast.enrich_episode_transcript(
            self.xiaoyuzhou_episode(),
            self.xiaoyuzhou_source(),
            {},
            no_cache=True,
        )

        self.assertEqual(result["transcript_status"], "ok")
        self.assertEqual(result["transcript"], "Segment one.\nSegment two.")
        run_opencli.assert_called_once()
        self.assertIn("transcript", run_opencli.call_args.args[1])

    @patch("fetch_podcast.run_ytdlp_transcript")
    @patch("fetch_podcast.resolve_ytdlp_bin", return_value="/usr/local/bin/yt-dlp")
    @patch("fetch_podcast.resolve_opencli_bin")
    def test_xiaoyuzhou_explicit_ytdlp_backend_uses_ytdlp(
        self,
        resolve_opencli,
        _resolve_ytdlp,
        run_transcript,
    ):
        source = self.xiaoyuzhou_source()
        source["transcript"]["backend"] = "yt-dlp"
        run_transcript.return_value = {
            "status": "ok",
            "transcript": "Subtitle transcript.",
        }

        result = fetch_podcast.enrich_episode_transcript(
            self.xiaoyuzhou_episode(),
            source,
            {},
            no_cache=True,
        )

        self.assertEqual(result["transcript_status"], "ok")
        self.assertEqual(result["transcript"], "Subtitle transcript.")
        resolve_opencli.assert_not_called()
        run_transcript.assert_called_once()

    @patch("fetch_podcast.run_opencli_json")
    def test_opencli_transcript_reads_relative_text_file_from_output_dir(self, run_opencli):
        def write_relative_transcript(_opencli_bin, args, **_kwargs):
            output_dir = Path(args[args.index("--output") + 1])
            (output_dir / "transcript.txt").write_text(
                "Segment one.\nSegment two.\n",
                encoding="utf-8",
            )
            return [
                {
                    "status": "success",
                    "segments": "2",
                    "text_file": "transcript.txt",
                }
            ]

        run_opencli.side_effect = write_relative_transcript

        result = fetch_podcast.run_opencli_transcript(
            "/usr/local/bin/opencli",
            self.xiaoyuzhou_episode(),
        )

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["transcript"], "Segment one.\nSegment two.")

    @patch("fetch_podcast.run_opencli_json")
    def test_opencli_transcript_rejects_text_file_outside_output_dir(self, run_opencli):
        with tempfile.TemporaryDirectory() as outside_dir:
            outside_file = Path(outside_dir) / "transcript.txt"
            outside_file.write_text("Outside transcript.\n", encoding="utf-8")
            run_opencli.return_value = [
                {
                    "status": "success",
                    "segments": "1",
                    "text_file": str(outside_file),
                }
            ]

            result = fetch_podcast.run_opencli_transcript(
                "/usr/local/bin/opencli",
                self.xiaoyuzhou_episode(),
            )

        self.assertEqual(result["status"], "error")
        self.assertIn("outside", result["error"])
        self.assertNotIn("transcript", result)

    @patch("fetch_podcast.os.path.commonpath", side_effect=ValueError("paths on different drives"))
    @patch("fetch_podcast.run_opencli_json")
    def test_opencli_transcript_handles_path_commonpath_value_error(
        self,
        run_opencli,
        _commonpath,
    ):
        run_opencli.return_value = [
            {
                "status": "success",
                "segments": "1",
                "text_file": "D:/transcript.txt",
            }
        ]

        result = fetch_podcast.run_opencli_transcript(
            "/usr/local/bin/opencli",
            self.xiaoyuzhou_episode(),
        )

        self.assertEqual(result["status"], "error")
        self.assertIn("outside", result["error"])
        self.assertNotIn("transcript", result)

    @patch("fetch_podcast.resolve_opencli_bin", return_value=None)
    def test_opencli_transcript_backend_unavailable_keeps_episode(self, _resolve):
        result = fetch_podcast.enrich_episode_transcript(
            self.xiaoyuzhou_episode(),
            self.xiaoyuzhou_source(),
            {},
            no_cache=True,
        )

        self.assertEqual(result["transcript_status"], "backend_unavailable")
        self.assertIn("transcript_error", result)
        self.assertNotIn("transcript", result)

    @patch("fetch_podcast.resolve_opencli_bin")
    def test_opencli_transcript_backend_rejects_non_xiaoyuzhou_episode(self, resolve_opencli):
        source = {
            **self.source,
            "transcript": {
                **self.source["transcript"],
                "backend": "opencli",
            },
        }

        result = fetch_podcast.enrich_episode_transcript(
            self.episode.copy(),
            source,
            {},
            no_cache=True,
        )

        self.assertEqual(result["transcript_status"], "error")
        self.assertIn("only supported for Xiaoyuzhou", result["transcript_error"])
        self.assertNotIn("transcript", result)
        resolve_opencli.assert_not_called()

    @patch("fetch_podcast.run_opencli_json", side_effect=RuntimeError("Transcript URL not found"))
    @patch("fetch_podcast.resolve_opencli_bin", return_value="/usr/local/bin/opencli")
    def test_opencli_transcript_failure_keeps_episode(self, _resolve, _run_opencli):
        result = fetch_podcast.enrich_episode_transcript(
            self.xiaoyuzhou_episode(),
            self.xiaoyuzhou_source(),
            {},
            no_cache=True,
        )

        self.assertEqual(result["transcript_status"], "error")
        self.assertIn("Transcript URL not found", result["transcript_error"])
        self.assertNotIn("transcript", result)

    @patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["opencli"],
            returncode=66,
            stdout="",
            stderr="No transcript rows",
        ),
    )
    def test_opencli_transcript_empty_result_returns_missing(self, _run):
        result = fetch_podcast.run_opencli_transcript(
            "/usr/local/bin/opencli",
            self.xiaoyuzhou_episode(),
        )

        self.assertEqual(result["status"], "missing")
        self.assertIn("No transcript", result["error"])
        self.assertNotIn("transcript", result)

    @patch("subprocess.run")
    def test_ytdlp_transcript_uses_language_priority(self, run):
        def write_subtitle(cmd, **_kwargs):
            language = cmd[cmd.index("--sub-langs") + 1]
            output = Path(cmd[cmd.index("--output") + 1])
            output.parent.mkdir(parents=True, exist_ok=True)
            (output.parent / f"abc.{language}.vtt").write_text(
                f"WEBVTT\n\n00:00:00.000 --> 00:00:01.000\n{language} transcript.\n",
                encoding="utf-8",
            )
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")

        run.side_effect = write_subtitle

        result = fetch_podcast.run_ytdlp_transcript(
            "/usr/local/bin/yt-dlp",
            self.episode,
            ["zh", "en"],
        )

        self.assertEqual(result["status"], "ok")
        self.assertIn("zh transcript.", result["transcript"])
        self.assertEqual(run.call_count, 1)
        self.assertIn("--no-playlist", run.call_args.args[0])

    @patch("subprocess.run")
    def test_ytdlp_transcript_falls_back_to_next_language(self, run):
        def maybe_write_subtitle(cmd, **_kwargs):
            language = cmd[cmd.index("--sub-langs") + 1]
            output = Path(cmd[cmd.index("--output") + 1])
            output.parent.mkdir(parents=True, exist_ok=True)
            if language == "en":
                (output.parent / "abc.en.vtt").write_text(
                    "WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nEnglish transcript.\n",
                    encoding="utf-8",
                )
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")

        run.side_effect = maybe_write_subtitle

        result = fetch_podcast.run_ytdlp_transcript(
            "/usr/local/bin/yt-dlp",
            self.episode,
            ["zh", "en"],
        )

        called_languages = [
            call.args[0][call.args[0].index("--sub-langs") + 1]
            for call in run.call_args_list
        ]
        self.assertEqual(called_languages, ["zh", "en"])
        self.assertEqual(result["status"], "ok")
        self.assertIn("English transcript.", result["transcript"])

    def test_cache_key_uses_guid(self):
        key = fetch_podcast.transcript_cache_key(self.episode, self.source)

        self.assertEqual(key, "training-data-podcast:youtube:abc123")

    def test_cache_key_namespaces_same_guid_by_source(self):
        other_source = {
            "id": "other-podcast",
            "name": "Other Podcast",
            "url": "https://example.com/feed.xml",
        }

        key = fetch_podcast.transcript_cache_key(self.episode, self.source)
        other_key = fetch_podcast.transcript_cache_key(self.episode, other_source)

        self.assertNotEqual(key, other_key)
        self.assertEqual(other_key, "other-podcast:youtube:abc123")

    @patch("fetch_podcast.resolve_ytdlp_bin", return_value=None)
    def test_transcript_cache_does_not_cross_sources_with_same_guid(self, _resolve):
        other_source = {
            **self.source,
            "id": "other-podcast",
            "name": "Other Podcast",
        }
        cache = {
            "transcripts": {
                fetch_podcast.transcript_cache_key(self.episode, self.source): {
                    "status": "ok",
                    "transcript": "Wrong source transcript.",
                    "error": "",
                    "ts": time.time(),
                }
            }
        }

        result = fetch_podcast.enrich_episode_transcript(
            self.episode.copy(),
            other_source,
            cache,
        )

        self.assertEqual(result["transcript_status"], "backend_unavailable")
        self.assertNotIn("transcript", result)

    @patch("subprocess.run", side_effect=OSError("missing binary"))
    def test_ytdlp_os_error_returns_error_status(self, _run):
        result = fetch_podcast.run_ytdlp_transcript(
            "/missing/yt-dlp",
            self.episode,
            ["en"],
        )

        self.assertEqual(result["status"], "error")
        self.assertIn("missing binary", result["error"])

    def test_parse_vtt_skips_note_blocks_and_deduplicates_adjacent_text(self):
        content = """WEBVTT

NOTE
This note should not leak.
Another note line.

00:00:00.000 --> 00:00:05.000
<c>Hello world.</c>

00:00:05.000 --> 00:00:10.000
Hello world.

00:00:10.000 --> 00:00:15.000
Next line.
"""

        transcript = fetch_podcast.parse_vtt_transcript(content)

        self.assertNotIn("note should not leak", transcript)
        self.assertEqual(transcript.count("Hello world."), 1)
        self.assertIn("Next line.", transcript)

    def test_transcript_languages_falls_back_for_blank_config(self):
        source = {
            "transcript": {
                "enabled": True,
                "backend": "auto",
                "languages": ["", "  "],
            },
        }

        self.assertEqual(fetch_podcast.transcript_languages(source), ["en", "zh", "zh-Hans"])


class TestPodcastCliOutput(unittest.TestCase):
    @patch("fetch_podcast.fetch_source")
    def test_run_fetch_writes_expected_output_shape(self, fetch_source):
        source = {
            "id": "test-podcast",
            "type": "podcast",
            "name": "Test Podcast",
            "enabled": True,
            "priority": True,
            "url": "https://example.com/feed.xml",
            "topics": ["llm"],
        }
        fetch_source.return_value = {
            "source_id": "test-podcast",
            "source_type": "podcast",
            "name": "Test Podcast",
            "url": "https://example.com/feed.xml",
            "priority": True,
            "topics": ["llm"],
            "status": "ok",
            "attempts": 1,
            "count": 1,
            "articles": [
                {
                    "title": "Episode",
                    "link": "https://example.com/episode",
                    "date": "2026-05-04T20:05:00+00:00",
                    "guid": "episode",
                    "topics": ["llm"],
                    "show_name": "Test Podcast",
                    "platform": "rss",
                    "transcript_status": "disabled",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "podcast.json"
            cache = {"transcripts": {}}
            result = fetch_podcast.run_fetch([source], 48, output, cache, no_cache=True)

            data = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        self.assertEqual(data["source_type"], "podcast")
        self.assertEqual(data["total_articles"], 1)
        self.assertEqual(data["sources"][0]["source_id"], "test-podcast")

    def test_save_podcast_cache_round_trips_via_atomic_path(self):
        cache = {
            "metadata": {},
            "transcripts": {
                "episode": {
                    "status": "ok",
                    "transcript": "Text",
                    "error": "",
                    "ts": 1777925100,
                }
            }
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / "podcast-cache.json"
            with patch.object(fetch_podcast, "PODCAST_CACHE_PATH", str(cache_path)):
                fetch_podcast.save_podcast_cache(cache)

                loaded = fetch_podcast.load_podcast_cache()

        self.assertEqual(loaded, cache)

    @patch("fetch_podcast.hydrate_youtube_metadata")
    @patch("fetch_podcast.run_ytdlp_metadata")
    @patch("fetch_podcast.resolve_ytdlp_bin", return_value="/usr/local/bin/yt-dlp")
    def test_fetch_youtube_source_reuses_metadata_cache(
        self,
        _resolve,
        run_metadata,
        hydrate_metadata,
    ):
        source = {
            "id": "training-data-podcast",
            "type": "podcast",
            "name": "Training Data",
            "url": "https://www.youtube.com/playlist?list=abc",
            "platform": "youtube",
            "topics": ["llm"],
            "transcript": {"enabled": False},
        }
        payload = {
            "entries": [
                {
                    "id": "abc123",
                    "title": "Cached Episode",
                    "webpage_url": "https://www.youtube.com/watch?v=abc123",
                    "upload_date": "20260504",
                }
            ]
        }
        cache = {
            "metadata": {
                fetch_podcast.metadata_cache_key(source): {
                    "payload": payload,
                    "ts": time.time(),
                }
            },
            "transcripts": {},
        }

        episodes = fetch_podcast.fetch_youtube_source(
            source,
            utc("2026-05-01T00:00:00Z"),
            cache,
            no_cache=False,
        )

        run_metadata.assert_not_called()
        hydrate_metadata.assert_not_called()
        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0]["title"], "Cached Episode")

    @patch("fetch_podcast.enrich_episode_transcript", side_effect=lambda episode, *_args, **_kwargs: episode)
    @patch("fetch_podcast.hydrate_youtube_metadata")
    @patch("fetch_podcast.run_ytdlp_metadata")
    @patch("fetch_podcast.resolve_ytdlp_bin", return_value="/usr/local/bin/yt-dlp")
    def test_fetch_youtube_source_refetches_wrong_shape_metadata_cache(
        self,
        _resolve,
        run_metadata,
        hydrate_metadata,
        _enrich_transcript,
    ):
        source = {
            "id": "training-data-podcast",
            "type": "podcast",
            "name": "Training Data",
            "url": "https://www.youtube.com/playlist?list=abc",
            "platform": "youtube",
            "topics": ["llm"],
            "transcript": {"enabled": False},
        }
        cache_key = fetch_podcast.metadata_cache_key(source)
        cache = {
            "metadata": {
                cache_key: {
                    "payload": [{"id": "wrong-shape"}],
                    "ts": time.time(),
                }
            },
            "transcripts": {},
        }
        raw_payload = {"entries": [{"id": "fresh"}]}
        fresh_payload = {
            "entries": [
                {
                    "id": "fresh",
                    "title": "Fresh Episode",
                    "webpage_url": "https://www.youtube.com/watch?v=fresh",
                    "upload_date": "20260504",
                }
            ]
        }
        run_metadata.return_value = raw_payload
        hydrate_metadata.return_value = fresh_payload

        first = fetch_podcast.fetch_youtube_source(
            source,
            utc("2026-01-01T00:00:00Z"),
            cache,
            no_cache=False,
        )
        second = fetch_podcast.fetch_youtube_source(
            source,
            utc("2026-01-01T00:00:00Z"),
            cache,
            no_cache=False,
        )

        self.assertEqual([episode["guid"] for episode in first], ["youtube:fresh"])
        self.assertEqual([episode["guid"] for episode in second], ["youtube:fresh"])
        self.assertEqual(cache["metadata"][cache_key]["payload"], fresh_payload)
        run_metadata.assert_called_once_with("/usr/local/bin/yt-dlp", source)
        hydrate_metadata.assert_called_once_with(raw_payload, "/usr/local/bin/yt-dlp")

    @patch("fetch_podcast.run_opencli_json")
    @patch("fetch_podcast.resolve_opencli_bin", return_value="/usr/local/bin/opencli")
    def test_fetch_xiaoyuzhou_source_uses_opencli(self, _resolve, run_opencli):
        source = {
            "id": "whynottv-podcast",
            "type": "podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "platform": "xiaoyuzhou",
            "topics": ["podcast"],
            "transcript": {"enabled": False},
        }
        run_opencli.return_value = [
            {
                "eid": "69f441cd5390b7cc928acdcc",
                "title": "Danfei Xu",
                "date": "2026-05-01",
            }
        ]

        episodes = fetch_podcast.fetch_xiaoyuzhou_source(
            source,
            utc("2026-01-01T00:00:00Z"),
            {"metadata": {}, "transcripts": {}},
            no_cache=True,
        )

        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0]["guid"], "xiaoyuzhou:69f441cd5390b7cc928acdcc")
        run_opencli.assert_called_once_with(
            "/usr/local/bin/opencli",
            [
                "xiaoyuzhou",
                "podcast-episodes",
                "686a1832222ae2de21fea940",
                "--limit",
                str(fetch_podcast.MAX_EPISODES_PER_SOURCE),
                "-f",
                "json",
            ],
        )

    @patch("fetch_podcast.enrich_episode_transcript")
    @patch("fetch_podcast.run_opencli_json")
    @patch("fetch_podcast.resolve_opencli_bin", return_value="/usr/local/bin/opencli")
    def test_fetch_xiaoyuzhou_source_accepts_empty_opencli_result(
        self,
        _resolve,
        run_opencli,
        enrich_transcript,
    ):
        source = {
            "id": "whynottv-podcast",
            "type": "podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "platform": "xiaoyuzhou",
            "topics": ["podcast"],
            "transcript": {"enabled": False},
        }
        run_opencli.return_value = []
        cache = {"metadata": {}, "transcripts": {}}

        episodes = fetch_podcast.fetch_xiaoyuzhou_source(
            source,
            utc("2026-01-01T00:00:00Z"),
            cache,
            no_cache=False,
        )

        self.assertEqual(episodes, [])
        self.assertEqual(cache["metadata"][fetch_podcast.metadata_cache_key(source)]["payload"], [])
        enrich_transcript.assert_not_called()

    @patch("fetch_podcast.enrich_episode_transcript")
    @patch("fetch_podcast.run_opencli_json")
    @patch("fetch_podcast.resolve_opencli_bin", return_value="/usr/local/bin/opencli")
    def test_fetch_xiaoyuzhou_source_reuses_metadata_cache(
        self,
        _resolve,
        run_opencli,
        enrich_transcript,
    ):
        source = {
            "id": "whynottv-podcast",
            "type": "podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940?utm_source=share",
            "topics": ["podcast"],
            "transcript": {"enabled": True, "backend": "opencli"},
        }
        run_opencli.return_value = [
            {
                "eid": "69f441cd5390b7cc928acdcc",
                "title": "Danfei Xu",
                "date": "2026-05-01",
            }
        ]
        enrich_transcript.side_effect = lambda episode, *_args, **_kwargs: {
            **episode,
            "transcript_status": "ok",
            "transcript": "Cached transcript.",
        }
        cache = {"metadata": {}, "transcripts": {}}

        first = fetch_podcast.fetch_xiaoyuzhou_source(
            source,
            utc("2026-01-01T00:00:00Z"),
            cache,
            no_cache=False,
        )
        second = fetch_podcast.fetch_xiaoyuzhou_source(
            source,
            utc("2026-01-01T00:00:00Z"),
            cache,
            no_cache=False,
        )

        cache_key = (
            "xiaoyuzhou:686a1832222ae2de21fea940:"
            f"{fetch_podcast.MAX_EPISODES_PER_SOURCE}:v{fetch_podcast.METADATA_CACHE_VERSION}"
        )
        self.assertEqual(fetch_podcast.metadata_cache_key(source), cache_key)
        self.assertEqual(
            fetch_podcast.metadata_cache_key({**source, "platform": "xiaoyuzhou"}),
            cache_key,
        )
        self.assertEqual(
            fetch_podcast.metadata_cache_key(
                {**source, "platform": "rss", "url": "https://example.com/feed.xml"},
                source["url"],
            ),
            f"rss:{source['url']}:{fetch_podcast.MAX_EPISODES_PER_SOURCE}:v{fetch_podcast.METADATA_CACHE_VERSION}",
        )
        self.assertIn(cache_key, cache["metadata"])
        self.assertEqual(cache["metadata"][cache_key]["payload"][0]["title"], "Danfei Xu")
        run_opencli.assert_called_once()
        self.assertEqual(enrich_transcript.call_count, 2)
        self.assertEqual(first[0]["transcript"], "Cached transcript.")
        self.assertEqual(second[0]["transcript"], "Cached transcript.")

    @patch("fetch_podcast.enrich_episode_transcript", side_effect=lambda episode, *_args, **_kwargs: episode)
    @patch("fetch_podcast.run_opencli_json")
    @patch("fetch_podcast.resolve_opencli_bin", return_value="/usr/local/bin/opencli")
    def test_fetch_xiaoyuzhou_source_caches_raw_payload_before_cutoff_filtering(
        self,
        _resolve,
        run_opencli,
        _enrich_transcript,
    ):
        source = {
            "id": "whynottv-podcast",
            "type": "podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "platform": "xiaoyuzhou",
            "topics": ["podcast"],
            "transcript": {"enabled": False},
        }
        raw_payload = [
            {"eid": "older", "title": "Older Episode", "date": "2026-04-01"},
            {"eid": "newer", "title": "Newer Episode", "date": "2026-05-01"},
        ]
        run_opencli.return_value = raw_payload
        cache = {"metadata": {}, "transcripts": {}}

        first = fetch_podcast.fetch_xiaoyuzhou_source(
            source,
            utc("2026-04-15T00:00:00Z"),
            cache,
            no_cache=False,
        )
        second = fetch_podcast.fetch_xiaoyuzhou_source(
            source,
            utc("2026-03-01T00:00:00Z"),
            cache,
            no_cache=False,
        )

        cache_key = fetch_podcast.metadata_cache_key(source)
        self.assertEqual([episode["guid"] for episode in first], ["xiaoyuzhou:newer"])
        self.assertEqual(
            [episode["guid"] for episode in second],
            ["xiaoyuzhou:newer", "xiaoyuzhou:older"],
        )
        self.assertEqual(cache["metadata"][cache_key]["payload"], raw_payload)
        run_opencli.assert_called_once()

    def test_metadata_cache_key_uses_source_url_for_explicit_xiaoyuzhou_fallback(self):
        source = {
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "platform": "xiaoyuzhou",
        }

        key = fetch_podcast.metadata_cache_key(source, "https://example.com/feed.xml")

        self.assertEqual(
            key,
            "xiaoyuzhou:686a1832222ae2de21fea940:"
            f"{fetch_podcast.MAX_EPISODES_PER_SOURCE}:v{fetch_podcast.METADATA_CACHE_VERSION}",
        )

    @patch("fetch_podcast.enrich_episode_transcript", side_effect=lambda episode, *_args, **_kwargs: episode)
    @patch("fetch_podcast.run_opencli_json")
    @patch("fetch_podcast.resolve_opencli_bin", return_value="/usr/local/bin/opencli")
    def test_fetch_xiaoyuzhou_source_refetches_wrong_shape_metadata_cache(
        self,
        _resolve,
        run_opencli,
        _enrich_transcript,
    ):
        source = {
            "id": "whynottv-podcast",
            "type": "podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "platform": "xiaoyuzhou",
            "topics": ["podcast"],
            "transcript": {"enabled": False},
        }
        cache_key = fetch_podcast.metadata_cache_key(source)
        cache = {
            "metadata": {
                cache_key: {
                    "payload": {"eid": "wrong-shape"},
                    "ts": time.time(),
                }
            },
            "transcripts": {},
        }
        run_opencli.return_value = [
            {"eid": "fresh", "title": "Fresh Episode", "date": "2026-05-01"},
        ]

        episodes = fetch_podcast.fetch_xiaoyuzhou_source(
            source,
            utc("2026-01-01T00:00:00Z"),
            cache,
            no_cache=False,
        )

        self.assertEqual([episode["guid"] for episode in episodes], ["xiaoyuzhou:fresh"])
        self.assertIsInstance(cache["metadata"][cache_key]["payload"], list)
        run_opencli.assert_called_once()

    @patch("fetch_podcast.resolve_opencli_bin", return_value=None)
    def test_fetch_xiaoyuzhou_source_requires_opencli(self, _resolve):
        source = {
            "id": "whynottv-podcast",
            "type": "podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "platform": "xiaoyuzhou",
            "topics": ["podcast"],
        }

        with self.assertRaises(RuntimeError) as context:
            fetch_podcast.fetch_xiaoyuzhou_source(
                source,
                utc("2026-01-01T00:00:00Z"),
                {"metadata": {}, "transcripts": {}},
                no_cache=True,
            )

        self.assertEqual(str(context.exception), "opencli is not available")

    def test_fetch_source_routes_xiaoyuzhou_platform(self):
        source = {
            "id": "whynottv-podcast",
            "type": "podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "platform": "xiaoyuzhou",
            "topics": ["podcast"],
        }
        cutoff = utc("2026-01-01T00:00:00Z")

        with patch.object(
            fetch_podcast,
            "fetch_xiaoyuzhou_source",
            return_value=[],
        ) as fetch_xiaoyuzhou:
            result = fetch_podcast.fetch_source(source, cutoff, {"transcripts": {}}, no_cache=True)

        fetch_xiaoyuzhou.assert_called_once()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["platform"], "xiaoyuzhou")

    @patch("fetch_podcast.resolve_opencli_bin", return_value=None)
    def test_fetch_source_returns_error_result_when_xiaoyuzhou_opencli_missing(self, _resolve):
        source = {
            "id": "whynottv-podcast",
            "type": "podcast",
            "name": "WhynotTV Podcast",
            "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
            "platform": "xiaoyuzhou",
            "topics": ["podcast"],
        }

        result = fetch_podcast.fetch_source(
            source,
            utc("2026-01-01T00:00:00Z"),
            {"transcripts": {}},
            no_cache=True,
        )

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["articles"], [])
        self.assertEqual(result["platform"], "xiaoyuzhou")
        self.assertIn("opencli is not available", result["error"])

    def test_save_podcast_cache_suppresses_replace_failure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / "podcast-cache.json"
            with patch.object(fetch_podcast, "PODCAST_CACHE_PATH", str(cache_path)):
                with patch("fetch_podcast.os.replace", side_effect=OSError("replace failed")) as replace:
                    fetch_podcast.save_podcast_cache({"transcripts": {}})

            leftovers = list(Path(tmpdir).glob("follow-news-podcast-cache-*"))

        replace.assert_called_once()
        self.assertEqual(leftovers, [])

    @patch("fetch_podcast.fetch_rss_source", side_effect=RuntimeError("network failed"))
    def test_fetch_source_returns_error_result_on_fetch_failure(self, _fetch_rss):
        source = {
            "id": "test-podcast",
            "type": "podcast",
            "name": "Test Podcast",
            "url": "https://example.com/feed.xml",
            "topics": ["llm"],
        }
        cutoff = utc("2026-05-01T00:00:00Z")

        result = fetch_podcast.fetch_source(source, cutoff, {"transcripts": {}}, no_cache=True)

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["articles"], [])
        self.assertIn("network failed", result["error"])

    @patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["yt-dlp"],
            returncode=0,
            stdout="{not-json",
            stderr="",
        ),
    )
    def test_run_ytdlp_metadata_raises_on_invalid_json(self, _run):
        source = {"url": "https://www.youtube.com/playlist?list=abc"}

        with self.assertRaises(RuntimeError):
            fetch_podcast.run_ytdlp_metadata("/usr/local/bin/yt-dlp", source)

    @patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["yt-dlp"],
            returncode=1,
            stdout="",
            stderr="metadata failed",
        ),
    )
    def test_run_ytdlp_metadata_raises_on_nonzero_exit(self, _run):
        source = {"url": "https://www.youtube.com/playlist?list=abc"}

        with self.assertRaises(RuntimeError):
            fetch_podcast.run_ytdlp_metadata("/usr/local/bin/yt-dlp", source)

    @patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["yt-dlp"],
            returncode=0,
            stdout='{"entries":[]}',
            stderr="",
        ),
    )
    def test_run_ytdlp_metadata_uses_flat_playlist_discovery(self, run):
        source = {"url": "https://www.youtube.com/playlist?list=abc"}

        fetch_podcast.run_ytdlp_metadata("/usr/local/bin/yt-dlp", source)

        cmd = run.call_args.args[0]
        self.assertIn("--flat-playlist", cmd)
        self.assertIn("--playlist-items", cmd)
        self.assertEqual(
            cmd[cmd.index("--playlist-items") + 1],
            "1:20,-20:",
        )

    @patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["yt-dlp"],
            returncode=0,
            stdout='{"id":"abc123","upload_date":"20260504"}',
            stderr="",
        ),
    )
    def test_run_ytdlp_video_metadata_uses_no_playlist_skip_download(self, run):
        fetch_podcast.run_ytdlp_video_metadata(
            "/usr/local/bin/yt-dlp",
            "https://www.youtube.com/watch?v=abc123",
        )

        cmd = run.call_args.args[0]
        self.assertIn("--skip-download", cmd)
        self.assertIn("--no-playlist", cmd)
        self.assertNotIn("--flat-playlist", cmd)

    def test_output_cache_is_fresh_rejects_arbitrary_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "podcast.json"
            output.write_text(json.dumps({"ok": True}), encoding="utf-8")

            self.assertFalse(fetch_podcast.output_cache_is_fresh(output))

    def test_output_cache_is_fresh_accepts_valid_podcast_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "podcast.json"
            params = {
                "defaults": str(Path(tmpdir) / "defaults"),
                "config": None,
                "hours": 336,
                "no_cache": False,
            }
            output.write_text(
                json.dumps(
                    {
                        "source_type": "podcast",
                        "sources": [],
                        "input_params": params,
                    }
                ),
                encoding="utf-8",
            )

            self.assertTrue(fetch_podcast.output_cache_is_fresh(output, params))

    def test_output_cache_is_fresh_rejects_different_runtime_params(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "podcast.json"
            params = {
                "defaults": str(Path(tmpdir) / "defaults"),
                "config": None,
                "hours": 1,
                "no_cache": False,
            }
            output.write_text(
                json.dumps(
                    {
                        "source_type": "podcast",
                        "sources": [],
                        "input_params": params,
                    }
                ),
                encoding="utf-8",
            )

            expected = {**params, "hours": 336}

            self.assertFalse(fetch_podcast.output_cache_is_fresh(output, expected))

    def test_output_cache_is_fresh_rejects_missing_runtime_params_when_expected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "podcast.json"
            expected = {
                "defaults": str(Path(tmpdir) / "defaults"),
                "config": None,
                "hours": 336,
                "no_cache": False,
            }
            output.write_text(
                json.dumps(
                    {
                        "source_type": "podcast",
                        "sources": [],
                    }
                ),
                encoding="utf-8",
            )

            self.assertFalse(fetch_podcast.output_cache_is_fresh(output, expected))

    def test_output_request_params_change_when_config_contents_change(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            defaults = Path(tmpdir) / "defaults"
            config = Path(tmpdir) / "config"
            defaults.mkdir()
            config.mkdir()
            (defaults / "sources.json").write_text(
                json.dumps({"sources": []}),
                encoding="utf-8",
            )
            overlay = config / "follow-news-sources.json"
            overlay.write_text(
                json.dumps({"sources": [{"id": "one"}]}),
                encoding="utf-8",
            )

            first = fetch_podcast.output_request_params(defaults, config, 336)
            overlay.write_text(
                json.dumps({"sources": [{"id": "two"}]}),
                encoding="utf-8",
            )
            second = fetch_podcast.output_request_params(defaults, config, 336)

        self.assertEqual(first["defaults"], second["defaults"])
        self.assertEqual(first["config"], second["config"])
        self.assertNotEqual(first["config_fingerprint"], second["config_fingerprint"])

    @patch("fetch_podcast.save_podcast_cache")
    @patch("fetch_podcast.run_fetch", return_value=0)
    @patch("fetch_podcast.load_podcast_sources", return_value=[])
    def test_main_no_cache_does_not_save_cache(self, _load_sources, _run_fetch, save_cache):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "podcast.json"
            argv = [
                "fetch-podcast.py",
                "--defaults",
                str(Path(tmpdir) / "defaults"),
                "--output",
                str(output),
                "--no-cache",
                "--force",
            ]
            with patch.object(sys, "argv", argv):
                result = fetch_podcast.main()

        self.assertEqual(result, 0)
        save_cache.assert_not_called()
