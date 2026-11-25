"""Security regression tests for contained generated-project verification."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import verify_generated  # noqa: E402


class GeneratedProjectVerificationSecurityTests(unittest.TestCase):
    def test_package_inspection_requires_a_lockfile(self) -> None:
        """Verification must fail before install when the dependency graph is unlocked."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            (project / "package.json").write_text(json.dumps({"name": "demo"}))

            result = verify_generated.inspect_package(project)

        self.assertFalse(result["ok"])
        self.assertIn("package-lock.json is required", result["violations"])

    def test_smoke_transports_do_not_clone_the_parent_environment(self) -> None:
        """Generated smoke clients must receive an explicit minimal environment only."""
        self.assertNotIn("...process.env", verify_generated._SMOKE_READ_MJS)
        self.assertNotIn("...process.env", verify_generated._SMOKE_WRITE_DENY_MJS)
        self.assertIn(
            "env: { TYPE_MCP_BASE_URL: process.env.TYPE_MCP_BASE_URL, PATH: process.env.PATH }",
            verify_generated._SMOKE_READ_MJS,
        )

    def test_template_uses_patched_dependency_ranges(self) -> None:
        """Generated projects must not carry the ranges flagged by the security audit."""
        package_template = (SKILL_DIR / "templates" / "typescript-stdio" / "package.json.tmpl").read_text()
        self.assertIn('"@modelcontextprotocol/sdk": "^1.30.0"', package_template)
        self.assertIn('"vitest": "^4.1.10"', package_template)
        self.assertNotIn('"@modelcontextprotocol/sdk": "^1.0.0"', package_template)
        self.assertNotIn('"vitest": "^3.0.0"', package_template)
        self.assertIn('"@theorvane/type-mcp": "0.3.2"', package_template)
        self.assertNotIn('"@theorvane/type-mcp": "0.2.0"', package_template)
        lockfile = json.loads(
            (SKILL_DIR / "templates" / "typescript-stdio" / "package-lock.json.tmpl").read_text()
        )
        type_mcp = lockfile["packages"]["node_modules/@theorvane/type-mcp"]
        self.assertEqual(type_mcp["version"], "0.3.2")
        self.assertEqual(
            type_mcp["resolved"],
            "https://registry.npmjs.org/@theorvane/type-mcp/-/type-mcp-0.3.2.tgz",
        )
        self.assertEqual(
            type_mcp["integrity"],
            "sha512-Rpspxnyl+UZeeakhng9PSCdsnVM4BTBkZ2XQsI5/ywoAU8OAKUMS+DQntY6aNCCgTtzwb3u0Wq7YVrSxfRwwWg==",
        )
        self.assertEqual(lockfile["packages"][""]["dependencies"]["@theorvane/type-mcp"], "0.3.2")
        self.assertEqual(type_mcp["dependencies"]["@modelcontextprotocol/sdk"], "1.30.0")

    def test_template_lockfile_resolves_patched_security_dependency_versions(self) -> None:
        """Generated projects must pin patched transitive resolutions."""
        lockfile = json.loads(
            (SKILL_DIR / "templates" / "typescript-stdio" / "package-lock.json.tmpl").read_text()
        )
        packages = lockfile["packages"]
        fast_uri = packages["node_modules/fast-uri"]
        self.assertEqual(fast_uri["version"], "3.1.5")
        self.assertEqual(
            fast_uri["resolved"],
            "https://registry.npmjs.org/fast-uri/-/fast-uri-3.1.5.tgz",
        )
        self.assertEqual(
            fast_uri["integrity"],
            "sha512-gHwA1O9LDIcKunMKhObS/HimwtehO1nPUECKAu5TpKgaO19fcWEl4bliWe1jWxVFvIXztJjjQ4L8XQ1EU9f7Jw==",
        )
        self.assertEqual(packages["node_modules/postcss"]["version"], "8.5.24")
        hono = packages["node_modules/hono"]
        self.assertEqual(hono["version"], "4.12.34")
        self.assertEqual(hono["resolved"], "https://registry.npmjs.org/hono/-/hono-4.12.34.tgz")
        self.assertEqual(
            hono["integrity"],
            "sha512-GqXJqY/xJkJmuloTrnV1ZEXG3fqte+VjkUqoRNZXcrUidiUOP4fMSIHHY4tsqZBK++kVyWmt/AAfSUuy57/eSA==",
        )


if __name__ == "__main__":
    unittest.main()
