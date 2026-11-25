"""Native configuration codec preservation/fail-closed tests."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills/api-to-typemcp/scripts"))
from agent_clients import McpServerSpec  # noqa: E402
from config_codecs import UnsupportedConfigFormat, render_codex_toml, patch_jsonc  # noqa: E402


class CodecTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = McpServerSpec("petstore-mcp", "node", ("/safe/dist/index.js",), Path("/safe"))
    def test_codex_toml_appends_missing_server_without_removing_profiles(self) -> None:
        source = "model = 'x'\n\n[profiles.safe]\nmodel = 'safe'\n"
        rendered = render_codex_toml(source, self.spec)
        self.assertIn("[profiles.safe]", rendered)
        self.assertIn("[mcp_servers.petstore_mcp]", rendered)
        self.assertIn('command = "node"', rendered)
    def test_codex_toml_rejects_existing_target_table(self) -> None:
        source = "[mcp_servers.petstore_mcp]\ncommand = 'old'\n"
        with self.assertRaises(UnsupportedConfigFormat): render_codex_toml(source, self.spec)
    def test_codex_toml_ignores_target_header_in_comment(self) -> None:
        rendered = render_codex_toml("# [mcp_servers.petstore_mcp]\nmodel = 'x'\n", self.spec)
        self.assertIn("[mcp_servers.petstore_mcp]", rendered)

    def test_jsonc_is_manual_export_only_without_preserving_codec(self) -> None:
        with self.assertRaises(UnsupportedConfigFormat):
            patch_jsonc('{\n // user comment\n "mcpServers": {}\n}', self.spec)
if __name__ == "__main__": unittest.main()
