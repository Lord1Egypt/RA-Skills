"""Static analysis of generated TypeScript projects.

Validates generated code structure without running npm/node:
- package.json has no file:/git:/link: dependencies
- server.ts uses only published TypeMCP APIs
- index.ts calls createMcpServer + startStdioServer
- policy.ts rejects wildcards before request construction
- .env.example has variable names only (no values)
- All generated files are valid UTF-8
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = REPO_ROOT / "skills" / "api-to-typemcp"
ENTRY = SKILL_DIR / "scripts" / "api_to_typemcp.py"
FIXTURES = SKILL_DIR / "tests" / "fixtures"


def run_cli(args: list[str], env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, str(ENTRY), *args],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )


class GeneratedProjectStaticTests(unittest.TestCase):
    """Static checks on a generated project from the Petstore fixture."""

    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory()
        cls.tmp = Path(cls._tmp.name)
        cls.state_dir = cls.tmp / "state"
        cls.state_dir.mkdir()
        cls.env = {"TYPE_MCP_APPROVAL_STATE_DIR": str(cls.state_dir)}

        # Generate the project.
        result = run_cli(
            ["manifest", "--file", str(FIXTURES / "petstore.openapi.json"), "--json"],
            env_extra=cls.env,
        )
        digest = json.loads(result.stdout)["digest"]

        run_cli(
            ["approve", "--file", str(FIXTURES / "petstore.openapi.json"),
             "--manifest-digest", digest],
            env_extra=cls.env,
        )

        cls.out = cls.tmp / "project"
        cls.out.mkdir()
        run_cli(
            ["generate", "--file", str(FIXTURES / "petstore.openapi.json"),
             "--output", str(cls.out), "--confirm-manifest-digest", digest],
            env_extra=cls.env,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    # ------------------------------------------------------------------
    # package.json: no local/git dependencies
    # ------------------------------------------------------------------

    def test_no_local_or_git_dependencies(self) -> None:
        pkg = json.loads((self.out / "package.json").read_text())
        for section in ("dependencies", "devDependencies"):
            for name, version in pkg.get(section, {}).items():
                self.assertNotIn("file:", version, f"{section}.{name}")
                self.assertNotIn("git:", version, f"{section}.{name}")
                self.assertFalse(version.startswith("link:"), f"{section}.{name}")

    # ------------------------------------------------------------------
    # server.ts: only published TypeMCP APIs
    # ------------------------------------------------------------------

    def test_server_uses_only_published_apis(self) -> None:
        server = (self.out / "src" / "server.ts").read_text()
        # Must import from the npm package.
        self.assertIn('from "@theorvane/type-mcp"', server)
        # Must not import from local paths or relative TypeMCP source.
        self.assertNotIn("from \"../type-mcp", server)
        self.assertNotIn("from \"./type-mcp", server)
        # Must use decorators.
        self.assertIn("@McpServer", server)
        self.assertIn("@McpTool", server)

    # ------------------------------------------------------------------
    # index.ts: createMcpServer + startStdioServer
    # ------------------------------------------------------------------

    def test_index_starts_stdio(self) -> None:
        index = (self.out / "src" / "index.ts").read_text()
        self.assertIn("createMcpServer", index)
        self.assertIn("startStdioServer", index)
        # Must not use HTTP transport in the default stdio template.
        self.assertNotIn("startHttpServer", index)

    # ------------------------------------------------------------------
    # policy.ts: wildcard rejection, fails before request
    # ------------------------------------------------------------------

    def test_policy_rejects_wildcards(self) -> None:
        policy = (self.out / "src" / "policy.ts").read_text()
        self.assertIn('"*"', policy)
        self.assertIn("authorizeOperation", policy)

    def test_policy_called_before_client_in_server(self) -> None:
        """In server.ts, authorizeOperation must appear before this.client.request."""
        server = (self.out / "src" / "server.ts").read_text()
        # Find first occurrence of each in each tool method.
        auth_pos = server.find("authorizeOperation")
        request_pos = server.find("this.client.request")
        self.assertGreater(auth_pos, -1, "authorizeOperation not found in server.ts")
        self.assertGreater(request_pos, -1, "this.client.request not found in server.ts")
        self.assertLess(auth_pos, request_pos,
                        "authorizeOperation must appear before this.client.request")

    # ------------------------------------------------------------------
    # .env.example: names only, no values
    # ------------------------------------------------------------------

    def test_env_example_names_only(self) -> None:
        env = (self.out / ".env.example").read_text()
        for line in env.strip().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            self.assertNotIn("=", line, f"Value found in .env.example: {line}")

    # ------------------------------------------------------------------
    # All files valid UTF-8
    # ------------------------------------------------------------------

    def test_all_files_valid_utf8(self) -> None:
        for path in sorted(self.out.rglob("*")):
            if path.is_file():
                try:
                    path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    self.fail(f"Not valid UTF-8: {path.relative_to(self.out)}")

    # ------------------------------------------------------------------
    # operations.ts: all operations present
    # ------------------------------------------------------------------

    def test_operations_ts_has_all_operations(self) -> None:
        ops = (self.out / "src" / "operations.ts").read_text()
        # Petstore has createPet and getPet.
        self.assertIn("createPet", ops)
        self.assertIn("getPet", ops)

    # ------------------------------------------------------------------
    # schemas.ts: Zod schemas for all operations
    # ------------------------------------------------------------------

    def test_schemas_ts_has_zod_objects(self) -> None:
        schemas = (self.out / "src" / "schemas.ts").read_text()
        self.assertIn("z.object", schemas)
        self.assertIn("createPetInput", schemas)
        self.assertIn("getPetInput", schemas)

    # ------------------------------------------------------------------
    # Manifest copy: no secret/path leakage
    # ------------------------------------------------------------------

    def test_manifest_copy_no_secrets(self) -> None:
        manifest_text = (self.out / "api-to-typemcp.manifest.json").read_text()
        manifest = json.loads(manifest_text)
        # No local paths.
        self.assertNotIn(str(FIXTURES), manifest_text)
        self.assertNotIn("petstore.openapi.json", manifest_text)
        # Source descriptor is constant.
        self.assertEqual(manifest["source"]["descriptor"], "local-structured-spec")


if __name__ == "__main__":
    unittest.main()
