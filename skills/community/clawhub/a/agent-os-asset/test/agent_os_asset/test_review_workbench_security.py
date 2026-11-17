"""Workbench security regressions: temporary fixtures, no listening sockets."""

from __future__ import annotations

from email.message import Message
from html.parser import HTMLParser
import io
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from test_review_workbench import SCRIPT, SERVER, load_module


class ScriptCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.current = {"attrs": dict(attrs), "text": ""}

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"] += data

    def handle_endtag(self, tag):
        if tag == "script" and self.current is not None:
            self.scripts.append(self.current)
            self.current = None


class WorkbenchSecurityTest(unittest.TestCase):
    def setUp(self):
        self.renderer = load_module(SCRIPT, "security_renderer")
        self.server_module = load_module(SERVER, "security_server")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / "workspace"
        self.root.mkdir()
        self.workbench = self.root / "cleanup-asset-review-workbench.html"
        self.html = self.render()
        self.workbench.write_text(self.html, encoding="utf-8")
        self.handler_type = self.server_module.configured_handler(
            self.root, self.root / "adapter.py", self.root / "pipeline.py",
            allow_write=True, allow_apply=True, allow_file_open=True,
        )
        self.payload = {"scope": ".", "decisions": [{
            "asset_id": "asset-a", "decision": "keep", "pii_label": "non_pii"
        }]}

    def render(self, scope=".", rows=None):
        return self.renderer.render_workbench(
            root=self.root, scope=scope, rows=rows or [],
            adapter_path=self.root / "adapter.py",
            pipeline_path=self.root / "pipeline.py", shortcut_available=False,
        )

    def request(self, method, path, payload=None, *, headers=None, peer="127.0.0.1"):
        handler = object.__new__(self.handler_type)
        handler.command = method
        handler.path = path
        handler.directory = str(self.root)
        handler.client_address = (peer, 50000)
        handler.server = SimpleNamespace(server_address=("127.0.0.1", 8766))
        handler.headers = Message()
        values = {
            "Host": "127.0.0.1:8766", "Origin": "http://127.0.0.1:8766",
            "Content-Type": "application/json",
            "X-Review-Token": getattr(self.handler_type, "request_token", "legacy-no-token"),
        }
        body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        values["Content-Length"] = str(len(body))
        values.update(headers or {})
        for name, value in values.items():
            if value is not None:
                handler.headers[name] = value
        handler.rfile = io.BytesIO(body)
        handler.wfile = io.BytesIO()
        handler.statuses = []
        handler.response_headers = {}
        handler.send_response = lambda status, *args: handler.statuses.append(int(status))
        handler.send_header = lambda name, value: handler.response_headers.__setitem__(name, value)
        handler.end_headers = lambda: None
        handler.log_message = lambda *args: None
        return handler

    def dispatch(self, handler):
        getattr(handler, "do_" + handler.command)()
        return handler.statuses[-1]

    def test_scope_title_cannot_create_executable_script(self):
        payload = '</title><script>globalThis.injected=1</script><title>'
        parser = ScriptCollector()
        parser.feed(self.render(scope=payload, rows=[{"asset_id": "a", "title": payload}]))
        self.assertEqual(len(parser.scripts), 2)
        self.assertFalse(any(script["text"] == "globalThis.injected=1" for script in parser.scripts))
        data = next(script for script in parser.scripts if script["attrs"].get("id") == "asset-data")
        self.assertEqual(json.loads(data["text"])["scope"], payload)

    def test_saved_decisions_cannot_overwrite_hardlinked_source(self):
        source = self.root / "source.txt"
        source.write_text("SOURCE_SENTINEL", encoding="utf-8")
        output = self.server_module.imported_decision_path(self.root, ".")
        output.parent.mkdir(parents=True)
        os.link(source, output)
        handler = self.request("POST", "/__save_decisions", self.payload)
        self.assertEqual(self.dispatch(handler), 200)
        self.assertEqual(source.read_text(), "SOURCE_SENTINEL")
        self.assertEqual(json.loads(output.read_text())["scope"], ".")

    def test_saved_decisions_cannot_redirect_state_into_source_directory(self):
        source_dir = self.root / "source"
        source_dir.mkdir()
        (self.root / ".cleanup-extracted").symlink_to(source_dir, target_is_directory=True)
        handler = self.request("POST", "/__save_decisions", self.payload)
        self.assertGreaterEqual(self.dispatch(handler), 400)
        self.assertEqual(list(source_dir.iterdir()), [])

    def test_asset_json_cannot_change_html_script_parser_state(self):
        payload = '<!--<script>untrusted</script><img src=x onerror=bad()>'
        parser = ScriptCollector()
        parser.feed(self.render(rows=[{"asset_id": "a", "title": payload}]))
        self.assertEqual(len(parser.scripts), 2)
        data = next(script for script in parser.scripts if script["attrs"].get("id") == "asset-data")
        self.assertNotIn("<!--", data["text"])
        self.assertEqual(json.loads(data["text"])["assets"][0]["title"], payload)

    def test_unauthorized_requests_never_save_or_execute(self):
        invalid = [
            {"Origin": "https://attacker.invalid"}, {"Origin": "null"}, {"Origin": None},
            {"Host": "attacker.invalid:8766"}, {"Host": "127.0.0.1:9999"}, {"Host": None},
            {"X-Review-Token": None}, {"X-Review-Token": "wrong"},
        ]
        for endpoint in ("/__save_decisions", "/__apply_decisions", "/__open"):
            for headers in invalid:
                with self.subTest(endpoint=endpoint, headers=headers):
                    handler = self.request("POST", endpoint, self.payload, headers=headers)
                    handler.save_payload = Mock(return_value=self.root / "mock.json")
                    result = SimpleNamespace(returncode=0, stdout='{"results":[]}', stderr="")
                    with patch.object(self.server_module.subprocess, "run", return_value=result) as run:
                        self.assertEqual(self.dispatch(handler), 403)
                    handler.save_payload.assert_not_called()
                    run.assert_not_called()

    def test_no_cors_preflight_or_get_side_effect(self):
        for method, path in (("OPTIONS", "/__apply_decisions"), ("GET", "/__open?path=cleanup-asset-review-workbench.html")):
            with self.subTest(method=method):
                handler = self.request(method, path)
                with patch.object(self.server_module.subprocess, "run") as run:
                    self.assertGreaterEqual(self.dispatch(handler), 400)
                run.assert_not_called()
                self.assertFalse(any(name.lower().startswith("access-control-") for name in handler.response_headers))

    def test_static_routes_cannot_serve_sources_directories_or_symlinks(self):
        outside = self.root.parent / "outside.html"
        outside.write_text("OUTSIDE_SENTINEL", encoding="utf-8")
        (self.root / "source.html").write_text("<script>bad()</script>", encoding="utf-8")
        (self.root / "linked.html").symlink_to(outside)
        (self.root / "linked-dir").symlink_to(self.root.parent, target_is_directory=True)
        routes = ["/", "/source.html", "/linked.html", "/linked-dir/outside.html",
                  "/../outside.html", "/%2e%2e/outside.html", "/%2e%2e%2foutside.html"]
        for method in ("GET", "HEAD"):
            for path in routes:
                with self.subTest(method=method, path=path):
                    handler = self.request(method, path)
                    self.assertGreaterEqual(self.dispatch(handler), 400)
                    self.assertNotIn(b"OUTSIDE_SENTINEL", handler.wfile.getvalue())
                    if method == "HEAD":
                        self.assertEqual(handler.wfile.getvalue(), b"")
        self.workbench.unlink()
        self.workbench.symlink_to(outside)
        for method in ("GET", "HEAD"):
            handler = self.request(method, "/cleanup-asset-review-workbench.html")
            self.assertGreaterEqual(self.dispatch(handler), 400)
            self.assertNotIn(b"OUTSIDE_SENTINEL", handler.wfile.getvalue())

    def test_only_workbench_get_injects_instance_token_without_persisting_it(self):
        other = self.server_module.configured_handler(self.root, self.root / "adapter.py", self.root / "pipeline.py")
        token = getattr(self.handler_type, "request_token", "")
        self.assertGreaterEqual(len(token), 32)
        self.assertNotEqual(token, other.request_token)
        for method in ("GET", "HEAD"):
            handler = self.request(method, "/cleanup-asset-review-workbench.html", headers={"Origin": None})
            self.assertEqual(self.dispatch(handler), 200)
            self.assertEqual(handler.response_headers["Cache-Control"], "no-store")
            self.assertEqual(handler.response_headers["X-Content-Type-Options"], "nosniff")
            if method == "GET":
                self.assertIn(token.encode(), handler.wfile.getvalue())
            else:
                self.assertEqual(handler.wfile.getvalue(), b"")
        self.assertNotIn(token, self.workbench.read_text(encoding="utf-8"))
        bad_host = self.request("GET", "/cleanup-asset-review-workbench.html", headers={"Host": "evil.invalid"})
        self.assertEqual(self.dispatch(bad_host), 403)
        remote_peer = self.request("GET", "/cleanup-asset-review-workbench.html", peer="192.0.2.1")
        self.assertEqual(self.dispatch(remote_peer), 403)

    def test_source_html_cannot_obtain_token_by_copying_template_or_linking_workbench(self):
        (self.root / "source.html").write_text(self.html, encoding="utf-8")
        (self.root / "alias.html").symlink_to(self.workbench)
        other_scope = self.root / "other"
        other_scope.mkdir()
        (other_scope / self.workbench.name).write_text(self.html, encoding="utf-8")
        for method in ("GET", "HEAD"):
            for path in ("/source.html", "/alias.html", "/other/cleanup-asset-review-workbench.html"):
                with self.subTest(method=method, path=path):
                    handler = self.request(method, path)
                    self.assertEqual(self.dispatch(handler), 404)
                    self.assertNotIn(self.handler_type.request_token.encode(), handler.wfile.getvalue())
                    self.assertFalse(any(name.lower().startswith("access-control-") for name in handler.response_headers))

    def test_selected_html_is_untrusted_and_is_rebuilt_with_installed_renderer(self):
        payload = {
            "root": "/attacker", "scope": "../other", "static_apply_command": "FORGED_COMMAND",
            "summary": {"assets": "FORGED_SUMMARY"}, "shortcut_available": True,
            "assets": [{"asset_id": "a", "title": '</script><script>FORGED_ROW()</script>',
                        "source_paths": ["note.txt"], "summary": "retained text"}],
        }
        encoded = json.dumps(payload).replace("<", "\\u003c")
        forged = (
            '<html><head><meta name="review-token" content=""><base href="https://attacker.invalid/">'
            '</head><body onload="FORGED_HANDLER()"><script>FORGED_SCRIPT()</script>'
            f'<script id="asset-data" type="application/json">{encoded}</script></body></html>'
        )
        self.workbench.write_text(forged, encoding="utf-8")
        poisoned_renderer = SimpleNamespace(render_workbench=Mock(side_effect=AssertionError("untrusted import")))
        with patch.dict(sys.modules, {"review_workbench": poisoned_renderer}):
            self.handler_type = self.server_module.configured_handler(self.root, self.root / "adapter.py", self.root / "pipeline.py")
            handler = self.request("GET", "/cleanup-asset-review-workbench.html")
            self.assertEqual(self.dispatch(handler), 200)
        output = handler.wfile.getvalue().decode()
        expected = self.render(rows=payload["assets"]).replace(
            '<meta name="review-token" content="">',
            f'<meta name="review-token" content="{self.handler_type.request_token}">',
        )
        self.assertEqual(output, expected)
        self.assertNotIn("FORGED_SCRIPT", output)
        self.assertNotIn("FORGED_COMMAND", output)
        self.assertNotIn("FORGED_HANDLER", output)
        self.assertNotIn("FORGED_SUMMARY", output)
        self.assertEqual(self.workbench.read_text(encoding="utf-8"), forged)
        parser = ScriptCollector(); parser.feed(output)
        data = next(script for script in parser.scripts if script["attrs"].get("id") == "asset-data")
        restored = json.loads(data["text"])
        self.assertEqual(restored["root"], str(self.root))
        self.assertEqual(restored["scope"], ".")
        self.assertEqual(restored["assets"][0]["title"], payload["assets"][0]["title"])

    def test_workbench_requires_one_valid_asset_data_object(self):
        valid = '<script id="asset-data" type="application/json">{"assets":[]}</script>'
        cases = [
            "", valid + valid,
            '<script id="asset-data">{"assets":[]}</script>',
            '<script id="asset-data" id="other" type="application/json">{"assets":[]}</script>',
            '<div id="asset-data">{"assets":[]}</div>',
            '<script id="asset-data" type="application/json">{"assets":[]}',
        ]
        for data in ('{', '[]', '{"assets":"bad"}', '{"assets":[1]}',
                     '{"assets":[],"assets":[]}', '{"assets":[{"source_paths":"bad"}]}',
                     '{"assets":[{"title":"\\ud800"}]}'):
            cases.append(f'<script id="asset-data" type="application/json">{data}</script>')
        for content in cases:
            with self.subTest(content=content):
                self.workbench.write_text('<meta name="review-token" content="">' + content, encoding="utf-8")
                for method in ("GET", "HEAD"):
                    handler = self.request(method, "/cleanup-asset-review-workbench.html")
                    self.assertEqual(self.dispatch(handler), 409)
                    self.assertNotIn(self.handler_type.request_token.encode(), handler.wfile.getvalue())

    def test_legacy_asset_data_without_token_marker_can_be_safely_rebuilt(self):
        self.workbench.write_text(
            '<script id="asset-data" type="application/json">{"assets":[]}</script>', encoding="utf-8"
        )
        handler = self.request("GET", "/cleanup-asset-review-workbench.html")
        self.assertEqual(self.dispatch(handler), 200)
        self.assertIn(self.handler_type.request_token.encode(), handler.wfile.getvalue())

    def test_duplicate_headers_foreign_instance_tokens_and_cross_site_get_are_rejected(self):
        for name in ("Host", "Origin", "X-Review-Token", "Content-Type", "Content-Length"):
            handler = self.request("POST", "/__save_decisions", self.payload)
            handler.headers[name] = handler.headers[name]
            handler.save_payload = Mock(return_value=self.root / "mock.json")
            self.assertGreaterEqual(self.dispatch(handler), 400)
            handler.save_payload.assert_not_called()
        other = self.server_module.configured_handler(self.root, SCRIPT, SERVER)
        handler = self.request("POST", "/__save_decisions", self.payload, headers={"X-Review-Token": other.request_token})
        self.assertEqual(self.dispatch(handler), 403)
        for headers in ({"Origin": "https://attacker.invalid"}, {"Origin": None, "Sec-Fetch-Site": "cross-site"}):
            handler = self.request("GET", "/cleanup-asset-review-workbench.html", headers=headers)
            self.assertEqual(self.dispatch(handler), 403)
            self.assertNotIn(self.handler_type.request_token.encode(), handler.wfile.getvalue())

    def test_loopback_authorities_and_configured_scope(self):
        for address, authority in (("127.0.0.1", "localhost:8766"), ("::1", "[::1]:8766")):
            handler = self.request("GET", "/cleanup-asset-review-workbench.html", peer=address,
                                   headers={"Host": authority, "Origin": "http://" + authority})
            handler.server.server_address = (address, 8766)
            self.assertEqual(self.dispatch(handler), 200)
        scope = self.root / "nested"
        scope.mkdir()
        (scope / self.workbench.name).write_text(self.render(scope="nested"), encoding="utf-8")
        self.handler_type = self.server_module.configured_handler(self.root, SCRIPT, SERVER, "nested", allow_write=True)
        handler = self.request("GET", "/nested/cleanup-asset-review-workbench.html")
        self.assertEqual(self.dispatch(handler), 200)
        handler = self.request("GET", "/cleanup-asset-review-workbench.html")
        self.assertEqual(self.dispatch(handler), 404)
        handler = self.request("POST", "/__save_decisions", self.payload)
        self.assertEqual(self.dispatch(handler), 400)

    def test_post_body_limits_media_type_and_decision_schema(self):
        cases = [
            (self.payload, {"Content-Type": "text/plain"}, 415),
            (self.payload, {"Content-Length": "999999999"}, 413),
            (self.payload, {"Content-Length": "-1"}, 400),
            (self.payload, {"Transfer-Encoding": "chunked"}, 400),
            (self.payload, {"Content-Length": "999"}, 400),
            (self.payload, {"Content-Type": "application/json; charset=iso-8859-1"}, 415),
            (b'{"scope":".","decisions":', {}, 400),
            (b'\xff', {}, 400),
            (b'{"scope":".","scope":"nested","decisions":[]}', {}, 400),
            (b'{"scope":".","decisions":[{"asset_id":"a","decision":"keep","reason":"\\ud800"}]}', {}, 400),
            ({"scope": ".", "decisions": ["keep"]}, {}, 400),
            ({"scope": ".", "decisions": [{"asset_id": "a", "decision": "execute"}]}, {}, 400),
            ({"scope": ".", "decisions": [{"asset_id": "a", "decision": "keep", "pii_label": False}]}, {}, 400),
            ({"scope": ".", "decisions": [{"asset_id": "a", "decision": "keep", "source_paths": "bad"}]}, {}, 400),
            ({"scope": ".", "decisions": self.payload["decisions"] * 2}, {}, 400),
            ({"scope": "../", "decisions": []}, {}, 400),
        ]
        for payload, headers, expected in cases:
            with self.subTest(payload=payload, headers=headers):
                handler = self.request("POST", "/__save_decisions", payload, headers=headers)
                handler.save_payload = Mock(return_value=self.root / "mock.json")
                self.assertEqual(self.dispatch(handler), expected)
                handler.save_payload.assert_not_called()

    def test_authorized_save_apply_and_open_keep_working(self):
        handler = self.request("POST", "/__save_decisions", self.payload)
        self.assertEqual(self.dispatch(handler), 200)
        saved = Path(json.loads(handler.wfile.getvalue())["path"])
        self.assertEqual(json.loads(saved.read_text())["decisions"], self.payload["decisions"])
        handler = self.request("POST", "/__apply_decisions", self.payload)
        result = SimpleNamespace(returncode=0, stdout='{"results":[]}', stderr="")
        with patch.object(self.server_module.subprocess, "run", return_value=result) as run:
            self.assertEqual(self.dispatch(handler), 200)
            self.assertIn("--execute-decisions", run.call_args.args[0])
        source = self.root / "note $(not-a-command) 'quoted'.txt"
        source.write_text("synthetic", encoding="utf-8")
        handler = self.request("POST", "/__open", {"path": source.name})
        with patch.object(self.server_module.subprocess, "run", return_value=result) as run:
            self.assertEqual(self.dispatch(handler), 200)
            self.assertEqual(run.call_args.args[0], ["open", str(source)])

    def test_public_server_requires_separate_explicit_capabilities(self):
        for options, allowed in (
            ({}, set()),
            ({"allow_write": True}, {"/__save_decisions"}),
            ({"allow_apply": True}, {"/__save_decisions", "/__apply_decisions"}),
            ({"allow_file_open": True}, {"/__open"}),
        ):
            self.handler_type = self.server_module.configured_handler(
                self.root, SCRIPT, SERVER, **options
            )
            for endpoint in {"/__save_decisions", "/__apply_decisions", "/__open"} - allowed:
                with self.subTest(options=options, endpoint=endpoint):
                    handler = self.request("POST", endpoint, self.payload)
                    handler.save_payload = Mock()
                    with patch.object(self.server_module.subprocess, "run") as run:
                        self.assertEqual(self.dispatch(handler), 403)
                    handler.save_payload.assert_not_called()
                    run.assert_not_called()

    def test_open_rejects_workspace_escape(self):
        outside = self.root.parent / "outside.txt"
        outside.write_text("synthetic", encoding="utf-8")
        (self.root / "escape.txt").symlink_to(outside)
        for path in (str(outside), "../outside.txt", "escape.txt"):
            handler = self.request("POST", "/__open", {"path": path})
            with patch.object(self.server_module.subprocess, "run") as run:
                self.assertEqual(self.dispatch(handler), 400)
            run.assert_not_called()

    def test_open_is_limited_to_selected_scope_and_its_archive_mirror(self):
        scope = self.root / "group" / "chosen"
        archive = self.root / "Archived" / "group" / "chosen"
        sibling = self.root / "group" / "other" / "note.txt"
        other_archive = self.root / "Archived" / "group" / "other" / "note.txt"
        for parent in (scope, archive, sibling.parent, other_archive.parent):
            parent.mkdir(parents=True, exist_ok=True)
        own = scope / "note.txt"
        archived = archive / "note.txt"
        for path in (own, archived, sibling, other_archive):
            path.write_text("synthetic", encoding="utf-8")
        (scope / "escape.txt").symlink_to(sibling)
        (archive / "escape.txt").symlink_to(other_archive)
        self.handler_type = self.server_module.configured_handler(self.root, SCRIPT, SERVER, "group/chosen", allow_file_open=True)
        # A forged visible row must not grant access to a sibling outside this scope.
        (scope / self.workbench.name).write_text(self.render(scope="group/chosen", rows=[
            {"asset_id": "a", "source_paths": [str(sibling)]}
        ]), encoding="utf-8")
        result = SimpleNamespace(returncode=0, stdout="", stderr="")
        for path in (own, archived):
            handler = self.request("POST", "/__open", {"path": str(path.relative_to(self.root))})
            with patch.object(self.server_module.subprocess, "run", return_value=result) as run:
                self.assertEqual(self.dispatch(handler), 200)
                self.assertEqual(run.call_args.args[0], ["open", str(path)])
        for path in (sibling, other_archive, scope / "escape.txt", archive / "escape.txt", self.root):
            for name in (str(path), str(path.relative_to(self.root))):
                with self.subTest(path=name):
                    handler = self.request("POST", "/__open", {"path": name})
                    with patch.object(self.server_module.subprocess, "run", return_value=result) as run:
                        self.assertEqual(self.dispatch(handler), 400)
                    run.assert_not_called()

    def test_archive_symlink_cannot_expand_the_open_boundary(self):
        (self.root / "chosen").mkdir()
        (self.root / "Archived").mkdir()
        sibling = self.root / "sibling"
        sibling.mkdir()
        (sibling / "note.txt").write_text("synthetic", encoding="utf-8")
        (self.root / "Archived" / "chosen").symlink_to(sibling, target_is_directory=True)
        self.handler_type = self.server_module.configured_handler(self.root, SCRIPT, SERVER, "chosen", allow_file_open=True)
        handler = self.request("POST", "/__open", {"path": "Archived/chosen/note.txt"})
        with patch.object(self.server_module.subprocess, "run", return_value=SimpleNamespace(returncode=0)) as run:
            self.assertEqual(self.dispatch(handler), 400)
        run.assert_not_called()

    def test_legacy_or_symlinked_workbench_is_not_given_a_token(self):
        self.workbench.write_text("<html><head></head><body>legacy</body></html>", encoding="utf-8")
        handler = self.request("GET", "/cleanup-asset-review-workbench.html")
        self.assertEqual(self.dispatch(handler), 409)
        self.assertNotIn(self.handler_type.request_token.encode(), handler.wfile.getvalue())
        source = self.root / "source.html"
        source.write_text(self.html, encoding="utf-8")
        self.workbench.unlink()
        self.workbench.symlink_to(source)
        handler = self.request("GET", "/cleanup-asset-review-workbench.html")
        self.assertEqual(self.dispatch(handler), 404)

    def test_static_apply_command_keeps_shell_metacharacters_literal(self):
        unusual_root = self.root / "dir $(printf INJECTED) 'quoted'"
        unusual_root.mkdir()
        downloads = self.root / "Downloads"
        downloads.mkdir()
        decision_file = downloads / "asset-decisions $(printf INJECTED) 'quoted'.json"
        decision_file.write_text("{}", encoding="utf-8")
        scope = "scope $(printf INJECTED) 'quoted'"
        with patch.object(self.renderer.Path, "home", return_value=self.root):
            command = self.renderer.static_apply_command(unusual_root, scope, SCRIPT, SERVER)
        result = subprocess.run(
            ["/bin/sh", "-c", 'python3() { printf "%s\\0" "$@"; }; ' + command],
            text=True, capture_output=True, check=True, timeout=5,
        )
        self.assertEqual(result.stdout.split("\0")[:-1], [
            str(SERVER), "--root", str(unusual_root), "--scope", scope,
            "--cleanup-tool", str(SCRIPT), "--stage", "apply", "--decisions",
            str(decision_file), "--execute-decisions",
        ])

    def test_nonloopback_bind_is_rejected_before_server_creation(self):
        args = SimpleNamespace(root=self.root, scope=".", adapter=SCRIPT, pipeline=SERVER,
                               host="0.0.0.0", port=8766, open=False)
        with patch.object(self.server_module, "parse_args", return_value=args), patch.object(self.server_module, "ThreadingHTTPServer") as server:
            with self.assertRaises((ValueError, SystemExit)):
                self.server_module.main()
            server.assert_not_called()

    @unittest.skipUnless(shutil.which("node"), "Node.js is needed to exercise browser JavaScript")
    def test_frontend_sends_token_and_quotes_open_command_as_one_literal_argument(self):
        parser = ScriptCollector(); parser.feed(self.html)
        js = next(script["text"] for script in parser.scripts if not script["attrs"])
        harness = r'''
const vm = require('node:vm');
const input = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
const calls = [], handlers = {}, nodes = new Map();
function node(id) {
  if (!nodes.has(id)) nodes.set(id, {content:'test-token', value:'', textContent:'', innerHTML:'', addEventListener(){}, append(){}});
  return nodes.get(id);
}
node('asset-data').textContent = JSON.stringify({root:'/synthetic', assets:[], summary:{}, scope:'.'});
const context = vm.createContext({
  document: {getElementById:node, querySelector:()=>node('token'), addEventListener:(type, callback)=>handlers[type]=callback},
  location:{protocol:'http:'}, Option:function(){}, navigator:{}, window:{},
  fetch:async (path, options)=>{calls.push({path, options}); return {ok:true, text:async ()=>'{}', json:async ()=>({})};}
});
vm.runInContext(input.js, context);
(async()=>{
  await vm.runInContext("postJson('/__save_decisions')", context);
  await vm.runInContext("postJson('/__apply_decisions')", context);
  handlers.click({target:{closest:selector=>selector==='.open-file'?{dataset:{path:input.path}}:null}, preventDefault(){}});
  await new Promise(resolve=>setImmediate(resolve));
  const command = vm.runInContext('openCommand('+JSON.stringify(input.path)+')', context);
  process.stdout.write(JSON.stringify({calls, command}));
})();
'''
        path = "$(printf INJECTED) `printf INJECTED` 'quoted'\nname.txt"
        result = subprocess.run([shutil.which("node"), "-e", harness],
                                input=json.dumps({"js": js, "path": path}), text=True,
                                capture_output=True, check=True, timeout=10)
        output = json.loads(result.stdout)
        self.assertEqual(shlex.split(output["command"]), ["open", "/synthetic/" + path])
        literal = subprocess.run(
            ["/bin/sh", "-c", 'open() { printf "%s" "$1"; }; ' + output["command"]],
            text=True, capture_output=True, check=True, timeout=5,
        )
        self.assertEqual(literal.stdout, "/synthetic/" + path)
        self.assertEqual([call["path"] for call in output["calls"]],
                         ["/__save_decisions", "/__apply_decisions", "/__open"])
        for call in output["calls"]:
            self.assertEqual(call["options"]["method"], "POST")
            self.assertEqual(call["options"]["headers"]["X-Review-Token"], "test-token")
            self.assertEqual(call["options"]["headers"]["Content-Type"], "application/json")
        self.assertEqual(json.loads(output["calls"][-1]["options"]["body"]), {"path": path})


if __name__ == "__main__":
    unittest.main()
