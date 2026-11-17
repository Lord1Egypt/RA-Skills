#!/usr/bin/env python3
"""Create a small Postman v2.1 collection for one HTTP endpoint."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlparse
from uuid import uuid4


def parse_key_value(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError(f"Expected KEY=VALUE, got: {value}")
    key, val = value.split("=", 1)
    key = key.strip()
    if not key:
        raise argparse.ArgumentTypeError(f"Empty key in: {value}")
    return key, val


def read_domain_candidates(domains_path: str, service: str) -> list[str]:
    path = Path(domains_path)
    if not path.exists():
        return []

    service_tokens = [token for token in re.split(r"[-_.\s]+", service.lower()) if token]
    scored: list[tuple[int, str]] = []
    seen: set[str] = set()

    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        for host in re.findall(r"[A-Za-z0-9][A-Za-z0-9.-]*\.[A-Za-z]{2,}", line):
            host_l = host.lower()
            if host_l in seen:
                continue
            seen.add(host_l)
            score = 0
            if service.lower() in host_l:
                score += 100
            score += sum(10 for token in service_tokens if token in host_l)
            if score:
                scored.append((score, host))

    scored.sort(key=lambda item: (-item[0], item[1]))
    return [host for _, host in scored]


def remember_domain(domains_path: str, service: str, domain: str) -> None:
    path = Path(domains_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    service = service.strip()
    domain = domain.strip().rstrip("/")
    if not service or not domain:
        raise SystemExit("--service and --domain are required with --remember-domain")

    if path.exists():
        text = path.read_text(encoding="utf-8")
    else:
        text = "# Stored Service Domains\n\n## Service mappings\n\n| Service | Domain | Notes |\n| --- | --- | --- |\n"

    row = f"| {service} | {domain} | Remembered after user confirmation |"
    if row in text:
        return
    if f"| {service} | {domain} |" in text:
        return

    marker = "| --- | --- | --- |"
    if marker in text:
        text = text.replace(marker, marker + "\n" + row, 1)
    else:
        text = text.rstrip() + "\n\n## Service mappings\n\n| Service | Domain | Notes |\n| --- | --- | --- |\n" + row + "\n"
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def split_url(base_url: str, path: str) -> tuple[str, list[str], list[dict[str, str]]]:
    base_url = base_url.rstrip("/")
    path = "/" + path.lstrip("/")
    parsed = urlparse(base_url + path)
    raw_path = parsed.path
    query = [{"key": key, "value": val} for key, val in parse_qsl(parsed.query)]
    return parsed.geturl().split("?", 1)[0], [part for part in raw_path.split("/") if part], query


def make_collection(args: argparse.Namespace) -> dict:
    raw_url, path_parts, url_query = split_url(args.base_url, args.path)
    query = url_query + [{"key": key, "value": val} for key, val in args.query]
    headers = [{"key": key, "value": val, "type": "text"} for key, val in args.header]

    request: dict = {
        "method": args.method.upper(),
        "header": headers,
        "url": {
            "raw": raw_url,
            "protocol": urlparse(raw_url).scheme or None,
            "host": urlparse(raw_url).netloc.split(".") if urlparse(raw_url).netloc else [args.base_url],
            "path": path_parts,
        },
    }
    if query:
        request["url"]["query"] = query

    path_variables = []
    for part in path_parts:
        match = re.fullmatch(r"\{(.+)\}|:(.+)", part)
        if match:
            key = match.group(1) or match.group(2)
            path_variables.append({"key": key, "value": "{{" + key + "}}"})
    if path_variables:
        request["url"]["variable"] = path_variables

    body_json = args.body_json
    if args.body_json_file:
        body_json = Path(args.body_json_file).read_text(encoding="utf-8")

    if body_json:
        try:
            json.loads(body_json)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"--body-json is not valid JSON: {exc}") from exc
        request["body"] = {
            "mode": "raw",
            "raw": body_json,
            "options": {"raw": {"language": "json"}},
        }
        if not any(header["key"].lower() == "content-type" for header in headers):
            request["header"].append({"key": "Content-Type", "value": "application/json", "type": "text"})

    return {
        "info": {
            "_postman_id": str(uuid4()),
            "name": args.name,
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": [{"name": args.name, "request": request, "response": []}],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=False, default="Exported endpoint")
    parser.add_argument("--method", choices=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"], default="GET")
    parser.add_argument("--base-url", default="{{baseUrl}}")
    parser.add_argument("--path", default="/")
    parser.add_argument("--query", action="append", default=[], type=parse_key_value, help="Query parameter as KEY=VALUE")
    parser.add_argument("--header", action="append", default=[], type=parse_key_value, help="Header as KEY=VALUE")
    parser.add_argument("--body-json", help="Raw JSON request body")
    parser.add_argument("--body-json-file", help="Path to a JSON request body file")
    parser.add_argument("--output", help="Output collection JSON path")
    parser.add_argument("--domains", default=str(Path(__file__).resolve().parents[1] / "references" / "domains.md"))
    parser.add_argument("--service", default="")
    parser.add_argument("--domain", default="")
    parser.add_argument("--remember-domain", action="store_true")
    parser.add_argument("--print-domain-candidates", action="store_true")
    args = parser.parse_args()

    if args.remember_domain:
        remember_domain(args.domains, args.service, args.domain)
        return 0

    if args.print_domain_candidates:
        if not args.service:
            raise SystemExit("--service is required with --print-domain-candidates")
        for host in read_domain_candidates(args.domains, args.service):
            print(host)
        return 0

    collection = make_collection(args)
    data = json.dumps(collection, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(data + "\n", encoding="utf-8")
    else:
        sys.stdout.write(data + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
