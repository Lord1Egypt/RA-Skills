"""Black-box tests for the bundled local structured-spec entry point."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ENTRYPOINT = SKILL_DIR / "scripts" / "api_to_typemcp.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run_engine(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ENTRYPOINT), *args],
        text=True,
        capture_output=True,
        check=False,
    )


class EngineCliTests(unittest.TestCase):
    def test_inspect_accepts_explicit_local_openapi_file(self) -> None:
        result = run_engine("inspect", "--file", str(FIXTURES / "petstore.openapi.json"), "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["source"]["kind"], "openapi")
        self.assertEqual(payload["operationCount"], 2)
        self.assertNotIn(str(FIXTURES), result.stdout)
        self.assertNotIn("fixture-secret-query", result.stdout)

    def test_inspect_discovers_only_supplied_swagger_ui_config(self) -> None:
        """Swagger UI inspect returns a reference but never fetches its spec."""
        result = run_engine("inspect", "--file", str(FIXTURES / "swagger-ui.html"), "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload, {
            "source": {"kind": "swagger-ui-config", "descriptor": "local-swagger-ui"},
            "spec_url": "/v3/openapi.json",
        })
        self.assertNotIn(str(FIXTURES), result.stdout)

    def test_agent_install_cli_requires_preview_then_separate_approval(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); project = root / "project"; (project / "dist").mkdir(parents=True)
            (project / "dist/index.js").write_text("// built", encoding="utf-8")
            home = root / "home"; (home / ".cursor").mkdir(parents=True)
            config = home / ".cursor/mcp.json"; config.write_text('{"mcpServers":{}}\n', encoding="utf-8")
            state = root / "state"; env = {**os.environ, "TYPE_MCP_APPROVAL_STATE_DIR": str(state)}
            common = ["--project", str(project), "--home", str(home), "--targets", "cursor", "--server-name", "petstore-mcp"]
            preview = subprocess.run([sys.executable, str(ENTRYPOINT), "install-plan", *common], text=True, capture_output=True, env=env, check=False)
            self.assertEqual(preview.returncode, 0, preview.stderr)
            plan = json.loads(preview.stdout); self.assertEqual(plan["status"], "review-required")
            self.assertEqual(config.read_text(), '{"mcpServers":{}}\n')
            rejected = subprocess.run([sys.executable, str(ENTRYPOINT), "install-apply", *common, "--confirm-plan-digest", plan["plan_digest"]], text=True, capture_output=True, env=env, check=False)
            self.assertEqual(rejected.returncode, 2)
            approved = subprocess.run([sys.executable, str(ENTRYPOINT), "install-approve", "--plan-digest", plan["plan_digest"]], text=True, capture_output=True, env=env, check=False)
            self.assertEqual(approved.returncode, 0, approved.stderr)
            applied = subprocess.run([sys.executable, str(ENTRYPOINT), "install-apply", *common, "--confirm-plan-digest", plan["plan_digest"]], text=True, capture_output=True, env=env, check=False)
            self.assertEqual(applied.returncode, 0, applied.stderr)
            applied_payload = json.loads(applied.stdout)
            self.assertEqual(applied_payload["targets"][0]["client_id"], "cursor")
            self.assertIn("petstore-mcp", json.loads(config.read_text())["mcpServers"])

    def test_swagger_ui_cli_rejects_oversized_file_before_reading(self) -> None:
        """Bounded CLI discovery must stat-limit HTML before reading it."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "swagger-ui.html"
            path.write_bytes(b"x" * (2 * 1024 * 1024 + 1))
            result = run_engine("inspect", "--file", str(path), "--json")

        self.assertEqual(result.returncode, 2)
        self.assertIn("Swagger UI input exceeds", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_failed_output_validation_does_not_consume_receipt(self) -> None:
        """A local output-target error must leave the approved receipt usable."""
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "state"
            missing_output = Path(directory) / "missing-output"
            valid_output = Path(directory) / "valid-output"
            valid_output.mkdir()
            env = os.environ.copy()
            env["TYPE_MCP_APPROVAL_STATE_DIR"] = str(state)
            fixture = FIXTURES / "petstore.openapi.json"
            manifest = run_engine("manifest", "--file", str(fixture), "--json")
            digest = json.loads(manifest.stdout)["digest"]
            approved = subprocess.run(
                [sys.executable, str(ENTRYPOINT), "approve", "--file", str(fixture), "--manifest-digest", digest],
                text=True, capture_output=True, env=env, check=False,
            )
            self.assertEqual(approved.returncode, 0, approved.stderr)
            failed = subprocess.run(
                [sys.executable, str(ENTRYPOINT), "generate", "--file", str(fixture),
                 "--confirm-manifest-digest", digest, "--output", str(missing_output)],
                text=True, capture_output=True, env=env, check=False,
            )
            self.assertEqual(failed.returncode, 2)
            self.assertIn("output directory does not exist", failed.stderr)
            generated = subprocess.run(
                [sys.executable, str(ENTRYPOINT), "generate", "--file", str(fixture),
                 "--confirm-manifest-digest", digest, "--output", str(valid_output)],
                text=True, capture_output=True, env=env, check=False,
            )
            self.assertEqual(generated.returncode, 0, generated.stderr)

    def test_rejects_malformed_and_unsupported_local_documents_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            malformed = Path(directory) / "bad.json"
            malformed.write_text("{not json", encoding="utf-8")
            unsupported = Path(directory) / "unsupported.json"
            unsupported.write_text('{"openapi":"3.1.0","paths":{}}', encoding="utf-8")
            malformed_base_url = Path(directory) / "malformed-base-url.json"
            malformed_base_url.write_text(
                '{"openapi":"3.0.0","servers":[{"url":"https://api.example.test:bad"}],"paths":{}}',
                encoding="utf-8",
            )
            mixed_yaml_keys = Path(directory) / "mixed-keys.yaml"
            mixed_yaml_keys.write_text(
                "openapi: '3.0.0'\nservers:\n  - url: https://api.example.test\npaths:\n  /pets: {}\n  1: {}\n",
                encoding="utf-8",
            )

            for path in (malformed, unsupported, malformed_base_url, mixed_yaml_keys):
                result = run_engine("inspect", "--file", str(path), "--json")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_yaml_alias_fanout_is_bounded_without_traceback(self) -> None:
        aliases = ["a: &a ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']"]
        previous = "a"
        for index in range(1, 8):
            name = f"a{index}"
            aliases.append(f"{name}: &{name} [{', '.join(f'*{previous}' for _ in range(10))}]")
            previous = name
        document = "openapi: '3.0.0'\nservers:\n  - url: https://api.example.test\npaths:\n  /pets: {}\n" + "\n".join(aliases)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "aliases.yaml"
            path.write_text(document, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ENTRYPOINT), "inspect", "--file", str(path), "--json"],
                text=True,
                capture_output=True,
                check=False,
                timeout=2,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_yaml_requires_the_bundled_python_dependency_without_traceback(self) -> None:
        result = subprocess.run(
            [sys.executable, "-S", str(ENTRYPOINT), "inspect", "--file", str(FIXTURES / "petstore.swagger.yaml"), "--json"],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("YAML support requires PyYAML", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
