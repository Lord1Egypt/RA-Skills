#!/usr/bin/env python3
"""Prepare immutable local evidence, then validate analysis offline. Never write Calibre."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, quote, unquote

SCRIPT_DIR = Path(__file__).resolve().parent
MAX_OUTPUT = 16 * 1024 * 1024
MAX_TEXT = 32 * 1024 * 1024
SCHEMA_VERSION = 3


def error(message):
    raise ValueError(message)


def digest(data):
    return "sha256:" + hashlib.sha256(data).hexdigest()


def file_hash(path):
    with Path(path).open("rb") as stream:
        h = hashlib.file_digest(stream, "sha256")
    return "sha256:" + h.hexdigest()


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def read_json(path):
    p = Path(path)
    if p.stat().st_size > MAX_TEXT:
        error("JSON file exceeds size limit")
    return json.loads(p.read_text(encoding="utf-8"))


def write_new(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    # Exclusive creation: never replace evidence/another run's proposal.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as out:
        out.write(data)
        out.flush()
        os.fsync(out.fileno())


def load_config(ns):
    name = ns.config or os.environ.get("CALIBRE_CATALOG_CONFIG")
    p = Path(name or Path.home() / ".config/calibre-catalog-read/config.json").expanduser()
    if not p.exists():
        if name:
            error("configured config file does not exist")
        return {}
    obj = read_json(p)
    if not isinstance(obj, dict) or set(obj) - {"with_library", "library_id", "username", "password_env", "reading_script"}:
        error("invalid or unknown catalog config keys")
    if any(not isinstance(v, str) for v in obj.values()):
        error("catalog config values must be strings")
    return obj


def normalize_endpoint(raw, library_id=""):
    raw = str(raw or "").strip()
    if not raw:
        error("missing explicit/configured endpoint; automatic discovery is disabled")
    if re.match(r"^https?://", raw, re.I):
        u = urlsplit(raw)
        if not u.hostname or u.username or u.password or u.query:
            error("endpoint requires a host, no embedded credentials/query")
        fragment = unquote(u.fragment or library_id)
        if not fragment or fragment == "-" or fragment.startswith("library_id="):
            error("use the CLI URL #LIBRARY_ID, not a browser URL or discovery selector")
        port = u.port  # also validates malformed ports
        host = u.hostname.lower()
        if ":" in host:
            host = "[" + host + "]"
        if port and port != (443 if u.scheme.lower() == "https" else 80):
            host += ":" + str(port)
        return urlunsplit((u.scheme.lower(), host, u.path or "/", "", quote(fragment, safe="")))
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw):
        error("endpoint must be an http(s) URL or existing library directory")
    p = Path(raw).expanduser().resolve()
    if not (p / "metadata.db").is_file():
        error("local library must already contain metadata.db")
    return str(p)


def library_identity(endpoint):
    return normalize_endpoint(endpoint)


def resolve_endpoint(ns, config):
    raw = ns.with_library or next((os.environ[k] for k in ("CALIBRE_WITH_LIBRARY", "CALIBRE_LIBRARY_URL", "CALIBRE_CONTENT_SERVER_URL") if os.environ.get(k)), config.get("with_library", ""))
    return normalize_endpoint(raw, ns.library_id or os.environ.get("CALIBRE_LIBRARY_ID", "") or config.get("library_id", ""))


def run_process(args, *, password="", timeout=120):
    env = {k: os.environ[k] for k in ("PATH", "HOME", "LANG", "LC_ALL", "SYSTEMROOT", "WINDIR", "CALIBRE_CONFIG_DIRECTORY", "QT_QPA_PLATFORM") if k in os.environ}
    try:
        # Spool output, rather than buffering arbitrarily large converter logs in memory.
        with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
            result = subprocess.run(args, input=(password + "\n").encode() if password else b"", stdout=out, stderr=err, env=env, timeout=timeout)
            if out.tell() > MAX_OUTPUT or err.tell() > MAX_OUTPUT:
                error("subprocess output exceeded 16 MiB; refusing truncated output")
            out.seek(0); err.seek(0)
            stdout, stderr = out.read().decode("utf-8"), err.read().decode("utf-8", "replace")
    except FileNotFoundError:
        error("required executable not found: " + args[0])
    except subprocess.TimeoutExpired:
        error("subprocess timed out")
    if result.returncode:
        diagnostic = (stderr or stdout).replace(password, "[redacted]") if password else (stderr or stdout)
        error("subprocess failed (exit=" + str(result.returncode) + "): " + diagnostic[:1000])
    return stdout


def calibre(args, ns, config, endpoint):
    password = os.environ.get(ns.password_env or config.get("password_env", "CALIBRE_PASSWORD"), "")
    cli_endpoint = endpoint
    if endpoint.startswith(("http://", "https://")):
        host, fragment = endpoint.rsplit("#", 1)
        cli_endpoint = host + "#" + unquote(fragment)
    auth = ["--with-library", cli_endpoint, "--timeout", str(ns.timeout)]
    username = ns.username or os.environ.get("CALIBRE_USERNAME") or config.get("username")
    if username:
        auth += ["--username", username]
    if password:
        auth += ["--password", "<stdin>"]
    return run_process(["calibredb", *args, *auth], password=password, timeout=ns.timeout + 5)


def prepare(ns):
    if ns.book_id < 1 or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,100}", ns.run_id):
        error("positive book id and simple unique run id required")
    if not 1 <= ns.timeout <= 3600 or not 1 <= ns.min_text_chars <= MAX_TEXT or not 1 <= ns.chunk_chars <= 100000:
        error("invalid timeout/text/chunk limit")
    config = load_config(ns)
    endpoint = resolve_endpoint(ns, config)
    rows = json.loads(calibre(["list", "--for-machine", "--fields", "title,authors,uuid,tags,formats", "--search", "id:" + str(ns.book_id), "--limit", "2"], ns, config, endpoint))
    matches = [r for r in rows if isinstance(r, dict) and r.get("id") == ns.book_id] if isinstance(rows, list) else []
    if len(matches) != 1 or not matches[0].get("uuid"):
        error("book id/UUID not uniquely returned")
    meta = matches[0]
    if any(tag.casefold() in ("manga", "comic", "comics", "漫画", "マンガ", "コミック", "graphic novel") for tag in meta.get("tags", [])):
        return {"ok": True, "status": "skipped", "reason": "excluded_content", "book_id": ns.book_id}
    root = Path(ns.cache_dir or os.environ.get("CALIBRE_CATALOG_CACHE_DIR") or Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "calibre-catalog-read").expanduser().resolve()
    run_dir = root / hashlib.sha256(endpoint.encode()).hexdigest()[:24] / ns.run_id
    run_dir.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    run_dir.mkdir(mode=0o700)  # no stale/partial run reuse
    export_dir = run_dir / "export"
    export_dir.mkdir(mode=0o700)
    calibre(["export", str(ns.book_id), "--to-dir", str(export_dir), "--single-dir", "--formats", ns.format,
             "--dont-update-metadata", "--dont-write-opf", "--dont-save-cover", "--dont-save-extra-files"], ns, config, endpoint)
    sources = [p for p in export_dir.rglob("*") if p.is_file() and p.suffix.lower() == "." + ns.format.lower() and not p.is_symlink()]
    if len(sources) != 1:
        error("export must contain exactly one requested format")
    source = sources[0]
    text_path = run_dir / "extracted.txt"
    try:
        run_process(["ebook-convert", str(source), str(text_path)], timeout=ns.timeout)
    except ValueError:
        if ns.format != "PDF":
            raise
        run_process(["pdftotext", "-layout", str(source), str(text_path)], timeout=ns.timeout)
    if text_path.stat().st_size > MAX_TEXT:
        error("extracted text exceeds 32 MiB; choose an explicit partial workflow")
    text = text_path.read_text(encoding="utf-8")
    chars = len("".join(text.split()))
    if not text.strip() or (chars < ns.min_text_chars and not ns.force_low_text):
        return {"ok": True, "status": "skipped", "reason": "low_text_requires_confirmation", "text_chars": chars, "text_path": str(text_path), "run_dir": str(run_dir)}
    parts = []
    for i, start in enumerate(range(0, len(text), ns.chunk_chars), 1):
        part_id = f"part-{i:04d}"
        part = text[start:start + ns.chunk_chars]
        p = run_dir / (part_id + ".txt")
        write_new(p, part.encode("utf-8"))
        parts.append({"id": part_id, "path": str(p), "sha256": file_hash(p), "chars": len(part)})
    manifest = {"version": SCHEMA_VERSION, "run_id": ns.run_id, "book_id": ns.book_id, "book_uuid": meta["uuid"], "title": meta["title"],
                "library_id": endpoint, "format": ns.format, "lang": ns.lang, "file_hash": file_hash(source), "source_file": str(source),
                "text_path": str(text_path), "text_hash": file_hash(text_path), "source_files": parts,
                "coverage": {"expected_files": len(parts), "source_chars": len(text)}, "low_text_confirmed": bool(ns.force_low_text)}
    manifest["manifest_digest"] = digest(canonical(manifest))
    input_path = run_dir / "subagent_input.json"
    write_new(input_path, canonical(manifest) + b"\n")
    return {"ok": True, "status": "prepared", "remote_writes": False, "prepared_input": str(input_path), "input_sha256": file_hash(input_path),
            "run_id": ns.run_id, "book_id": ns.book_id, "library_id": endpoint, "file_hash": manifest["file_hash"], "coverage": manifest["coverage"]}


def validate_manifest(input_path, expected_hash=None):
    input_path = Path(input_path).resolve()
    if expected_hash and file_hash(input_path) != expected_hash:
        error("prepared input changed since run registration")
    obj = read_json(input_path)
    if not isinstance(obj, dict) or obj.get("version") != SCHEMA_VERSION:
        error("invalid prepared manifest version")
    expected = {"version", "run_id", "book_id", "book_uuid", "title", "library_id", "format", "lang", "file_hash", "source_file", "text_path", "text_hash", "source_files", "coverage", "low_text_confirmed", "manifest_digest"}
    if set(obj) != expected or type(obj["book_id"]) is not int or not 1 <= obj["book_id"] <= 9007199254740991 or not isinstance(obj["run_id"], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,100}", obj["run_id"]):
        error("invalid prepared manifest fields/target")
    if any(not isinstance(obj[k], str) or not obj[k] for k in ("book_uuid", "library_id", "source_file", "text_path")) or not isinstance(obj["title"], str) or obj["lang"] not in ("ja", "en") or obj["format"] not in ("EPUB", "PDF") or type(obj["low_text_confirmed"]) is not bool:
        error("invalid prepared identity/types")
    if any(not isinstance(obj[k], str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", obj[k]) for k in ("file_hash", "text_hash", "manifest_digest")):
        error("invalid prepared hash")
    claimed = obj.get("manifest_digest")
    if claimed != digest(canonical({k: v for k, v in obj.items() if k != "manifest_digest"})):
        error("prepared manifest digest mismatch")
    root = input_path.parent
    def local_file(value):
        p = Path(value)
        if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(root):
            error("prepared source escaped its run directory or is missing")
        return p
    if file_hash(local_file(obj["source_file"])) != obj["file_hash"] or file_hash(local_file(obj["text_path"])) != obj["text_hash"]:
        error("prepared source/text hash mismatch")
    parts = obj.get("source_files")
    if not isinstance(parts, list) or not parts:
        error("prepared manifest has no source parts")
    ids, texts = set(), []
    for part in parts:
        if set(part) != {"id", "path", "sha256", "chars"} or part["id"] in ids:
            error("invalid/duplicate prepared part")
        ids.add(part["id"])
        p = local_file(part["path"])
        if file_hash(p) != part["sha256"]:
            error("prepared part hash mismatch")
        text = p.read_text(encoding="utf-8")
        if type(part["chars"]) is not int or len(text) != part["chars"] or not text:
            error("prepared part character count mismatch")
        texts.append(text)
    text = local_file(obj["text_path"]).read_text(encoding="utf-8")
    if "".join(texts) != text or obj["coverage"] != {"expected_files": len(parts), "source_chars": len(text)}:
        error("prepared coverage does not match source parts")
    return obj


def validate_analysis(obj, manifest):
    required = {"run_id", "book_id", "library_id", "file_hash", "lang", "summary", "highlights", "reread", "tags", "coverage"}
    if not isinstance(obj, dict) or set(obj) != required:
        error("analysis fields do not match the output contract")
    for k in ("run_id", "book_id", "library_id", "file_hash", "lang"):
        if type(obj[k]) is not type(manifest[k]) or obj[k] != manifest[k]:
            error("analysis target mismatch: " + k)
    def strings(values, low, high, length):
        return isinstance(values, list) and low <= len(values) <= high and all(isinstance(x, str) and x.strip() and len(x) <= length for x in values)
    if not isinstance(obj["summary"], str) or not obj["summary"].strip() or len(obj["summary"]) > 1200:
        error("invalid summary")
    if not strings(obj["highlights"], 2, 8, 400) or not strings(obj["tags"], 1, 12, 100):
        error("invalid highlights/tags")
    if any("," in tag or "\0" in tag for tag in obj["tags"]):
        error("a tag must not contain comma/NUL")
    coverage = obj["coverage"]
    if not isinstance(coverage, dict) or set(coverage) != {"mode", "expected_files", "read_files", "read_chars", "part_ids"}:
        error("invalid coverage fields")
    parts = {p["id"]: p for p in manifest["source_files"]}
    read = coverage["part_ids"]
    if not strings(read, 1, len(parts), 120) or len(set(read)) != len(read) or set(read) - parts.keys():
        error("coverage contains unknown/duplicate/no parts")
    expected = {"expected_files": len(parts), "read_files": len(read), "read_chars": sum(parts[k]["chars"] for k in read)}
    if any(type(coverage[k]) is not int or coverage[k] != v for k, v in expected.items()):
        error("coverage counts do not match prepared source parts")
    full = set(read) == parts.keys()
    if coverage["mode"] != ("full" if full else "partial"):
        error("coverage mode does not match the reported parts")
    if not isinstance(obj["reread"], list) or not 1 <= len(obj["reread"]) <= 8:
        error("invalid reread items")
    for item in obj["reread"]:
        if not isinstance(item, dict) or set(item) != {"section", "page", "chunk_id", "reason"} or not all(isinstance(v, str) and v.strip() and len(v) <= 400 for v in item.values()) or item["chunk_id"] not in read:
            error("invalid reread anchor; use a reported source part id")
    return obj


def complete(ns):
    manifest = validate_manifest(ns.prepared_input, ns.expected_input_sha256)
    analysis = validate_analysis(read_json(ns.analysis_json), manifest)
    payload = {k: analysis[k] for k in ("summary", "highlights", "reread", "tags", "lang", "file_hash", "coverage")}
    payload["generated_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    proposal = {"id": manifest["book_id"], "expected_library": manifest["library_id"], "expected_uuid": manifest["book_uuid"], "analysis": payload}
    destination = Path(ns.proposal_jsonl).expanduser().resolve()
    write_new(destination, canonical(proposal) + b"\n")
    return {"ok": True, "status": "proposal_created", "remote_writes": False, "run_id": manifest["run_id"], "proposal_jsonl": str(destination), "coverage": analysis["coverage"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare", help="read/export/extract into a new immutable run directory")
    p.add_argument("--book-id", type=int, required=True)
    p.add_argument("--run-id", required=True)
    for k in ("with-library", "library-id", "config", "username", "password-env", "cache-dir"):
        p.add_argument("--" + k)
    p.add_argument("--format", choices=("EPUB", "PDF"), default="EPUB")
    p.add_argument("--lang", choices=("ja", "en"), default="ja")
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--min-text-chars", type=int, default=1200)
    p.add_argument("--chunk-chars", type=int, default=16000)
    p.add_argument("--force-low-text", action="store_true")
    c = sub.add_parser("complete", help="validate prepared evidence and analysis offline; produce JSONL only")
    for k in ("prepared-input", "analysis-json", "proposal-jsonl"):
        c.add_argument("--" + k, required=True)
    c.add_argument("--expected-input-sha256")
    ns = ap.parse_args()
    print(json.dumps(prepare(ns) if ns.command == "prepare" else complete(ns), ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
