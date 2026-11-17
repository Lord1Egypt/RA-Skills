#!/usr/bin/env python3
"""Context-frugal intake + filing for the Purchasing PO-pricing-review workflow.

The expensive, context-bloating part of "check the docs in the Purchasing
folder against the POs" is reading the documents: `documents_get` returns each
file's bytes as base64, and rendering a PDF through a multimodal reader adds a
per-page image on top of that. Do that for 5-50 documents a run, many times a
day, and the agent's context window fills with base64 and page renders instead
of the few hundred characters of text that actually matter.

This helper moves that work OUT of the model's context. Over the same Odoo MCP
endpoint `odoo_mcp.py` uses, it lists a Documents-app folder, fetches each
file, decodes and extracts its **text locally**, and prints compact JSON — the
extracted text only, never the base64 or an image. One `extract` call returns
every document in the folder; the agent reads plain text and never sees a byte
of base64.

It also files a reviewed document into a sibling subfolder (`Matched` /
`Questions`) so the Purchasing inbox drains as the run proceeds.

Usage
-----
    python3 scripts/po_docs.py extract '{"folder": "Purchasing"}'
    python3 scripts/po_docs.py extract '{"folder_id": 479}'
    python3 scripts/po_docs.py move '{"document_id": 489, "to": "Matched", "under": "Purchasing"}'
    python3 scripts/po_docs.py move '{"document_id": 489, "to_folder_id": 492}'

Environment
-----------
Same as odoo_mcp.py: ODOO_MCP_URL and ODOO_MCP_TOKEN must be set. Text
extraction prefers poppler's `pdftotext -layout` (best table fidelity) and
falls back to `pypdf`; declare `pypdf` in the skill's install deps.

Output
------
`extract` -> {"folder": {"id", "name"}, "count": N, "total_matched": N,
  "documents": [{"document_id", "name", "mimetype", "file_size", "chars",
    "text", "open_activities", "needs_vision"}]}
`move`    -> {"moved": true, "document_id", "folder_id", "folder_name"}
On failure: {"error": {"type", "message"}} and a non-zero exit (the same
contract as odoo_mcp.py).
"""

from __future__ import annotations

import base64
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from typing import Any

import anyio

# Reuse odoo_mcp.py's transport + config + error contract (sibling module).
from odoo_mcp import _fail, _run  # noqa: E402


# ── MCP result unwrapping ────────────────────────────────────────────────────


def _result_field(result: Any, camel: str, snake: str) -> Any:
    """Read a CallToolResult field across mcp SDK generations — 1.x exposes
    camelCase attributes (`structuredContent`, `isError`), 2.x snake_case."""
    v = getattr(result, camel, None)
    if v is None:
        v = getattr(result, snake, None)
    return v


def _tool_json(result: Any) -> dict[str, Any]:
    """Pull the JSON payload out of an MCP CallToolResult.

    drivethru_mcp returns its dict either as structured content or as JSON
    text in the first content block — accept both, and unwrap a lone
    ``{"result": ...}`` envelope when present.
    """
    sc = _result_field(result, "structuredContent", "structured_content")
    if isinstance(sc, dict) and sc:
        if set(sc.keys()) == {"result"} and isinstance(sc["result"], dict):
            return sc["result"]
        return sc
    for block in getattr(result, "content", None) or []:
        text = getattr(block, "text", None)
        if text:
            try:
                parsed = json.loads(text)
            except (json.JSONDecodeError, TypeError):
                continue
            if isinstance(parsed, dict):
                return parsed
    return {}


def _unwrap_envelope(name: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Unwrap drivethru_mcp's tool envelope `{status, tool, data: {...}}`.

    The live server wraps every result this way, while the callers here expect
    the INNER data (`payload["folders"]`, `page["documents"]`, ...). A bare
    inner dict passes through untouched; an error envelope RAISES so a failure
    can never masquerade as an empty result.
    """
    if "status" in payload and "tool" in payload:
        if payload.get("status") == "error":
            raise RuntimeError(
                f"{name} failed: {json.dumps(payload.get('error') or payload)}"
            )
        data = payload.get("data")
        if isinstance(data, dict):
            return data
    return payload


async def _call(session: Any, name: str, args: dict[str, Any]) -> dict[str, Any]:
    result = await session.call_tool(name, args)
    if bool(_result_field(result, "isError", "is_error")):
        raise RuntimeError(f"{name} failed: {_tool_json(result) or result}")
    return _unwrap_envelope(name, _tool_json(result))


# ── PDF text extraction (local, no bytes leave this process) ─────────────────


def _pdftotext(data: bytes) -> str | None:
    """Extract text with poppler's `pdftotext -layout` if available."""
    exe = shutil.which("pdftotext")
    if not exe:
        return None
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(data)
        tmp.flush()
        try:
            out = subprocess.run(
                [exe, "-layout", "-nopgbrk", tmp.name, "-"],
                capture_output=True,
                timeout=60,
            )
        except (subprocess.SubprocessError, OSError):
            return None
    if out.returncode != 0:
        return None
    return out.stdout.decode("utf-8", "replace")


def _pypdf_text(data: bytes) -> str | None:
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    try:
        reader = PdfReader(io.BytesIO(data))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception:  # noqa: BLE001 - malformed PDF, hand back to caller
        return None


def _extract_text(data: bytes, mimetype: str) -> tuple[str, bool]:
    """Return (text, needs_vision). needs_vision flags files a text pass can't read."""
    is_pdf = "pdf" in (mimetype or "").lower() or data[:5] == b"%PDF-"
    if is_pdf:
        text = _pdftotext(data)
        if text is None:
            text = _pypdf_text(data)
        if text and text.strip():
            return _squeeze(text), False
        # A scanned/image-only PDF yields no text layer.
        return "", True
    if (mimetype or "").lower().startswith("image/"):
        return "", True
    # Plain text / csv / etc.
    return _squeeze(data.decode("utf-8", "replace")), False


def _squeeze(text: str) -> str:
    """Collapse runs of blank lines so the emitted text stays compact."""
    lines = [ln.rstrip() for ln in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    out: list[str] = []
    blanks = 0
    for ln in lines:
        if ln.strip():
            blanks = 0
            out.append(ln)
        else:
            blanks += 1
            if blanks <= 1:
                out.append("")
    return "\n".join(out).strip()


# ── folder resolution ────────────────────────────────────────────────────────


async def _resolve_folder(session: Any, name: str, parent_id: int | None = None) -> dict[str, Any]:
    args: dict[str, Any] = {"name": name}
    if parent_id is not None:
        args["parent_id"] = parent_id
    payload = await _call(session, "documents_list_folders", args)
    folders = payload.get("folders") or []
    if not folders:
        where = f" under folder {parent_id}" if parent_id is not None else ""
        raise ValueError(f"No Documents folder matching {name!r}{where}.")
    exact = [f for f in folders if (f.get("name") or "").strip().lower() == name.strip().lower()]
    return (exact or folders)[0]


# ── actions ──────────────────────────────────────────────────────────────────


async def _extract(session: Any, args: dict[str, Any]) -> dict[str, Any]:
    folder_id = args.get("folder_id")
    folder_name = args.get("folder")
    if folder_id is None:
        if not folder_name:
            raise ValueError("Pass `folder` (name) or `folder_id`.")
        folder = await _resolve_folder(session, str(folder_name))
        folder_id = folder["id"]
        folder_name = folder.get("name")
    folder_id = int(folder_id)

    limit = int(args.get("limit", 200))
    include_subfolders = bool(args.get("include_subfolders", False))

    metas: list[dict[str, Any]] = []
    offset = 0
    total = None
    while True:
        page = await _call(
            session,
            "documents_search",
            {
                "folder_id": folder_id,
                "limit": limit,
                "offset": offset,
                "include_subfolders": include_subfolders,
                # The server's default detail ("minimal") returns only
                # id/name/folder, dropping the mimetype/type this reader keys
                # on. Ask for the fields explicitly.
                "fields": ["name", "mimetype", "file_size", "type"],
            },
        )
        docs = page.get("documents") or []
        metas.extend(docs)
        total = page.get("total_matched", len(metas))
        offset += len(docs)
        if not docs or offset >= total:
            break

    out_docs: list[dict[str, Any]] = []
    for meta in metas:
        if meta.get("type") not in (None, "binary"):
            # URL bookmarks / nested folders carry no bytes to read.
            continue
        doc_id = meta["id"]
        full = await _call(
            session,
            "documents_get",
            # response_detail defaults to "minimal", which returns identity only
            # and OMITS data_base64 — even with include_content. "full" is what
            # surfaces the bytes.
            {"document_id": doc_id, "include_content": True, "response_detail": "full"},
        )
        b64 = full.get("data_base64")
        if not b64:
            # Over the 20MB transport guard, or a non-binary doc.
            out_docs.append(
                {
                    "document_id": doc_id,
                    "name": meta.get("name"),
                    "mimetype": meta.get("mimetype"),
                    "file_size": meta.get("file_size"),
                    "chars": 0,
                    "text": "",
                    "needs_vision": True,
                    "note": "no inline bytes (too large or non-binary); fetch directly",
                    "open_activities": full.get("open_activities") or [],
                }
            )
            continue
        data = base64.b64decode(b64)
        text, needs_vision = _extract_text(data, meta.get("mimetype", ""))
        out_docs.append(
            {
                "document_id": doc_id,
                "name": meta.get("name"),
                "mimetype": meta.get("mimetype"),
                "file_size": meta.get("file_size"),
                "chars": len(text),
                "text": text,
                "needs_vision": needs_vision,
                "open_activities": full.get("open_activities") or [],
            }
        )

    return {
        "folder": {"id": folder_id, "name": folder_name},
        "count": len(out_docs),
        "total_matched": total if total is not None else len(out_docs),
        "documents": out_docs,
    }


async def _move(session: Any, args: dict[str, Any]) -> dict[str, Any]:
    if "document_id" not in args:
        raise ValueError("`document_id` is required.")
    doc_id = int(args["document_id"])

    to_folder_id = args.get("to_folder_id")
    folder_name = None
    if to_folder_id is None:
        to = args.get("to")
        if to is None:
            raise ValueError("Pass `to` (e.g. 'Matched'/'Questions') or `to_folder_id`.")
        if isinstance(to, int) or (isinstance(to, str) and to.isdigit()):
            to_folder_id = int(to)
        else:
            under = args.get("under", "Purchasing")
            parent = await _resolve_folder(session, str(under))
            child = await _resolve_folder(session, str(to), parent_id=int(parent["id"]))
            to_folder_id = int(child["id"])
            folder_name = child.get("name")
    to_folder_id = int(to_folder_id)

    res = await _call(
        session,
        "documents_update",
        {"document_id": doc_id, "fields": {"folder_id": to_folder_id}},
    )
    doc = res.get("document") or {}
    return {
        "moved": bool(res.get("updated", True)),
        "document_id": doc_id,
        "folder_id": to_folder_id,
        "folder_name": folder_name or (doc.get("folder") or {}).get("name"),
    }


ACTIONS = {
    "extract": _extract,
    "move": _move,
}

USAGE = (
    "po_docs.py <extract|move>   # JSON args as 2nd arg or on stdin\n"
    "  extract {\"folder\": \"Purchasing\"}\n"
    "  move    {\"document_id\": 489, \"to\": \"Matched\", \"under\": \"Purchasing\"}"
)


def _read_args() -> dict[str, Any]:
    raw = None
    if len(sys.argv) >= 3:
        raw = sys.argv[2]
    elif not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
    raw = (raw or "").strip() or "{}"
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        _fail("invalid_arguments", f"Arguments must be valid JSON: {exc}", code=2)
        raise SystemExit(2)
    if not isinstance(parsed, dict):
        _fail("invalid_arguments", "Arguments must be a JSON object.", code=2)
        raise SystemExit(2)
    return parsed


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        _fail("usage", USAGE, code=2)
        return 2
    action = sys.argv[1]
    handler = ACTIONS.get(action)
    if handler is None:
        _fail("unknown_action", f"Unknown action {action!r}. Use: {', '.join(ACTIONS)}", code=2)
        return 2

    args = _read_args()

    async def fn(session: Any) -> dict[str, Any]:
        return await handler(session, args)

    res = anyio.run(lambda: _run(fn))
    if isinstance(res, int):  # config/connection error already printed by _run
        return res
    print(json.dumps(res, default=str, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
