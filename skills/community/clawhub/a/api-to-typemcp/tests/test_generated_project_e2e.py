"""Contained E2E tests for generated TypeMCP projects.

Generates a project from the Petstore fixture, installs it in a
scrubbed temp workspace, and runs typecheck/test/build/MCP smoke.
Requires Node 20+ and network access to npm (skipped in offline CI
via TYPEMCP_E2E_SKIP=1).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = REPO_ROOT / "skills" / "api-to-typemcp"
ENTRY = SKILL_DIR / "scripts" / "api_to_typemcp.py"
FIXTURES = SKILL_DIR / "tests" / "fixtures"
MOCK_UPSTREAM = FIXTURES / "mock_upstream.py"

sys.path.insert(0, str(SKILL_DIR / "scripts"))
sys.path.insert(0, str(FIXTURES))

SKIP_E2E = os.environ.get("TYPEMCP_E2E_SKIP", "") == "1"


def _node_available() -> bool:
    return shutil.which("node") is not None and shutil.which("npm") is not None


def run_cli(args: list[str], env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, str(ENTRY), *args],
        capture_output=True, text=True, env=env, timeout=30,
    )


def _generate_petstore_project(tmp: Path) -> Path:
    """Run the full manifest→approve→generate pipeline on the Petstore fixture."""
    state_dir = tmp / "state"
    state_dir.mkdir()
    env = {"TYPE_MCP_APPROVAL_STATE_DIR": str(state_dir)}

    result = run_cli(
        ["manifest", "--file", str(FIXTURES / "petstore.openapi.json"), "--json"],
        env_extra=env,
    )
    assert result.returncode == 0, f"manifest failed: {result.stderr}"
    digest = json.loads(result.stdout)["digest"]

    result = run_cli(
        ["approve", "--file", str(FIXTURES / "petstore.openapi.json"),
         "--manifest-digest", digest],
        env_extra=env,
    )
    assert result.returncode == 0, f"approve failed: {result.stderr}"

    out = tmp / "project"
    out.mkdir()
    result = run_cli(
        ["generate", "--file", str(FIXTURES / "petstore.openapi.json"),
         "--output", str(out), "--confirm-manifest-digest", digest],
        env_extra=env,
    )
    assert result.returncode == 0, f"generate failed: {result.stderr}"
    return out


@unittest.skipIf(SKIP_E2E, "TYPEMCP_E2E_SKIP=1")
@unittest.skipUnless(_node_available(), "Node.js/npm not available")
class GeneratedProjectE2ETests(unittest.TestCase):
    """Full contained E2E: install, typecheck, test, build, MCP smoke."""

    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory(prefix="typemcp-e2e-setup-")
        cls.tmp = Path(cls._tmp.name)
        cls.project = _generate_petstore_project(cls.tmp)

        # Start mock upstream (bounded port read — 10 s timeout).
        cls._upstream_proc = subprocess.Popen(
            [sys.executable, str(MOCK_UPSTREAM)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        import selectors
        sel = selectors.DefaultSelector()
        sel.register(cls._upstream_proc.stdout, selectors.EVENT_READ)
        ready = sel.select(timeout=10)
        sel.close()
        cls.assertTrue(ready, "Mock upstream did not print port within 10 s")
        port_line = cls._upstream_proc.stdout.readline().strip()
        cls.base_url = f"http://127.0.0.1:{port_line}"

    @classmethod
    def tearDownClass(cls) -> None:
        if hasattr(cls, "_upstream_proc"):
            cls._upstream_proc.terminate()
            cls._upstream_proc.wait(timeout=5)
        cls._tmp.cleanup()

    def _verify(self, **kwargs) -> dict:
        from verify_generated import verify_project
        return verify_project(self.project, base_url=self.base_url, **kwargs)

    # ------------------------------------------------------------------
    # Install + typecheck + test + build
    # ------------------------------------------------------------------

    def test_install_typecheck_test_build(self) -> None:
        """npm ci --ignore-scripts, tsc --noEmit, vitest run, npm run build."""
        results = self._verify(skip_mcp=True)

        for step in ("inspect", "install", "typecheck", "test", "build"):
            self.assertIn(step, results, f"Missing step: {step}")
            if isinstance(results[step], dict):
                self.assertTrue(
                    results[step].get("ok", False),
                    f"Step '{step}' failed: {json.dumps(results[step], indent=2)[:1000]}",
                )

    def test_install_resolves_published_typemcp(self) -> None:
        """The installed node_modules must contain the published @theorvane/type-mcp."""
        results = self._verify(skip_mcp=True)
        self.assertTrue(results["install"]["ok"], "install failed")
        installed_runtime = results["installed_runtime"]
        self.assertTrue(installed_runtime["ok"], installed_runtime)
        self.assertEqual(installed_runtime["version"], "0.3.2")
        self.assertEqual(
            installed_runtime["resolved"],
            "https://registry.npmjs.org/@theorvane/type-mcp/-/type-mcp-0.3.2.tgz",
        )
        self.assertEqual(
            installed_runtime["integrity"],
            "sha512-Rpspxnyl+UZeeakhng9PSCdsnVM4BTBkZ2XQsI5/ywoAU8OAKUMS+DQntY6aNCCgTtzwb3u0Wq7YVrSxfRwwWg==",
        )

    # ------------------------------------------------------------------
    # MCP stdio smoke: read tool
    # ------------------------------------------------------------------

    def test_mcp_stdio_read_tool(self) -> None:
        """List tools and call a read tool via the MCP stdio transport."""
        results = self._verify(skip_mcp=False)

        self.assertIn("mcp_read", results, "Missing mcp_read step")
        mcp = results["mcp_read"]
        self.assertTrue(mcp.get("ok", False),
                        f"MCP read smoke failed: {json.dumps(mcp, indent=2)[:1500]}")

        # Parse the smoke output to verify tools were listed.
        stdout = mcp.get("stdout_tail", "")
        # Find the last JSON line.
        json_lines = [l for l in stdout.strip().splitlines() if l.startswith("{")]
        self.assertTrue(json_lines, f"No JSON output from smoke: {stdout[:500]}")
        smoke_data = json.loads(json_lines[-1])
        self.assertIn("toolNames", smoke_data)
        self.assertGreater(len(smoke_data["toolNames"]), 0, "No tools listed")

    # ------------------------------------------------------------------
    # MCP stdio smoke: protected-write denied
    # ------------------------------------------------------------------

    def test_mcp_stdio_write_denied_without_allowlist(self) -> None:
        """Calling a protected-write tool without allowlist must fail safely."""
        results = self._verify(skip_mcp=False)

        self.assertIn("mcp_write_deny", results, "Missing mcp_write_deny step")
        mcp = results["mcp_write_deny"]
        # The smoke script itself should succeed (exit 0) but report isError=true.
        self.assertTrue(mcp.get("ok", False),
                        f"MCP write-deny smoke failed: {json.dumps(mcp, indent=2)[:1500]}")

        stdout = mcp.get("stdout_tail", "")
        json_lines = [l for l in stdout.strip().splitlines() if l.startswith("{")]
        self.assertTrue(json_lines, f"No JSON output: {stdout[:500]}")
        smoke_data = json.loads(json_lines[-1])

        if smoke_data.get("writeToolFound"):
            self.assertTrue(smoke_data.get("isError", False),
                            "Write tool succeeded without allowlist — policy bypass!")

        # Verify the denied POST never reached the mock upstream.
        import urllib.request
        with urllib.request.urlopen(f"{self.base_url}/_stats", timeout=5) as resp:
            stats = json.loads(resp.read())
        post_count = sum(v for k, v in stats.items() if k.startswith("POST"))
        self.assertEqual(post_count, 0,
                         f"Denied write operation reached upstream: {stats}")


@unittest.skipIf(SKIP_E2E, "TYPEMCP_E2E_SKIP=1")
@unittest.skipUnless(_node_available(), "Node.js/npm not available")
class MockUpstreamTests(unittest.TestCase):
    """Verify the mock upstream fixture itself works."""

    def test_mock_upstream_serves_pets(self) -> None:
        from mock_upstream import MockUpstream

        server = MockUpstream()
        server.start()
        try:
            import urllib.request
            with urllib.request.urlopen(f"{server.base_url}/pets", timeout=5) as resp:
                data = json.loads(resp.read())
            self.assertIsInstance(data, list)
            self.assertGreater(len(data), 0)
            self.assertEqual(data[0]["name"], "Buddy")

            # Verify counters.
            stats = server.stats()
            self.assertIn("GET /pets", stats)
            self.assertEqual(stats["GET /pets"], 1)
        finally:
            server.stop()

    def test_mock_upstream_counts_posts(self) -> None:
        from mock_upstream import MockUpstream

        server = MockUpstream()
        server.start()
        try:
            import urllib.request
            req = urllib.request.Request(
                f"{server.base_url}/pets",
                data=json.dumps({"name": "Rex"}).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read())
            self.assertEqual(data["status"], "created")
            self.assertEqual(server.stats().get("POST /pets"), 1)
        finally:
            server.stop()


if __name__ == "__main__":
    unittest.main()
