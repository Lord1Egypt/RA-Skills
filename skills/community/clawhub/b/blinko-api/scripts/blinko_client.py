#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request


class Blinko:
    def __init__(self, base_url=None, api_token=None):
        host = base_url if base_url is not None else os.getenv("BLINKO_HOST", "http://127.0.0.1:1111")
        token = api_token if api_token is not None else os.getenv("BLINKO_TOKEN", "")
        self.base_url = (host or "").rstrip("/")
        self.api_token = token or ""

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        return headers

    def _request(self, path, method="GET", body=None):
        url = f"{self.base_url}{path}"
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")

        request = urllib.request.Request(url, data=data, headers=self._headers(), method=method)

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                content_type = response.headers.get("content-type", "")
                text = response.read().decode("utf-8", errors="replace")
                if "application/json" in content_type.lower():
                    return json.loads(text) if text else None
                return text
        except urllib.error.HTTPError as error:
            message = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Blinko API {error.code} {error.reason}: {message}") from error
        except urllib.error.URLError as error:
            raise RuntimeError(f"Blinko request failed: {error.reason}") from error

    def list_notes(self, query=None):
        payload = query or {}
        return self._request("/v1/note/list", method="POST", body=payload)

    def get_note(self, note_id):
        return self._request("/v1/note/detail", method="POST", body={"id": note_id})

    def upsert_note(self, content, note_id=None, note_type=0, attachments=None, references=None):
        payload = {
            "content": content,
            "type": note_type,
            "attachments": attachments if attachments is not None else [],
            "references": references if references is not None else [],
        }
        if note_id is not None:
            payload["id"] = note_id
        return self._request("/v1/note/upsert", method="POST", body=payload)

    def delete_note(self, note_id):
        return self._request("/v1/note/batch-delete", method="POST", body={"ids": [note_id]})

    def list_blinkos(self, query=None):
        return self.list_notes(query=query)

    def get_blinko(self, blinko_id):
        return self.get_note(blinko_id)

    def upsert_blinko(self, content, blinko_id=None, blinko_type=0):
        return self.upsert_note(content=content, note_id=blinko_id, note_type=blinko_type)

    def delete_blinko(self, blinko_id):
        return self.delete_note(blinko_id)

    def promote_blinko_to_note(self, blinko_id):
        blinko = self.get_blinko(blinko_id)
        if not blinko:
            raise RuntimeError("Blinko not found")

        content = None
        if isinstance(blinko, dict):
            content = blinko.get("content")
            if content is None and isinstance(blinko.get("data"), dict):
                content = blinko["data"].get("content")

        if not content:
            raise RuntimeError("Blinko not found")

        return self.upsert_note(content=content, note_type=0)


def parse_json_arg(value, arg_name):
    try:
        return json.loads(value)
    except json.JSONDecodeError as error:
        raise argparse.ArgumentTypeError(f"Invalid JSON for {arg_name}: {error}") from error


def print_result(result):
    if isinstance(result, (dict, list)):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif result is None:
        print("null")
    else:
        print(result)


def build_parser():
    parser = argparse.ArgumentParser(description="Blinko API client.")
    parser.add_argument("--host", default=os.getenv("BLINKO_HOST", "http://127.0.0.1:1111"), help="Blinko host")
    parser.add_argument("--token", default=os.getenv("BLINKO_TOKEN", ""), help="Blinko API token")

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_notes = subparsers.add_parser("list-notes", help="List notes")
    list_notes.add_argument("--query", default="{}", help="JSON query body")

    get_note = subparsers.add_parser("get-note", help="Get note by id")
    get_note.add_argument("id", type=int, help="Note id")

    upsert_note = subparsers.add_parser("upsert-note", help="Create or update a note")
    upsert_note.add_argument("--id", type=int, help="Optional note id")
    upsert_note.add_argument("--content", required=True, help="Note content")
    upsert_note.add_argument("--type", type=int, default=0, help="Note type")
    upsert_note.add_argument("--attachments", default="[]", help="JSON array for attachments")
    upsert_note.add_argument("--references", default="[]", help="JSON array for references")

    delete_note = subparsers.add_parser("delete-note", help="Delete note by id")
    delete_note.add_argument("id", type=int, help="Note id")

    list_blinkos = subparsers.add_parser("list-blinkos", help="List blinkos")
    list_blinkos.add_argument("--query", default="{}", help="JSON query body")

    get_blinko = subparsers.add_parser("get-blinko", help="Get blinko by id")
    get_blinko.add_argument("id", type=int, help="Blinko id")

    upsert_blinko = subparsers.add_parser("upsert-blinko", help="Create or update a blinko")
    upsert_blinko.add_argument("--id", type=int, help="Optional blinko id")
    upsert_blinko.add_argument("--content", required=True, help="Blinko content")
    upsert_blinko.add_argument("--type", type=int, default=0, help="Blinko type")

    delete_blinko = subparsers.add_parser("delete-blinko", help="Delete blinko by id")
    delete_blinko.add_argument("id", type=int, help="Blinko id")

    promote = subparsers.add_parser("promote-blinko", help="Promote a blinko to a note")
    promote.add_argument("id", type=int, help="Blinko id")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    client = Blinko(base_url=args.host, api_token=args.token)

    try:
        if args.command == "list-notes":
            query = parse_json_arg(args.query, "--query")
            if not isinstance(query, dict):
                raise RuntimeError("--query must be a JSON object")
            result = client.list_notes(query=query)
        elif args.command == "get-note":
            result = client.get_note(args.id)
        elif args.command == "upsert-note":
            attachments = parse_json_arg(args.attachments, "--attachments")
            references = parse_json_arg(args.references, "--references")
            if not isinstance(attachments, list):
                raise RuntimeError("--attachments must be a JSON array")
            if not isinstance(references, list):
                raise RuntimeError("--references must be a JSON array")
            if any(not isinstance(attachment, dict) for attachment in attachments):
                raise RuntimeError("--attachments must contain only objects")
            required_attachment_keys = {"name", "path", "size", "type"}
            for attachment in attachments:
                missing = required_attachment_keys - set(attachment.keys())
                if missing:
                    raise RuntimeError(
                        "--attachments items must include name, path, size, type"
                    )
            if any(not isinstance(reference, int) for reference in references):
                raise RuntimeError("--references must contain only numeric note IDs")
            result = client.upsert_note(
                content=args.content,
                note_id=args.id,
                note_type=args.type,
                attachments=attachments,
                references=references,
            )
        elif args.command == "delete-note":
            result = client.delete_note(args.id)
        elif args.command == "list-blinkos":
            query = parse_json_arg(args.query, "--query")
            if not isinstance(query, dict):
                raise RuntimeError("--query must be a JSON object")
            result = client.list_blinkos(query=query)
        elif args.command == "get-blinko":
            result = client.get_blinko(args.id)
        elif args.command == "upsert-blinko":
            result = client.upsert_blinko(content=args.content, blinko_id=args.id, blinko_type=args.type)
        elif args.command == "delete-blinko":
            result = client.delete_blinko(args.id)
        elif args.command == "promote-blinko":
            result = client.promote_blinko_to_note(args.id)
        else:
            raise RuntimeError(f"Unknown command: {args.command}")

        print_result(result)
    except (RuntimeError, argparse.ArgumentTypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
