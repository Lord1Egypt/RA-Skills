import contextlib
import importlib.util
import io
import json
import os
import subprocess
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).parents[1] / "scripts" / "concept_radar.py"
spec = importlib.util.spec_from_file_location("generic_concept_radar", SCRIPT)
radar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(radar)


class Response:
    def __init__(self, payload=b"", headers=None, url="https://example.test/"):
        self.payload = payload
        self.status = 200
        self.headers = headers or {}
        self.url = url

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.payload

    def geturl(self):
        return self.url


def author():
    return {"id": "tester", "display_name": "Test Author"}


def candidate(key="url:https://example.test/concept"):
    body = "A complete synthetic concept body."
    return {
        "source_type": "url",
        "source_key": key,
        "revision": "r1",
        "author_id": None,
        "author_name": "example.test",
        "title": "A concept",
        "body": body,
        "published_at": None,
        "updated_at": None,
        "canonical_url": "https://example.test/concept",
        "content_hash": radar.content_hash(body),
        "semantic_hash": radar.semantic_hash(body),
    }


def card(source=None):
    source = source or candidate()
    url = source["canonical_url"]
    evidence = [{
        "field": field,
        "quote": f"Evidence for {field}.",
        "source_url": url,
    } for field in sorted(radar.EVIDENCE_FIELDS)]
    return {
        "source_key": source["source_key"],
        "revision": source["revision"],
        "canonical_url": url,
        "concept_name": "Evidence-backed Concept",
        "what": "A structured knowledge mechanism.",
        "why_important": "It separates claims from evidence.",
        "problem_solved": "It avoids unsupported summaries.",
        "compared_with": "Free-form summaries",
        "similarities": "Both compress source material.",
        "differences": "This one maps claims to evidence.",
        "use_when": "When decisions need traceability.",
        "not_replacement": "It does not replace quick reading.",
        "maturity": "emerging",
        "confidence": 0.8,
        "action_recommendation": "Trial it in one low-risk workflow.",
        "comparison_sources": [{"title": "Primary source", "url": url}],
        "evidence": evidence,
        "scores": {
            "novelty": 2,
            "problem_clarity": 2,
            "mechanism_clarity": 1,
            "evidence_quality": 2,
            "source_authority": 1,
            "promotional_penalty": 0,
        },
    }


class FetchTests(unittest.TestCase):
    def test_single_url_extracts_html_and_metadata(self):
        html = b"<html><head><title>Concept Page</title><style>x</style></head><body><h1>Idea</h1><p>Useful mechanism.</p><script>bad</script></body></html>"

        def opener(request, timeout=30):
            self.assertEqual(request.full_url, "https://example.test/concept")
            return Response(
                html,
                {"Content-Type": "text/html; charset=utf-8", "ETag": '"v1"'},
                request.full_url,
            )

        rows, metadata = radar.scan_url("https://example.test/concept#top", {}, opener)
        self.assertEqual(rows[0]["title"], "Concept Page")
        self.assertIn("Useful mechanism.", rows[0]["body"])
        self.assertNotIn("bad", rows[0]["body"])
        self.assertEqual(rows[0]["revision"], '"v1"')
        self.assertEqual(metadata["transport"], "single_url")

    def test_atom_and_rss_are_preserved(self):
        atom = b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>tag:x,1</id><title>A</title><updated>2026-02-03T04:05:06Z</updated><summary>Body</summary><link href="https://example.test/a"/></entry></feed>'
        row = radar.parse_feed(atom, author(), "https://example.test/feed")[0]
        self.assertEqual((row["source_key"], row["body"]), ("atom:tag:x,1", "Body"))
        rss = b"<rss><channel><item><title>R</title><link>https://example.test/r</link><description>RSS body</description></item></channel></rss>"
        row = radar.parse_feed(rss, author(), "https://example.test/feed")[0]
        self.assertEqual((row["source_key"], row["body"]), ("rss:https://example.test/r", "RSS body"))

    def test_gist_rate_limit_fallback_is_preserved(self):
        calls = []

        def opener(request, timeout=30):
            url = request.full_url
            calls.append(url)
            if url.startswith("https://api.github.com/"):
                raise urllib.error.HTTPError(
                    url, 403, "rate limited", {"x-ratelimit-remaining": "0"},
                    io.BytesIO(b'{"message":"API rate limit exceeded"}'),
                )
            if url == "https://gist.github.com/u":
                return Response(b'<a href="/u/a1">one</a>', url=url)
            if url == "https://gist.githubusercontent.com/u/a1/raw":
                return Response(
                    b"complete body",
                    url="https://gist.githubusercontent.com/u/a1/raw/deadbeef/a.md",
                )
            raise AssertionError(url)

        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": ""}, clear=False), \
                mock.patch.object(radar.time, "sleep"):
            rows, metadata = radar.scan_gists(
                author(), {"username": "u"}, {}, opener
            )
        self.assertEqual(rows[0]["body"], "complete body")
        self.assertEqual(metadata["transport"], "gist_profile_raw")
        self.assertIn("https://gist.github.com/u", calls)


class DedupTests(unittest.TestCase):
    def test_revision_content_and_semantic_dedup(self):
        source = candidate()
        states = (
            {"items": {source["source_key"]: {"revision": source["revision"]}}},
            {"items": {"other": {"content_hash": source["content_hash"]}}},
            {"items": {"other": {"semantic_hash": source["semantic_hash"]}}},
        )
        for state in states:
            with self.subTest(state=state):
                self.assertTrue(radar.is_seen(source, state))
        changed = dict(
            source, revision="new", content_hash="new", semantic_hash="new"
        )
        self.assertFalse(radar.is_seen(changed, states[-1]))


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.runtime = self.root / "runtime"
        self.runtime.mkdir()
        self.config = self.root / "config.json"
        self.state = self.root / "state.json"
        self.selection = self.root / "selection.json"
        self.source = candidate()
        self.config.write_text(json.dumps({
            "schema_version": 1,
            "selection": {"minimum_score": 6, "max_items_per_run": 5},
            "authors": [],
        }))
        self.reset_state()

    def reset_state(self):
        self.state.write_text(json.dumps({
            "schema_version": 1,
            "sources": {},
            "items": {},
            "concepts": {},
            "pending_scan": {"mode": "single-url", "source_updates": {}},
        }))
        (self.runtime / "candidates.json").write_text(json.dumps({
            "schema_version": 1,
            "mode": "single-url",
            "candidates": [self.source],
        }))

    def tearDown(self):
        self.temp.cleanup()

    def test_card_schema_fields_render_to_markdown_and_json(self):
        item = card(self.source)
        self.selection.write_text(json.dumps({"items": [item]}))
        output, markdown = radar.validate_selection(
            self.selection, self.config, self.state, self.runtime
        )
        self.assertEqual(output["items"][0]["maturity"], "emerging")
        for value in (
            "成熟度", "置信度", "行动建议", "对比来源", "证据",
            item["action_recommendation"],
        ):
            self.assertIn(value, markdown)
        saved = json.loads((self.runtime / "concept-radar.json").read_text())
        self.assertEqual(saved["items"][0]["confidence"], 0.8)
        self.assertTrue((self.runtime / "concept-radar.md").exists())

    def test_evidence_policy_and_new_fields_are_enforced(self):
        cases = {
            "maturity": lambda item: item.update(maturity="unknown"),
            "confidence": lambda item: item.update(confidence=1.2),
            "comparison_sources": lambda item: item.update(comparison_sources=[]),
            "evidence": lambda item: item.update(evidence=[]),
        }
        for expected, mutate in cases.items():
            with self.subTest(expected=expected):
                self.reset_state()
                item = card(self.source)
                mutate(item)
                self.selection.write_text(json.dumps({"items": [item]}))
                with self.assertRaisesRegex(radar.RadarError, expected):
                    radar.validate_selection(
                        self.selection, self.config, self.state, self.runtime
                    )

    def test_default_doctor_never_checks_lark(self):
        def forbidden(*args, **kwargs):
            raise AssertionError("default doctor must not call lark-cli")

        with mock.patch.object(radar.shutil, "which", side_effect=forbidden):
            result = radar.run_doctor(self.config, self.state, runner=forbidden)
        self.assertEqual(result["publishing"], "not requested")
        self.assertNotIn("lark_cli", result)

    def test_empty_selection_exports_without_publishing(self):
        self.selection.write_text(json.dumps({"items": []}))
        output, markdown = radar.validate_selection(
            self.selection, self.config, self.state, self.runtime
        )
        self.assertEqual((output["items"], markdown), ([], ""))

        def forbidden(*args, **kwargs):
            raise AssertionError("must not call lark-cli")

        self.assertIsNone(radar.publish_feishu(
            self.state, self.runtime, forbidden
        ))

    def test_cli_single_url_mode_is_inferred(self):
        html = b"<html><title>A</title><body>Body</body></html>"
        self.state.write_text(json.dumps({
            "schema_version": 1,
            "sources": {},
            "items": {},
            "concepts": {},
            "pending_scan": None,
        }))

        def opener(request, timeout=30):
            return Response(html, {"Content-Type": "text/html"}, request.full_url)

        with mock.patch.object(radar, "request_bytes", wraps=radar.request_bytes), \
                mock.patch.object(urllib.request, "urlopen", side_effect=opener):
            output = io.StringIO()
            argv = [
                "--config", str(self.config),
                "--state", str(self.state),
                "--runtime", str(self.runtime),
                "scan", "--url", "https://example.test/new",
            ]
            with contextlib.redirect_stdout(output):
                self.assertEqual(radar.main(argv), 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["result"]["candidates"][0]["source_type"], "url")


class PublishTests(unittest.TestCase):
    def test_feishu_publish_is_explicit_and_commits_only_on_success(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = root / "runtime"
            runtime.mkdir()
            state_path = root / "state.json"
            item = card()
            fingerprint = radar.fingerprint(item["concept_name"])
            item["concept_fingerprint"] = fingerprint
            state_path.write_text(json.dumps({
                "schema_version": 1,
                "sources": {},
                "items": {item["source_key"]: {"status": "exported"}},
                "concepts": {fingerprint: {
                    "status": "exported",
                    "preferred_source": item["source_key"],
                    "message_id": None,
                }},
                "pending_scan": None,
            }))
            (runtime / "concept-radar.md").write_text("digest")
            (runtime / "concept-radar.json").write_text(json.dumps({"items": [item]}))

            def runner(argv, **kwargs):
                if argv[1] == "whoami":
                    value = {
                        "identity": "user",
                        "available": True,
                        "tokenStatus": "ready",
                        "onBehalfOf": {"openId": "ou_test"},
                    }
                else:
                    value = {"ok": True, "identity": "user", "message_id": "m1"}
                return subprocess.CompletedProcess(
                    argv, 0, stdout=json.dumps(value), stderr=""
                )

            self.assertEqual(
                radar.publish_feishu(state_path, runtime, runner), "m1"
            )
            saved = json.loads(state_path.read_text())
            self.assertEqual(saved["concepts"][fingerprint]["status"], "published")
            self.assertEqual(saved["concepts"][fingerprint]["message_id"], "m1")


if __name__ == "__main__":
    unittest.main()
