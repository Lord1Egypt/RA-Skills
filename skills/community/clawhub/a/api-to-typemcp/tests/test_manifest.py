"""Manifest contract tests exercise the script by absolute path, not package imports."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ENTRYPOINT = SKILL_DIR / "scripts" / "api_to_typemcp.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def manifest_for(name: str) -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, str(ENTRYPOINT), "manifest", "--file", str(FIXTURES / name), "--json"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


def canonical_without_digest(manifest: dict[str, object]) -> bytes:
    value = dict(manifest)
    value.pop("digest", None)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


class ManifestTests(unittest.TestCase):
    def test_openapi_manifest_is_normalized_deterministic_and_secret_free(self) -> None:
        first = manifest_for("petstore.openapi.json")
        second = manifest_for("petstore.openapi.json")

        self.assertEqual(first, second)
        self.assertEqual(first["schema"], "api-to-typemcp.manifest")
        self.assertEqual(first["version"], 1)
        self.assertEqual(first["protocol"], "http")
        self.assertEqual(first["source"]["kind"], "openapi")
        self.assertEqual(first["source"]["descriptor"], "local-structured-spec")
        self.assertEqual(first["baseUrl"], "https://api.example.test/v1")
        self.assertEqual(
            first["digest"],
            "sha256:" + hashlib.sha256(canonical_without_digest(first)).hexdigest(),
        )

        operations = {operation["operationId"]: operation for operation in first["operations"]}
        self.assertEqual(set(operations), {"getPet", "createPet"})
        self.assertEqual(operations["getPet"]["method"], "GET")
        self.assertEqual(operations["getPet"]["path"], "/pets/{petId}")
        self.assertEqual(operations["getPet"]["policy"], "read")
        self.assertEqual(operations["getPet"]["parameters"][0]["name"], "petId")
        self.assertEqual(operations["createPet"]["method"], "POST")
        self.assertEqual(operations["createPet"]["policy"], "protected-write")
        self.assertTrue(operations["createPet"]["requestBody"]["required"])
        self.assertEqual(operations["createPet"]["responses"][0]["status"], "201")

        rendered = json.dumps(first, sort_keys=True)
        self.assertNotIn("fixture-secret-query", rendered)
        self.assertNotIn(str(FIXTURES), rendered)
        self.assertNotIn("?api_key=", rendered)

    def test_swagger_yaml_normalizes_to_the_same_operation_contract(self) -> None:
        manifest = manifest_for("petstore.swagger.yaml")

        self.assertEqual(manifest["source"]["kind"], "swagger")
        self.assertEqual(manifest["baseUrl"], "https://api.example.test/v1")
        operations = {operation["operationId"]: operation for operation in manifest["operations"]}
        self.assertEqual(operations["getPet"]["policy"], "read")
        self.assertEqual(operations["createPet"]["policy"], "protected-write")
        self.assertEqual(operations["createPet"]["requestBody"]["contentType"], "application/json")

    def test_manifest_rejects_secret_bearing_or_unsafe_operation_values(self) -> None:
        unsafe = {
            "openapi": "3.0.0",
            "servers": [{"url": "https://api.example.test"}],
            "paths": {
                "/pets?token=source-secret": {
                    "get": {
                        "operationId": "getPet",
                        "responses": {"200": {"description": "response-secret"}},
                    }
                }
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unsafe.json"
            path.write_text(json.dumps(unsafe), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ENTRYPOINT), "manifest", "--file", str(path), "--json"],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("source-secret", result.stderr)
        self.assertNotIn("response-secret", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_descriptor_is_secret_free(self) -> None:
        document = {
            "openapi": "3.0.0",
            "servers": [{"url": "https://api.example.test"}],
            "paths": {"/pets": {"get": {"operationId": "getPets", "responses": {"200": {"description": "ok"}}}}},
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "spec?api_key=descriptor-secret.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ENTRYPOINT), "manifest", "--file", str(path), "--json"],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("descriptor-secret", result.stdout)
        self.assertEqual(json.loads(result.stdout)["source"]["descriptor"], "local-structured-spec")

    def test_required_must_be_boolean(self) -> None:
        document = {
            "openapi": "3.0.0",
            "servers": [{"url": "https://api.example.test"}],
            "paths": {
                "/pets": {
                    "get": {
                        "operationId": "getPets",
                        "parameters": [{"name": "limit", "in": "query", "required": "false", "schema": {"type": "integer"}}],
                        "responses": {"200": {"description": "ok"}},
                    }
                }
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unsafe.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ENTRYPOINT), "manifest", "--file", str(path), "--json"],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)

    def test_response_summary_is_generated_without_copying_untrusted_prose(self) -> None:
        manifest = manifest_for("petstore.openapi.json")
        operations = {operation["operationId"]: operation for operation in manifest["operations"]}
        response = operations["getPet"]["responses"][0]

        self.assertEqual(response, {"status": "200", "summary": "HTTP 200 response"})

    def test_authentication_scheme_names_are_normalized_without_secrets(self) -> None:
        document = {
            "openapi": "3.0.0",
            "servers": [{"url": "https://api.example.test"}],
            "paths": {"/pets": {"get": {"operationId": "getPets", "responses": {"200": {"description": "ok"}}}}},
            "components": {
                "securitySchemes": {
                    "apiAuth": {"type": "apiKey", "in": "header", "name": "X-Api-Key"},
                    "bearerAuth": {"type": "http", "scheme": "bearer"},
                }
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "auth.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ENTRYPOINT), "manifest", "--file", str(path), "--json"],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads(result.stdout)
        auth = manifest["authentication"]
        self.assertEqual(len(auth), 2)
        by_name = {entry["name"]: entry for entry in auth}
        self.assertEqual(by_name["apiAuth"]["type"], "apiKey")
        self.assertEqual(by_name["apiAuth"]["in"], "header")
        self.assertEqual(by_name["apiAuth"]["parameterName"], "X-Api-Key")
        self.assertEqual(by_name["bearerAuth"]["type"], "http")
        self.assertEqual(by_name["bearerAuth"]["scheme"], "bearer")
        rendered = json.dumps(manifest, sort_keys=True)
        self.assertNotIn("secret", rendered.lower())

    def test_unsupported_auth_scheme_type_is_rejected(self) -> None:
        document = {
            "openapi": "3.0.0",
            "servers": [{"url": "https://api.example.test"}],
            "paths": {"/pets": {"get": {"operationId": "getPets", "responses": {"200": {"description": "ok"}}}}},
            "components": {"securitySchemes": {"custom": {"type": "mutualTLS"}}},
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad-auth.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ENTRYPOINT), "manifest", "--file", str(path), "--json"],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)

    def test_unsupported_http_method_is_rejected_not_silently_omitted(self) -> None:
        document = {
            "openapi": "3.0.0",
            "servers": [{"url": "https://api.example.test"}],
            "paths": {
                "/pets": {
                    "get": {"operationId": "getPets", "responses": {"200": {"description": "ok"}}},
                    "trace": {"operationId": "tracePets", "responses": {"200": {"description": "ok"}}},
                }
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trace.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ENTRYPOINT), "manifest", "--file", str(path), "--json"],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("TRACE", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_unbound_path_template_variable_is_rejected(self) -> None:
        document = {
            "openapi": "3.0.0",
            "servers": [{"url": "https://api.example.test"}],
            "paths": {
                "/pets/{id}": {
                    "get": {"operationId": "getPet", "responses": {"200": {"description": "ok"}}},
                }
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unbound.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ENTRYPOINT), "manifest", "--file", str(path), "--json"],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)

    def test_lone_surrogate_in_json_is_rejected_without_traceback(self) -> None:
        raw = '{"openapi":"3.0.0","servers":[{"url":"https://api.example.test"}],"paths":{"/pets":{"get":{"operationId":"getPets","responses":{"200":{"description":"\\ud800ok"}}}}}}'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "surrogate.json"
            path.write_text(raw, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ENTRYPOINT), "manifest", "--file", str(path), "--json"],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_json_keys_are_rejected(self) -> None:
        raw = '{"openapi":"3.0.0","servers":[{"url":"https://api.example.test"}],"paths":{"/pets":{"get":{"operationId":"getPets","responses":{"200":{"description":"ok"}}},"get":{"operationId":"getPets2","responses":{"200":{"description":"ok"}}}}}}'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dup-keys.json"
            path.write_text(raw, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ENTRYPOINT), "manifest", "--file", str(path), "--json"],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("duplicate", result.stderr.lower())
        self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_yaml_keys_are_rejected(self) -> None:
        raw = "openapi: '3.0.0'\nservers:\n  - url: https://api.example.test\npaths:\n  /pets:\n    get:\n      operationId: getPets\n      responses:\n        '200':\n          description: ok\n    get:\n      operationId: getPets2\n      responses:\n        '200':\n          description: ok\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dup-keys.yaml"
            path.write_text(raw, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ENTRYPOINT), "manifest", "--file", str(path), "--json"],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("duplicate", result.stderr.lower())
        self.assertNotIn("Traceback", result.stderr)

    def test_manifest_includes_authentication_field_even_when_empty(self) -> None:
        manifest = manifest_for("petstore.openapi.json")
        self.assertIn("authentication", manifest)
        self.assertEqual(manifest["authentication"], [])


if __name__ == "__main__":
    unittest.main()
