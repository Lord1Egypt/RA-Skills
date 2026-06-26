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

import intent  # noqa: E402
import workflow  # noqa: E402


def fixture(name: str):
    with (FIXTURES_DIR / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def make_search_payload(query: str, episode: int | None = None, latest_season: bool = False) -> dict:
    season = 6 if latest_season or "steel ball run" in query.lower() or "飙马野郎" in query.lower() else 1
    target_episode = episode or 12
    title = f"{query} S{season:02d}E{target_episode:02d} 1080p 简中 WEB-DL"
    payload = {
        "query": query,
        "search_queries": [query],
        "episode": episode,
        "latest_season_requested": latest_season,
        "resolved_latest_season": season if latest_season else None,
        "available_seasons": [1, season] if latest_season and season != 1 else [season],
        "total": 1,
        "results": [
            {
                "title": title,
                "size": "1.2 GiB",
                "seeders": 88,
                "torrent_id": "2087784",
                "infohash": "977d12b6795ccd9e27f80d4411548fd1deeea2fa",
                "season_numbers": [season],
                "episode_numbers": [target_episode],
                "score": 320,
                "tags": ["中字", "1080P", "WEB-DL"],
            }
        ],
        "has_chinese_subtitle": True,
        "warnings": [],
    }
    if episode is None:
        payload["latest_episode"] = target_episode
    return payload


def fake_verify(query: str, output_json: bool = False):
    return {
        "status": "found",
        "query": query,
        "match": {
            "id": 1,
            "name": query,
            "name_jp": query,
        },
        "alternatives": [],
    }


def fake_run_search(query: str, **kwargs):
    return make_search_payload(query, kwargs.get("episode"), kwargs.get("latest_season", False))


def fake_queue_download(best: dict, download_dir: str, downloader: str):
    if downloader == "cli-only":
        return {
            "status": "fallback_to_magnet",
            "mode": "cli-only",
            "reason": "cli-only 模式按请求直接返回磁力链接",
            "magnet": "magnet:?xt=urn:btih:test",
            "torrent_url": "https://nyaa.si/download/2087784.torrent",
            "name": best["title"],
        }
    return {
        "status": "queued",
        "downloader": "transmission-daemon",
        "download_dir": download_dir,
        "name": best["title"],
        "infohash": best["infohash"],
        "magnet": "magnet:?xt=urn:btih:test",
        "torrent_url": "https://nyaa.si/download/2087784.torrent",
        "transmission_id": "1",
        "transmission_status": "Downloading",
        "progress": "12%",
    }


class IntentReplayTests(unittest.TestCase):
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

    def test_positive_replay_samples_reach_target_status_and_intent_match_rate(self):
        data = fixture("intent_replay.json")
        exact_matches = 0

        with patch.object(workflow, "verify_anime", side_effect=fake_verify), patch.object(
            workflow, "run_search", side_effect=fake_run_search
        ), patch.object(workflow, "queue_download", side_effect=fake_queue_download), patch.object(
            workflow, "fetch_download_status",
            return_value={
                "status": "queued",
                "name": "Recent Task",
                "transmission_id": "1",
                "transmission_state": "Downloading",
                "progress": "42%",
            },
        ), patch.object(
            workflow,
            "load_last_download_state",
            return_value={"status": "queued", "name": "Recent Task", "transmission_id": "1"},
        ):
            for sample in data["positive"]:
                parsed = intent.parse_intent(sample["query"])
                self.assertTrue(
                    parsed["should_trigger_skill"],
                    msg=f"Expected skill trigger for sample: {sample['query']}",
                )

                matched = True
                for key, expected in sample["intent"].items():
                    if parsed.get(key) != expected:
                        matched = False

                output = workflow.workflow(sample["query"])
                self.assertEqual(output["status"], sample["expected_status"], msg=sample["query"])
                self.assertEqual(
                    output["decision"]["confirmation_required"],
                    sample["confirmation_required"],
                    msg=sample["query"],
                )
                self.assertFalse(isinstance(output.get("next_question"), list), msg=sample["query"])

                if matched:
                    exact_matches += 1

        rate = exact_matches / len(data["positive"])
        self.assertGreaterEqual(rate, 0.9, msg=f"intent exact match rate too low: {rate:.2%}")

    def test_negative_replay_samples_do_not_trigger_skill(self):
        data = fixture("intent_replay.json")
        for query in data["negative"]:
            self.assertFalse(intent.should_trigger_skill(query), msg=query)

    def test_explicit_profile_update_is_persisted_and_reused(self):
        with patch.object(workflow, "verify_anime", side_effect=fake_verify), patch.object(
            workflow, "run_search", side_effect=fake_run_search
        ), patch.object(workflow, "queue_download", side_effect=fake_queue_download):
            first = workflow.workflow("以后默认给我 720p 简中，帮我下载 JOJO 最新一季第一集")
            second = workflow.workflow("先找 JOJO 最新一季第一集，别下载")

        self.assertTrue(first["profile_update"]["saved"])
        self.assertTrue((self.state_dir / "user_profile.json").exists())
        self.assertIn("subtitle_pref", second["decision"]["profile_applied"])
        self.assertEqual(second["search"]["preferences_applied"]["subtitle_pref"], "simplified")


if __name__ == "__main__":
    unittest.main()
