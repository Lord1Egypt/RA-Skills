import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
FIXTURES_DIR = ROOT / "tests" / "fixtures"

sys.path.insert(0, str(SCRIPTS_DIR))

import search_nyaa  # noqa: E402
import workflow  # noqa: E402


def fixture(name: str):
    with (FIXTURES_DIR / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


class SearchNyaaTests(unittest.TestCase):
    def test_non_video_entries_filtered_from_run_search(self):
        results = fixture("jojo_search_results.json")

        with patch.object(search_nyaa, "search_nyaa_once", return_value=results):
            output = search_nyaa.run_search(
                "JOJO",
                aliases=["STEEL BALL RUN JoJo's Bizarre Adventure"],
                episode=1,
                latest_season=True,
            )

        titles = [item["title"] for item in output["results"]]
        self.assertEqual(output["resolved_latest_season"], 6)
        self.assertEqual(output["total"], 2)
        self.assertEqual(output["results"][0]["torrent_id"], "2087784")
        self.assertFalse(any("JOJOLands" in title for title in titles))
        self.assertFalse(any("FULL GAME" in title for title in titles))

    def test_part_range_is_not_mistaken_for_episode_batch(self):
        results = fixture("jojo_search_results.json")
        filtered = search_nyaa.filter_episode(results[:3], 1)
        ids = [item["torrent_id"] for item in filtered]

        self.assertEqual(ids, ["2087784", "2088732"])
        self.assertEqual(
            search_nyaa.extract_episode_numbers(results[0]["title"]),
            [],
        )


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.state_dir = Path(self.temp_dir.name)
        self.state_patches = [
            patch.object(workflow, "STATE_DIR", self.state_dir),
            patch.object(workflow, "PROFILE_PATH", self.state_dir / "user_profile.json"),
            patch.object(workflow, "LAST_DOWNLOAD_PATH", self.state_dir / "last_download.json"),
        ]
        for item in self.state_patches:
            item.start()

    def tearDown(self):
        for item in reversed(self.state_patches):
            item.stop()
        self.temp_dir.cleanup()

    def test_jojo_latest_season_first_episode_resolves_without_manual_choice(self):
        verify_payload = fixture("verification_found_jojo_latest.json")
        search_results = fixture("jojo_search_results.json")
        verify_calls = []

        def fake_verify(query: str, output_json: bool = False):
            verify_calls.append(query)
            return verify_payload

        with patch.object(workflow, "verify_anime", side_effect=fake_verify), patch.object(
            workflow, "run_search", side_effect=lambda query, **kwargs: search_nyaa.run_search(query, **kwargs)
        ), patch.object(search_nyaa, "search_nyaa_once", return_value=search_results):
            output = workflow.workflow("JOJO", episode=1, latest_season=True)

        self.assertEqual(verify_calls, ["飙马野郎 JOJO的奇妙冒险 第一赛段"])
        self.assertEqual(output["status"], "ready")
        self.assertFalse(output["needs_user_choice"])
        self.assertEqual(output["intent"]["action"], "search")
        self.assertEqual(output["decision"]["autonomy_mode"], "auto_execute")
        self.assertEqual(output["best_result"]["torrent_id"], "2087784")

    def test_bangumi_api_error_still_allows_search(self):
        verify_payload = fixture("verification_api_error.json")
        search_results = fixture("jojo_search_results.json")

        with patch.object(workflow, "verify_anime", return_value=verify_payload), patch.object(
            workflow, "run_search", side_effect=lambda query, **kwargs: search_nyaa.run_search(query, **kwargs)
        ), patch.object(search_nyaa, "search_nyaa_once", return_value=search_results):
            output = workflow.workflow("JOJO", episode=1, latest_season=True)

        self.assertEqual(output["status"], "ready")
        self.assertEqual(output["decision"]["confidence"], "high")
        self.assertEqual(output["best_result"]["torrent_id"], "2087784")

    def test_ambiguous_without_consensus_returns_need_disambiguation(self):
        verify_payload = fixture("verification_ambiguous_jojo.json")
        search_payload = {
            "query": "JOJO",
            "search_queries": ["JOJO"],
            "episode": 1,
            "latest_season_requested": True,
            "resolved_latest_season": 6,
            "total": 2,
            "results": [
                {
                    "title": "JoJo S06E01",
                    "size": "1.0 GiB",
                    "seeders": 100,
                    "torrent_id": "6",
                    "infohash": "hash6",
                    "season_numbers": [6],
                    "episode_numbers": [1],
                },
                {
                    "title": "JoJo S01E01",
                    "size": "1.0 GiB",
                    "seeders": 80,
                    "torrent_id": "1",
                    "infohash": "hash1",
                    "season_numbers": [1],
                    "episode_numbers": [1],
                },
            ],
            "has_chinese_subtitle": False,
            "warnings": [],
        }

        with patch.object(workflow, "verify_anime", return_value=verify_payload), patch.object(
            workflow, "run_search", return_value=search_payload
        ):
            output = workflow.workflow("JOJO", episode=1, latest_season=True)

        self.assertEqual(output["status"], "need_disambiguation")
        self.assertFalse(output["auto_resolved_by_search"])
        self.assertTrue(output["needs_user_choice"])
        self.assertEqual(output["decision"]["autonomy_mode"], "ask_once")
        self.assertTrue(output.get("next_question"))

    def test_cli_only_download_returns_magnet_payload(self):
        verify_payload = fixture("verification_found_jojo_latest.json")
        search_payload = {
            "query": "STEEL BALL RUN JoJo's Bizarre Adventure",
            "search_queries": ["STEEL BALL RUN JoJo's Bizarre Adventure"],
            "episode": 1,
            "latest_season_requested": True,
            "resolved_latest_season": 6,
            "total": 1,
            "results": [
                {
                    "title": "JoJo S06E01",
                    "size": "1.0 GiB",
                    "seeders": 100,
                    "torrent_id": "2087784",
                    "infohash": "977d12b6795ccd9e27f80d4411548fd1deeea2fa",
                    "season_numbers": [6],
                    "episode_numbers": [1],
                }
            ],
            "has_chinese_subtitle": False,
            "warnings": [],
        }

        with patch.object(workflow, "verify_anime", return_value=verify_payload), patch.object(
            workflow, "run_search", return_value=search_payload
        ):
            output = workflow.workflow(
                "JOJO",
                episode=1,
                latest_season=True,
                do_download=True,
                downloader="cli-only",
            )

        self.assertEqual(output["status"], "fallback_to_magnet")
        self.assertEqual(output["download"]["status"], "fallback_to_magnet")
        self.assertEqual(output["intent"]["action"], "magnet")
        self.assertIn("magnet:?", output["download"]["magnet"])
        self.assertIn("2087784.torrent", output["download"]["torrent_url"])

    def test_transmission_unavailable_falls_back_to_magnet(self):
        verify_payload = fixture("verification_found_jojo_latest.json")
        search_payload = {
            "query": "STEEL BALL RUN JoJo's Bizarre Adventure",
            "search_queries": ["STEEL BALL RUN JoJo's Bizarre Adventure"],
            "episode": 1,
            "latest_season_requested": True,
            "resolved_latest_season": 6,
            "total": 1,
            "results": [
                {
                    "title": "JoJo S06E01",
                    "size": "1.0 GiB",
                    "seeders": 100,
                    "torrent_id": "2087784",
                    "infohash": "977d12b6795ccd9e27f80d4411548fd1deeea2fa",
                    "season_numbers": [6],
                    "episode_numbers": [1],
                }
            ],
            "has_chinese_subtitle": False,
            "warnings": [],
        }

        with patch.object(workflow, "verify_anime", return_value=verify_payload), patch.object(
            workflow, "run_search", return_value=search_payload
        ), patch.object(workflow, "_ensure_transmission", return_value=(False, "Transmission 未安装，已回退到磁力链接模式")):
            output = workflow.workflow("JOJO", episode=1, latest_season=True, do_download=True)

        self.assertEqual(output["status"], "fallback_to_magnet")
        self.assertEqual(output["download"]["status"], "fallback_to_magnet")
        self.assertIn("Transmission 未安装", output["download"]["reason"])

    def test_natural_language_download_query_auto_executes_to_queue(self):
        verify_payload = fixture("verification_found_jojo_latest.json")
        search_payload = {
            "query": "STEEL BALL RUN JoJo's Bizarre Adventure",
            "search_queries": ["STEEL BALL RUN JoJo's Bizarre Adventure"],
            "episode": 1,
            "latest_season_requested": True,
            "resolved_latest_season": 6,
            "available_seasons": [1, 6],
            "total": 1,
            "results": [
                {
                    "title": "JoJo S06E01 1080p 简中 WEB-DL",
                    "size": "1.0 GiB",
                    "seeders": 100,
                    "torrent_id": "2087784",
                    "infohash": "977d12b6795ccd9e27f80d4411548fd1deeea2fa",
                    "season_numbers": [6],
                    "episode_numbers": [1],
                    "score": 320,
                    "tags": ["中字", "1080P", "WEB-DL"],
                }
            ],
            "has_chinese_subtitle": True,
            "warnings": [],
        }

        with patch.object(workflow, "verify_anime", return_value=verify_payload), patch.object(
            workflow, "run_search", return_value=search_payload
        ), patch.object(
            workflow,
            "queue_download",
            return_value={
                "status": "queued",
                "downloader": "transmission-daemon",
                "download_dir": "/tmp/downloads",
                "name": "JoJo S06E01 1080p 简中 WEB-DL",
                "infohash": "977d12b6795ccd9e27f80d4411548fd1deeea2fa",
                "magnet": "magnet:?xt=urn:btih:test",
                "torrent_url": "https://nyaa.si/download/2087784.torrent",
                "transmission_id": "1",
                "transmission_status": "Downloading",
                "progress": "12%",
            },
        ):
            output = workflow.workflow("帮我找一下 JOJO 最新一季第一集然后下载下来")

        self.assertEqual(output["status"], "queued")
        self.assertEqual(output["intent"]["action"], "download")
        self.assertFalse(output["decision"]["confirmation_required"])
        self.assertEqual(output["decision"]["autonomy_mode"], "auto_execute")

    def test_status_query_reads_last_download_state(self):
        record = {
            "status": "queued",
            "name": "JoJo S06E01 1080p 简中 WEB-DL",
            "transmission_id": "1",
            "download_dir": "/tmp/downloads",
            "magnet": "magnet:?xt=urn:btih:test",
            "torrent_url": "https://nyaa.si/download/2087784.torrent",
        }

        with patch.object(workflow, "load_last_download_state", return_value=record), patch.object(
            workflow,
            "fetch_download_status",
            return_value={
                "status": "queued",
                "name": "JoJo S06E01 1080p 简中 WEB-DL",
                "transmission_id": "1",
                "transmission_state": "Downloading",
                "progress": "42%",
                "download_dir": "/tmp/downloads",
            },
        ):
            output = workflow.workflow("刚才那个下载怎么样")

        self.assertEqual(output["status"], "queued")
        self.assertEqual(output["intent"]["action"], "status")
        self.assertEqual(output["download"]["transmission_state"], "Downloading")
        self.assertIn("JoJo", output["summary"])


if __name__ == "__main__":
    unittest.main()
