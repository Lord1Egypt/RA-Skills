"""Integration regressions for document-derived manifest safety (Task 6)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "skills" / "api-to-typemcp"
SCRIPTS = SKILL / "scripts"
FIXTURES = SKILL / "tests" / "fixtures"
ENTRY = SCRIPTS / "api_to_typemcp.py"
sys.path.insert(0, str(SCRIPTS))


class DocumentIntakeTests(unittest.TestCase):
    def _manifest(self, file: Path, base_url: str = "https://api.example.test") -> dict:
        result = subprocess.run(
            [sys.executable, str(ENTRY), "manifest", "--file", str(file),
             "--base-url", base_url, "--json"],
            capture_output=True, text=True, timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_document_manifest_preserves_confidence_and_safe_evidence(self) -> None:
        manifest = self._manifest(FIXTURES / "api-reference.md")
        self.assertEqual(manifest["source"]["descriptor"], "local-markdown-document")
        for op in manifest["operations"]:
            self.assertEqual(op["confidence"], "explicit")
            self.assertEqual(op["evidence"]["snippet"], f"{op['method']} {op['path']}")

    def test_absolute_url_is_normalized_against_explicit_base_url(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "reference.md"
            source.write_text("GET https://api.example.test/v1/pets\n")
            manifest = self._manifest(source)
        self.assertEqual(manifest["baseUrl"], "https://api.example.test")
        self.assertEqual(manifest["operations"][0]["path"], "/v1/pets")

    def test_absolute_url_with_default_port_is_same_origin(self) -> None:
        """https://host and https://host:443 are the same normalized origin."""
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "reference.md"
            source.write_text("GET https://api.example.test:443/pets\n")
            manifest = self._manifest(source, "https://api.example.test")
        self.assertEqual(manifest["operations"][0]["path"], "/pets")

    def test_absolute_url_with_different_origin_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "reference.md"
            source.write_text("GET https://other.example.test/pets\n")
            result = subprocess.run(
                [sys.executable, str(ENTRY), "manifest", "--file", str(source),
                 "--base-url", "https://api.example.test", "--json"],
                capture_output=True, text=True, timeout=20,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error:", result.stderr)

    def test_structured_spec_cannot_supply_custom_evidence(self) -> None:
        spec = {
            "openapi": "3.0.3",
            "info": {"title": "test", "version": "1"},
            "servers": [{"url": "https://api.example.test"}],
            "paths": {"/pets": {"get": {
                "operationId": "listPets", "responses": {"200": {"description": "ok"}},
                "x-api-to-typemcp-evidence": {
                    "line": 1, "snippet": "Authorization: Bearer LEAKED_SECRET_123",
                    "confidence": "explicit",
                },
            }}},
        }
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "spec.json"
            source.write_text(json.dumps(spec))
            manifest = self._manifest(source)
        evidence = manifest["operations"][0]["evidence"]
        self.assertEqual(evidence, {"source": "structured-spec"})
        self.assertNotIn("LEAKED_SECRET_123", json.dumps(manifest))

    def test_generated_artifact_contains_no_document_prose_secrets(self) -> None:
        """The rendered manifest must only contain normalized evidence fields."""
        from render import render_project

        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "reference.md"
            source.write_text("GET /pets Authorization: Bearer LEAKED_SECRET_123\n")
            manifest = self._manifest(source)
            out = Path(tmp) / "output"
            out.mkdir()
            render_project(manifest, out)
            artifact = (out / "api-to-typemcp.manifest.json").read_text()
        self.assertNotIn("LEAKED_SECRET_123", artifact)
        self.assertIn("GET /pets", artifact)


if __name__ == "__main__":
    unittest.main()
