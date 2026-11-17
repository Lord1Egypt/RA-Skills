"""Small client for the EmpirioLabs AI API, shared by the EmpirioLabs AI agent skills.

Python 3.8 or later, standard library only. The source of truth is
shared/empiriolabs_api.py in https://github.com/EmpirioLabs-AI/skills, and each
skill carries an identical copy in its scripts/ folder so it works on its own.

The API key is read from the EMPIRIOLABS_API_KEY environment variable. It is
sent only to the EmpirioLabs AI API host, in the Authorization header, and is
never printed, logged, or written to disk.
"""

from __future__ import annotations

import base64
import gzip
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

__version__ = "1.0.0"

API_BASE = "https://api.empiriolabs.ai/v1"
KEY_ENV = "EMPIRIOLABS_API_KEY"
KEYS_URL = "https://platform.empiriolabs.ai/dashboard/api-keys"
BILLING_URL = "https://platform.empiriolabs.ai/dashboard/billing"
DOCS_URL = "https://docs.empiriolabs.ai"
USER_AGENT = "empiriolabs-skills/" + __version__ + " (python-urllib)"

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_USAGE = 2
EXIT_TIMEOUT = 3

JOB_RUNNING = {"queued", "pending", "processing", "running", "in_progress", "starting", "submitted"}
JOB_SUCCEEDED = {"completed", "succeeded", "success", "done"}
JOB_FAILED = {"failed", "error", "cancelled", "canceled", "expired", "rejected"}

RETRY_STATUSES = {429, 500, 502, 503, 504}
MAX_INLINE_BYTES = 20 * 1024 * 1024

_EXTENSIONS = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/webp": ".webp",
    "image/gif": ".gif",
    "image/avif": ".avif",
    "video/mp4": ".mp4",
    "video/webm": ".webm",
    "video/quicktime": ".mov",
    "audio/mpeg": ".mp3",
    "audio/mp3": ".mp3",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/wave": ".wav",
    "audio/ogg": ".ogg",
    "audio/opus": ".opus",
    "audio/flac": ".flac",
    "audio/x-flac": ".flac",
    "audio/aac": ".aac",
    "audio/mp4": ".m4a",
    "audio/x-m4a": ".m4a",
    "audio/pcm": ".pcm",
    "audio/l16": ".pcm",
}
_KNOWN_SUFFIXES = set(_EXTENSIONS.values()) | {".jpeg", ".mpga", ".m4v", ".glb"}
_KEY_SHAPE = re.compile(r"sk-empiriolabs-[A-Za-z0-9_\-]+")
_ERROR_HINTS = {
    401: "Check that " + KEY_ENV + " holds a valid key. Keys are managed at " + KEYS_URL + ".",
    402: "Add credits at " + BILLING_URL + ", then run the command again.",
    404: "Check the model id or job id. List models with --list-models.",
    413: "The input is too large. Pass a URL to the file instead of a local copy.",
    429: "Too many requests right now. Wait a moment and run the command again.",
}


class ApiError(Exception):
    """A request failed. The message is safe to show to the user."""

    def __init__(self, message, status=None, code=None, kind=None, exit_code=EXIT_ERROR):
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.kind = kind
        self.exit_code = exit_code


class JobTimeout(ApiError):
    """A job was still running when the wait limit was reached."""

    def __init__(self, job_id, status, waited):
        super().__init__(
            "Job " + str(job_id) + " is still " + str(status or "running") + " after "
            + str(int(waited)) + " seconds.",
            code="job_timeout",
            exit_code=EXIT_TIMEOUT,
        )
        self.job_id = job_id
        self.job_status = status


class Response:
    """Status, lower-cased headers, and body of an HTTP response."""

    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body

    @property
    def content_type(self):
        return (self.headers.get("content-type") or "").split(";")[0].strip().lower()

    def json(self):
        try:
            return json.loads(self.body.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            raise ApiError("The service returned a response that is not valid JSON.", status=self.status)


# ---------------------------------------------------------------------------
# Console helpers
# ---------------------------------------------------------------------------

def setup_console():
    """Never crash on characters the console cannot show."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass


def log(message):
    """Progress lines go to stderr so stdout stays machine-readable."""
    sys.stdout.flush()
    print(redact(str(message)), file=sys.stderr, flush=True)


def print_json(payload):
    print(redact(json.dumps(payload, indent=2, ensure_ascii=False)), flush=True)


def redact(text):
    """Remove anything shaped like an EmpirioLabs AI key from text we print."""
    if not text:
        return text
    current = (os.environ.get(KEY_ENV) or "").strip()
    if current and len(current) >= 8:
        text = text.replace(current, "[redacted]")
    return _KEY_SHAPE.sub("sk-empiriolabs-[redacted]", text)


def fail(error):
    """Print an error and return the exit code for it."""
    log("Error: " + (error.message if isinstance(error, ApiError) else str(error)))
    return error.exit_code if isinstance(error, ApiError) else EXIT_ERROR


def resume_hint(script, job_id, out=None):
    """The command that picks up a job that is still running."""
    parts = ["python3", "scripts/" + script, "--job-id", str(job_id)]
    if out:
        parts += ["--out", out]
    quoted = ['"' + p + '"' if re.search(r"\s", p) else p for p in parts]
    return "Resume later with: " + " ".join(quoted)


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

def api_key(required=True):
    value = (os.environ.get(KEY_ENV) or "").strip()
    if not value and required:
        raise ApiError(
            KEY_ENV + " is not set. Create an API key at " + KEYS_URL
            + " and set it as an environment variable before running this command.",
            code="missing_api_key",
        )
    return value


def api_url(path):
    if path.startswith(("http://", "https://")):
        return path
    if path.startswith("/v1/"):
        path = path[3:]
    return API_BASE + (path if path.startswith("/") else "/" + path)


def is_api_url(url):
    target = urllib.parse.urlsplit(url)
    base = urllib.parse.urlsplit(API_BASE)
    return target.scheme == base.scheme and target.netloc.lower() == base.netloc.lower()


def _open(req, timeout):
    """The single network call. Tests replace this function."""
    return urllib.request.urlopen(req, timeout=timeout)


def _read(resp):
    body = resp.read()
    headers = {k.lower(): v for k, v in resp.headers.items()}
    if headers.get("content-encoding", "").lower() == "gzip":
        body = gzip.decompress(body)
    return body, headers


def _retry_after(headers, attempt):
    value = (headers or {}).get("retry-after")
    try:
        return max(0.5, min(float(value), 30.0))
    except (TypeError, ValueError):
        return min(2.0 ** attempt, 20.0)


def _error_message(status, body, reason):
    message = code = kind = None
    try:
        payload = json.loads(body.decode("utf-8")) if body else None
    except (ValueError, UnicodeDecodeError):
        payload = None
    if isinstance(payload, dict):
        err = payload.get("error")
        if isinstance(err, dict):
            message = err.get("message")
            code = err.get("code")
            kind = err.get("type")
        elif isinstance(err, str):
            message = err
        detail = payload.get("detail")
        if not message and isinstance(detail, str):
            message = detail
        elif not message and isinstance(detail, dict):
            message = detail.get("message") or detail.get("detail")
        elif not message and isinstance(detail, list) and detail:
            first = detail[0]
            message = first.get("msg") if isinstance(first, dict) else str(first)
        if not message and isinstance(payload.get("message"), str):
            message = payload["message"]
    if not message:
        text = body.decode("utf-8", "replace").strip() if body else ""
        message = text[:300] if text and not text.startswith("<") else (reason or "Request failed")
    message = "HTTP " + str(status) + ": " + str(message)
    hint = _ERROR_HINTS.get(status)
    if hint:
        message += " " + hint
    return redact(message), code, kind


def request(method, path, json_body=None, data=None, content_type=None, auth=True,
            timeout=60.0, retries=None, accept="application/json"):
    """Send one API request and return a Response, raising ApiError on failure.

    GET requests retry on rate limits, server errors, and network errors.
    Other methods retry only when the service answers 429, because a request
    that failed in flight may already have been processed and billed.
    """
    url = api_url(path)
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    if accept == "application/json":
        headers["Accept-Encoding"] = "gzip"
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        content_type = "application/json"
    if content_type:
        headers["Content-Type"] = content_type
    if auth and is_api_url(url):
        headers["Authorization"] = "Bearer " + api_key()
    idempotent = method.upper() in ("GET", "HEAD")
    attempts = (retries if retries is not None else 4) if idempotent else 3
    for attempt in range(1, attempts + 1):
        req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
        try:
            with _open(req, timeout) as resp:
                body, resp_headers = _read(resp)
                return Response(resp.status, resp_headers, body)
        except urllib.error.HTTPError as exc:
            body = exc.read() if exc.fp is not None else b""
            exc_headers = {k.lower(): v for k, v in (exc.headers.items() if exc.headers else [])}
            if exc_headers.get("content-encoding", "").lower() == "gzip" and body:
                try:
                    body = gzip.decompress(body)
                except OSError:
                    pass
            retryable = exc.code == 429 or (idempotent and exc.code in RETRY_STATUSES)
            if retryable and attempt < attempts:
                time.sleep(_retry_after(exc_headers, attempt))
                continue
            message, code, kind = _error_message(exc.code, body, exc.reason)
            raise ApiError(message, status=exc.code, code=code, kind=kind)
        except (urllib.error.URLError, OSError) as exc:
            reason = getattr(exc, "reason", exc)
            if idempotent and attempt < attempts:
                time.sleep(min(2.0 ** attempt, 20.0))
                continue
            text = "Could not reach " + urllib.parse.urlsplit(url).netloc + ": " + str(reason)
            if "CERTIFICATE_VERIFY_FAILED" in str(reason):
                text += ". Python could not verify the TLS certificate; install your system CA certificates."
            elif not idempotent:
                text += ". The request may still have been processed, so check before sending it again."
            raise ApiError(redact(text), code="network_error")
    raise ApiError("Request failed after retries.", code="network_error")


def get_json(path, auth=True, timeout=60.0):
    return request("GET", path, auth=auth, timeout=timeout).json()


def post_json(path, body, timeout=120.0):
    return request("POST", path, json_body=body, timeout=timeout)


def encode_multipart(fields, files):
    """fields: [(name, value)], files: [(name, filename, content_type, bytes)]."""
    boundary = "----empiriolabs" + uuid.uuid4().hex
    out = bytearray()
    for name, value in fields:
        out += ("--" + boundary + "\r\n").encode("ascii")
        out += ('Content-Disposition: form-data; name="' + _safe_header(name) + '"\r\n\r\n').encode("utf-8")
        out += str(value).encode("utf-8") + b"\r\n"
    for name, filename, ctype, payload in files:
        out += ("--" + boundary + "\r\n").encode("ascii")
        out += ('Content-Disposition: form-data; name="' + _safe_header(name) + '"; filename="'
                + _safe_header(filename) + '"\r\n').encode("utf-8")
        out += ("Content-Type: " + ctype + "\r\n\r\n").encode("ascii")
        out += payload + b"\r\n"
    out += ("--" + boundary + "--\r\n").encode("ascii")
    return bytes(out), "multipart/form-data; boundary=" + boundary


def _safe_header(value):
    return re.sub(r'["\r\n\\]', "_", str(value))


# ---------------------------------------------------------------------------
# Model catalog
# ---------------------------------------------------------------------------

def list_models(timeout=60.0):
    """The public model catalog. No API key is needed."""
    payload = get_json("/models", auth=False, timeout=timeout)
    models = payload.get("data") if isinstance(payload, dict) else payload
    return models if isinstance(models, list) else []


def get_model(model_id, timeout=60.0):
    """One catalog entry, or None when the catalog has no entry with that id."""
    try:
        return get_json("/models/" + urllib.parse.quote(model_id, safe=""), auth=False, timeout=timeout)
    except ApiError as exc:
        if exc.status == 404:
            return None
        raise


def supports(model, endpoint):
    return endpoint in (model.get("supported_endpoints") or [])


def candidates(models, endpoint, category=None, feature=None):
    out = []
    for model in models:
        if not supports(model, endpoint):
            continue
        if category and model.get("category") != category:
            continue
        if feature and feature not in (model.get("features") or []):
            continue
        if model.get("status") not in (None, "available"):
            continue
        out.append(model)
    return out


def pick_default(models, endpoint, category=None, feature=None):
    """Choose a model from the live catalog: featured first, then Native Inference, then catalog order."""
    pool = candidates(models, endpoint, category, feature)
    if not pool:
        raise ApiError("No model in the live catalog supports " + endpoint + ". Pass --model explicitly.")
    ranked = sorted(
        enumerate(pool),
        key=lambda item: (0 if item[1].get("is_featured") else 1,
                          0 if item[1].get("native_inference") else 1,
                          item[0]),
    )
    return ranked[0][1]


def resolve_model(model_id, endpoint, category=None, feature=None):
    """Return (model_id, catalog_entry_or_None) for a request on endpoint."""
    if model_id:
        entry = get_model(model_id)
        if entry is None:
            log("Note: " + model_id + " is not in the public catalog; sending the request anyway.")
            return model_id, None
        if not supports(entry, endpoint):
            raise ApiError(
                model_id + " does not support " + endpoint + ". Run with --list-models to see models that do.",
                code="unsupported_endpoint",
                exit_code=EXIT_USAGE,
            )
        return entry.get("id") or model_id, entry
    entry = pick_default(list_models(), endpoint, category, feature)
    return entry["id"], entry


def price_summary(model, limit=3):
    rows = model.get("pricing_rows") or []
    parts = []
    for row in rows[:limit]:
        if not isinstance(row, dict):
            continue
        label = str(row.get("label") or "").strip()
        value = str(row.get("value") or "").strip()
        spec = str(row.get("spec") or "").strip()
        text = " ".join(p for p in (value, spec) if p)
        parts.append(label + ": " + text if label else text)
    if len(rows) > limit:
        parts.append("+" + str(len(rows) - limit) + " more")
    return "; ".join(parts) if parts else "see " + str(model.get("api_url") or DOCS_URL)


def print_model_list(models, endpoint, category=None, feature=None):
    pool = candidates(models, endpoint, category, feature)
    default = pick_default(models, endpoint, category, feature)["id"] if pool else None
    rows = []
    for model in pool:
        mark = "*" if model["id"] == default else " "
        rows.append({
            "default": model["id"] == default,
            "id": model["id"],
            "name": model.get("display_name") or model["id"],
            "price": price_summary(model),
        })
        print(mark + " " + model["id"].ljust(32) + " " + price_summary(model))
    log(str(len(pool)) + " models support " + endpoint + ". * marks the default when --model is omitted.")
    return rows


def param_spec(model, name):
    for param in (model or {}).get("supported_parameters") or []:
        if isinstance(param, dict) and param.get("name") == name:
            return param
    return None


def match_option(model, name, value):
    """Map value onto the model's own spelling of an enum option, or None."""
    spec = param_spec(model, name)
    options = spec.get("options") if spec else None
    if not options:
        return None
    for option in options:
        if str(option).lower() == str(value).lower():
            return option
    return None


def format_from_path(model, out, names=("format", "output_format")):
    """(parameter, option) that asks the model for the file type named by out's extension."""
    if not model or not out or is_dir_target(os.path.expanduser(out)):
        return None
    ext = os.path.splitext(out)[1].lstrip(".").lower()
    if not ext:
        return None
    alternatives = {"jpg": ("jpg", "jpeg"), "jpeg": ("jpeg", "jpg")}.get(ext, (ext,))
    for name in names:
        for alt in alternatives:
            option = match_option(model, name, alt)
            if option is not None:
                return name, option
    return None


# ---------------------------------------------------------------------------
# Jobs and results
# ---------------------------------------------------------------------------

def wait_for_job(job_id, timeout=600.0, label="Job", poll_interval=2.0, max_interval=10.0):
    """Poll GET /v1/jobs/{job_id} until the job finishes. Returns the job object."""
    started = time.monotonic()
    delay = poll_interval
    last = None
    path = "/jobs/" + urllib.parse.quote(str(job_id), safe="")
    while True:
        job = get_json(path)
        status = str(job.get("status") or "").lower()
        if status != last:
            progress = job.get("progress")
            suffix = ""
            if isinstance(progress, (int, float)) and 0 < progress < 1:
                suffix = " (" + str(int(progress * 100)) + "%)"
            log(label + " " + str(job_id) + ": " + (status or "unknown") + suffix)
            last = status
        if status in JOB_SUCCEEDED:
            return job
        if status in JOB_FAILED:
            err = job.get("error")
            message = None
            code = kind = None
            if isinstance(err, dict):
                inner = err.get("error") if isinstance(err.get("error"), dict) else err
                message = inner.get("message")
                code = inner.get("code")
                kind = inner.get("type")
            elif isinstance(err, str):
                message = err
            raise ApiError(redact(label + " " + str(job_id) + " " + status + ": "
                                  + (message or "no details were returned")),
                           code=code, kind=kind)
        waited = time.monotonic() - started
        if waited + delay > timeout:
            raise JobTimeout(job_id, status, waited)
        time.sleep(delay)
        delay = min(delay * 1.5, max_interval)


def job_id_of(payload):
    if isinstance(payload, dict):
        value = payload.get("job_id") or (payload.get("id") if payload.get("status") in JOB_RUNNING else None)
        return str(value) if value else None
    return None


def media_items(payload):
    """Media entries ({"url"} or {"b64_json"}) from a response or a job."""
    if not isinstance(payload, dict):
        return []
    for key in ("data", "images", "videos", "audio", "outputs"):
        items = _items(payload.get(key))
        if items:
            return items
    for key in ("url", "video_url", "audio_url", "image_url"):
        value = payload.get(key)
        if isinstance(value, str) and value.startswith(("http://", "https://")):
            return [{"url": value}]
    for key in ("b64_json", "audio_base64"):
        if isinstance(payload.get(key), str):
            return [{"b64_json": payload[key]}]
    for key in ("result", "output"):
        nested = payload.get(key)
        if isinstance(nested, dict):
            items = media_items(nested)
            if items:
                return items
        elif isinstance(nested, list):
            items = _items(nested)
            if items:
                return items
    return []


def _items(value):
    if isinstance(value, dict):
        value = [value]
    if not isinstance(value, list):
        return []
    out = []
    for entry in value:
        if isinstance(entry, str) and entry.startswith(("http://", "https://")):
            out.append({"url": entry})
        elif isinstance(entry, dict):
            url = entry.get("url") or entry.get("video_url") or entry.get("audio_url") or entry.get("image_url")
            if isinstance(url, str) and url.startswith(("http://", "https://")):
                item = {"url": url}
            elif isinstance(entry.get("b64_json"), str):
                item = {"b64_json": entry["b64_json"]}
            else:
                continue
            for extra in ("filename", "content_type", "mime_type", "format"):
                if isinstance(entry.get(extra), str):
                    item[extra] = entry[extra]
            out.append(item)
    return out


# ---------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------

def extension_for(content_type=None, url=None, filename=None, fallback=".bin"):
    for name in (filename, urllib.parse.urlsplit(url).path if url else None):
        if name:
            suffix = os.path.splitext(name)[1].lower()
            if suffix in _KNOWN_SUFFIXES:
                return ".jpg" if suffix == ".jpeg" else suffix
    ctype = (content_type or "").split(";")[0].strip().lower()
    if ctype in _EXTENSIONS:
        return _EXTENSIONS[ctype]
    guessed = mimetypes.guess_extension(ctype) if ctype else None
    return guessed or fallback


def is_dir_target(out):
    return out.endswith(("/", "\\")) or os.path.isdir(out)


def _same_ext(a, b):
    aliases = {".jpeg": ".jpg", ".mpga": ".mp3"}
    return aliases.get(a.lower(), a.lower()) == aliases.get(b.lower(), b.lower())


def target_path(out, stem, ext, index, count, overwrite=False, name_hint=None):
    """Where output number index (1-based) of count is saved.

    out may be a directory (existing, or ending with a slash) or a file path.
    A file path keeps its name, but its extension follows the format the service
    actually returned, so a file is never saved under the wrong type.
    """
    if not out:
        out = "."
    out = os.path.expanduser(out)
    suffix = "-" + str(index) if count > 1 else ""
    if is_dir_target(out):
        if name_hint:
            hinted = re.sub(r"[^A-Za-z0-9._-]+", "-", os.path.splitext(os.path.basename(name_hint))[0]).strip("-.")
            stem = hinted[:80] or stem
        path = os.path.join(out, stem + suffix + ext)
    else:
        base, user_ext = os.path.splitext(out)
        if not user_ext:
            final_ext = ext
        elif user_ext.lower() not in _KNOWN_SUFFIXES:
            base, final_ext = out, ext
        elif ext != ".bin" and not _same_ext(user_ext, ext):
            log("Note: the service returned " + ext + " data, so the file is saved with that extension.")
            final_ext = ext
        else:
            final_ext = user_ext
        path = base + suffix + final_ext
    path = os.path.abspath(path)
    if not overwrite:
        path = free_path(path)
    return path


def free_path(path):
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    n = 2
    while os.path.exists(base + "-" + str(n) + ext):
        n += 1
    return base + "-" + str(n) + ext


def write_bytes(path, payload):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    partial = path + ".part"
    with open(partial, "wb") as handle:
        handle.write(payload)
    os.replace(partial, path)
    return path


def download(url, path_for_ext, timeout=300.0, attempts=3):
    """Save url to the path returned by path_for_ext(extension). Returns the path.

    Hosted result URLs are pre-signed, so no credentials are attached unless the
    URL is on the API host itself.
    """
    if not url.startswith(("http://", "https://")):
        raise ApiError("Refusing to download a non-HTTP URL.")
    headers = {"User-Agent": USER_AGENT}
    if is_api_url(url):
        headers["Authorization"] = "Bearer " + api_key()
    for attempt in range(1, attempts + 1):
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with _open(req, timeout) as resp:
                ctype = resp.headers.get("Content-Type", "") if resp.headers else ""
                path = path_for_ext(extension_for(ctype, url))
                folder = os.path.dirname(path)
                if folder:
                    os.makedirs(folder, exist_ok=True)
                partial = path + ".part"
                try:
                    with open(partial, "wb") as handle:
                        while True:
                            chunk = resp.read(1024 * 256)
                            if not chunk:
                                break
                            handle.write(chunk)
                    os.replace(partial, path)
                except BaseException:
                    if os.path.exists(partial):
                        os.remove(partial)
                    raise
                return path
        except urllib.error.HTTPError as exc:
            if exc.code in RETRY_STATUSES and attempt < attempts:
                time.sleep(min(2.0 ** attempt, 20.0))
                continue
            raise ApiError("Download failed with HTTP " + str(exc.code) + ". The result URL is printed "
                           "above and can be fetched again.", status=exc.code)
        except (urllib.error.URLError, OSError) as exc:
            if attempt < attempts:
                time.sleep(min(2.0 ** attempt, 20.0))
                continue
            raise ApiError("Download failed: " + str(getattr(exc, "reason", exc)))
    raise ApiError("Download failed after retries.")


def save_items(items, out, stem, overwrite=False, timeout=300.0, fallback_ext=".bin"):
    """Save media items and return the list of saved file paths."""
    saved = []
    count = len(items)
    for index, item in enumerate(items, start=1):
        hint = item.get("filename")
        if item.get("url"):

            def path_for(ext, _index=index, _hint=hint):
                if ext == ".bin" and _hint:
                    named = os.path.splitext(_hint)[1].lower()
                    if named in _KNOWN_SUFFIXES:
                        ext = ".jpg" if named == ".jpeg" else named
                if ext == ".bin":
                    ext = fallback_ext
                return target_path(out, stem, ext, _index, count, overwrite, name_hint=_hint)

            saved.append(download(item["url"], path_for, timeout=timeout))
        elif item.get("b64_json"):
            raw = item["b64_json"]
            ctype = item.get("content_type") or item.get("mime_type")
            if raw.startswith("data:") and "," in raw:
                header, raw = raw.split(",", 1)
                ctype = ctype or header[5:].split(";")[0]
            ext = extension_for(ctype, filename=hint, fallback=fallback_ext)
            path = target_path(out, stem, ext, index, count, overwrite, name_hint=hint)
            saved.append(write_bytes(path, base64.b64decode(raw)))
    return saved


def default_stem(prefix):
    return prefix + "-" + time.strftime("%Y%m%d-%H%M%S")


def inline_file(value, max_bytes=MAX_INLINE_BYTES):
    """An https URL is returned as is; a local file becomes a data URI."""
    if value.startswith(("http://", "https://", "data:")):
        return value
    path = os.path.expanduser(value)
    if not os.path.isfile(path):
        raise ApiError("Input not found: " + value + ". Pass an https URL or the path of a local file.",
                       exit_code=EXIT_USAGE)
    size = os.path.getsize(path)
    if size > max_bytes:
        raise ApiError("Input " + value + " is " + str(size // (1024 * 1024)) + " MB. Files over "
                       + str(max_bytes // (1024 * 1024)) + " MB must be passed as an https URL.",
                       exit_code=EXIT_USAGE)
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as handle:
        payload = handle.read()
    return "data:" + mime + ";base64," + base64.b64encode(payload).decode("ascii")


def parse_params(pairs):
    """--param key=value pairs. Values are read as JSON when possible, else as text."""
    params = {}
    for pair in pairs or []:
        if "=" not in pair:
            raise ApiError("--param expects key=value, got: " + pair, exit_code=EXIT_USAGE)
        key, raw = pair.split("=", 1)
        key = key.strip()
        if not key:
            raise ApiError("--param expects key=value, got: " + pair, exit_code=EXIT_USAGE)
        try:
            params[key] = json.loads(raw)
        except ValueError:
            params[key] = raw
    return params
