"""Read-only documentation contract for opt-in MCP agent installation."""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REFERENCE = ROOT / "skills/api-to-typemcp/references/agent-mcp-installation.md"
CLIENTS = ("hermes", "claude-code", "codex", "cursor", "vscode-copilot", "gemini-cli", "opencode")


def section(text: str, name: str) -> str:
    begin = text.index(f"## {name}")
    end = text.find("\n## ", begin + 3)
    return text[begin:] if end < 0 else text[begin:end]


class AgentInstallDocsTests(unittest.TestCase):
    def test_client_reference_has_source_and_secret_boundary(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        for client in CLIENTS:
            with self.subTest(client=client):
                self.assertIn("Official reference:", section(text, client))
        self.assertIn("never reads `.env`", text)
        self.assertIn("Portable export does not modify", text)

    def test_reference_documents_verification_and_qualified_opencode_path(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        for client in ("cursor", "vscode-copilot", "gemini-cli", "opencode"):
            with self.subTest(client=client):
                self.assertIn("Verification:", section(text, client))
        self.assertIn("`opencode mcp add`", section(text, "opencode"))
        self.assertIn("Linux/XDG example", section(text, "opencode"))


if __name__ == "__main__":
    unittest.main()
