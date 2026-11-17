"""Consumer-level CLI regressions using only local HTTP fixtures and stdlib."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit


HELPER = Path(__file__).resolve().parents[1] / "scripts" / "mealie.py"
TOKEN = "fake-token-for-local-tests"
BINARY = b"\x00\xff\x80recipe\r\n\x00"
RECIPE = {
    "id": "recipe-fixture-id",
    "slug": "fixture-soup",
    "name": "Fixture soup",
    "recipeIngredient": [{"note": "1 cup water"}],
    "recipeInstructions": [{"text": "Warm the water."}],
}
OPENAPI = {
    "openapi": "3.1.0",
    "info": {"title": "Local regression fixture", "version": "1"},
    "paths": {
        "/api/items/{item_id}": {
            "put": {
                "operationId": "update_fixture_item",
                "parameters": [
                    {"name": "item_id", "in": "path", "required": True,
                     "schema": {"type": "string"}},
                    {"name": "tag", "in": "query", "schema": {"type": "string"}},
                ],
                "requestBody": {"content": {"application/json": {"schema": {"type": "object"}}}},
                "responses": {"200": {"description": "Updated"}},
            }
        },
        "/api/recipes/create/html-or-json": {
            "post": {
                "operationId": "create_recipe_from_html_or_json_api_recipes_create_html_or_json_post",
                "requestBody": {"required": True, "content": {"application/json": {
                    "schema": {"$ref": "#/components/schemas/ScrapeRecipeData"}
                }}},
                "responses": {"201": {"description": "Created", "content": {
                    "application/json": {"schema": {"type": "string"}}
                }}},
            }
        },
        "/api/recipes/{slug}": {
            "get": {
                "operationId": "get_recipe_fixture",
                "parameters": [{"name": "slug", "in": "path", "required": True,
                                "schema": {"type": "string"}}],
                "responses": {"200": {"description": "Recipe"}},
            }
        },
    },
    "components": {"schemas": {"ScrapeRecipeData": {
        "type": "object", "required": ["data"], "properties": {
            "data": {"type": "string"}, "url": {"type": "string"},
            "includeTags": {"type": "boolean", "default": False},
            "includeCategories": {"type": "boolean", "default": False},
        }
    }}},
}


class FixtureHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def respond(self, status, body, content_type="application/json", **headers):
        if content_type == "application/json":
            body = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        for name, value in headers.items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def dispatch(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self.server.requests.append({
            "method": self.command, "path": self.path,
            "headers": dict(self.headers.items()), "body": body,
        })
        path = urlsplit(self.path).path
        if path == "/openapi.json":
            self.respond(200, OPENAPI)
        elif path == "/api/error":
            self.respond(422, {"detail": "Fixture validation failure"})
        elif path == "/api/redirect":
            self.respond(302, {"detail": "Redirect fixture"},
                         Location=self.server.redirect_target)
        elif path == "/api/binary":
            self.respond(200, BINARY, "application/octet-stream")
        elif path == "/api/recipes/create/html-or-json" and self.command == "POST":
            self.respond(201, RECIPE["slug"])
        elif path == "/api/recipes/fixture-soup" and self.command == "GET":
            self.respond(200, RECIPE)
        elif path in ("/api/echo", "/api/upload") or path.startswith("/api/items/"):
            self.respond(200, {"ok": True})
        else:
            self.respond(404, {"detail": "Unknown fixture route"})

    do_GET = dispatch
    do_POST = dispatch
    do_PUT = dispatch


class MealieCLITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.servers = []
        cls.threads = []
        for _ in range(2):
            server = ThreadingHTTPServer(("127.0.0.1", 0), FixtureHandler)
            server.daemon_threads = True
            server.requests = []
            server.redirect_target = ""
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            cls.servers.append(server)
            cls.threads.append(thread)
        cls.server, cls.destination = cls.servers
        cls.url = "http://127.0.0.1:%d" % cls.server.server_port
        cls.destination_url = "http://127.0.0.1:%d" % cls.destination.server_port
        cls.server.redirect_target = cls.destination_url + "/api/echo"

    @classmethod
    def tearDownClass(cls):
        for server in cls.servers:
            server.shutdown()
            server.server_close()
        for thread in cls.threads:
            thread.join(timeout=5)

    def setUp(self):
        for server in self.servers:
            server.requests.clear()
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.directory = Path(self.tempdir.name)

    def cli(self, *args):
        environment = os.environ.copy()
        environment.update(MEALIE_URL=self.url, MEALIE_API_TOKEN=TOKEN)
        return subprocess.run(
            [sys.executable, str(HELPER), *args], env=environment,
            capture_output=True, timeout=15,
        )

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        return json.loads(result.stdout)

    def assert_error(self, result):
        self.assertNotEqual(result.returncode, 0)
        self.assertIsInstance(json.loads(result.stderr), dict)

    def matching_requests(self, method, path):
        return [request for request in self.server.requests
                if request["method"] == method and urlsplit(request["path"]).path == path]

    def test_json_body_and_repeated_query(self):
        payload = {"name": "Soupe à l’oignon", "servings": 2}
        result = self.cli("request", "POST", "/api/echo", "--json", json.dumps(payload),
                          "--query", "tag=one", "--query", "tag=two words",
                          "--header", "X-Fixture=custom")
        self.assert_success(result)
        requests = self.matching_requests("POST", "/api/echo")
        self.assertEqual(len(requests), 1)
        request = requests[0]
        self.assertEqual(json.loads(request["body"]), payload)
        self.assertEqual(parse_qs(urlsplit(request["path"]).query), {"tag": ["one", "two words"]})
        headers = {key.lower(): value for key, value in request["headers"].items()}
        self.assertEqual(headers["authorization"], "Bearer " + TOKEN)
        self.assertEqual(headers["x-fixture"], "custom")
        self.assertEqual(headers["content-type"].split(";")[0], "application/json")

    def test_multipart_repeated_files_and_fields(self):
        first = self.directory / "first.bin"
        second = self.directory / "second.bin"
        first.write_bytes(b"first\x00\xff")
        second.write_bytes(b"second\r\nfile")
        result = self.cli("request", "POST", "/api/upload",
                          "--field", "label=one", "--field", "label=two",
                          "--file", "images=" + str(first),
                          "--file", "images=" + str(second))
        self.assert_success(result)
        requests = self.matching_requests("POST", "/api/upload")
        self.assertEqual(len(requests), 1)
        request = requests[0]
        headers = {key.lower(): value for key, value in request["headers"].items()}
        message = BytesParser(policy=policy.default).parsebytes(
            ("Content-Type: " + headers["content-type"] + "\r\nMIME-Version: 1.0\r\n\r\n").encode()
            + request["body"]
        )
        self.assertTrue(message.is_multipart())
        parts = list(message.iter_parts())
        fields = [part.get_payload(decode=True) for part in parts
                  if part.get_param("name", header="content-disposition") == "label"]
        files = [(part.get_filename(), part.get_payload(decode=True)) for part in parts
                 if part.get_param("name", header="content-disposition") == "images"]
        self.assertEqual(fields, [b"one", b"two"])
        self.assertEqual(files, [(first.name, first.read_bytes()), (second.name, second.read_bytes())])

    def test_http_error_is_nonzero_and_not_retried(self):
        result = self.cli("request", "POST", "/api/error", "--json", "{}")
        self.assert_error(result)
        self.assertEqual(len(self.matching_requests("POST", "/api/error")), 1)

    def test_redirect_is_rejected_without_forwarding_authorization(self):
        result = self.cli("request", "GET", "/api/redirect")
        self.assert_error(result)
        self.assertEqual(len(self.matching_requests("GET", "/api/redirect")), 1)
        self.assertEqual(self.destination.requests, [])

    def test_absolute_and_network_path_escapes_are_rejected(self):
        for path in (self.destination_url + "/api/echo", "//127.0.0.1:%d/api/echo" % self.destination.server_port):
            with self.subTest(path=path):
                self.assert_error(self.cli("request", "GET", path))
        self.assertEqual(self.destination.requests, [])
        self.assertEqual(self.server.requests, [])

    def test_binary_output_preserves_exact_bytes(self):
        output = self.directory / "download.bin"
        result = self.cli("request", "GET", "/api/binary", "--output", str(output))
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        self.assertEqual(output.read_bytes(), BINARY)

    def test_call_discovers_operation_and_substitutes_path(self):
        result = self.cli("call", "update_fixture_item", "--path", "item_id=hello world",
                          "--query", "tag=a", "--query", "tag=b", "--json", '{"active":true}')
        self.assert_success(result)
        self.assertTrue(self.matching_requests("GET", "/openapi.json"))
        requests = self.matching_requests("PUT", "/api/items/hello%20world")
        self.assertEqual(len(requests), 1)
        self.assertEqual(parse_qs(urlsplit(requests[0]["path"]).query), {"tag": ["a", "b"]})
        self.assertEqual(json.loads(requests[0]["body"]), {"active": True})

    def test_json_string_response_remains_valid_json(self):
        result = self.cli("request", "POST", "/api/recipes/create/html-or-json",
                          "--json", '{"data":"fixture"}')
        self.assertEqual(self.assert_success(result), RECIPE["slug"])

    def test_import_recipe_posts_schema_org_and_verifies_with_get(self):
        source = {
            "@context": "https://schema.org", "@type": "Recipe", "name": "Fixture soup",
            "recipeIngredient": ["1 cup water"],
            "recipeInstructions": [{"@type": "HowToStep", "text": "Warm the water."}],
        }
        recipe_file = self.directory / "recipe.json"
        recipe_file.write_text(json.dumps(source), encoding="utf-8")
        result = self.cli("import-recipe", str(recipe_file), "--source-url", "https://example.test/soup",
                          "--include-tags", "--include-categories")
        output = self.assert_success(result)
        posts = self.matching_requests("POST", "/api/recipes/create/html-or-json")
        gets = self.matching_requests("GET", "/api/recipes/fixture-soup")
        self.assertEqual(len(posts), 1)
        self.assertEqual(len(gets), 1)
        self.assertLess(self.server.requests.index(posts[0]), self.server.requests.index(gets[0]))
        payload = json.loads(posts[0]["body"])
        self.assertEqual(json.loads(payload["data"]), source)
        self.assertEqual(payload["url"], "https://example.test/soup")
        self.assertIs(payload["includeTags"], True)
        self.assertIs(payload["includeCategories"], True)
        self.assertEqual(output["slug"], RECIPE["slug"])
        self.assertEqual(output["recipe"], RECIPE)


if __name__ == "__main__":
    unittest.main()
