import importlib.util
import io
import json
import pathlib
import sys
import unittest
from unittest import mock


SCRIPT_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "managed_agents.py"
spec = importlib.util.spec_from_file_location("managed_agents", SCRIPT_PATH)
managed_agents = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = managed_agents
spec.loader.exec_module(managed_agents)


class ToolsetBuilderTests(unittest.TestCase):
    def test_build_agent_toolset_with_default_and_overrides(self):
        args = mock.Mock(
            agent_toolset=True,
            enable_tool=["read", "write"],
            disable_tool=["web_fetch"],
            tool_policy=["bash=ask", "write=allow"],
            default_tool_enabled=False,
            default_tool_policy="ask",
        )
        payload = managed_agents._build_agent_toolset(args)
        self.assertEqual(payload["type"], "agent_toolset_20260401")
        self.assertEqual(payload["default_config"]["enabled"], False)
        self.assertEqual(payload["default_config"]["permission_policy"]["type"], "always_ask")
        configs = {item["name"]: item for item in payload["configs"]}
        self.assertEqual(configs["read"]["enabled"], True)
        self.assertEqual(configs["web_fetch"]["enabled"], False)
        self.assertEqual(configs["bash"]["permission_policy"]["type"], "always_ask")
        self.assertEqual(configs["write"]["permission_policy"]["type"], "always_allow")

    def test_build_agent_toolset_returns_none_when_unused(self):
        args = mock.Mock(
            agent_toolset=False,
            enable_tool=[],
            disable_tool=[],
            tool_policy=[],
            default_tool_enabled=None,
            default_tool_policy=None,
        )
        self.assertIsNone(managed_agents._build_agent_toolset(args))


class EnvironmentConfigTests(unittest.TestCase):
    def test_build_environment_config_accepts_bare_hosts(self):
        args = mock.Mock(
            config_json=None,
            network="limited",
            allowed_host=["api.example.com"],
            allow_mcp_servers=True,
            allow_package_managers=False,
            apt=[], cargo=[], gem=[], go=[], npm=[], pip=["pandas==2.2.0"],
        )
        config = managed_agents._build_environment_config(args)
        self.assertEqual(config["type"], "cloud")
        self.assertEqual(config["networking"]["type"], "limited")
        self.assertEqual(config["networking"]["allowed_hosts"], ["api.example.com"])
        self.assertTrue(config["networking"]["allow_mcp_servers"])
        self.assertEqual(config["packages"]["pip"], ["pandas==2.2.0"])

    def test_build_environment_config_rejects_urls(self):
        args = mock.Mock(
            config_json=None,
            network="limited",
            allowed_host=["https://api.example.com"],
            allow_mcp_servers=False,
            allow_package_managers=False,
            apt=[], cargo=[], gem=[], go=[], npm=[], pip=[],
        )
        with self.assertRaises(managed_agents.CliError):
            managed_agents._build_environment_config(args)


class EventBuilderTests(unittest.TestCase):
    def test_build_send_events_supports_interrupt_message_confirm_and_custom_result(self):
        args = mock.Mock(
            event_json=[],
            interrupt=True,
            message="Pivot to the auth bug.",
            confirm_tool_use_id="tool_evt_1",
            confirm_result="deny",
            deny_message="Do not edit files yet.",
            custom_tool_use_id="custom_evt_1",
            custom_tool_text="{\"ok\": false}",
            custom_tool_is_error=True,
        )
        events = managed_agents._build_send_events(args)
        self.assertEqual(events[0]["type"], "user.interrupt")
        self.assertEqual(events[1]["type"], "user.message")
        self.assertEqual(events[2]["type"], "user.tool_confirmation")
        self.assertEqual(events[2]["result"], "deny")
        self.assertEqual(events[2]["deny_message"], "Do not edit files yet.")
        self.assertEqual(events[3]["type"], "user.custom_tool_result")
        self.assertTrue(events[3]["is_error"])


class StreamSummaryTests(unittest.TestCase):
    def test_summarize_stream_event_formats_message_and_tool_use(self):
        msg = managed_agents._summarize_stream_event(
            {"type": "agent.message", "content": [{"type": "text", "text": "hello"}]}
        )
        self.assertEqual(msg, "hello")
        tool_use = managed_agents._summarize_stream_event(
            {"type": "agent.tool_use", "name": "bash", "evaluated_permission": "ask"}
        )
        self.assertIn("agent tool: bash", tool_use)


class FileUploadBuilderTests(unittest.TestCase):
    def test_build_file_upload_request_uses_filename_and_detected_mime(self):
        with mock.patch.object(managed_agents.Path, "read_bytes", return_value=b"alpha"), \
             mock.patch.object(managed_agents.Path, "exists", return_value=True), \
             mock.patch.object(managed_agents.Path, "is_file", return_value=True):
            body, content_type = managed_agents._build_file_upload_request(
                "/tmp/data.csv",
                filename="renamed.csv",
            )

        self.assertIn("multipart/form-data; boundary=", content_type)
        self.assertIn(b'filename="renamed.csv"', body)
        self.assertIn(b"Content-Type: text/csv", body)
        self.assertIn(b"alpha", body)

    def test_build_file_upload_request_rejects_missing_file(self):
        with mock.patch.object(managed_agents.Path, "exists", return_value=False):
            with self.assertRaises(managed_agents.CliError):
                managed_agents._build_file_upload_request("/tmp/missing.txt")


class ResourceBuilderTests(unittest.TestCase):
    def test_build_resource_payload_supports_file_resource(self):
        args = mock.Mock(resource_json=None, type="file", file_id="file_123", mount_path="/workspace/data.csv")
        payload = managed_agents._build_resource_payload(args)
        self.assertEqual(payload["type"], "file")
        self.assertEqual(payload["file_id"], "file_123")
        self.assertEqual(payload["mount_path"], "/workspace/data.csv")

    def test_build_resource_payload_rejects_missing_file_id(self):
        args = mock.Mock(resource_json=None, type="file", file_id=None, mount_path=None)
        with self.assertRaises(managed_agents.CliError):
            managed_agents._build_resource_payload(args)


class DoctorTests(unittest.TestCase):
    def test_doctor_validates_allowed_host_and_notes(self):
        args = mock.Mock(
            backend="http",
            api_key_env="ANTHROPIC_API_KEY",
            timeout=30.0,
            live=False,
            allowed_host=["api.example.com"],
        )
        with mock.patch.dict(managed_agents.os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), \
             mock.patch.object(managed_agents, "Anthropic", None):
            report = managed_agents._doctor_checks(args)

        self.assertTrue(report["ok"])
        self.assertEqual(report["resolved_backend"], "http")
        checks = {item["name"]: item for item in report["checks"]}
        self.assertTrue(checks["allowed_host_validation"]["ok"])
        self.assertIn("bare hostnames", " ".join(report["notes"]))

    def test_doctor_auto_backend_resolves_to_http_without_sdk(self):
        args = mock.Mock(
            backend="auto",
            api_key_env="ANTHROPIC_API_KEY",
            timeout=30.0,
            live=False,
            allowed_host=[],
        )
        with mock.patch.dict(managed_agents.os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), \
             mock.patch.object(managed_agents, "Anthropic", None):
            report = managed_agents._doctor_checks(args)

        self.assertTrue(report["ok"])
        self.assertEqual(report["resolved_backend"], "http")
        checks = {item["name"]: item for item in report["checks"]}
        self.assertTrue(checks["http_fallback_ready"]["ok"])

    def test_doctor_live_uses_read_only_list_calls(self):
        args = mock.Mock(
            backend="http",
            api_key_env="ANTHROPIC_API_KEY",
            timeout=30.0,
            live=True,
            allowed_host=[],
        )
        fake_client = mock.Mock()
        fake_client.list_environments.return_value = {"data": []}
        fake_client.list_sessions.return_value = {"data": []}
        fake_client.list_files.return_value = {"data": []}
        with mock.patch.dict(managed_agents.os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), \
             mock.patch.object(managed_agents, "Anthropic", None), \
             mock.patch.object(managed_agents, "ManagedAgentsClient", return_value=fake_client):
            report = managed_agents._doctor_checks(args)

        self.assertTrue(report["ok"])
        fake_client.list_environments.assert_called_once_with({"limit": 1})
        fake_client.list_sessions.assert_called_once_with({"limit": 1})
        fake_client.list_files.assert_called_once_with({"limit": 1})

    def test_doctor_missing_api_key_still_reports_resolved_backend_and_live_failures(self):
        args = mock.Mock(
            backend="http",
            api_key_env="ANTHROPIC_API_KEY",
            timeout=30.0,
            live=True,
            allowed_host=[],
        )
        with mock.patch.dict(managed_agents.os.environ, {}, clear=True), \
             mock.patch.object(managed_agents, "Anthropic", None):
            report = managed_agents._doctor_checks(args)

        self.assertFalse(report["ok"])
        self.assertEqual(report["resolved_backend"], "http")
        checks = {item["name"]: item for item in report["checks"]}
        self.assertFalse(checks["api_key_present"]["ok"])
        self.assertFalse(checks["live_environment_list"]["ok"])
        self.assertFalse(checks["live_session_list"]["ok"])
        self.assertFalse(checks["live_file_list"]["ok"])


class HttpClientTests(unittest.TestCase):
    def test_request_sends_beta_headers_and_json_payload(self):
        response = mock.MagicMock()
        response.read.return_value = b'{"ok": true}'
        response.__enter__.return_value = response
        response.__exit__.return_value = False

        with mock.patch.dict(managed_agents.os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), \
             mock.patch.object(managed_agents, "Anthropic", None), \
             mock.patch.object(managed_agents.urllib.request, "urlopen", return_value=response) as urlopen:
            client = managed_agents.ManagedAgentsClient(backend="http")
            payload = client._request("POST", "/v1/agents", payload={"name": "x"})

        self.assertTrue(payload["ok"])
        request_obj = urlopen.call_args.args[0]
        self.assertEqual(request_obj.headers["Anthropic-beta"], managed_agents.MANAGED_AGENTS_BETA)
        self.assertEqual(request_obj.headers["Anthropic-version"], managed_agents.ANTHROPIC_VERSION)
        self.assertEqual(request_obj.headers["X-api-key"], "test-key")
        self.assertEqual(json.loads(request_obj.data.decode("utf-8")), {"name": "x"})

    def test_upload_file_uses_files_beta_and_multipart(self):
        response = mock.MagicMock()
        response.read.return_value = b'{"id": "file_123"}'
        response.__enter__.return_value = response
        response.__exit__.return_value = False

        with mock.patch.dict(managed_agents.os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), \
             mock.patch.object(managed_agents, "Anthropic", None), \
             mock.patch.object(managed_agents, "_build_file_upload_request", return_value=(b"BODY", "multipart/form-data; boundary=x")), \
             mock.patch.object(managed_agents.urllib.request, "urlopen", return_value=response) as urlopen:
            client = managed_agents.ManagedAgentsClient(backend="http")
            payload = client.upload_file("/tmp/input.csv")

        self.assertEqual(payload["id"], "file_123")
        request_obj = urlopen.call_args.args[0]
        self.assertEqual(request_obj.headers["Anthropic-beta"], managed_agents.FILES_API_BETA)
        self.assertEqual(request_obj.headers["Content-type"], "multipart/form-data; boundary=x")
        self.assertEqual(request_obj.data, b"BODY")

    def test_list_files_uses_managed_agents_beta(self):
        response = mock.MagicMock()
        response.read.return_value = b'{"data": []}'
        response.__enter__.return_value = response
        response.__exit__.return_value = False

        with mock.patch.dict(managed_agents.os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), \
             mock.patch.object(managed_agents, "Anthropic", None), \
             mock.patch.object(managed_agents.urllib.request, "urlopen", return_value=response) as urlopen:
            client = managed_agents.ManagedAgentsClient(backend="http")
            payload = client.list_files({"scope_id": "sesn_123"})

        self.assertEqual(payload["data"], [])
        request_obj = urlopen.call_args.args[0]
        self.assertEqual(request_obj.headers["Anthropic-beta"], managed_agents.MANAGED_AGENTS_BETA)
        self.assertIn("scope_id=sesn_123", request_obj.full_url)

    def test_download_file_writes_bytes_from_content_endpoint(self):
        response = mock.MagicMock()
        response.read.return_value = b"hello"
        response.__enter__.return_value = response
        response.__exit__.return_value = False

        with mock.patch.dict(managed_agents.os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), \
             mock.patch.object(managed_agents, "Anthropic", None), \
             mock.patch.object(managed_agents.urllib.request, "urlopen", return_value=response) as urlopen:
            client = managed_agents.ManagedAgentsClient(backend="http")
            payload = client.download_file("file_123")

        self.assertEqual(payload, b"hello")
        request_obj = urlopen.call_args.args[0]
        self.assertTrue(request_obj.full_url.endswith("/v1/files/file_123/content"))
        self.assertEqual(request_obj.headers["Anthropic-beta"], managed_agents.MANAGED_AGENTS_BETA)

    def test_add_session_resource_posts_to_resource_endpoint(self):
        response = mock.MagicMock()
        response.read.return_value = b'{"id": "sesrsc_123"}'
        response.__enter__.return_value = response
        response.__exit__.return_value = False

        with mock.patch.dict(managed_agents.os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), \
             mock.patch.object(managed_agents, "Anthropic", None), \
             mock.patch.object(managed_agents.urllib.request, "urlopen", return_value=response) as urlopen:
            client = managed_agents.ManagedAgentsClient(backend="http")
            payload = client.add_session_resource("sess_123", {"type": "file", "file_id": "file_123"})

        self.assertEqual(payload["id"], "sesrsc_123")
        request_obj = urlopen.call_args.args[0]
        self.assertTrue(request_obj.full_url.endswith("/v1/sessions/sess_123/resources"))
        self.assertEqual(json.loads(request_obj.data.decode("utf-8")), {"type": "file", "file_id": "file_123"})

    def test_delete_agent_uses_delete_endpoint(self):
        response = mock.MagicMock()
        response.read.return_value = b'{"id": "agent_123", "type": "agent_deleted"}'
        response.__enter__.return_value = response
        response.__exit__.return_value = False

        with mock.patch.dict(managed_agents.os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), \
             mock.patch.object(managed_agents, "Anthropic", None), \
             mock.patch.object(managed_agents.urllib.request, "urlopen", return_value=response) as urlopen:
            client = managed_agents.ManagedAgentsClient(backend="http")
            payload = client.delete_agent("agent_123")

        self.assertEqual(payload["type"], "agent_deleted")
        request_obj = urlopen.call_args.args[0]
        self.assertTrue(request_obj.full_url.endswith("/v1/agents/agent_123"))
        self.assertEqual(request_obj.get_method(), "DELETE")

    def test_stream_events_parses_sse_data_frames(self):
        raw = io.BytesIO(b'data: {"id":"1","type":"agent.message","content":[{"type":"text","text":"hi"}]}\n\n')
        raw.__enter__ = lambda self=raw: self
        raw.__exit__ = lambda exc_type, exc, tb, self=raw: False

        with mock.patch.dict(managed_agents.os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=True), \
             mock.patch.object(managed_agents, "Anthropic", None), \
             mock.patch.object(managed_agents.urllib.request, "urlopen", return_value=raw):
            client = managed_agents.ManagedAgentsClient(backend="http")
            events = list(client.stream_events("sess_123"))

        self.assertEqual(events[0]["id"], "1")
        self.assertEqual(events[0]["type"], "agent.message")


if __name__ == "__main__":
    unittest.main()
