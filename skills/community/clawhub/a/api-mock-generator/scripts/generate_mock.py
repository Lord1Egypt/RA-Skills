#!/usr/bin/env python3
"""API Mock Generator — generate mock API servers from OpenAPI/Swagger specs.

Parses OpenAPI 3.x or Swagger 2.0 specs and generates a standalone Python mock
server with realistic fake data. Pure Python stdlib (http.server).
"""

import argparse
import json
import os
import random
import re
import string
import sys
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Optional
from urllib.parse import urlparse, parse_qs


# --- Fake Data Generation ---

FIRST_NAMES = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Iris", "Jack"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson", "Moore"]
DOMAINS = ["example.com", "test.org", "demo.io", "sample.net", "mock.dev"]
WORDS = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "sed", "do",
         "eiusmod", "tempor", "incididunt", "labore", "dolore", "magna", "aliqua"]
CITIES = ["New York", "London", "Tokyo", "Paris", "Berlin", "Sydney", "Toronto", "Mumbai", "Seoul", "Amsterdam"]
COUNTRIES = ["US", "UK", "JP", "FR", "DE", "AU", "CA", "IN", "KR", "NL"]


def fake_string(prop_name: str = "", min_len: int = 5, max_len: int = 20) -> str:
    """Generate a contextual fake string based on property name."""
    name_lower = prop_name.lower()

    if "email" in name_lower:
        return f"{random.choice(FIRST_NAMES).lower()}.{random.choice(LAST_NAMES).lower()}@{random.choice(DOMAINS)}"
    if "name" in name_lower and "first" in name_lower:
        return random.choice(FIRST_NAMES)
    if "name" in name_lower and "last" in name_lower:
        return random.choice(LAST_NAMES)
    if "name" in name_lower:
        return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    if "phone" in name_lower or "tel" in name_lower:
        return f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
    if "url" in name_lower or "website" in name_lower or "link" in name_lower:
        return f"https://{random.choice(DOMAINS)}/{fake_slug()}"
    if "city" in name_lower:
        return random.choice(CITIES)
    if "country" in name_lower:
        return random.choice(COUNTRIES)
    if "address" in name_lower:
        return f"{random.randint(1,9999)} {random.choice(LAST_NAMES)} St"
    if "zip" in name_lower or "postal" in name_lower:
        return f"{random.randint(10000,99999)}"
    if "id" in name_lower or "uuid" in name_lower:
        return fake_uuid()
    if "title" in name_lower or "subject" in name_lower:
        return " ".join(random.choices(WORDS, k=random.randint(3, 6))).capitalize()
    if "description" in name_lower or "bio" in name_lower or "summary" in name_lower:
        return " ".join(random.choices(WORDS, k=random.randint(8, 15))).capitalize() + "."
    if "token" in name_lower or "key" in name_lower or "secret" in name_lower:
        return "".join(random.choices(string.ascii_letters + string.digits, k=32))
    if "password" in name_lower:
        return "".join(random.choices(string.ascii_letters + string.digits + "!@#$", k=16))
    if "image" in name_lower or "avatar" in name_lower or "photo" in name_lower:
        return f"https://picsum.photos/seed/{random.randint(1,1000)}/200/200"
    if "color" in name_lower:
        return f"#{random.randint(0, 0xFFFFFF):06x}"
    if "status" in name_lower:
        return random.choice(["active", "inactive", "pending", "completed"])
    if "tag" in name_lower or "category" in name_lower:
        return random.choice(["tech", "science", "art", "business", "health"])

    return " ".join(random.choices(WORDS, k=random.randint(2, 5)))


def fake_slug() -> str:
    return "-".join(random.choices(WORDS, k=random.randint(2, 3)))


def fake_uuid() -> str:
    parts = [
        "".join(random.choices("0123456789abcdef", k=8)),
        "".join(random.choices("0123456789abcdef", k=4)),
        "4" + "".join(random.choices("0123456789abcdef", k=3)),
        random.choice("89ab") + "".join(random.choices("0123456789abcdef", k=3)),
        "".join(random.choices("0123456789abcdef", k=12)),
    ]
    return "-".join(parts)


def fake_integer(prop_name: str = "", minimum: int = 0, maximum: int = 10000) -> int:
    name_lower = prop_name.lower()
    if "age" in name_lower:
        return random.randint(18, 80)
    if "year" in name_lower:
        return random.randint(1990, 2026)
    if "port" in name_lower:
        return random.randint(1024, 65535)
    if "count" in name_lower or "quantity" in name_lower:
        return random.randint(0, 100)
    if "price" in name_lower or "amount" in name_lower or "cost" in name_lower:
        return random.randint(1, 999)
    return random.randint(minimum, maximum)


def fake_number(prop_name: str = "") -> float:
    name_lower = prop_name.lower()
    if "price" in name_lower or "amount" in name_lower or "cost" in name_lower:
        return round(random.uniform(0.99, 999.99), 2)
    if "lat" in name_lower:
        return round(random.uniform(-90, 90), 6)
    if "lon" in name_lower or "lng" in name_lower:
        return round(random.uniform(-180, 180), 6)
    if "rate" in name_lower or "score" in name_lower:
        return round(random.uniform(0, 5), 1)
    return round(random.uniform(0, 1000), 2)


def fake_date() -> str:
    days = random.randint(-365, 365)
    dt = datetime.now() + timedelta(days=days)
    return dt.strftime("%Y-%m-%d")


def fake_datetime() -> str:
    days = random.randint(-365, 365)
    dt = datetime.now() + timedelta(days=days, hours=random.randint(0, 23), minutes=random.randint(0, 59))
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


# --- Schema → Data Generator ---

def generate_from_schema(schema: dict, prop_name: str = "", definitions: dict = None, depth: int = 0) -> Any:
    """Generate fake data from an OpenAPI schema object."""
    if depth > 10:
        return None

    if definitions is None:
        definitions = {}

    # Handle $ref
    ref = schema.get("$ref")
    if ref:
        ref_name = ref.split("/")[-1]
        if ref_name in definitions:
            return generate_from_schema(definitions[ref_name], prop_name, definitions, depth + 1)
        return {}

    # Handle enum
    if "enum" in schema:
        return random.choice(schema["enum"])

    # Handle example
    if "example" in schema:
        return schema["example"]

    # Handle default
    if "default" in schema:
        return schema["default"]

    # Handle oneOf/anyOf
    for key in ("oneOf", "anyOf"):
        if key in schema:
            return generate_from_schema(random.choice(schema[key]), prop_name, definitions, depth + 1)

    # Handle allOf (merge)
    if "allOf" in schema:
        merged = {}
        for sub in schema["allOf"]:
            val = generate_from_schema(sub, prop_name, definitions, depth + 1)
            if isinstance(val, dict):
                merged.update(val)
        return merged

    schema_type = schema.get("type", "string")

    if schema_type == "object":
        obj = {}
        for name, prop_schema in schema.get("properties", {}).items():
            obj[name] = generate_from_schema(prop_schema, name, definitions, depth + 1)
        return obj

    if schema_type == "array":
        items_schema = schema.get("items", {"type": "string"})
        count = random.randint(1, min(3, schema.get("maxItems", 3)))
        return [generate_from_schema(items_schema, prop_name, definitions, depth + 1) for _ in range(count)]

    if schema_type == "string":
        fmt = schema.get("format", "")
        if fmt == "date":
            return fake_date()
        if fmt in ("date-time", "datetime"):
            return fake_datetime()
        if fmt == "email":
            return fake_string("email")
        if fmt == "uri" or fmt == "url":
            return fake_string("url")
        if fmt == "uuid":
            return fake_uuid()
        if fmt == "ipv4":
            return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        min_l = schema.get("minLength", 5)
        max_l = schema.get("maxLength", 20)
        return fake_string(prop_name, min_l, max_l)

    if schema_type == "integer":
        return fake_integer(prop_name, schema.get("minimum", 0), schema.get("maximum", 10000))

    if schema_type == "number":
        return fake_number(prop_name)

    if schema_type == "boolean":
        return random.choice([True, False])

    return None


# --- OpenAPI Parser ---

def load_spec(path: str) -> dict:
    """Load an OpenAPI/Swagger spec from JSON or YAML file."""
    with open(path, "r") as f:
        content = f.read()

    # Try JSON first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Try YAML (basic parsing without PyYAML)
    # For full YAML support, suggest installing PyYAML
    try:
        import yaml
        return yaml.safe_load(content)
    except ImportError:
        print("Warning: YAML spec detected but PyYAML not installed. Use JSON format or: pip install pyyaml", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error parsing spec: {e}", file=sys.stderr)
        sys.exit(2)


def extract_routes(spec: dict) -> list:
    """Extract routes from OpenAPI spec."""
    routes = []

    # Determine spec version
    is_v3 = spec.get("openapi", "").startswith("3.")
    definitions_key = "components" if is_v3 else "definitions"
    definitions = spec.get(definitions_key, {})
    if is_v3:
        definitions = definitions.get("schemas", {})

    paths = spec.get("paths", {})
    for path, methods in paths.items():
        for method, operation in methods.items():
            if method.lower() in ("get", "post", "put", "patch", "delete", "head", "options"):
                # Get response schema
                responses = operation.get("responses", {})

                # Find success response (200, 201, or first 2xx)
                response_schema = None
                status_code = 200

                for code in ["200", "201", "202", "204"]:
                    if code in responses:
                        status_code = int(code)
                        resp = responses[code]
                        if is_v3:
                            content = resp.get("content", {})
                            json_content = content.get("application/json", {})
                            response_schema = json_content.get("schema")
                        else:
                            response_schema = resp.get("schema")
                        break

                if not response_schema and responses:
                    # Take first 2xx response
                    for code, resp in responses.items():
                        if str(code).startswith("2"):
                            status_code = int(code)
                            if is_v3:
                                content = resp.get("content", {})
                                json_content = content.get("application/json", {})
                                response_schema = json_content.get("schema")
                            else:
                                response_schema = resp.get("schema")
                            break

                # Convert path params from {id} to regex
                regex_path = re.sub(r'\{(\w+)\}', r'(?P<\1>[^/]+)', path)

                routes.append({
                    "path": path,
                    "regex": f"^{regex_path}$",
                    "method": method.upper(),
                    "operation_id": operation.get("operationId", ""),
                    "summary": operation.get("summary", ""),
                    "status_code": status_code,
                    "response_schema": response_schema,
                    "definitions": definitions,
                })

    return routes


# --- Mock Server ---

class MockHandler(BaseHTTPRequestHandler):
    """HTTP handler that serves mock responses."""

    routes = []
    delay_ms = 0
    error_rate = 0.0

    def do_GET(self): self._handle()
    def do_POST(self): self._handle()
    def do_PUT(self): self._handle()
    def do_PATCH(self): self._handle()
    def do_DELETE(self): self._handle()
    def do_HEAD(self): self._handle()
    def do_OPTIONS(self): self._handle()

    def _handle(self):
        # Simulate errors
        if self.error_rate > 0 and random.random() < self.error_rate:
            error_code = random.choice([400, 401, 403, 404, 500, 502, 503])
            self._send_json(error_code, {"error": f"Simulated {error_code} error"})
            return

        # Simulate delay
        if self.delay_ms > 0:
            import time
            time.sleep(self.delay_ms / 1000.0)

        # Parse path
        parsed = urlparse(self.path)
        path = parsed.path
        method = self.command

        # CORS preflight
        if method == "OPTIONS":
            self.send_response(204)
            self._cors_headers()
            self.end_headers()
            return

        # Find matching route
        for route in self.routes:
            if route["method"] != method:
                continue
            match = re.match(route["regex"], path)
            if match:
                schema = route["response_schema"]
                if schema:
                    data = generate_from_schema(schema, "", route["definitions"])
                else:
                    data = {"status": "ok"}

                self._send_json(route["status_code"], data)
                return

        # No route found
        self._send_json(404, {
            "error": "Not Found",
            "message": f"No mock route for {method} {path}",
            "available_routes": [f"{r['method']} {r['path']}" for r in self.routes]
        })

    def _send_json(self, status: int, data: Any):
        body = json.dumps(data, indent=2, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self._cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")


# --- Static Mock Generation ---

def generate_static_mocks(routes: list, output_dir: str):
    """Generate static JSON mock files for each route."""
    os.makedirs(output_dir, exist_ok=True)

    manifest = []

    for route in routes:
        schema = route["response_schema"]
        data = generate_from_schema(schema, "", route["definitions"]) if schema else {"status": "ok"}

        # Create filename from path
        safe_name = route["path"].strip("/").replace("/", "_").replace("{", "").replace("}", "")
        if not safe_name:
            safe_name = "root"
        filename = f"{route['method'].lower()}_{safe_name}.json"

        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, default=str)

        manifest.append({
            "method": route["method"],
            "path": route["path"],
            "file": filename,
            "status": route["status_code"],
            "summary": route["summary"],
        })

    # Write manifest
    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump({"routes": manifest}, f, indent=2)

    return manifest


# --- Output Formatters ---

def format_routes_text(routes: list) -> str:
    """Show discovered routes as text."""
    out = [f"Discovered {len(routes)} routes:\n"]
    for r in routes:
        has_schema = "✓" if r["response_schema"] else "✗"
        summary = f" — {r['summary']}" if r.get("summary") else ""
        out.append(f"  {r['method']:7} {r['path']:40} [{r['status_code']}] schema:{has_schema}{summary}")
    return "\n".join(out)


def format_routes_json(routes: list) -> str:
    """Show discovered routes as JSON."""
    data = [{
        "method": r["method"],
        "path": r["path"],
        "status_code": r["status_code"],
        "has_schema": r["response_schema"] is not None,
        "operation_id": r.get("operation_id", ""),
        "summary": r.get("summary", ""),
    } for r in routes]
    return json.dumps({"routes": data, "total": len(data)}, indent=2)


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="Generate mock API servers from OpenAPI/Swagger specs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s serve api.json                    # Start mock server
  %(prog)s serve api.json --port 8080        # Custom port
  %(prog)s serve api.json --delay 200        # 200ms response delay
  %(prog)s serve api.json --error-rate 0.1   # 10%% random errors
  %(prog)s generate api.json -o mocks/       # Generate static JSON files
  %(prog)s routes api.json                   # List discovered routes
  %(prog)s sample api.json /users            # Generate sample for a path
        """
    )

    sub = parser.add_subparsers(dest="command")

    # Serve command
    serve_parser = sub.add_parser("serve", help="Start mock API server")
    serve_parser.add_argument("spec", help="Path to OpenAPI/Swagger spec file")
    serve_parser.add_argument("--port", "-p", type=int, default=3000, help="Port (default: 3000)")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Host (default: 127.0.0.1)")
    serve_parser.add_argument("--delay", "-d", type=int, default=0, help="Response delay in ms")
    serve_parser.add_argument("--error-rate", "-e", type=float, default=0.0, help="Random error rate 0.0-1.0")

    # Generate command
    gen_parser = sub.add_parser("generate", help="Generate static mock JSON files")
    gen_parser.add_argument("spec", help="Path to OpenAPI/Swagger spec file")
    gen_parser.add_argument("--output", "-o", default="mocks", help="Output directory (default: mocks)")

    # Routes command
    routes_parser = sub.add_parser("routes", help="List discovered routes")
    routes_parser.add_argument("spec", help="Path to OpenAPI/Swagger spec file")
    routes_parser.add_argument("--format", choices=["text", "json"], default="text")

    # Sample command
    sample_parser = sub.add_parser("sample", help="Generate sample response for a path")
    sample_parser.add_argument("spec", help="Path to OpenAPI/Swagger spec file")
    sample_parser.add_argument("path", help="API path (e.g. /users)")
    sample_parser.add_argument("--method", "-m", default="GET", help="HTTP method")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Load spec
    spec = load_spec(args.spec)
    routes = extract_routes(spec)

    if args.command == "routes":
        if args.format == "json":
            print(format_routes_json(routes))
        else:
            print(format_routes_text(routes))

    elif args.command == "sample":
        target_path = args.path
        target_method = args.method.upper()
        for route in routes:
            if route["path"] == target_path and route["method"] == target_method:
                schema = route["response_schema"]
                if schema:
                    data = generate_from_schema(schema, "", route["definitions"])
                    print(json.dumps(data, indent=2, default=str))
                else:
                    print('{"status": "ok"}')
                return
        print(f"No route found for {target_method} {target_path}", file=sys.stderr)
        sys.exit(1)

    elif args.command == "generate":
        manifest = generate_static_mocks(routes, args.output)
        print(f"Generated {len(manifest)} mock files in {args.output}/")
        for entry in manifest:
            print(f"  {entry['method']:7} {entry['path']:40} → {entry['file']}")

    elif args.command == "serve":
        MockHandler.routes = routes
        MockHandler.delay_ms = args.delay
        MockHandler.error_rate = args.error_rate

        server = HTTPServer((args.host, args.port), MockHandler)
        print(f"Mock API server running on http://{args.host}:{args.port}")
        print(f"Routes: {len(routes)} | Delay: {args.delay}ms | Error rate: {args.error_rate*100:.0f}%")
        print(format_routes_text(routes))
        print("\nPress Ctrl+C to stop")

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            server.shutdown()


if __name__ == "__main__":
    main()
