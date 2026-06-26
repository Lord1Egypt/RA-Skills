#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bohrium-kb-upload.py

Upload a local file into Bohrium Knowledge Base via OpenAPI multipart + binary upload.

Flow (confirmed):
0) (Optional) POST https://open.bohrium.com/openapi/v1/knowledge/knowledge_base/create
   body: {"knowledgeBaseName": "Daily Paper-YYMMDD", "introduction": "...", "cover": "", "privilege": 1}
   header: accessKey

1) GET https://open.bohrium.com/openapi/v1/knowledge/file/multipart
   query: fileName, md5, parentId(nodeId), size
   header: accessKey
   -> returns data.host, data.path, data.token

2) POST {host}/api/upload/binary
   headers:
     - Authorization: Bearer {token}
     - X-Storage-Param: base64(json)
   body: raw file bytes

X-Storage-Param is base64( json_to_bytes({
  "path": <multipart.data.path>,
  "option": {
     "contentDisposition": 'inline; filename="{encoded_file_name}"; filename*=UTF-8\'\'{encoded_file_name}',
     "contentType": <guessed from suffix>
  }
}) )

Filename encoding: JavaScript encodeURIComponent-compatible percent-encoding.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import sys
import urllib.parse
from dataclasses import dataclass
from pathlib import Path


def load_access_key_from_openclaw_config() -> str:
    """Fallback: read ACCESS_KEY from ~/.openclaw/openclaw.json

    Expected path:
      skills.entries.bohrium-knowledge-file-upload.env.ACCESS_KEY

    Returns empty string if not found.
    """

    try:
        cfg_path = Path("~/.openclaw/openclaw.json").expanduser()
        if not cfg_path.exists():
            return ""
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        return (
            (((cfg.get("skills") or {}).get("entries") or {}).get("bohrium-knowledge-file-upload") or {})
            .get("env")
            or {}
        ).get("ACCESS_KEY", "")
    except Exception:
        return ""

import urllib.request


OPENAPI_MULTIPART = "https://open.bohrium.com/openapi/v1/knowledge/file/multipart"
OPENAPI_SUBMIT = "https://open.bohrium.com/openapi/v1/knowledge/file/submit"


def encode_uri_component(s: str) -> str:
    """Approximate JavaScript encodeURIComponent.

    It percent-encodes UTF-8 bytes and keeps these characters unescaped:
    A-Z a-z 0-9 - _ . ! ~ * ' ( )

    (Matches typical encodeURIComponent behavior for our filename use-case.)
    """

    return urllib.parse.quote(s, safe="-_.!~*'()")


def md5_hex(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def guess_content_type(path: Path) -> str:
    # custom mapping first
    suffix = path.suffix.lower()
    if suffix in {".md", ".markdown"}:
        return "text/markdown; charset=utf-8"
    if suffix in {".txt"}:
        return "text/plain; charset=utf-8"

    ctype, _ = mimetypes.guess_type(str(path))
    if ctype is None:
        return "application/octet-stream"

    # text/* defaults to utf-8
    if ctype.startswith("text/"):
        return f"{ctype}; charset=utf-8"
    return ctype


@dataclass
class MultipartInfo:
    host: str
    path: str
    token: str
    file_exist: bool = False


def _http_json(method: str, url: str, headers: dict[str, str] | None = None, data: bytes | None = None, timeout: int = 60) -> dict:
    req = urllib.request.Request(url, method=method, headers=headers or {}, data=data)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read()
        # urllib raises for HTTP errors automatically
    return json.loads(body.decode("utf-8"))


def get_multipart_info(access_key: str, file_name: str, md5: str, parent_id: int, size: int) -> MultipartInfo:
    qs = urllib.parse.urlencode({
        "fileName": file_name,
        "md5": md5,
        "parentId": parent_id,
        "size": size,
    })
    url = f"{OPENAPI_MULTIPART}?{qs}"
    data = _http_json("GET", url, headers={"accessKey": access_key}, timeout=60)
    if data.get("code") != 0:
        raise RuntimeError(f"multipart failed: {data}")
    d = data.get("data") or {}
    return MultipartInfo(
        host=d.get("host", ""),
        path=d.get("path", ""),
        token=d.get("token", ""),
        file_exist=bool(d.get("fileExist")),
    )


def make_storage_param(remote_path: str, encoded_file_name: str, content_type: str) -> str:
    payload = {
        "path": remote_path,
        "option": {
            "contentDisposition": (
                f'inline; filename="{encoded_file_name}"; '
                f"filename*=UTF-8''{encoded_file_name}"
            ),
            "contentType": content_type,
        },
    }
    b = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return base64.b64encode(b).decode("utf-8")


def upload_binary(host: str, token: str, storage_param: str, local_path: Path) -> dict:
    url = host.rstrip("/") + "/api/upload/binary"
    body = local_path.read_bytes()
    data = _http_json(
        "POST",
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "X-Storage-Param": storage_param,
            # optional; server seems fine without, but keep it explicit
            "Content-Type": "application/octet-stream",
        },
        data=body,
        timeout=300,
    )
    return data


def submit_file(access_key: str, file_name: str, md5: str, parent_id: int, size: int, url_path: str) -> dict:
    body = json.dumps({
        "fileName": file_name,
        "md5": md5,
        "parentId": parent_id,
        "size": size,
        "url": url_path,
    }, ensure_ascii=False).encode("utf-8")

    data = _http_json(
        "POST",
        OPENAPI_SUBMIT,
        headers={
            "accessKey": access_key,
            "Content-Type": "application/json",
        },
        data=body,
        timeout=60,
    )
    return data


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Upload file to Bohrium Knowledge Base via multipart flow")
    p.add_argument("local_file", help="Local file path")
    p.add_argument("--access-key", default=os.environ.get("ACCESS_KEY", ""), help="Bohrium OpenAPI accessKey (or set ACCESS_KEY env)")
    p.add_argument("--parent-id", type=int, required=True, help="Knowledge base nodeId (parentId in multipart API)")
    p.add_argument("--file-name", default="", help="Override fileName (default: basename of local file)")
    p.add_argument("--md5", default="", help="Override md5 (default: computed from file)")
    p.add_argument("--size", type=int, default=0, help="Override size in bytes (default: file size)")
    p.add_argument("--content-type", default="", help="Override contentType (default: guessed by suffix)")
    p.add_argument("--dry-run", action="store_true", help="Only print computed params, do not upload")

    args = p.parse_args(argv)

    access_key = args.access_key.strip()
    if not access_key:
        access_key = load_access_key_from_openclaw_config().strip()
    if not access_key:
        print(
            "ERROR: accessKey missing. Provide --access-key or set ACCESS_KEY env, or configure skills.entries.bohrium-knowledge-file-upload.env.ACCESS_KEY in ~/.openclaw/openclaw.json.",
            file=sys.stderr,
        )
        return 2

    local_path = Path(args.local_file).expanduser().resolve()
    if not local_path.exists() or not local_path.is_file():
        print(f"ERROR: local file not found: {local_path}", file=sys.stderr)
        return 2

    file_name = args.file_name or local_path.name
    size = args.size or local_path.stat().st_size
    md5 = args.md5 or md5_hex(local_path)
    content_type = args.content_type or guess_content_type(local_path)

    encoded_file_name = encode_uri_component(file_name)

    if args.dry_run:
        print(json.dumps({
            "fileName": file_name,
            "md5": md5,
            "size": size,
            "parentId": args.parent_id,
            "contentType": content_type,
            "encodedFileName": encoded_file_name,
        }, ensure_ascii=False, indent=2))
        return 0

    mp = get_multipart_info(access_key, file_name, md5, args.parent_id, size)

    upload_result = None
    final_path = mp.path

    if mp.file_exist:
        # Still need to submit to register / make it visible in KB.
        upload_result = {"skipped": True, "reason": "fileExist=true"}
    else:
        if not mp.host or not mp.token or not mp.path:
            print(f"ERROR: multipart missing host/token/path: {mp}", file=sys.stderr)
            return 1
        storage_param = make_storage_param(mp.path, encoded_file_name, content_type)
        upload_result = upload_binary(mp.host, mp.token, storage_param, local_path)
        # Prefer server-returned path if present
        if isinstance(upload_result, dict):
            final_path = (upload_result.get("data") or {}).get("path") or final_path

    submit_result = submit_file(access_key, file_name, md5, args.parent_id, size, final_path)

    print(json.dumps({
        "multipart": {"host": mp.host, "path": mp.path, "fileExist": mp.file_exist},
        "uploadResult": upload_result,
        "submitResult": submit_result,
        "finalPath": final_path,
    }, ensure_ascii=False, indent=2))

    # Treat "file already exists" as idempotent success.
    # Bohrium sometimes returns code=230117 on submit even when multipart says fileExist=true.
    try:
        if isinstance(submit_result, dict):
            code = submit_result.get("code")
            if code == 0:
                return 0
            if code == 230117:
                # file already exists
                return 0
    except Exception:
        pass
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
