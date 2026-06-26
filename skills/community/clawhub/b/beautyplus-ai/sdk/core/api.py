"""AI API core module for BeautyPlus AI SDK."""

import copy
import datetime
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode, urlparse

import requests

from sdk.core.config import USER_AGENT, GID_CACHE_FILE, INVOKE, REGIONS, TOKEN_POLICY_APP
from sdk.core.models import TaskResult, TaskStatus
from sdk.utils.cache import GidCache
from sdk.auth.signer import Signer, HeaderHost


# Progress logging
PROGRESS_ENABLED = os.environ.get("MT_AI_PROGRESS", "1").strip().lower() not in (
    "0", "false", "no", "off",
)


def _progress_log(msg: str) -> None:
    if not PROGRESS_ENABLED:
        return
    print(f"[beautyplus-ai] {msg}", file=sys.stderr, flush=True)


def safe_url_preview(url: str, max_len: int = 72) -> str:
    """Shorten URLs for logs and JSON pipeline_trace."""
    if not url:
        return ""
    s = str(url).strip().replace("\n", " ")
    if len(s) <= max_len:
        return s
    return s[: max_len - 3] + "..."


# Keys whose values must not appear in progress logs (token_policy, etc.)
_REDACT_LOG_KEYS = frozenset(
    {
        "access_key",
        "secret_key",
        "session_token",
        "security_token",
        "app_secret",
        "password",
        "private_key",
        "authorization",
        # camelCase / compact variants
        "accesskey",
        "secretkey",
        "sessiontoken",
        "appsecret",
    }
)


def _redact_secrets_for_log(obj: Any) -> Any:
    """Return a deep copy safe for logging (OSS/WAPI credentials stripped)."""
    if isinstance(obj, dict):
        out: Dict[str, Any] = {}
        for k, v in obj.items():
            lk = str(k).lower().replace("-", "_")
            if lk == "credentials" or lk in _REDACT_LOG_KEYS or lk.endswith("_secret"):
                out[k] = "<redacted>"
            else:
                out[k] = _redact_secrets_for_log(v)
        return out
    if isinstance(obj, list):
        return [_redact_secrets_for_log(x) for x in obj]
    return obj


def _default_task_type(raw: Any) -> str:
    """Normalize task_type from INVOKE or token_policy; empty or missing → mtlab."""
    if raw is None:
        return "mtlab"
    s = str(raw).strip()
    return s or "mtlab"


_USER_ORIGIN_IMAGE_URL_PLACEHOLDER = "{userOriginImageUrl}"


def _replace_user_origin_image_url(obj: Any, user_image_url: str) -> Any:
    """Replace placeholder strings in-place (deep structure)."""
    if isinstance(obj, dict):
        for k in obj:
            obj[k] = _replace_user_origin_image_url(obj[k], user_image_url)
        return obj
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = _replace_user_origin_image_url(obj[i], user_image_url)
        return obj
    if isinstance(obj, str):
        return obj.replace(_USER_ORIGIN_IMAGE_URL_PLACEHOLDER, user_image_url)
    return obj


def _init_images_from_media_profiles(
    media_profiles: Any, user_image_url: str
) -> Optional[Any]:
    """
    Parse INVOKE ``media_profiles`` JSON string. If the object contains
    ``media_info_list`` and it is a list, return that list (deep-copied) with
    ``{userOriginImageUrl}`` replaced for use as algorithm ``init_images``;
    otherwise return None (caller uses default ``[{"url": url}]``).
    Invalid JSON raises ValueError.
    """
    if not isinstance(media_profiles, str) or not media_profiles.strip():
        return None
    try:
        parsed = json.loads(media_profiles.strip())
    except json.JSONDecodeError as e:
        raise ValueError(
            f"config INVOKE media_profiles is not valid JSON: {e}"
        ) from e
    if not isinstance(parsed, dict):
        return None
    media_info_list = parsed.get("media_info_list")
    if not isinstance(media_info_list, list):
        return None
    out = copy.deepcopy(media_info_list)
    _replace_user_origin_image_url(out, str(user_image_url) if user_image_url is not None else "")
    return out


def _brief_media_ref(data) -> str:
    if data is None:
        return "—"
    if isinstance(data, str):
        return safe_url_preview(data)
    if isinstance(data, dict):
        u = data.get("url") or data.get("uri")
        if u:
            return safe_url_preview(str(u))
        return safe_url_preview(json.dumps(data, ensure_ascii=False), max_len=64)
    return safe_url_preview(str(data))


def _upload_source_hint(file) -> str:
    if isinstance(file, str):
        p = Path(file)
        try:
            sz = p.stat().st_size
            return f"file={p.name} bytes={sz}"
        except OSError:
            return f"file={p.name}"
    try:
        raw = file.getvalue()  # BytesIO
        return f"stream bytes={len(raw)}"
    except (AttributeError, TypeError):
        return "stream"


def _normalize_image_suffix(raw) -> str:
    s = str(raw or "").strip().lower().lstrip(".")
    if s in ("jpg", "jpeg", "png"):
        return s
    return "jpg"


def _image_suffix_from_source(source) -> str:
    if not isinstance(source, str):
        return "jpg"
    raw = source.strip()
    if not raw:
        return "jpg"
    if raw.startswith(("http://", "https://")):
        raw = urlparse(raw).path or ""
    ext = Path(raw).suffix
    return _normalize_image_suffix(ext)


def _log_outputs_ready(body: dict, prefix: str) -> None:
    if not PROGRESS_ENABLED or not isinstance(body, dict):
        return
    urls = body.get("output_urls")
    if not isinstance(urls, list):
        urls = _extract_output_urls(body)
    n = len(urls)
    line = f"{prefix} output_urls={n}"
    if n and urls:
        line += f" primary={safe_url_preview(str(urls[0]))}"
    line += " → download via HTTP GET on each URL"
    _progress_log(line)


def _failure_status_codes_from_env():
    """
    Optional terminal task data.status values (integers).
    MT_AI_TASK_FAILURE_STATUSES: comma-separated, default "3". Empty / false disables.
    """
    raw = os.environ.get("MT_AI_TASK_FAILURE_STATUSES", "3").strip()
    if not raw or raw.lower() in ("0", "false", "no", "off", "none"):
        return frozenset()
    out = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            out.add(int(part))
        except ValueError:
            continue
    return frozenset(out)


def _max_consecutive_poll_errors() -> int:
    raw = os.environ.get("MT_AI_POLL_MAX_CONSECUTIVE_ERRORS", "5").strip() or "5"
    try:
        n = int(raw)
    except ValueError:
        n = 5
    return max(1, min(n, 100))


def _meta_indicates_error(meta) -> bool:
    if os.environ.get("MT_AI_IGNORE_META_CODE", "").strip().lower() in (
        "1",
        "true",
        "yes",
    ):
        return False
    if not isinstance(meta, dict):
        return False
    code = meta.get("code")
    if code is None:
        return False
    if code == 0 or code == "0":
        return False
    return True


def _poll_timeout_payload(task_id, n_polls, elapsed_s, last_api_status):
    return {
        "error": "poll_timeout",
        "skill_status": "failed",
        "task_id": task_id,
        "polls": n_polls,
        "elapsed_seconds": round(elapsed_s, 1),
        "last_api_status": last_api_status,
        "agent_instruction": (
            "Polling exhausted before the task finished. Increase sessions_spawn "
            "runTimeoutSeconds (default 3600); for videoscreenclear/hdvideoallinone use "
            "spawn-run-task in the main session — do not rely on blocking run-task there "
            "under a short tool or session wait cap. Or adjust MT_AI_POLL_* env vars. "
            "Do not treat as success; user may retry."
        ),
    }


def _task_failed_payload(task_id, task_result_dict, reason="task_failed"):
    meta = task_result_dict.get("meta", {}) if isinstance(task_result_dict, dict) else {}
    detail = ""
    if isinstance(meta, dict):
        detail = (meta.get("msg") or meta.get("message") or "") or detail
    data = task_result_dict.get("data") if isinstance(task_result_dict, dict) else None
    if isinstance(data, dict) and not detail:
        detail = str(data.get("message") or data.get("error") or "")[:300]
    if not detail:
        detail = reason
    return {
        "error": reason,
        "skill_status": "failed",
        "task_id": task_id,
        "detail": detail,
        "meta": meta if isinstance(meta, dict) else {},
        "data": data,
        "agent_instruction": (
            "The algorithm reported failure (see detail / meta). Do not treat as "
            "success; explain to the user and suggest retry or input checks."
        ),
    }


def _poll_aborted_payload(task_id, n_polls, message, last_api_status):
    return {
        "error": "poll_aborted",
        "skill_status": "failed",
        "task_id": task_id,
        "polls": n_polls,
        "detail": message,
        "last_api_status": last_api_status,
        "agent_instruction": (
            "Status polling stopped after repeated query errors. Check network, "
            "credentials, and task_id; retry or use query-task after fixing connectivity."
        ),
    }


def _is_http_url(s) -> bool:
    return isinstance(s, str) and s.startswith(("http://", "https://"))


def _urls_from_media_info_list(items):
    out = []
    if not isinstance(items, list):
        return out
    for it in items:
        if isinstance(it, dict):
            md = it.get("media_data")
            if _is_http_url(md):
                out.append(md)
    return out


def _append_url_strings(bucket: list, seen: set, values):
    if isinstance(values, list):
        for x in values:
            if _is_http_url(x) and x not in seen:
                seen.add(x)
                bucket.append(x)
    elif _is_http_url(values) and values not in seen:
        seen.add(values)
        bucket.append(values)


def _extract_output_urls(body: dict) -> list[str]:
    if not isinstance(body, dict):
        return []
    inner = body.get("data")
    if not isinstance(inner, dict):
        return []
    result = inner.get("result")
    if not isinstance(result, dict):
        return []

    ordered: list[str] = []
    seen: set[str] = set()

    for key in ("urls", "images", "videos"):
        _append_url_strings(ordered, seen, result.get(key))
    _append_url_strings(ordered, seen, result.get("url"))

    nested_data = result.get("data")
    nested_mil = nested_data.get("media_info_list") if isinstance(nested_data, dict) else None
    for mil in (result.get("media_info_list"), nested_mil):
        for u in _urls_from_media_info_list(mil):
            if u not in seen:
                seen.add(u)
                ordered.append(u)

    mtlab = result.get("mtlab_res")
    if isinstance(mtlab, dict):
        for u in _urls_from_media_info_list(mtlab.get("media_info_list")):
            if u not in seen:
                seen.add(u)
                ordered.append(u)

    return ordered


def _extract_task_id(body):
    """Best-effort task id from API response shape (for resume / status queries)."""
    if not isinstance(body, dict):
        return None
    data = body.get("data")
    if not isinstance(data, dict):
        return None
    result = data.get("result")
    if isinstance(result, dict):
        tid = result.get("id")
        if tid is not None:
            s = str(tid).strip()
            if s:
                return s
    return None


def _with_output_urls(body, task_id=None):
    """
    Attach output_urls and, when known, full task_id for downstream recovery
    (re-poll status without re-submitting).
    """
    if not isinstance(body, dict):
        return body
    out = {**body, "output_urls": _extract_output_urls(body)}
    tid = None
    if task_id is not None:
        s = str(task_id).strip()
        if s:
            tid = s
    if not tid:
        tid = _extract_task_id(body)
    if tid:
        out["task_id"] = tid
    return out


_DEFAULT_STATUS_POLL_MIN_TOTAL_MS = 3_600_000  # 1h cumulative sleep budget if server durations sum to less


def _status_poll_min_total_ms():
    """
    Minimum sum (ms) of status poll sleeps. Default 1 hour when env unset.
    MT_AI_POLL_MIN_TOTAL_MS overrides; 0 / false / no / off disables extension.
    """
    raw = os.environ.get("MT_AI_POLL_MIN_TOTAL_MS", "").strip()
    if not raw:
        return _DEFAULT_STATUS_POLL_MIN_TOTAL_MS
    if raw.lower() in ("0", "false", "no", "off"):
        return None
    try:
        v = int(raw)
    except ValueError:
        return _DEFAULT_STATUS_POLL_MIN_TOTAL_MS
    if v <= 0:
        return None
    return v


def _extend_status_poll_durations_ms(durations):
    """
    Ensure cumulative sleep between status polls is at least min_total_ms when
    the server list sums to less (e.g. token "8" means 8 ms). If the server sum is
    already >= min_total_ms, leave it unchanged. Task completion still returns
    immediately inside the polling loop.
    """
    min_total_ms = _status_poll_min_total_ms()
    if min_total_ms is None:
        return durations
    try:
        base_total = sum(int(d) for d in durations)
    except ValueError:
        return durations
    if base_total >= min_total_ms:
        return durations
    step_raw = os.environ.get("MT_AI_POLL_EXTEND_STEP_MS", "30000").strip() or "30000"
    try:
        step_ms = int(step_raw)
    except ValueError:
        step_ms = 30000
    step_ms = max(step_ms, 1000)
    out = list(durations)
    total = base_total
    while total < min_total_ms:
        add = min(step_ms, min_total_ms - total)
        out.append(str(add))
        total += add
    return out


def _deep_merge_params(base, override):
    """Shallow keys from override win; nested dicts are merged recursively."""
    if not base:
        return copy.deepcopy(override) if override else {}
    if not override:
        return copy.deepcopy(base)
    out = copy.deepcopy(base)
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge_params(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def _default_connection_config():
    """Connection settings from project config.py (regions, token_policy)."""
    return {
        "regions": dict(getattr(REGIONS, "copy", lambda: REGIONS)()),
        "token_policy_type": "mtai",
        "token_policy_types": None,
        "token_policy_app": TOKEN_POLICY_APP,
    }


def _merge_connection_config(base, override):
    """Merge optional constructor override into connection config."""
    if not override:
        return copy.deepcopy(base)
    out = copy.deepcopy(base)
    for key, val in override.items():
        if key == "regions" and isinstance(val, dict):
            merged = copy.deepcopy(out.get("regions") or {})
            merged.update(val)
            out["regions"] = merged
        elif key == "token_policy_types" and isinstance(val, dict):
            merged = copy.deepcopy(out.get("token_policy_types") or {})
            merged.update(val)
            out["token_policy_types"] = merged
        else:
            out[key] = copy.deepcopy(val) if isinstance(val, dict) else val
    return out


class AiApi:
    """AI API actions for BeautyPlus SDK."""

    def __init__(self, key, secret, region="cn-north-4", oss_region=None, config=None):
        """
        :param key: your access key.
        :param secret: your access secret key.
        :param region: api access region . default "cn-north-4"
        :param oss_region: optional OSS bucket region when token_policy url cannot be parsed (e.g. custom domain)
        :param config: optional dict overriding config.py connection fields (regions,
            token_policy_type, token_policy_types). Invoke task names live in config.INVOKE.
        """
        self.Key = key
        self.Secret = secret
        self._config = _merge_connection_config(_default_connection_config(), config)
        self.region = region
        self.oss_region = oss_region
        self.aiStrategy = None
        self.storageStrategy = None
        # EndPoint resolved after fetch_config injects regions
        self.EndPoint = self._config.get("regions", {}).get(region)
        self.gid_cache = GidCache(GID_CACHE_FILE)

    def _token_policy_type_for(self, name):
        """name is 'upload' or 'ai' — query param for /ai/token_policy?type= """
        types_map = self._config.get("token_policy_types")
        if types_map:
            return types_map.get(name) or self._config.get("token_policy_type", "mtai")
        return self._config.get("token_policy_type", "mtai")

    def _token_policy_app_for(self):
        app = self._config.get("token_policy_app")
        if app is None:
            return None
        app = str(app).strip()
        return app or None

    def getStorageStrategy(self, suffix="jpg"):
        return self.getStrategy("upload", suffix=suffix)

    def getAiStrategy(self):
        return self.getStrategy("ai")

    def _ensure_endpoint(self):
        """Raise if no endpoint is configured for the current region."""
        if not self.EndPoint:
            raise RuntimeError(
                f"No endpoint configured for region {self.region!r}. "
                "Call fetch_config() first or set regions in config."
            )

    def getStrategy(self, name, suffix=None):
        self._ensure_endpoint()
        typ = self._token_policy_type_for(name)
        now = datetime.datetime.now()
        unix_epoch = datetime.datetime(1970, 1, 1)
        unix_time = (now - unix_epoch).total_seconds()
        if name == "ai" and self.aiStrategy and self.aiStrategy["ttl"] + self.strategyLoadTime > unix_time:
            return self.aiStrategy

        signer = Signer(self.Key, self.Secret)
        headers = {
            HeaderHost: self.EndPoint,
            "User-Agent": USER_AGENT,
        }
        query = {"type": typ}
        if name == "upload":
            query["suffix"] = _normalize_image_suffix(suffix)
        app = self._token_policy_app_for()
        if app:
            query["app"] = app
        uri = "https://" + self.EndPoint + "/ai/token_policy?" + urlencode(query)
        sign_request = signer.sign(uri, "GET", headers, "")
        session = requests.Session()
        resp = session.send(sign_request)
        _progress_log(
            f"token_policy GET type={typ} host={self.EndPoint} → HTTP {resp.status_code}"
        )
        if resp.status_code == 200:
            try:
                policydata = json.loads(resp.content)
            except (json.JSONDecodeError, UnicodeDecodeError):
                _progress_log("token_policy failed: non-JSON response body")
                return None
            if policydata is None:
                return None
            if _meta_indicates_error(policydata.get("meta")):
                msg = ""
                meta = policydata.get("meta")
                if isinstance(meta, dict):
                    msg = str(meta.get("msg") or meta.get("message") or "")
                _progress_log(
                    f"token_policy meta error type={typ} app={app or '-'} msg={safe_url_preview(msg, max_len=120)!r}"
                )
                return None
            policy = policydata.get("data") or {}
            policy_key = typ if isinstance(policy.get(typ), dict) else "mtai"
            policy_block = policy.get(policy_key) or {}
            api_block = policy_block.get("api") or {}
            upload_block = policy_block.get("upload") or {}
            api_order = api_block.get("order") or []
            upload_order = upload_block.get("order") or []
            if not api_order or not upload_order:
                _progress_log(
                    f"token_policy missing api/upload order for key={policy_key!r}"
                )
                return None
            cloud = api_order[0]
            storageCloud = upload_order[0]
            self.aiStrategy = api_block.get(cloud)
            self.storageStrategy = upload_block.get(storageCloud)
            if not isinstance(self.aiStrategy, dict) or not isinstance(self.storageStrategy, dict):
                _progress_log(
                    f"token_policy invalid strategy payload for key={policy_key!r}"
                )
                return None
            unix_time = (now - unix_epoch).total_seconds()
            self.strategyLoadTime = unix_time
            if name == "ai":
                return self.aiStrategy
            return self.storageStrategy
        _progress_log(
            f"token_policy failed body={safe_url_preview(resp.text, max_len=120)!r}"
        )
        return None

    def getFileUrl(self, file, upload_source=None):
        """
        Upload data to the object.

        :param file: The data to upload. This can either be bytes or a string.
                     When this argument is a string, it is interpreted as a file name.
        """
        from sdk.storage.oss import OssUploader, resolve_oss_region, normalize_oss_endpoint
        import alibabacloud_oss_v2 as oss

        suffix = _image_suffix_from_source(
            upload_source if upload_source is not None else file
        )
        policy = self.getStorageStrategy(suffix=suffix)
        if policy is None:
            return None
        creds = policy["credentials"]
        credentials_provider = oss.credentials.StaticCredentialsProvider(
            creds["access_key"],
            creds["secret_key"],
            creds.get("session_token"),
        )
        cfg = oss.config.load_default()
        cfg.credentials_provider = credentials_provider
        cfg.region = resolve_oss_region(policy, self.oss_region)
        cfg.endpoint = normalize_oss_endpoint(policy["url"])
        client = oss.Client(cfg)
        try:
            key = policy.get("key") or ""
            key_tail = key if len(key) <= 32 else "…" + key[-31:]
            _progress_log(
                f"OSS upload start {_upload_source_hint(file)} "
                f"bucket={policy.get('bucket')} key={key_tail}"
            )
            if isinstance(file, str):
                result = client.put_object_from_file(
                    oss.PutObjectRequest(
                        bucket=policy["bucket"],
                        key=policy["key"],
                    ),
                    file,
                )
            else:
                result = client.put_object(
                    oss.PutObjectRequest(
                        bucket=policy["bucket"],
                        key=policy["key"],
                        body=file,
                    )
                )
            if result.status_code != 200:
                raise RuntimeError(
                    f"OSS put_object failed: status={result.status_code}, request_id={getattr(result, 'request_id', None)}"
                )
            ref = _brief_media_ref(policy.get("data"))
            _progress_log(f"OSS upload done → input media URL: {ref}")
            return policy["data"]
        finally:
            if not isinstance(file, str) and getattr(file, "close", None):
                file.close()

    def run(
        self,
        imageUrl,
        params,
        task,
        taskType,
        context="",
        on_async_submitted=None,
    ):
        """
        apply effect to the object.
        :param imageUrl: the image url array [{"url":"url"}]
        :param params: api params object
        :param task: task name to be apply
        :param taskType: from INVOKE preset or token_policy; empty or missing → mtlab
        :param context: context string
        :return: The handled result data in json.
        """
        taskType = _default_task_type(taskType)
        signer = Signer(self.Key, self.Secret)
        policy = self.getAiStrategy()
        host = policy["url"]
        if host.find("https") > -1:
            host = host[8:]
        elif host.find("http") > -1:
            host = host[7:]

        headers = {
            HeaderHost: host,
            "User-Agent": USER_AGENT,
        }

        data = {
            "params": json.dumps(params),
            "context": context,
            "task": task,
            "task_type": taskType,
            "sync_timeout": policy["sync_timeout"],
            "init_images": imageUrl,
        }
        uri = policy["url"] + "/" + policy["push_path"]
        sign_request = signer.sign(uri, "POST", headers, json.dumps(data))
        _progress_log(
            f"algorithm POST {policy['push_path']} task={task} task_type={taskType} "
            f"sync_timeout={policy['sync_timeout']}s"
        )
        session = requests.Session()
        resp = session.send(sign_request, timeout=policy["sync_timeout"] + 10)
        if resp.status_code == 200:
            taskResult = json.loads(resp.content)
            if taskResult["data"]["status"] == 9:
                tid = taskResult["data"]["result"]["id"]
                _progress_log(f"async submitted task_id={tid} → polling status until done")
                if callable(on_async_submitted):
                    try:
                        on_async_submitted(str(tid).strip())
                    except Exception:
                        pass
                return self.status(tid, policy)
            else:
                out = _with_output_urls(taskResult)
                _log_outputs_ready(out, "sync complete")
                return out
        _progress_log(f"algorithm POST HTTP {resp.status_code} (see response body in error)")
        raw = json.loads(resp.content)
        return _with_output_urls(raw) if isinstance(raw, dict) else raw

    def status(self, taskId, policy):
        """
        query task execute status
        :param taskId: the task id
        :param policy: query policy with retry and gaps with every retry
        :return: The handled result data in json.
        """
        host = policy["url"]
        if host.find("https") > -1:
            host = host[8:]
        elif host.find("http") > -1:
            host = host[7:]
        uri = policy["url"] + "/" + policy["status_query"]["path"] + "?task_id=" + taskId
        loops = policy["status_query"]["durations"]
        durations = [p.strip() for p in str.split(loops, ",") if p.strip()]
        durations = _extend_status_poll_durations_ms(durations)
        n = len(durations)
        start = time.monotonic()
        last_api_status = None
        last_nonjson_detail = None
        err_streak = 0
        max_err = _max_consecutive_poll_errors()

        for idx, d in enumerate(durations, start=1):
            result = self.queryStatus(uri, policy)
            if result["is_finished"]:
                if result.get("is_failure"):
                    raw = result.get("result")
                    if not isinstance(raw, dict):
                        raw = {"meta": {"msg": str(raw)}}
                    return _task_failed_payload(taskId, raw, reason="task_failed")
                out = _with_output_urls(result["result"], task_id=taskId)
                _log_outputs_ready(out, f"poll complete task_id={taskId}")
                return out

            raw = result.get("result")
            if isinstance(raw, str):
                err_streak += 1
                last_nonjson_detail = raw[:120]
                if err_streak >= max_err:
                    elapsed = time.monotonic() - start
                    _progress_log(
                        f"poll aborted after {err_streak} consecutive query errors "
                        f"({elapsed:.0f}s), task_id={taskId}, detail={last_nonjson_detail!r}"
                    )
                    return _poll_aborted_payload(
                        taskId, idx, raw[:500], last_api_status
                    )
            else:
                err_streak = 0
                last_nonjson_detail = None
            if isinstance(raw, dict):
                try:
                    last_api_status = raw.get("data", {}).get("status")
                except (AttributeError, TypeError):
                    pass

            elapsed = time.monotonic() - start
            if idx == 1 or idx % 3 == 0 or idx == n:
                parts = [
                    f"poll {idx}/{n}",
                    f"task_id={taskId}",
                    f"api_status={last_api_status!r}",
                    f"elapsed={elapsed:.0f}s",
                ]
                if last_nonjson_detail:
                    parts.append(f"detail={last_nonjson_detail}")
                _progress_log(" ".join(parts))

            time.sleep(int(d) / 1000)

        elapsed = time.monotonic() - start
        _progress_log(
            f"timeout after {n} polls ({elapsed:.0f}s), task_id={taskId}, "
            f"last_api_status={last_api_status!r}"
        )
        return _poll_timeout_payload(taskId, n, elapsed, last_api_status)

    def queryStatus(self, uri, policy):
        signer = Signer(self.Key, self.Secret)
        host = policy["url"]
        if host.find("https") > -1:
            host = host[8:]
        elif host.find("http") > -1:
            host = host[7:]
        headers = {
            HeaderHost: host,
            "User-Agent": USER_AGENT,
        }
        sign_request = signer.sign(uri, "GET", headers, "")
        read_timeout = min(int(policy.get("sync_timeout", 60)) + 10, 120)
        req_timeout = (5, read_timeout)
        session = requests.Session()
        resp = None
        last_exc = None
        for attempt in range(3):
            try:
                resp = session.send(sign_request, timeout=req_timeout)
                last_exc = None
                break
            except requests.exceptions.RequestException as e:
                last_exc = e
                if attempt < 2:
                    time.sleep(3)
        if last_exc is not None:
            return {
                "is_finished": False,
                "result": " task query network error: " + str(last_exc),
            }
        if resp.status_code == 200:
            try:
                taskResult = json.loads(resp.content)
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                return {
                    "is_finished": False,
                    "result": " task query invalid JSON: " + str(e),
                }
            if _meta_indicates_error(taskResult.get("meta")):
                return {
                    "is_finished": True,
                    "is_failure": True,
                    "result": taskResult,
                }
            data = taskResult.get("data")
            if not isinstance(data, dict):
                return {"is_finished": False, "result": taskResult}
            st = data.get("status")
            if st in (10, 2, 20):
                return {"is_finished": True, "result": taskResult}
            fail_codes = _failure_status_codes_from_env()
            if fail_codes and st in fail_codes:
                return {
                    "is_finished": True,
                    "is_failure": True,
                    "result": taskResult,
                }
            return {"is_finished": False, "result": taskResult}
        return {"is_finished": False, "result": " task query failure: " + uri}

    def invoke_task(self, name, url, params=None, context="", on_async_submitted=None):
        """
        Run invoke with merged params: preset from config.INVOKE[name], overridden by ``params``.
        Optional ``task_type`` on the preset (server-driven); if absent or empty, uses mtlab.

        Optional ``media_profiles`` on the preset: JSON string. After decode, if the object
        contains ``media_info_list`` (list), that list is sent as algorithm ``init_images``,
        with ``{userOriginImageUrl}`` replaced by the user's image URL. Invalid JSON raises
        ValueError. If absent, empty, or without a list ``media_info_list``,
        ``init_images`` defaults to ``[{"url": url}]``.
        """
        table = INVOKE
        if name not in table:
            raise KeyError(f"Unknown invoke preset {name!r}; add it to config.INVOKE")
        spec = table[name]
        if not isinstance(spec, dict) or "task" not in spec:
            raise ValueError(
                f"config.INVOKE[{name!r}] must include 'task'; optional 'params' (default {{}}), "
                f"optional 'task_type' (default mtlab)"
            )
        cfg_params = spec.get("params")
        if cfg_params is not None and not isinstance(cfg_params, dict):
            raise TypeError(f"config.INVOKE[{name!r}]['params'] must be a dict or omit")
        merged = _deep_merge_params(cfg_params or {}, params or {})
        task_type = _default_task_type(spec.get("task_type"))
        init_images = _init_images_from_media_profiles(
            spec.get("media_profiles"), url
        )
        return self.invoke(
            url,
            merged,
            spec["task"],
            context,
            task_type=task_type,
            on_async_submitted=on_async_submitted,
            init_images=init_images,
        )

    def invoke_task_with_spec(self, spec, url, params=None, context="", on_async_submitted=None):
        """
        Run invoke using a server-supplied spec dict from /skill/consume.json.

        ``spec`` must contain ``task`` and optionally ``params``, ``task_type``, and
        ``media_profiles``.
        """
        label = spec.get("task", "<unknown>") if isinstance(spec, dict) else "<unknown>"
        if not isinstance(spec, dict) or "task" not in spec:
            raise ValueError(
                f"invoke_spec must include 'task'; optional 'params' (default {{}}), "
                f"optional 'task_type' (default mtlab). Got: {spec!r}"
            )
        cfg_params = spec.get("params")
        if cfg_params is not None and not isinstance(cfg_params, dict):
            raise TypeError(f"invoke_spec['params'] must be a dict or omit (preset={label!r})")
        merged = _deep_merge_params(cfg_params or {}, params or {})
        task_type = _default_task_type(spec.get("task_type"))
        init_images = _init_images_from_media_profiles(
            spec.get("media_profiles"), url
        )
        return self.invoke(
            url,
            merged,
            spec["task"],
            context,
            task_type=task_type,
            on_async_submitted=on_async_submitted,
            init_images=init_images,
        )

    def txt2img(self, params, context=""):
        policy = self.getAiStrategy()
        tt = _default_task_type(policy.get("task_type") if policy else None)
        return self.run(None, params, "txt2img", tt, context)

    def img2img(self, url, params, context=""):
        policy = self.getAiStrategy()
        tt = _default_task_type(policy.get("task_type") if policy else None)
        return self.run([{"url": url}], params, "img2img", tt, context)

    def inferenceConf(self):
        pass

    def invoke(
        self,
        url,
        params,
        task,
        context="",
        on_async_submitted=None,
        *,
        task_type=None,
        init_images: Optional[Any] = None,
    ):
        """
        invoke ai task
        :param url: the task id
        :param params: task params
        :param task: ai task name, such as v1/sod, v1/znxc_async
        :param task_type: keyword-only; from INVOKE or caller; empty or missing → mtlab
        :param init_images: keyword-only; if set and url is not None, used as algorithm
            init_images instead of [{"url": url}]. Ignored when url is None.
        :return: The handled result data in json.
        """
        task_type = _default_task_type(task_type)
        if url is None:
            return self.run(
                None,
                params,
                task,
                task_type,
                context,
                on_async_submitted=on_async_submitted,
            )
        if init_images is not None:
            return self.run(
                init_images,
                params,
                task,
                task_type,
                context,
                on_async_submitted=on_async_submitted,
            )
        return self.run(
            [{"url": url}],
            params,
            task,
            task_type,
            context,
            on_async_submitted=on_async_submitted,
        )

    def get_gid(self, gid: str):
        """
        Return cached GID payload if present; reserved hook for remote fetch.
        """
        data = self.gid_cache.get(gid)
        if data is not None:
            return data
        return None

    def set_gid(self, gid: str, data: dict) -> None:
        """Persist GID-associated data to the local cache."""
        self.gid_cache.set(gid, data)

    def fetch_gid_from_api(self, gid: str):
        """
        Reserved: fetch GID data from API (not implemented).
        """
        pass
