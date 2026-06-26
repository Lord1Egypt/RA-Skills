#!/usr/bin/env python3
"""
Analyze JSON data and suggest an OpenAPI spec.
"""
import json, sys, re
from pathlib import Path

def analyze_json(data, depth=0):
    """Recursively analyze JSON structure."""
    info = {"types": set(), "fields": [], "nested": 0}
    if isinstance(data, dict):
        info["fields"] = list(data.keys())
        for k, v in data.items():
            t = type(v).__name__
            info["types"].add(t)
            if isinstance(v, (dict, list)):
                info["nested"] += 1
                sub = analyze_json(v, depth+1)
                info["types"].update(sub["types"])
    elif isinstance(data, list) and data:
        info["types"].add("array")
        if data and isinstance(data[0], dict):
            info["fields"] = list(data[0].keys())
    return info

def suggest_endpoints(info):
    """Infer REST endpoints from JSON fields."""
    endpoints = []
    for field in info["fields"]:
        normalized = re.sub(r"(?<=[a-z])(?=[A-Z])|_", " ", field).lower()
        singular = normalized.rstrip("s")
        endpoints.append({
            "method": "GET",
            "path": f"/{normalized}",
            "summary": f"Get {normalized}",
            "description": f"Returns a list of {normalized}."
        })
        endpoints.append({
            "method": "POST",
            "path": f"/{normalized}",
            "summary": f"Create {singular}",
            "description": f"Creates a new {singular}."
        })
    return endpoints

def to_openapi(info, title="API Design"):
    endpoints = suggest_endpoints(info)
    paths = {}
    for ep in endpoints:
        path = ep["path"]
        if path not in paths:
            paths[path] = {}
        method = ep["method"].lower()
        paths[path][method] = {
            "summary": ep["summary"],
            "description": ep["description"],
            "responses": {"200": {"description": "Successful response"}}
        }

    spec = {
        "openapi": "3.0.0",
        "info": {"title": title, "version": "1.0.0"},
        "paths": paths
    }
    return json.dumps(spec, indent=2)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("file", help="JSON file path")
    p.add_argument("-o", "--output", help="Output .json path")
    args = p.parse_args()

    with open(args.file) as f:
        data = json.load(f)

    info = analyze_json(data)
    spec = to_openapi(info)
    if args.output:
        Path(args.output).write_text(spec)
        print(f"✅ OpenAPI spec written to {args.output}")
    else:
        print(spec)