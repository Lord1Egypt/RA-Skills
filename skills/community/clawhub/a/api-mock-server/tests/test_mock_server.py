"""
Unit tests for api-mock-server
"""
import os
import sys
import json
import unittest
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from mock_server import MockServer, MockRequest


class MockFlaskRequest:
    """Mock Flask request for testing."""
    def __init__(self, method="GET", path="/", json_data=None, args=None, headers=None):
        self.method = method
        self.path = path
        self._json = json_data or {}
        self.args = args or {}
        self.headers = headers or {}
    
    def get_json(self, silent=True):
        return self._json


class TestMockServer(unittest.TestCase):
    
    def test_add_static_route(self):
        server = MockServer(port=3005)
        server.get("/test", {"message": "hello"})
        self.assertIn("GET:/test", server._routes)
    
    def test_add_dynamic_route(self):
        server = MockServer(port=3006)
        handler = lambda req: {"id": req.params["id"]}
        server.get("/items/{id}", handler)
        self.assertIn("GET:/items/{id}", server._routes)
    
    def test_resolve_static_path(self):
        server = MockServer(port=3007)
        server.get("/health", {"status": "ok"})
        route, params = server._resolve_path("GET", "/health")
        self.assertIsNotNone(route)
        self.assertEqual(params, {})
    
    def test_resolve_dynamic_path(self):
        server = MockServer(port=3008)
        server.get("/users/{id}", {"data": "user"})
        route, params = server._resolve_path("GET", "/users/42")
        self.assertIsNotNone(route)
        self.assertEqual(params, {"id": "42"})
    
    def test_resolve_not_found(self):
        server = MockServer(port=3009)
        route, params = server._resolve_path("GET", "/missing")
        self.assertIsNone(route)
    
    def test_handler_returns_dict(self):
        server = MockServer(port=3010)
        handler = lambda req: {"result": "success"}
        server.post("/submit", handler)
        
        mock_req = MockRequest(MockFlaskRequest(method="POST", json_data={"key": "val"}))
        route, _ = server._resolve_path("POST", "/submit")
        result = route["handler"](mock_req)
        self.assertEqual(result, {"result": "success"})
    
    def test_from_config(self):
        config = {
            "port": 3011,
            "routes": [
                {
                    "method": "GET",
                    "path": "/config-test",
                    "response": {"test": True}
                }
            ]
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            path = f.name
        
        server = MockServer.from_config(path)
        self.assertIn("GET:/config-test", server._routes)
        os.remove(path)
    
    def test_wrap_response_static(self):
        server = MockServer(port=3012)
        wrapped = server._wrap_response({"static": True})
        result = wrapped(None)
        self.assertEqual(result, {"static": True})
    
    def test_wrap_response_callable(self):
        server = MockServer(port=3013)
        fn = lambda req: {"dynamic": True}
        wrapped = server._wrap_response(fn)
        self.assertEqual(wrapped, fn)


if __name__ == "__main__":
    unittest.main()
