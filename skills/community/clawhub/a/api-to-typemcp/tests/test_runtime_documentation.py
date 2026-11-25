"""Focused contract tests for the bundled TypeMCP runtime documentation."""

from __future__ import annotations

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TYPE_MCP_CURRENT_RELEASE = "@theorvane/type-mcp@0.3.2"
TYPE_MCP_RELEASE_SHA = "e75bcf6a81ef4df57301b6154a0088845020886f"
STANDARD_DECORATOR_IMPORT = 'import { McpServer, McpTool } from "@theorvane/type-mcp"'
LEGACY_DECORATOR_IMPORT = 'import { McpServer, McpTool } from "@theorvane/type-mcp/legacy"'


class RuntimeDocumentationContractTests(unittest.TestCase):
    """Keep public standard and legacy decorator guidance unambiguous."""

    def test_docs_describe_current_release_and_distinct_decorator_entrypoints(self) -> None:
        """Both bundled docs name the public compatibility contract precisely."""
        for relative_path in ("SKILL.md", "references/type-mcp-runtime.md"):
            with self.subTest(path=relative_path):
                content = (SKILL_ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(TYPE_MCP_CURRENT_RELEASE, content)
                self.assertIn(STANDARD_DECORATOR_IMPORT, content)
                self.assertIn(LEGACY_DECORATOR_IMPORT, content)
                self.assertIn("ESM/NodeNext", content)
                self.assertIn("CommonJS/Node16", content)
                self.assertIn("experimentalDecorators", content)
                self.assertIn("distinct entrypoints", content)
                self.assertIn("published", content)
                self.assertIn(TYPE_MCP_RELEASE_SHA, content)
                self.assertNotIn("future upgrade", content)

    def test_generator_remains_standard_esm_without_legacy_decorator_changes(self) -> None:
        """Compatibility docs must not redirect generated output to legacy CJS."""
        package_template = (SKILL_ROOT / "templates/typescript-stdio/package.json.tmpl").read_text(encoding="utf-8")
        server_renderer = (SKILL_ROOT / "scripts/render.py").read_text(encoding="utf-8")
        tsconfig_template = (SKILL_ROOT / "templates/typescript-stdio/tsconfig.json.tmpl").read_text(encoding="utf-8")
        self.assertIn('"type": "module"', package_template)
        self.assertIn(STANDARD_DECORATOR_IMPORT, server_renderer)
        self.assertNotIn("@theorvane/type-mcp/legacy", server_renderer)
        self.assertNotIn("experimentalDecorators", tsconfig_template)


if __name__ == "__main__":
    unittest.main()
