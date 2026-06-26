#!/usr/bin/env python3
"""
API Mock Server - Core Implementation
"""
import json
import os
import sys
import time
import argparse
from typing import Dict, Any, Optional, Callable

from flask import Flask, request, jsonify, Response
from jsonschema import validate, ValidationError
from faker import Faker


class MockRequest:
    """Wrapper for incoming mock requests."""
    def __init__(self, flask_request, path_params=None):
        self._req = flask_request
        self.params = path_params or {}
        self.query = dict(flask_request.args)
        self.body = flask_request.get_json(silent=True) or {}
        self.headers = dict(flask_request.headers)
    
    def get(self, key, default=None):
        return self.body.get(key, default)


class MockServer:
    """Lightweight API mock server."""
    
    def __init__(self, port=3000, host="0.0.0.0", latency=0):
        self.port = port
        self.host = host
        self.latency = latency
        self.app = Flask(__name__)
        self._routes = {}
        self.fake = Faker()
    
    def _add_route(self, method, path, handler, validate_schema=None):
        """Internal route registration."""
        route_key = f"{method.upper()}:{path}"
        self._routes[route_key] = {
            "handler": handler,
            "validate": validate_schema,
            "path": path
        }
    
    def get(self, path, response, validate_schema=None):
        """Define a GET route."""
        handler = self._wrap_response(response)
        self._add_route("GET", path, handler, validate_schema)
    
    def post(self, path, response, validate_schema=None):
        """Define a POST route."""
        handler = self._wrap_response(response)
        self._add_route("POST", path, handler, validate_schema)
    
    def put(self, path, response, validate_schema=None):
        """Define a PUT route."""
        handler = self._wrap_response(response)
        self._add_route("PUT", path, handler, validate_schema)
    
    def delete(self, path, response, validate_schema=None):
        """Define a DELETE route."""
        handler = self._wrap_response(response)
        self._add_route("DELETE", path, handler, validate_schema)
    
    def patch(self, path, response, validate_schema=None):
        """Define a PATCH route."""
        handler = self._wrap_response(response)
        self._add_route("PATCH", path, handler, validate_schema)
    
    def _wrap_response(self, response):
        """Wrap static/dynamic responses into a callable."""
        if callable(response):
            return response
        return lambda req: response
    
    def _resolve_path(self, method, request_path):
        """Match request path against registered routes."""
        for route_key, route_data in self._routes.items():
            rmethod, rpath = route_key.split(":", 1)
            if rmethod != method.upper():
                continue
            # Convert {param} to regex
            pattern = r"^" + rpath.replace("{", "(?P<").replace("}", ">[^/]+)") + r"$"
            import re
            match = re.match(pattern, request_path)
            if match:
                return route_data, match.groupdict()
        return None, {}
    
    def start(self):
        """Start the Flask server."""
        @self.app.route("/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
        @self.app.route("/", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
        def catch_all(subpath=""):
            if self.latency:
                time.sleep(self.latency / 1000.0)
            
            request_path = "/" + subpath
            method = request.method
            route_data, params = self._resolve_path(method, request_path)
            
            if not route_data:
                return jsonify({"error": "Not found", "path": request_path, "method": method}), 404
            
            # Validate request body
            if route_data.get("validate") and request.get_json(silent=True):
                try:
                    validate(instance=request.get_json(silent=True), schema=route_data["validate"])
                except ValidationError as e:
                    return jsonify({"error": "Validation failed", "details": str(e)}), 400
            
            # Build mock request
            mock_req = MockRequest(request, path_params=params)
            
            # Call handler
            try:
                result = route_data["handler"](mock_req)
                if isinstance(result, (dict, list)):
                    return jsonify(result)
                elif isinstance(result, tuple) and len(result) == 2:
                    return jsonify(result[0]), result[1]
                return Response(str(result), mimetype="text/plain")
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        print(f"Mock server starting on http://{self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=False)
    
    @classmethod
    def from_config(cls, path: str):
        """Load server configuration from JSON file."""
        with open(path) as f:
            config = json.load(f)
        
        server = cls(
            port=config.get("port", 3000),
            host=config.get("host", "0.0.0.0"),
            latency=config.get("latency", 0)
        )
        
        for route in config.get("routes", []):
            method = route["method"].lower()
            path_str = route["path"]
            response = route["response"]
            schema = route.get("validate")
            
            if method == "get":
                server.get(path_str, response, schema)
            elif method == "post":
                server.post(path_str, response, schema)
            elif method == "put":
                server.put(path_str, response, schema)
            elif method == "delete":
                server.delete(path_str, response, schema)
            elif method == "patch":
                server.patch(path_str, response, schema)
        
        return server


def main():
    parser = argparse.ArgumentParser(description="API Mock Server")
    parser.add_argument("--config", help="Path to routes JSON config")
    parser.add_argument("--port", type=int, default=3000, help="Server port")
    parser.add_argument("--host", default="0.0.0.0", help="Server host")
    parser.add_argument("--latency", type=int, default=0, help="Artificial latency in ms")
    args = parser.parse_args()
    
    if args.config:
        server = MockServer.from_config(args.config)
    else:
        server = MockServer(port=args.port, host=args.host, latency=args.latency)
        # Default hello route
        server.get("/", {"message": "API Mock Server running"})
    
    server.start()


if __name__ == "__main__":
    main()
