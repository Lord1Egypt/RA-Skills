import importlib
import os
import sys
import tempfile
import unittest


SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)


class DiscordThreadPersistenceTests(unittest.TestCase):
    def setUp(self):
        self._env = dict(os.environ)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._env)

    def test_thread_id_persists_across_module_reloads(self):
        with tempfile.TemporaryDirectory() as td:
            thread_file = os.path.join(td, "thread-id")
            os.environ["WEBHOOK_URL"] = "https://example.invalid/webhook"
            os.environ["THREAD_MODE"] = "true"
            os.environ["BOT_TOKEN"] = "bot-token"
            os.environ["CODEFLOW_DISCORD_THREAD_ID_FILE"] = thread_file

            from platforms import discord as dc

            dc = importlib.reload(dc)
            calls: list[tuple[str, dict, object]] = []

            def fake_http_post_json(url: str, payload: dict, headers=None) -> dict:
                calls.append((url, payload, headers))
                if "wait=true" in url:
                    return {"id": "m1", "channel_id": "c1"}
                if url.endswith("/threads") or "/threads" in url:
                    return {"id": "t1"}
                return {}

            dc._http_post_json = fake_http_post_json
            dc.post("hello", name="Agent")

            with open(thread_file, "r", encoding="utf-8") as f:
                self.assertEqual(f.read().strip(), "t1")
            self.assertEqual(sum("wait=true" in url for url, _, _ in calls), 1)

            calls.clear()
            dc = importlib.reload(dc)
            dc._http_post_json = fake_http_post_json
            dc.post("hello again", name="Agent")

            self.assertEqual(sum("wait=true" in url for url, _, _ in calls), 0)
            post_urls = [url for url, _, _ in calls if "/threads" not in url]
            self.assertTrue(any("thread_id=t1" in url for url in post_urls))


if __name__ == "__main__":
    unittest.main()
