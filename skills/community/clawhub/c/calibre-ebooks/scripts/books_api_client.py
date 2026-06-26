#!/usr/bin/env python3
"""Books API client for the calibre-ebooks OpenClaw skill."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urljoin, urlparse
from urllib.request import Request, urlopen


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_OUTPUT_ROOT = SKILL_DIR / "tmp" / "downloads"
TMP_OUTPUT_ROOT = Path("/tmp/calibre-ebooks")
QUERY_NAMES = ["q", "query", "search", "term", "text", "title", "author", "tag", "tags", "subject"]
LIMIT_NAMES = ["limit", "page_size", "pageSize", "per_page", "perPage", "size", "count"]
DEFAULT_BASE_URL = "http://127.0.0.1:6180"
SEARCH_STOPWORDS = {
    "a", "o", "e", "os", "as", "um", "uma", "uns", "umas", "de", "do", "da",
    "dos", "das", "em", "no", "na", "nos", "nas", "ao", "aos", "pelo",
    "pela", "por", "para", "com", "sem", "sobre", "que", "se", "como",
    "qual", "quais", "the", "of", "and", "to", "in", "for", "with",
    "book", "books", "ebook", "ebooks", "livro", "livros", "pdf", "epub",
    "algum", "alguma", "alguns", "algumas", "havia", "existe", "existem",
    "tem", "tenho", "tinha", "biblioteca", "acervo", "local", "procurar",
    "procure", "buscar", "busque", "pesquisar", "pesquise", "encontrar",
    "encontre",
}


def env_candidates() -> list[Path]:
    return [
        SCRIPT_DIR / ".env",
        SKILL_DIR / ".env",
        Path.cwd() / ".env",
    ]


def parse_env_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if stripped.startswith("export "):
        stripped = stripped[len("export "):].lstrip()
    if "=" not in stripped:
        return None
    key, value = stripped.split("=", 1)
    key = key.strip()
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", key):
        return None
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    else:
        value = re.sub(r"\s+#.*$", "", value).rstrip()
    return key, value


def search_terms(query: str, max_terms: int = 8) -> list[str]:
    import unicodedata

    normalized = unicodedata.normalize("NFKD", query or "")
    ascii_query = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    terms = []
    seen = set()
    for token in re.findall(r"[A-Za-zÀ-ÿ0-9]+", ascii_query.lower()):
        if len(token) < 3 or token in SEARCH_STOPWORDS:
            continue
        if token not in seen:
            terms.append(token)
            seen.add(token)
        if len(terms) >= max_terms:
            break
    return terms


def load_env_files() -> None:
    seen: set[Path] = set()
    for candidate in env_candidates():
        env_file = candidate.resolve()
        if env_file in seen or not env_file.is_file():
            continue
        seen.add(env_file)
        for line in env_file.read_text(encoding="utf-8").splitlines():
            parsed = parse_env_line(line)
            if not parsed:
                continue
            key, value = parsed
            os.environ.setdefault(key, value)


def base_url(value: str | None) -> str:
    return (value or os.environ.get("BOOKS_API_URL") or DEFAULT_BASE_URL).rstrip("/")


def api_key() -> str | None:
    value = os.environ.get("BOOKS_API_KEY") or os.environ.get("API_KEY")
    if value and value.strip():
        return value.strip()
    return None


def api_url(base: str, path: str, params: dict[str, str] | None = None) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        raise ValueError("Full URLs are not allowed here; pass an API path such as /api/books")
    url = urljoin(f"{base}/", path.lstrip("/"))
    if not params:
        return url
    query = urlencode({key: value for key, value in params.items() if value not in (None, "")})
    return f"{url}{'&' if urlparse(url).query else '?'}{query}" if query else url


def request_bytes(url: str, method: str = "GET", body: str | bytes | None = None, extra_headers: dict[str, str] | None = None) -> tuple[bytes, dict[str, str]]:
    headers = {}
    token = api_key()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if extra_headers:
        headers.update(extra_headers)
    data = None
    if body is not None:
        if isinstance(body, str):
            if "Content-Type" not in headers:
                headers["Content-Type"] = "application/json"
            data = body.encode("utf-8")
        else:
            data = body
    request = Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urlopen(request) as response:
            return response.read(), {key.lower(): value for key, value in response.headers.items()}
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"{method.upper()} {urlparse(url).path} failed: {error.code} {error.reason}"
            f"{chr(10) + detail if detail else ''}"
        ) from error
    except URLError as error:
        raise RuntimeError(f"{method.upper()} {urlparse(url).path} failed: {error.reason}") from error


def request_json(url: str, method: str = "GET", body: str | bytes | None = None, extra_headers: dict[str, str] | None = None) -> Any:
    payload, _headers = request_bytes(url, method=method, body=body, extra_headers=extra_headers)
    return json.loads(payload.decode("utf-8"))


def get_openapi(base: str) -> Any:
    return request_json(api_url(base, "/openapi.json"))


def operation_params(operation: dict[str, Any], location: str | None = None) -> list[dict[str, Any]]:
    return [param for param in operation.get("parameters", []) if location is None or param.get("in") == location]


def resolve_schema(schema: dict[str, Any], openapi: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(schema, dict):
        return {}
    if "$ref" in schema:
        ref = schema["$ref"]
        parts = ref.split("/")
        current = openapi
        for part in parts:
            if part == "#":
                continue
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return {}
        return resolve_schema(current, openapi)
    return schema


def get_request_body_properties(path: str, method: str, openapi: dict[str, Any]) -> list[str]:
    try:
        op = openapi.get("paths", {}).get(path, {}).get(method.lower(), {})
        body = op.get("requestBody", {})
        content = body.get("content", {})
        json_content = content.get("application/json", {})
        schema = json_content.get("schema", {})
        resolved = resolve_schema(schema, openapi)
        if resolved.get("type") == "object":
            return list(resolved.get("properties", {}).keys())
    except Exception:
        pass
    return []


def summarize_paths(openapi: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for path, item in openapi.get("paths", {}).items():
        for method, operation in item.items():
            if method not in {"get", "post", "put", "patch", "delete"}:
                continue
            rows.append(
                {
                    "method": method.upper(),
                    "path": path,
                    "operationId": operation.get("operationId"),
                    "summary": operation.get("summary"),
                    "query": [param["name"] for param in operation_params(operation, "query")],
                    "pathParams": [param["name"] for param in operation_params(operation, "path")],
                }
            )
    return rows


def score_search_candidate(row: dict[str, Any]) -> int:
    haystack = f"{row['path']} {row.get('operationId') or ''} {row.get('summary') or ''}".lower()
    score = 0
    if row["method"] == "GET":
        score += 2
    if any(name in QUERY_NAMES for name in row["query"]):
        score += 5
    if "search" in haystack:
        score += 4
    if "book" in haystack:
        score += 2
    if any(word in haystack for word in ("author", "title", "tag")):
        score += 1
    if row["pathParams"]:
        score -= 5
    return score


def find_search_candidates(openapi: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in summarize_paths(openapi):
        scored = {**row, "score": score_search_candidate(row)}
        if scored["score"] > 0 and scored["method"] == "GET":
            rows.append(scored)
    return sorted(rows, key=lambda item: item["score"], reverse=True)


def find_book_candidates(openapi: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in summarize_paths(openapi):
        if row["method"] != "GET" or not row["pathParams"]:
            continue
        haystack = f"{row['path']} {row.get('operationId') or ''} {row.get('summary') or ''}".lower()
        id_param = next((name for name in row["pathParams"] if re.search(r"(^id$|book.*id|calibre.*id)", name, re.I)), row["pathParams"][0])
        score = 0
        if "book" in haystack:
            score += 5
        if "format" in haystack:
            score += 1
        if re.search(r"book.*id|calibre.*id", id_param, re.I):
            score += 3
        if score > 0:
            rows.append({**row, "idParam": id_param, "score": score})
    return sorted(rows, key=lambda item: item["score"], reverse=True)


def score_semantic_candidate(row: dict[str, Any], openapi: dict[str, Any]) -> int:
    haystack = f"{row['path']} {row.get('operationId') or ''} {row.get('summary') or ''}".lower()
    score = 0
    if row["method"] == "POST":
        score += 2
        body_props = get_request_body_properties(row["path"], "POST", openapi)
        if any(p in body_props for p in ["query", "q", "text"]):
            score += 5
        if any(p in body_props for p in ["limit", "threshold", "score"]):
            score += 2
    elif row["method"] == "GET":
        score += 1
        if any(p in row["query"] for p in ["query", "q", "text"]):
            score += 3
    keywords = ["semantic", "rag", "content", "vector", "embedding", "excerpt", "context"]
    for word in keywords:
        if word in haystack:
            score += 4
    if row["pathParams"]:
        score -= 5
    return score


def find_semantic_candidates(openapi: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in summarize_paths(openapi):
        scored = {**row, "score": score_semantic_candidate(row, openapi)}
        if scored["score"] > 0:
            rows.append(scored)
    return sorted(rows, key=lambda item: item["score"], reverse=True)


def score_download_candidate(row: dict[str, Any]) -> int:
    haystack = f"{row['path']} {row.get('operationId') or ''} {row.get('summary') or ''}".lower()
    score = 0
    if row["method"] == "GET" and row["pathParams"]:
        score += 2
        id_param = row["pathParams"][0]
        if re.search(r"(^id$|book.*id|calibre.*id)", id_param, re.I):
            score += 3
        if "file" in haystack:
            score += 4
        if "download" in haystack:
            score += 4
        if any(fmt in haystack for fmt in ["epub", "pdf", "mobi", "azw3"]):
            score += 2
        if "cover" in haystack or "image" in haystack:
            score -= 10
        if "openlibrary" in haystack:
            score -= 2
    return score


def find_download_candidates(openapi: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in summarize_paths(openapi):
        scored = {**row, "score": score_download_candidate(row)}
        if scored["score"] > 0:
            rows.append(scored)
    return sorted(rows, key=lambda item: item["score"], reverse=True)


def score_cover_candidate(row: dict[str, Any]) -> int:
    haystack = f"{row['path']} {row.get('operationId') or ''} {row.get('summary') or ''}".lower()
    score = 0
    if row["method"] == "GET" and row["pathParams"]:
        score += 2
        id_param = row["pathParams"][0]
        if re.search(r"(^id$|book.*id|calibre.*id)", id_param, re.I):
            score += 3
        if "cover" in haystack:
            score += 6
        if "image" in haystack or "thumbnail" in haystack:
            score += 3
        if "file" in haystack or "download" in haystack:
            score -= 2
    return score


def find_cover_candidates(openapi: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in summarize_paths(openapi):
        scored = {**row, "score": score_cover_candidate(row)}
        if scored["score"] > 0:
            rows.append(scored)
    return sorted(rows, key=lambda item: item["score"], reverse=True)


def score_stats_candidate(row: dict[str, Any]) -> int:
    haystack = f"{row['path']} {row.get('operationId') or ''} {row.get('summary') or ''}".lower()
    score = 0
    if row["method"] == "GET" and not row["pathParams"]:
        if "stats" in haystack or "statistics" in haystack:
            score += 6
        if "summary" in haystack:
            score += 3
        if "library" in haystack:
            score += 2
        if "count" in haystack:
            score += 1
    return score


def find_stats_candidates(openapi: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in summarize_paths(openapi):
        scored = {**row, "score": score_stats_candidate(row)}
        if scored["score"] > 0:
            rows.append(scored)
    return sorted(rows, key=lambda item: item["score"], reverse=True)


def score_status_candidate(row: dict[str, Any]) -> int:
    haystack = f"{row['path']} {row.get('operationId') or ''} {row.get('summary') or ''}".lower()
    score = 0
    if row["method"] == "GET" and not row["pathParams"]:
        if "health" in haystack:
            score += 5
        if "status" in haystack:
            score += 4
        if "db" in haystack or "database" in haystack:
            score += 2
        if "calibre" in haystack:
            score += 1
    return score


def find_status_candidates(openapi: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in summarize_paths(openapi):
        scored = {**row, "score": score_status_candidate(row)}
        if scored["score"] > 0:
            rows.append(scored)
    return sorted(rows, key=lambda item: item["score"], reverse=True)


def score_upload_candidate(row: dict[str, Any]) -> int:
    haystack = f"{row['path']} {row.get('operationId') or ''} {row.get('summary') or ''}".lower()
    score = 0
    if row["method"] in {"POST", "PUT"}:
        if "upload" in haystack:
            score += 6
        if "import" in haystack:
            score += 4
        if "add" in haystack:
            score += 3
        if "file" in haystack:
            score += 1
    return score


def find_upload_candidates(openapi: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in summarize_paths(openapi):
        scored = {**row, "score": score_upload_candidate(row)}
        if scored["score"] > 0:
            rows.append(scored)
    return sorted(rows, key=lambda item: item["score"], reverse=True)


def score_queue_candidate(row: dict[str, Any]) -> int:
    haystack = f"{row['path']} {row.get('operationId') or ''} {row.get('summary') or ''}".lower()
    score = 0
    if row["method"] == "POST":
        if "downloads/queue" in row["path"]:
            score += 10
        elif "queue" in haystack and "download" in haystack:
            score += 8
        elif "queue" in haystack:
            score += 4
    return score


def find_queue_candidates(openapi: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in summarize_paths(openapi):
        scored = {**row, "score": score_queue_candidate(row)}
        if scored["score"] > 0:
            rows.append(scored)
    return sorted(rows, key=lambda item: item["score"], reverse=True)



def replace_path_param(path: str, name: str, value: str) -> str:
    return path.replace(f"{{{name}}}", quote(str(value), safe=""))


def map_path_params(path: str, path_params: list[str], provided_args: dict[str, Any]) -> str:
    for name in path_params:
        value = None
        if name in provided_args:
            value = provided_args[name]
        elif len(provided_args) == 1:
            value = list(provided_args.values())[0]
        else:
            for k, v in provided_args.items():
                if k.lower() in name.lower() or name.lower() in k.lower():
                    value = v
                    break
        if value is None:
            raise ValueError(f"Missing required path parameter: {name}")
        path = replace_path_param(path, name, value)
    return path


def map_query_params(candidate_query: list[str], provided_args: dict[str, Any]) -> dict[str, str]:
    params = {}
    for name in candidate_query:
        for key, val in provided_args.items():
            if val is None:
                continue
            is_match = False
            if key.lower() == name.lower():
                is_match = True
            elif key == "query" and name in QUERY_NAMES:
                is_match = True
            elif key == "limit" and name in LIMIT_NAMES:
                is_match = True
            elif key == "threshold" and name in ["threshold", "score", "min_score", "minScore"]:
                is_match = True
            elif key == "format" and name in ["format", "fmt", "ext", "extension"]:
                is_match = True
            elif key == "check_virus" and name in ["check_virus", "checkVirus", "virus_scan", "scan"]:
                is_match = True
            
            if is_match:
                params[name] = str(val)
                break
    return params


def build_multipart_formdata(fields: dict[str, str], files: dict[str, tuple[str, bytes]]) -> tuple[bytes, str]:
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = []
    for key, value in fields.items():
        body.append(f"--{boundary}".encode("utf-8"))
        body.append(f'Content-Disposition: form-data; name="{key}"'.encode("utf-8"))
        body.append(b"")
        body.append(value.encode("utf-8"))
    for key, (filename, content) in files.items():
        body.append(f"--{boundary}".encode("utf-8"))
        body.append(f'Content-Disposition: form-data; name="{key}"; filename="{filename}"'.encode("utf-8"))
        ext = Path(filename).suffix.lower()
        content_type = "application/octet-stream"
        if ext == ".pdf":
            content_type = "application/pdf"
        elif ext == ".epub":
            content_type = "application/epub+zip"
        body.append(f"Content-Type: {content_type}".encode("utf-8"))
        body.append(b"")
        body.append(content)
    body.append(f"--{boundary}--".encode("utf-8"))
    body.append(b"")
    payload = b"\r\n".join(body)
    return payload, f"multipart/form-data; boundary={boundary}"


def parse_query_pairs(pairs: list[str]) -> dict[str, str]:
    params = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"Invalid --query value, expected key=value: {pair}")
        key, value = pair.split("=", 1)
        params[key] = value
    return params


def content_disposition_filename(header: str | None) -> str | None:
    if not header:
        return None
    encoded = re.search(r"filename\*=UTF-8''([^;]+)", header, re.I)
    if encoded:
        return quote(encoded.group(1).strip().strip('"'), safe="%").replace("%25", "%")
    plain = re.search(r'filename="?([^";]+)"?', header, re.I)
    return plain.group(1).strip() if plain else None


def safe_basename(name: str | None) -> str:
    cleaned = re.sub(r"[^\w .()+\-[\]]+", "_", name or "", flags=re.UNICODE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or "download"


def fallback_filename(path_value: str, headers: dict[str, str], content_type: str) -> str:
    from_header = content_disposition_filename(headers.get("content-disposition"))
    if from_header:
        return safe_basename(from_header)
    fmt = headers.get("x-book-format")
    extension_by_type = {
        "application/pdf": ".pdf",
        "application/epub+zip": ".epub",
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "text/markdown": ".md",
        "text/plain": ".txt",
    }
    extension = f".{fmt.lower()}" if fmt else extension_by_type.get(content_type.split(";")[0], "")
    base = "-".join(part for part in path_value.split("?")[0].split("/") if part)
    return safe_basename(f"{base or 'download'}{extension}")


def resolve_output_path(output: str | None, output_dir: str | None, request_path: str, headers: dict[str, str], content_type: str) -> Path | None:
    filename = fallback_filename(request_path, headers, content_type)
    if output_dir:
        output_dir_path = Path(output_dir)
        output_path = checked_output_path(output_dir_path / filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return output_path
    if not output:
        return None
    output_path = Path(output)
    if output.endswith("/") or output_path.is_dir():
        output_path = checked_output_path(output_path / filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return output_path
    output_path = checked_output_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def checked_output_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.environ.get("ALLOW_ARBITRARY_OUTPUT_PATH", "").lower() in {"1", "true", "yes", "s", "sim"}:
        return resolved
    allowed_roots = [DEFAULT_OUTPUT_ROOT.resolve(), TMP_OUTPUT_ROOT.resolve()]
    if any(resolved.is_relative_to(root) for root in allowed_roots):
        return resolved
    raise RuntimeError(
        "Refusing to write outside skills/calibre-ebooks/tmp/downloads or /tmp/calibre-ebooks. "
        "Set ALLOW_ARBITRARY_OUTPUT_PATH=true to override."
    )


def command_search(base: str, openapi: dict[str, Any], query: str, limit: str | None) -> dict[str, Any]:
    attempted = []
    for candidate in find_search_candidates(openapi):
        query_name = next((name for name in candidate["query"] if name in QUERY_NAMES), candidate["query"][0] if candidate["query"] else None)
        if not query_name:
            continue
        retry_queries = [query] + [term for term in search_terms(query) if term != query.strip().lower()]
        for retry_query in retry_queries:
            params = {query_name: retry_query}
            limit_name = next((name for name in candidate["query"] if name in LIMIT_NAMES), None)
            if limit_name and limit:
                params[limit_name] = limit
            attempted.append({"method": candidate["method"], "path": candidate["path"], "params": params})
            try:
                data = request_json(api_url(base, candidate["path"], params))
                if data or retry_query == retry_queries[-1]:
                    return {
                        "endpoint": {"method": candidate["method"], "path": candidate["path"]},
                        "params": params,
                        "fallbackQuery": retry_query if retry_query != query else None,
                        "data": data,
                    }
            except RuntimeError as error:
                attempted[-1]["error"] = str(error)
    raise RuntimeError(f"No usable search endpoint succeeded. Candidates:\n{json.dumps(attempted, ensure_ascii=False, indent=2)}")


def command_semantic_search(base: str, openapi: dict[str, Any], query: str, limit: int | None, threshold: float | None) -> dict[str, Any]:
    candidates = find_semantic_candidates(openapi)
    if not candidates:
        raise RuntimeError("No semantic search endpoint found in OpenAPI.")
    
    candidate = candidates[0]
    provided = {"query": query, "limit": limit, "threshold": threshold}
    
    if candidate["method"] == "POST":
        body_props = get_request_body_properties(candidate["path"], "POST", openapi)
        body = {}
        query_prop = next((p for p in body_props if p in QUERY_NAMES), "query")
        body[query_prop] = query
        
        limit_prop = next((p for p in body_props if p in LIMIT_NAMES), None)
        if limit_prop and limit is not None:
            body[limit_prop] = int(limit)
            
        threshold_prop = next((p for p in body_props if p in ["threshold", "score", "min_score", "minScore"]), None)
        if threshold_prop and threshold is not None:
            body[threshold_prop] = float(threshold)
            
        url = api_url(base, candidate["path"])
        data = request_json(url, method="POST", body=json.dumps(body, ensure_ascii=False))
        return {
            "endpoint": {"method": "POST", "path": candidate["path"]},
            "body": body,
            "data": data,
        }
    else:
        params = map_query_params(candidate["query"], provided)
        url = api_url(base, candidate["path"], params)
        data = request_json(url, method="GET")
        return {
            "endpoint": {"method": "GET", "path": candidate["path"]},
            "params": params,
            "data": data,
        }


def command_book(base: str, openapi: dict[str, Any], book_id: str) -> dict[str, Any]:
    attempted = []
    for candidate in find_book_candidates(openapi):
        path = replace_path_param(candidate["path"], candidate["idParam"], book_id)
        attempted.append({"method": candidate["method"], "path": path})
        try:
            data = request_json(api_url(base, path))
            return {"endpoint": {"method": candidate["method"], "path": candidate["path"]}, "id": book_id, "data": data}
        except RuntimeError as error:
            attempted[-1]["error"] = str(error)
    raise RuntimeError(f"No usable book detail endpoint succeeded. Candidates:\n{json.dumps(attempted, ensure_ascii=False, indent=2)}")


def command_download(base: str, openapi: dict[str, Any], book_id: str, args: argparse.Namespace) -> Any:
    candidates = find_download_candidates(openapi)
    if not candidates:
        raise RuntimeError("No download/file endpoint found in OpenAPI.")
    
    candidate = candidates[0]
    path = map_path_params(candidate["path"], candidate["pathParams"], {"book_id": book_id})
    
    provided = {}
    if getattr(args, "format", None):
        provided["format"] = args.format
    if getattr(args, "check_virus", None):
        provided["check_virus"] = args.check_virus
    params = map_query_params(candidate["query"], provided)
    
    url = api_url(base, path, params)
    payload, headers = request_bytes(url, method="GET")
    content_type = headers.get("content-type", "")
    
    output_path = resolve_output_path(args.output, args.output_dir, path, headers, content_type)
    if output_path:
        output_path.write_bytes(payload)
        return {
            "endpoint": {"method": "GET", "path": candidate["path"]},
            "output": str(output_path),
            "bytes": len(payload),
            "contentType": content_type
        }
    if "application/json" in content_type:
        return json.loads(payload.decode("utf-8"))
    return payload.decode("utf-8", errors="replace")


def command_cover(base: str, openapi: dict[str, Any], book_id: str, args: argparse.Namespace) -> Any:
    candidates = find_cover_candidates(openapi)
    if not candidates:
        raise RuntimeError("No cover endpoint found in OpenAPI.")
    
    candidate = candidates[0]
    path = map_path_params(candidate["path"], candidate["pathParams"], {"book_id": book_id})
    
    url = api_url(base, path)
    payload, headers = request_bytes(url, method="GET")
    content_type = headers.get("content-type", "")
    
    output_path = resolve_output_path(args.output, args.output_dir, path, headers, content_type)
    if output_path:
        output_path.write_bytes(payload)
        return {
            "endpoint": {"method": "GET", "path": candidate["path"]},
            "output": str(output_path),
            "bytes": len(payload),
            "contentType": content_type
        }
    if "application/json" in content_type:
        return json.loads(payload.decode("utf-8"))
    return payload.decode("utf-8", errors="replace")


def command_stats(base: str, openapi: dict[str, Any]) -> Any:
    candidates = find_stats_candidates(openapi)
    if not candidates:
        raise RuntimeError("No library/stats endpoint found in OpenAPI.")
    
    candidate = candidates[0]
    url = api_url(base, candidate["path"])
    return {
        "endpoint": {"method": "GET", "path": candidate["path"]},
        "data": request_json(url, method="GET")
    }


def command_status(base: str, openapi: dict[str, Any]) -> Any:
    candidates = find_status_candidates(openapi)
    if not candidates:
        raise RuntimeError("No health/status endpoint found in OpenAPI.")
    
    candidate = candidates[0]
    url = api_url(base, candidate["path"])
    return {
        "endpoint": {"method": "GET", "path": candidate["path"]},
        "data": request_json(url, method="GET")
    }


def command_upload(base: str, openapi: dict[str, Any], file_path: str, check_virus: bool) -> Any:
    candidates = find_upload_candidates(openapi)
    if not candidates:
        raise RuntimeError("No upload/import endpoint found in OpenAPI.")
    
    candidate = candidates[0]
    path_obj = Path(file_path)
    if not path_obj.is_file():
        raise RuntimeError(f"File not found: {file_path}")
        
    content = path_obj.read_bytes()
    file_field_name = "file"
    
    fields = {}
    if check_virus:
        if "check_virus" not in candidate["query"]:
            fields["check_virus"] = "true"
            
    files = {file_field_name: (path_obj.name, content)}
    body_payload, content_type_header = build_multipart_formdata(fields, files)
    
    headers = {"Content-Type": content_type_header}
    provided = {}
    if check_virus:
        provided["check_virus"] = "true"
    params = map_query_params(candidate["query"], provided)
    
    url = api_url(base, candidate["path"], params)
    payload, resp_headers = request_bytes(url, method=candidate["method"], body=body_payload, extra_headers=headers)
    resp_content_type = resp_headers.get("content-type", "")
    if "application/json" in resp_content_type:
        return {
            "endpoint": {"method": candidate["method"], "path": candidate["path"]},
            "data": json.loads(payload.decode("utf-8"))
        }
    return {
        "endpoint": {"method": candidate["method"], "path": candidate["path"]},
        "data": payload.decode("utf-8", errors="replace")
    }


def command_queue(base: str, openapi: dict[str, Any], title: str, args: argparse.Namespace) -> Any:
    candidates = find_queue_candidates(openapi)
    if not candidates:
        raise RuntimeError("No queue endpoint found in OpenAPI.")
    
    candidate = candidates[0]
    
    body = {
        "title": title,
        "author": args.author,
        "source": args.source,
        "source_id": args.source_id,
        "olid": args.olid,
        "ocaid": args.ocaid,
        "download_url": args.download_url,
        "preferred_format": args.preferred_format,
        "priority": args.priority
    }
    
    body = {k: v for k, v in body.items() if v is not None}
    
    url = api_url(base, candidate["path"])
    payload, headers = request_bytes(url, method=candidate["method"], body=json.dumps(body), extra_headers={"Content-Type": "application/json"})
    
    content_type = headers.get("content-type", "")
    if "application/json" in content_type:
        return {
            "endpoint": {"method": candidate["method"], "path": candidate["path"]},
            "data": json.loads(payload.decode("utf-8"))
        }
    return {
        "endpoint": {"method": candidate["method"], "path": candidate["path"]},
        "data": payload.decode("utf-8", errors="replace")
    }


def command_find(openapi: dict[str, Any], keyword: str) -> list[dict[str, Any]]:
    keyword = keyword.lower()
    matches = []
    for row in summarize_paths(openapi):
        haystack = f"{row['path']} {row.get('operationId') or ''} {row.get('summary') or ''}".lower()
        if keyword in haystack:
            matches.append(row)
    return matches


def command_request(base: str, method: str, path: str, args: argparse.Namespace) -> Any:
    parsed_path = urlparse(path)
    if parsed_path.scheme or parsed_path.netloc:
        raise RuntimeError("Full URLs are not allowed for request; pass a local /api/... path.")
    if not path.startswith("/api/"):
        raise RuntimeError("request is limited to /api/... paths.")
    if method != "GET" and os.environ.get("ALLOW_MUTATING_API_REQUESTS", "").lower() not in {"1", "true", "yes", "s", "sim"}:
        raise RuntimeError("Mutating API requests are disabled. Set ALLOW_MUTATING_API_REQUESTS=true to enable them.")
    if args.body and method == "GET":
        raise RuntimeError("GET requests cannot include --body.")
    params = parse_query_pairs(args.query)
    payload, headers = request_bytes(api_url(base, path, params), method=method, body=args.body)
    content_type = headers.get("content-type", "")
    output_path = resolve_output_path(args.output, args.output_dir, path, headers, content_type)
    if output_path:
        output_path.write_bytes(payload)
        return {"output": str(output_path), "bytes": len(payload), "contentType": content_type}
    if "application/json" in content_type:
        return json.loads(payload.decode("utf-8"))
    return payload.decode("utf-8", errors="replace")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Client for the local Calibre-backed Books API.",
        epilog=(
            "Examples:\n"
            "  books_api_client.py docs\n"
            "  books_api_client.py paths\n"
            "  books_api_client.py search \"python\" --limit 10\n"
            "  books_api_client.py semantic \"ethics and virtue\" --limit 5 --threshold 0.25\n"
            "  books_api_client.py book 123\n"
            "  books_api_client.py download 123 --output-dir tmp/downloads\n"
            "  books_api_client.py cover 123 --output-dir tmp/calibre-covers\n"
            "  books_api_client.py stats\n"
            "  books_api_client.py status\n"
            "  books_api_client.py upload ebook.pdf --check-virus\n"
            "  books_api_client.py find \"enrich\"\n"
            "  books_api_client.py request GET /api/books --query limit=100"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--base",
        metavar="URL",
        help=(
            "Books API base URL. Overrides BOOKS_API_URL and the default "
            f"{DEFAULT_BASE_URL}."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("docs", help="Print Swagger, ReDoc, and OpenAPI URLs for the selected API base.")
    sub.add_parser("openapi", help="Fetch and print the current OpenAPI JSON document.")
    sub.add_parser("paths", help="Print API paths, methods, operation IDs, and path/query parameters.")

    search = sub.add_parser(
        "search",
        help="Search books using the best matching GET endpoint discovered from OpenAPI.",
    )
    search.add_argument("query", help="Search text, such as a title, author, tag, subject, or free term.")
    search.add_argument(
        "--limit",
        metavar="N",
        help="Maximum number of results when the discovered endpoint exposes a supported limit parameter.",
    )

    semantic = sub.add_parser(
        "semantic",
        help="Search embedded book content through the Books API semantic/RAG endpoint discovered dynamically.",
    )
    semantic.add_argument("query", help="Question, topic, or phrase to search in embedded book content.")
    semantic.add_argument(
        "--limit",
        metavar="N",
        type=int,
        default=10,
        help="Maximum number of semantic results, clamped to 1-50.",
    )
    semantic.add_argument(
        "--threshold",
        metavar="VALUE",
        type=float,
        default=0.3,
        help="Minimum similarity threshold, clamped to 0.0-1.0.",
    )

    book = sub.add_parser(
        "book",
        help="Fetch book details by ID using the best matching detail endpoint discovered from OpenAPI.",
    )
    book.add_argument("book_id", help="Book identifier accepted by the API path parameter.")

    download = sub.add_parser(
        "download",
        help="Download book file by ID using the best matching endpoint discovered dynamically.",
    )
    download.add_argument("book_id", help="Book identifier.")
    download.add_argument("--format", help="Optional desired format.")
    download.add_argument("--check-virus", action="store_true", help="Enable virus scan on download if supported.")
    download.add_argument("--output", help="Write to this file or directory.")
    download.add_argument("--output-dir", help="Write to this directory with API-provided filename.")

    cover = sub.add_parser(
        "cover",
        help="Download cover image by ID using the best matching endpoint discovered dynamically.",
    )
    cover.add_argument("book_id", help="Book identifier.")
    cover.add_argument("--output", help="Write to this file or directory.")
    cover.add_argument("--output-dir", help="Write to this directory with API-provided filename.")

    sub.add_parser("stats", help="Get library stats using the best matching endpoint discovered dynamically.")
    sub.add_parser("status", help="Get database status using the best matching endpoint discovered dynamically.")

    upload = sub.add_parser(
        "upload",
        help="Upload an ebook file using the best matching endpoint discovered dynamically.",
    )
    upload.add_argument("file_path", help="Path to local file to upload.")
    upload.add_argument("--check-virus", action="store_true", help="Enable virus scan on upload if supported.")

    queue = sub.add_parser(
        "queue",
        help="Add a book to the download queue using the best matching endpoint discovered dynamically.",
    )
    queue.add_argument("title", help="Book title.")
    queue.add_argument("--author", help="Book author.")
    queue.add_argument("--source", default="openlibrary", help="Source: 'openlibrary' or 'archive'.")
    queue.add_argument("--source-id", help="Source-specific ID.")
    queue.add_argument("--olid", help="OpenLibrary ID.")
    queue.add_argument("--ocaid", help="Archive.org ID.")
    queue.add_argument("--download-url", help="Direct download URL.")
    queue.add_argument("--preferred-format", default="PDF", help="Preferred format: PDF, EPUB, Kindle.")
    queue.add_argument("--priority", type=int, default=0, help="Download priority (higher = first).")

    find = sub.add_parser(
        "find",
        help="Search the OpenAPI schema for endpoints matching a keyword.",
    )
    find.add_argument("keyword", help="Keyword to search in paths, summaries, and operation IDs.")

    request = sub.add_parser(
        "request",
        help="Call an explicit API endpoint after inspecting OpenAPI.",
    )
    request.add_argument(
        "method",
        type=str.upper,
        help="HTTP method to send. Non-GET methods require ALLOW_MUTATING_API_REQUESTS=true.",
    )
    request.add_argument(
        "path",
        help="Books API path such as /api/books. Full http(s) URLs are rejected.",
    )
    request.add_argument(
        "--query",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Query string pair. Repeat for multiple parameters.",
    )
    request.add_argument(
        "--body",
        metavar="JSON",
        help="Raw JSON request body. Content-Type is set to application/json.",
    )
    request.add_argument(
        "--output",
        metavar="PATH",
        help=(
            "Write a non-JSON or file response to this file or directory. "
            "If PATH ends with / or is an existing directory, the API filename is used. "
            "By default writes are limited to skills/calibre-ebooks/tmp/downloads or /tmp/calibre-ebooks."
        ),
    )
    request.add_argument(
        "--output-dir",
        metavar="DIR",
        help="Write the response into DIR using the API-provided filename or a safe fallback filename.",
    )
    return parser


def print_result(data: Any) -> None:
    if isinstance(data, str):
        print(data)
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


def main(argv: list[str]) -> int:
    load_env_files()
    args = build_parser().parse_args(argv)
    base = base_url(args.base)

    if args.command == "docs":
        print_result({"swagger": f"{base}/docs", "redoc": f"{base}/redoc", "openapi": f"{base}/openapi.json"})
    elif args.command == "openapi":
        print_result(get_openapi(base))
    elif args.command == "paths":
        print_result(summarize_paths(get_openapi(base)))
    elif args.command == "search":
        print_result(command_search(base, get_openapi(base), args.query, args.limit))
    elif args.command == "semantic":
        print_result(command_semantic_search(base, get_openapi(base), args.query, args.limit, args.threshold))
    elif args.command == "book":
        print_result(command_book(base, get_openapi(base), args.book_id))
    elif args.command == "download":
        print_result(command_download(base, get_openapi(base), args.book_id, args))
    elif args.command == "cover":
        print_result(command_cover(base, get_openapi(base), args.book_id, args))
    elif args.command == "stats":
        print_result(command_stats(base, get_openapi(base)))
    elif args.command == "status":
        print_result(command_status(base, get_openapi(base)))
    elif args.command == "upload":
        print_result(command_upload(base, get_openapi(base), args.file_path, args.check_virus))
    elif args.command == "queue":
        print_result(command_queue(base, get_openapi(base), args.title, args))
    elif args.command == "find":
        print_result(command_find(get_openapi(base), args.keyword))
    elif args.command == "request":
        print_result(command_request(base, args.method, args.path, args))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except Exception as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
