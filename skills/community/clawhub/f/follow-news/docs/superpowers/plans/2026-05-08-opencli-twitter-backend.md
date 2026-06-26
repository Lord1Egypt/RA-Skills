# OpenCLI Twitter Backend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make OpenCLI the default Twitter/X backend for `follow-news`, while preserving existing Twitter JSON output and API fallback behavior.

**Architecture:** Add `OpenCliBackend` inside the existing `scripts/fetch-twitter.py` backend abstraction, then route `auto` through an ordered backend chain: OpenCLI, GetXAPI, twitterapi.io, official X API. Keep OpenCLI-specific parsing isolated in normalization helpers so `merge-sources.py` and non-Twitter source fetchers remain unchanged.

**Tech Stack:** Python 3.8 standard library, `unittest`, `unittest.mock`, OpenCLI executable (`opencli twitter tweets <handle> --limit <n> -f json`), existing JSON pipeline.

---

## Scope

本计划实现已批准的设计文档：

- `docs/superpowers/specs/2026-05-08-opencli-twitter-backend-design.md`

实现范围只覆盖 Twitter/X 后端、OpenClaw-facing 文档、CLI 参数和测试。RSS、Web、GitHub、GitHub Trending、Reddit 的采集逻辑不改。

## File Structure

- Modify: `scripts/fetch-twitter.py`
  - 新增 OpenCLI 常量、错误分类、命令执行、能力探测、tweet 归一化、`OpenCliBackend`。
  - 调整 backend selection 为显式 backend 和 `auto` backend chain 两种路径。
  - 先加载 Twitter sources，再通过 backend chain 执行采集，以支持 OpenCLI probe 后 fallback。
- Create: `tests/test_fetch_twitter_opencli.py`
  - 覆盖 OpenCLI record normalization、时间过滤、retweet 跳过、缺字段跳过、命令发现、fallback。
- Modify: `scripts/run-pipeline.py`
  - `--twitter-backend` 增加 `opencli` 和 `getxapi`。
- Modify: `scripts/test-pipeline.sh`
  - help 文案、credential gate 和 backend values 支持 `opencli|getxapi`。
- Modify: `SKILL.md`
  - `optionalBins` 增加 `opencli`。
  - `TWITTER_API_BACKEND` 枚举增加 `opencli|getxapi`。
  - 新增 `OPENCLI_BIN` 环境变量说明。
  - Quick Start 中说明 OpenCLI 为默认 Twitter 后端，API key 为 fallback。
- Modify: `README.md`, `README_CN.md`
  - 更新 Twitter/X 后端说明、环境变量示例和默认优先级。
- Modify: `references/digest-prompt.md`
  - 增加 OpenClaw agent 运行时提示：若 `jackwener/opencli` Skill 可用，优先诊断 OpenCLI，再要求 API key。
- Modify: `tests/test_config.py`
  - 增加 README/SKILL backend enum 同步断言。

## Task 1: Add OpenCLI Normalization Tests

**Files:**
- Create: `tests/test_fetch_twitter_opencli.py`
- Modify: none
- Test: `tests/test_fetch_twitter_opencli.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_fetch_twitter_opencli.py` with this content:

```python
#!/usr/bin/env python3
"""Tests for the OpenCLI Twitter backend."""

import json
import os
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import fetch_twitter


def utc(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


class TestOpenCliTweetNormalization(unittest.TestCase):
    def setUp(self):
        self.source = {
            "id": "sama-twitter",
            "type": "twitter",
            "name": "Sam Altman",
            "handle": "sama",
            "enabled": True,
            "priority": True,
            "topics": ["llm", "ai-agent"],
        }
        self.cutoff = utc("2026-05-08T00:00:00Z")

    def test_normalizes_opencli_tweet(self):
        record = {
            "id": "12345",
            "author": "sama",
            "text": "OpenCLI now powers this digest.",
            "created_at": "Fri May 08 04:03:02 +0000 2026",
            "likes": 10,
            "retweets": 2,
            "replies": 3,
            "views": 400,
            "url": "https://x.com/sama/status/12345",
            "is_retweet": False,
        }

        article = fetch_twitter.normalize_opencli_tweet(record, self.source, self.cutoff)

        self.assertEqual(article["title"], "OpenCLI now powers this digest.")
        self.assertEqual(article["link"], "https://x.com/sama/status/12345")
        self.assertEqual(article["date"], "2026-05-08T04:03:02+00:00")
        self.assertEqual(article["topics"], ["llm", "ai-agent"])
        self.assertEqual(article["tweet_id"], "12345")
        self.assertEqual(
            article["metrics"],
            {
                "like_count": 10,
                "retweet_count": 2,
                "reply_count": 3,
                "quote_count": 0,
                "impression_count": 400,
            },
        )

    def test_builds_link_and_defaults_metrics(self):
        record = {
            "id": "67890",
            "author": "sama",
            "text": "No metrics here.",
            "created_at": "2026-05-08T05:00:00Z",
            "is_retweet": False,
        }

        article = fetch_twitter.normalize_opencli_tweet(record, self.source, self.cutoff)

        self.assertEqual(article["link"], "https://x.com/sama/status/67890")
        self.assertEqual(
            article["metrics"],
            {
                "like_count": 0,
                "retweet_count": 0,
                "reply_count": 0,
                "quote_count": 0,
                "impression_count": 0,
            },
        )

    def test_skips_old_tweets(self):
        record = {
            "id": "old",
            "author": "sama",
            "text": "Old news.",
            "created_at": "2026-05-07T23:59:59Z",
            "is_retweet": False,
        }

        self.assertIsNone(fetch_twitter.normalize_opencli_tweet(record, self.source, self.cutoff))

    def test_skips_retweets(self):
        records = [
            {
                "id": "rt1",
                "author": "sama",
                "text": "A retweet.",
                "created_at": "2026-05-08T05:00:00Z",
                "is_retweet": True,
            },
            {
                "id": "rt2",
                "author": "sama",
                "text": "RT @openai: A retweet.",
                "created_at": "2026-05-08T05:00:00Z",
                "is_retweet": False,
            },
        ]

        for record in records:
            with self.subTest(record=record["id"]):
                self.assertIsNone(fetch_twitter.normalize_opencli_tweet(record, self.source, self.cutoff))

    def test_skips_malformed_records(self):
        records = [
            {"author": "sama", "text": "Missing ID", "created_at": "2026-05-08T05:00:00Z"},
            {"id": "1", "author": "sama", "created_at": "2026-05-08T05:00:00Z"},
            {"id": "1", "author": "sama", "text": "Missing date"},
            {"id": "1", "author": "sama", "text": "Bad date", "created_at": "not a date"},
        ]

        for record in records:
            with self.subTest(record=record):
                self.assertIsNone(fetch_twitter.normalize_opencli_tweet(record, self.source, self.cutoff))

    def test_extracts_records_from_common_json_shapes(self):
        shapes = [
            [{"id": "1"}],
            {"tweets": [{"id": "1"}]},
            {"data": [{"id": "1"}]},
            {"data": {"tweets": [{"id": "1"}]}},
            {"items": [{"id": "1"}]},
        ]

        for payload in shapes:
            with self.subTest(payload=payload):
                self.assertEqual(fetch_twitter.extract_opencli_tweet_records(payload), [{"id": "1"}])
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
python3 -m unittest tests.test_fetch_twitter_opencli.TestOpenCliTweetNormalization -v
```

Expected: FAIL with `AttributeError` for `normalize_opencli_tweet` or `extract_opencli_tweet_records`.

- [ ] **Step 3: Commit the failing tests**

```bash
git add tests/test_fetch_twitter_opencli.py
git commit -m "test: cover OpenCLI tweet normalization"
```

## Task 2: Implement OpenCLI Normalization Helpers

**Files:**
- Modify: `scripts/fetch-twitter.py`
- Test: `tests/test_fetch_twitter_opencli.py`

- [ ] **Step 1: Add imports and constants**

In `scripts/fetch-twitter.py`, update imports near the top:

```python
import json
import sys
import os
import argparse
import logging
import time
import tempfile
import re
import threading
import subprocess
import shutil
```

Also update the existing typing import:

```python
from typing import Dict, List, Any, Optional, Tuple
```

Add these constants after `MAX_TWEETS_PER_USER`:

```python
OPENCLI_TIMEOUT = 90
OPENCLI_MAX_WORKERS = 2
OPENCLI_GLOBAL_ERROR_CODES = {
    "opencli_missing",
    "opencli_capability_missing",
    "opencli_browser_unavailable",
    "opencli_auth_required",
    "opencli_timeout",
    "opencli_parse_error",
}
```

- [ ] **Step 2: Add OpenCLI error and parsing helpers**

Add this code after `clean_tweet_text`:

```python
class OpenCliBackendError(RuntimeError):
    """Error raised when OpenCLI cannot be used as a backend."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _parse_opencli_date(date_str: str) -> Optional[datetime]:
    """Parse OpenCLI Twitter date formats into an aware datetime."""
    if not date_str:
        return None

    value = str(date_str).strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except ValueError:
        pass

    for fmt in ("%a %b %d %H:%M:%S %z %Y", "%Y-%m-%d %H:%M:%S"):
        try:
            parsed = datetime.strptime(str(date_str), fmt)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed
        except ValueError:
            continue

    logging.debug(f"Failed to parse OpenCLI date: {date_str}")
    return None


def _as_int(value: Any) -> int:
    """Best-effort conversion for OpenCLI metric fields."""
    if value is None:
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def extract_opencli_tweet_records(payload: Any) -> List[Dict[str, Any]]:
    """Extract tweet records from common OpenCLI JSON output envelopes."""
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]

    if not isinstance(payload, dict):
        return []

    for key in ("tweets", "items", "results"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]

    data = payload.get("data")
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        return extract_opencli_tweet_records(data)

    return []


def normalize_opencli_tweet(
    record: Dict[str, Any],
    source: Dict[str, Any],
    cutoff: datetime,
) -> Optional[Dict[str, Any]]:
    """Normalize one OpenCLI tweet into the existing Twitter article shape."""
    tweet_id = str(record.get("id") or record.get("tweet_id") or "").strip()
    text = str(record.get("text") or record.get("full_text") or "").strip()
    created_at = _parse_opencli_date(record.get("created_at") or record.get("date") or "")

    if not tweet_id or not text or not created_at:
        return None
    if created_at < cutoff:
        return None
    if record.get("is_retweet") or text.startswith("RT @"):
        return None

    handle = source["handle"].lstrip("@")
    link = record.get("url") or record.get("link") or f"https://x.com/{handle}/status/{tweet_id}"

    return {
        "title": clean_tweet_text(text),
        "link": link,
        "date": created_at.isoformat(),
        "topics": source["topics"][:],
        "metrics": {
            "like_count": _as_int(record.get("likes") or record.get("like_count")),
            "retweet_count": _as_int(record.get("retweets") or record.get("retweet_count")),
            "reply_count": _as_int(record.get("replies") or record.get("reply_count")),
            "quote_count": _as_int(record.get("quotes") or record.get("quote_count")),
            "impression_count": _as_int(record.get("views") or record.get("impression_count")),
        },
        "tweet_id": tweet_id,
    }
```

- [ ] **Step 3: Run normalization tests**

Run:

```bash
python3 -m unittest tests.test_fetch_twitter_opencli.TestOpenCliTweetNormalization -v
```

Expected: PASS.

- [ ] **Step 4: Run the existing suite**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 5: Commit normalization implementation**

```bash
git add scripts/fetch-twitter.py tests/test_fetch_twitter_opencli.py
git commit -m "feat: normalize OpenCLI tweet output"
```

## Task 3: Add OpenCLI Discovery and Backend Selection Tests

**Files:**
- Modify: `tests/test_fetch_twitter_opencli.py`
- Test: `tests/test_fetch_twitter_opencli.py`

- [ ] **Step 1: Add discovery and fallback tests**

Append this code to `tests/test_fetch_twitter_opencli.py` before the final `if __name__ == "__main__"` block if one exists. If no final block exists, append it to the end of the file.

```python
class TestOpenCliDiscovery(unittest.TestCase):
    def test_resolves_opencli_bin_from_env(self):
        with patch.dict(os.environ, {"OPENCLI_BIN": "/custom/opencli"}):
            self.assertEqual(fetch_twitter.resolve_opencli_bin(), "/custom/opencli")

    def test_resolves_opencli_bin_from_path(self):
        with patch.dict(os.environ, {}, clear=True), patch("fetch_twitter.shutil.which", return_value="/usr/local/bin/opencli"):
            self.assertEqual(fetch_twitter.resolve_opencli_bin(), "/usr/local/bin/opencli")

    def test_missing_opencli_bin_raises(self):
        with patch.dict(os.environ, {}, clear=True), patch("fetch_twitter.shutil.which", return_value=None):
            with self.assertRaises(fetch_twitter.OpenCliBackendError) as ctx:
                fetch_twitter.resolve_opencli_bin()
        self.assertEqual(ctx.exception.code, "opencli_missing")

    def test_detects_twitter_tweets_capability_from_list_json(self):
        payloads = [
            [{"site": "twitter", "name": "tweets"}],
            {"commands": [{"site": "twitter", "name": "tweets"}]},
            {"twitter": ["search", "timeline", "tweets"]},
        ]
        for payload in payloads:
            with self.subTest(payload=payload):
                self.assertTrue(fetch_twitter.opencli_has_twitter_tweets(payload))

    def test_rejects_missing_twitter_tweets_capability(self):
        payload = {"commands": [{"site": "twitter", "name": "search"}]}
        self.assertFalse(fetch_twitter.opencli_has_twitter_tweets(payload))


class TestBackendSelection(unittest.TestCase):
    def test_auto_backend_order_starts_with_opencli(self):
        self.assertEqual(
            fetch_twitter.get_backend_order("auto"),
            ["opencli", "getxapi", "twitterapiio", "official"],
        )

    def test_explicit_opencli_has_no_api_fallback(self):
        self.assertEqual(fetch_twitter.get_backend_order("opencli"), ["opencli"])

    def test_explicit_api_backend_order_is_single_backend(self):
        self.assertEqual(fetch_twitter.get_backend_order("getxapi"), ["getxapi"])
        self.assertEqual(fetch_twitter.get_backend_order("twitterapiio"), ["twitterapiio"])
        self.assertEqual(fetch_twitter.get_backend_order("official"), ["official"])
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
python3 -m unittest tests.test_fetch_twitter_opencli.TestOpenCliDiscovery tests.test_fetch_twitter_opencli.TestBackendSelection -v
```

Expected: FAIL with missing `resolve_opencli_bin`, `opencli_has_twitter_tweets`, or `get_backend_order`.

- [ ] **Step 3: Commit failing tests**

```bash
git add tests/test_fetch_twitter_opencli.py
git commit -m "test: cover OpenCLI backend discovery"
```

## Task 4: Implement OpenCLI Discovery Helpers

**Files:**
- Modify: `scripts/fetch-twitter.py`
- Test: `tests/test_fetch_twitter_opencli.py`

- [ ] **Step 1: Add discovery helpers**

Add this code after `normalize_opencli_tweet`:

```python
def resolve_opencli_bin() -> str:
    """Resolve the OpenCLI executable from OPENCLI_BIN or PATH."""
    configured = os.getenv("OPENCLI_BIN")
    if configured:
        return configured

    found = shutil.which("opencli")
    if found:
        return found

    raise OpenCliBackendError(
        "opencli_missing",
        "OpenCLI executable not found. Set OPENCLI_BIN or install opencli on PATH.",
    )


def opencli_has_twitter_tweets(payload: Any) -> bool:
    """Return true when `opencli list -f json` exposes twitter tweets."""
    if isinstance(payload, list):
        for item in payload:
            if opencli_has_twitter_tweets(item):
                return True
        return False

    if isinstance(payload, dict):
        site = str(payload.get("site") or payload.get("group") or "").lower()
        name = str(payload.get("name") or payload.get("command") or "").lower()
        if site == "twitter" and name == "tweets":
            return True

        if "twitter" in payload:
            twitter_value = payload["twitter"]
            if isinstance(twitter_value, list):
                return "tweets" in [str(item).lower() for item in twitter_value]
            if isinstance(twitter_value, dict):
                return opencli_has_twitter_tweets(twitter_value)

        for key in ("commands", "items", "data", "sites"):
            if key in payload and opencli_has_twitter_tweets(payload[key]):
                return True

    return False


def get_backend_order(backend_name: str) -> List[str]:
    """Return backend candidates in the order they should be attempted."""
    if backend_name == "auto":
        return ["opencli", "getxapi", "twitterapiio", "official"]
    return [backend_name]
```

- [ ] **Step 2: Run discovery tests**

Run:

```bash
python3 -m unittest tests.test_fetch_twitter_opencli.TestOpenCliDiscovery tests.test_fetch_twitter_opencli.TestBackendSelection -v
```

Expected: PASS.

- [ ] **Step 3: Run full tests**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 4: Commit discovery helpers**

```bash
git add scripts/fetch-twitter.py tests/test_fetch_twitter_opencli.py
git commit -m "feat: discover OpenCLI twitter capability"
```

## Task 5: Add OpenCliBackend Execution Tests

**Files:**
- Modify: `tests/test_fetch_twitter_opencli.py`
- Test: `tests/test_fetch_twitter_opencli.py`

- [ ] **Step 1: Add backend subprocess tests**

Append this code to `tests/test_fetch_twitter_opencli.py`:

```python
class TestOpenCliBackend(unittest.TestCase):
    def setUp(self):
        self.source = {
            "id": "sama-twitter",
            "type": "twitter",
            "name": "Sam Altman",
            "handle": "sama",
            "enabled": True,
            "priority": True,
            "topics": ["llm"],
        }
        self.cutoff = utc("2026-05-08T00:00:00Z")

    def _completed(self, stdout, returncode=0, stderr=""):
        return subprocess.CompletedProcess(
            args=["opencli"],
            returncode=returncode,
            stdout=stdout,
            stderr=stderr,
        )

    @patch("fetch_twitter.resolve_opencli_bin", return_value="/bin/opencli")
    @patch("subprocess.run")
    def test_fetches_tweets_for_source(self, run_mock, _resolve_mock):
        run_mock.side_effect = [
            self._completed(json.dumps({"commands": [{"site": "twitter", "name": "tweets"}]})),
            self._completed("OpenCLI doctor ok"),
            self._completed(json.dumps([
                {
                    "id": "123",
                    "author": "sama",
                    "text": "A useful post.",
                    "created_at": "2026-05-08T01:00:00Z",
                    "likes": 5,
                    "retweets": 1,
                    "replies": 0,
                    "views": 100,
                    "url": "https://x.com/sama/status/123",
                    "is_retweet": False,
                }
            ])),
        ]

        backend = fetch_twitter.OpenCliBackend()
        results = backend.fetch_all([self.source], self.cutoff)

        self.assertEqual(results[0]["status"], "ok")
        self.assertEqual(results[0]["handle"], "sama")
        self.assertEqual(results[0]["count"], 1)
        self.assertEqual(results[0]["articles"][0]["tweet_id"], "123")
        self.assertIn(
            ["/bin/opencli", "twitter", "tweets", "sama", "--limit", "20", "-f", "json"],
            [call.args[0] for call in run_mock.call_args_list],
        )

    @patch("fetch_twitter.resolve_opencli_bin", return_value="/bin/opencli")
    @patch("subprocess.run")
    def test_missing_capability_raises_global_error(self, run_mock, _resolve_mock):
        run_mock.return_value = self._completed(json.dumps({"commands": [{"site": "twitter", "name": "search"}]}))

        with self.assertRaises(fetch_twitter.OpenCliBackendError) as ctx:
            fetch_twitter.OpenCliBackend()

        self.assertEqual(ctx.exception.code, "opencli_capability_missing")

    @patch("fetch_twitter.resolve_opencli_bin", return_value="/bin/opencli")
    @patch("subprocess.run")
    def test_auth_required_raises_global_error_on_probe(self, run_mock, _resolve_mock):
        run_mock.side_effect = [
            self._completed(json.dumps({"commands": [{"site": "twitter", "name": "tweets"}]})),
            self._completed("OpenCLI doctor ok"),
            self._completed("", returncode=77, stderr="Not logged into x.com"),
        ]

        backend = fetch_twitter.OpenCliBackend()

        with self.assertRaises(fetch_twitter.OpenCliBackendError) as ctx:
            backend.fetch_all([self.source], self.cutoff)

        self.assertEqual(ctx.exception.code, "opencli_auth_required")

    @patch("fetch_twitter.resolve_opencli_bin", return_value="/bin/opencli")
    @patch("subprocess.run")
    def test_single_source_error_does_not_raise_global_error(self, run_mock, _resolve_mock):
        second_source = dict(self.source)
        second_source["id"] = "openai-twitter"
        second_source["name"] = "OpenAI"
        second_source["handle"] = "OpenAI"

        run_mock.side_effect = [
            self._completed(json.dumps({"commands": [{"site": "twitter", "name": "tweets"}]})),
            self._completed("OpenCLI doctor ok"),
            self._completed(json.dumps([
                {
                    "id": "probe",
                    "author": "sama",
                    "text": "Probe works.",
                    "created_at": "2026-05-08T01:00:00Z",
                    "is_retweet": False,
                }
            ])),
            self._completed("", returncode=1, stderr="Could not resolve @OpenAI"),
        ]

        backend = fetch_twitter.OpenCliBackend()
        results = backend.fetch_all([self.source, second_source], self.cutoff)

        by_handle = {item["handle"]: item for item in results}
        self.assertEqual(by_handle["sama"]["status"], "ok")
        self.assertEqual(by_handle["OpenAI"]["status"], "error")
        self.assertIn("opencli_source_error", by_handle["OpenAI"]["error"])
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
python3 -m unittest tests.test_fetch_twitter_opencli.TestOpenCliBackend -v
```

Expected: FAIL with missing `OpenCliBackend`.

- [ ] **Step 3: Commit failing tests**

```bash
git add tests/test_fetch_twitter_opencli.py
git commit -m "test: cover OpenCLI backend execution"
```

## Task 6: Implement OpenCliBackend

**Files:**
- Modify: `scripts/fetch-twitter.py`
- Test: `tests/test_fetch_twitter_opencli.py`

- [ ] **Step 1: Add subprocess classification helpers**

Add this code after `get_backend_order`:

```python
def _classify_opencli_failure(returncode: int, stderr: str) -> str:
    """Map OpenCLI process failures into stable backend error codes."""
    text = (stderr or "").lower()
    if returncode == 69:
        return "opencli_browser_unavailable"
    if returncode == 75:
        return "opencli_timeout"
    if returncode == 77:
        return "opencli_auth_required"
    if "not logged" in text or "auth" in text or "permission" in text:
        return "opencli_auth_required"
    if "browser" in text and ("unavailable" in text or "connect" in text):
        return "opencli_browser_unavailable"
    return "opencli_source_error"
```

- [ ] **Step 2: Add `OpenCliBackend`**

Add this class before `OfficialBackend`:

```python
class OpenCliBackend(TwitterBackend):
    """OpenCLI backend using the browser-backed twitter tweets adapter."""

    def __init__(self, command: Optional[str] = None):
        self.command = command or resolve_opencli_bin()
        self._verify_capability()
        self._run_doctor()

    def _run_command(self, args: List[str], timeout: int = OPENCLI_TIMEOUT) -> subprocess.CompletedProcess:
        try:
            return subprocess.run(
                [self.command] + args,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=os.environ,
            )
        except subprocess.TimeoutExpired as exc:
            raise OpenCliBackendError("opencli_timeout", f"OpenCLI command timed out: {exc}") from exc

    def _verify_capability(self) -> None:
        result = self._run_command(["list", "-f", "json"], timeout=30)
        if result.returncode != 0:
            code = _classify_opencli_failure(result.returncode, result.stderr)
            raise OpenCliBackendError(code, result.stderr.strip() or "opencli list failed")

        try:
            payload = json.loads(result.stdout or "null")
        except json.JSONDecodeError as exc:
            raise OpenCliBackendError("opencli_parse_error", "opencli list returned invalid JSON") from exc

        if not opencli_has_twitter_tweets(payload):
            raise OpenCliBackendError(
                "opencli_capability_missing",
                "OpenCLI does not expose the twitter tweets command.",
            )

    def _run_doctor(self) -> None:
        result = self._run_command(["doctor"], timeout=30)
        if result.returncode == 0:
            return
        code = _classify_opencli_failure(result.returncode, result.stderr)
        if code in {"opencli_browser_unavailable", "opencli_auth_required"}:
            raise OpenCliBackendError(code, result.stderr.strip() or "opencli doctor failed")
        logging.warning(f"opencli doctor returned {result.returncode}: {(result.stderr or result.stdout).strip()[:200]}")

    def _parse_tweets_output(self, stdout: str, source: Dict[str, Any], cutoff: datetime) -> List[Dict[str, Any]]:
        try:
            payload = json.loads(stdout or "null")
        except json.JSONDecodeError as exc:
            raise OpenCliBackendError("opencli_parse_error", "opencli twitter tweets returned invalid JSON") from exc

        articles = []
        for record in extract_opencli_tweet_records(payload):
            article = normalize_opencli_tweet(record, source, cutoff)
            if article:
                articles.append(article)
        return articles

    def _fetch_user_tweets(self, source: Dict[str, Any], cutoff: datetime) -> Dict[str, Any]:
        handle = source["handle"].lstrip("@")
        result = self._run_command(
            ["twitter", "tweets", handle, "--limit", str(MAX_TWEETS_PER_USER), "-f", "json"]
        )

        if result.returncode != 0:
            code = _classify_opencli_failure(result.returncode, result.stderr)
            message = (result.stderr or result.stdout or "opencli twitter tweets failed").strip()
            if code in OPENCLI_GLOBAL_ERROR_CODES:
                raise OpenCliBackendError(code, message)
            return self._make_error(source, f"{code}: {message[:160]}", 0)

        articles = self._parse_tweets_output(result.stdout, source, cutoff)
        return self._make_result(source, articles, 0)

    def fetch_all(self, sources: List[Dict[str, Any]], cutoff: datetime) -> List[Dict[str, Any]]:
        if not sources:
            return []

        results: List[Dict[str, Any]] = []
        total = len(sources)

        # Probe one account first so auth/browser failures can fall back before all accounts run.
        first = self._fetch_user_tweets(sources[0], cutoff)
        results.append(first)
        logging.info(f"[1/{total}] @{first['handle']}: {first['count']} tweets via OpenCLI")

        remaining = sources[1:]
        if not remaining:
            return results

        done = 1
        with ThreadPoolExecutor(max_workers=OPENCLI_MAX_WORKERS) as pool:
            futures = {pool.submit(self._fetch_user_tweets, source, cutoff): source for source in remaining}
            for future in as_completed(futures):
                source = futures[future]
                try:
                    result = future.result()
                except OpenCliBackendError as exc:
                    result = self._make_error(source, f"{exc.code}: {exc.message[:160]}", 0)
                results.append(result)
                done += 1
                if result["status"] == "ok":
                    logging.info(f"[{done}/{total}] ✅ @{result['handle']}: {result['count']} tweets via OpenCLI")
                else:
                    logging.warning(f"[{done}/{total}] ❌ @{result['handle']}: {result.get('error', 'unknown')}")

        return results
```

- [ ] **Step 3: Run OpenCLI backend tests**

Run:

```bash
python3 -m unittest tests.test_fetch_twitter_opencli.TestOpenCliBackend -v
```

Expected: PASS.

- [ ] **Step 4: Run full tests**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 5: Commit OpenCliBackend**

```bash
git add scripts/fetch-twitter.py tests/test_fetch_twitter_opencli.py
git commit -m "feat: add OpenCLI twitter backend"
```

## Task 7: Refactor Backend Chain and CLI Options

**Files:**
- Modify: `scripts/fetch-twitter.py`
- Modify: `scripts/run-pipeline.py`
- Modify: `scripts/test-pipeline.sh`
- Test: `tests/test_fetch_twitter_opencli.py`

- [ ] **Step 1: Add backend chain tests**

Append this code to `tests/test_fetch_twitter_opencli.py`:

```python
class TestBackendChain(unittest.TestCase):
    def setUp(self):
        self.sources = [
            {
                "id": "sama-twitter",
                "type": "twitter",
                "name": "Sam Altman",
                "handle": "sama",
                "enabled": True,
                "priority": True,
                "topics": ["llm"],
            }
        ]
        self.cutoff = utc("2026-05-08T00:00:00Z")

    @patch.dict(os.environ, {"GETX_API_KEY": "x" * 20}, clear=True)
    @patch("fetch_twitter.OpenCliBackend", side_effect=fetch_twitter.OpenCliBackendError("opencli_missing", "missing"))
    @patch("fetch_twitter.GetXApiBackend")
    def test_auto_falls_back_from_opencli_to_getxapi(self, getx_cls, _opencli_cls):
        getx = getx_cls.return_value
        getx.fetch_all.return_value = [{"status": "ok", "count": 0, "articles": []}]

        backend_name, results, diagnostics = fetch_twitter.fetch_with_backend_chain(
            "auto", self.sources, self.cutoff, no_cache=False
        )

        self.assertEqual(backend_name, "getxapi")
        self.assertEqual(results, [{"status": "ok", "count": 0, "articles": []}])
        self.assertEqual(diagnostics[0]["backend"], "opencli")
        self.assertEqual(diagnostics[0]["code"], "opencli_missing")

    @patch.dict(os.environ, {}, clear=True)
    @patch("fetch_twitter.OpenCliBackend", side_effect=fetch_twitter.OpenCliBackendError("opencli_missing", "missing"))
    def test_explicit_opencli_does_not_fallback(self, _opencli_cls):
        backend_name, results, diagnostics = fetch_twitter.fetch_with_backend_chain(
            "opencli", self.sources, self.cutoff, no_cache=False
        )

        self.assertEqual(backend_name, "opencli")
        self.assertEqual(results, [])
        self.assertEqual(diagnostics[0]["code"], "opencli_missing")

    @patch.dict(os.environ, {}, clear=True)
    @patch("fetch_twitter.OpenCliBackend", side_effect=fetch_twitter.OpenCliBackendError("opencli_missing", "missing"))
    def test_auto_returns_no_results_when_no_backend_available(self, _opencli_cls):
        backend_name, results, diagnostics = fetch_twitter.fetch_with_backend_chain(
            "auto", self.sources, self.cutoff, no_cache=False
        )

        self.assertEqual(backend_name, "auto")
        self.assertEqual(results, [])
        self.assertTrue(any(item["backend"] == "opencli" for item in diagnostics))
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
python3 -m unittest tests.test_fetch_twitter_opencli.TestBackendChain -v
```

Expected: FAIL with missing `fetch_with_backend_chain`.

- [ ] **Step 3: Replace backend selection functions**

In `scripts/fetch-twitter.py`, keep existing API backend constructors but replace `select_backend` with these functions:

```python
def _instantiate_backend(backend_name: str, no_cache: bool = False) -> Optional[TwitterBackend]:
    """Instantiate one backend without applying fallback policy."""
    if backend_name == "opencli":
        logging.info("Using OpenCLI backend")
        return OpenCliBackend()

    if backend_name == "getxapi":
        key = os.getenv("GETX_API_KEY")
        if not key:
            logging.info("GETX_API_KEY not set; getxapi backend unavailable")
            return None
        logging.info("Using GetXAPI backend")
        return GetXApiBackend(key)

    if backend_name == "twitterapiio":
        key = os.getenv("TWITTERAPI_IO_KEY")
        if not key:
            logging.info("TWITTERAPI_IO_KEY not set; twitterapi.io backend unavailable")
            return None
        logging.info("Using twitterapi.io backend")
        return TwitterApiIoBackend(key)

    if backend_name == "official":
        token = os.getenv("X_BEARER_TOKEN")
        if not token:
            logging.info("X_BEARER_TOKEN not set; official backend unavailable")
            return None
        logging.info("Using official X API v2 backend")
        return OfficialBackend(token, no_cache=no_cache)

    logging.error(f"Unknown backend: {backend_name}")
    return None


def fetch_with_backend_chain(
    backend_name: str,
    sources: List[Dict[str, Any]],
    cutoff: datetime,
    no_cache: bool = False,
) -> Tuple[str, List[Dict[str, Any]], List[Dict[str, str]]]:
    """Fetch Twitter data using explicit backend or auto fallback chain."""
    diagnostics: List[Dict[str, str]] = []
    explicit = backend_name != "auto"

    for candidate in get_backend_order(backend_name):
        try:
            backend = _instantiate_backend(candidate, no_cache=no_cache)
        except OpenCliBackendError as exc:
            diagnostics.append({"backend": candidate, "code": exc.code, "message": exc.message})
            logging.warning(f"{candidate} unavailable: {exc.code}: {exc.message}")
            if explicit:
                return candidate, [], diagnostics
            continue

        if backend is None:
            diagnostics.append({
                "backend": candidate,
                "code": "backend_unavailable",
                "message": f"{candidate} backend is not configured",
            })
            if explicit:
                return candidate, [], diagnostics
            continue

        try:
            return candidate, backend.fetch_all(sources, cutoff), diagnostics
        except OpenCliBackendError as exc:
            diagnostics.append({"backend": candidate, "code": exc.code, "message": exc.message})
            logging.warning(f"{candidate} failed globally: {exc.code}: {exc.message}")
            if explicit:
                return candidate, [], diagnostics
            continue

    return backend_name, [], diagnostics
```

- [ ] **Step 4: Refactor `main` to load sources before backend chain**

In `scripts/fetch-twitter.py`, replace the block from `backend = select_backend(...)` through the old `results = backend.fetch_all(sources, cutoff)` with this structure:

```python
    # Auto-generate unique output path if not specified
    if not args.output:
        fd, temp_path = tempfile.mkstemp(prefix="follow-news-twitter-", suffix=".json")
        os.close(fd)
        args.output = Path(temp_path)

    try:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=args.hours)

        # Backward compatibility: if only --config provided, use old behavior
        if args.config and args.defaults == Path("config/defaults") and not args.defaults.exists():
            logger.debug("Backward compatibility mode: using --config as sole source")
            sources = load_twitter_sources(args.config, None)
        else:
            sources = load_twitter_sources(args.defaults, args.config)

        if not sources:
            logger.warning("No Twitter sources found or all disabled")

        logger.info(f"Fetching {len(sources)} Twitter accounts (window: {args.hours}h, backend: {backend_name})")

        selected_backend, results, backend_diagnostics = fetch_with_backend_chain(
            backend_name,
            sources,
            cutoff,
            no_cache=args.no_cache,
        )

        if not results:
            logger.warning("No Twitter backend available. Writing empty result and skipping Twitter fetch.")
            empty_result = {
                "generated": datetime.now(timezone.utc).isoformat(),
                "source_type": "twitter",
                "backend": selected_backend,
                "hours": args.hours,
                "sources_total": 0,
                "sources_ok": 0,
                "total_articles": 0,
                "sources": [],
                "skipped_reason": f"No usable backend for '{backend_name}'",
                "backend_diagnostics": backend_diagnostics,
            }
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(empty_result, f, ensure_ascii=False, indent=2)
            print(f"Output (empty): {args.output}")
            return 0
```

Then update the final output dict to include the selected backend and diagnostics:

```python
        output = {
            "generated": datetime.now(timezone.utc).isoformat(),
            "source_type": "twitter",
            "backend": selected_backend,
            "requested_backend": backend_name,
            "backend_diagnostics": backend_diagnostics,
            "defaults_dir": str(args.defaults),
            "config_dir": str(args.config) if args.config else None,
            "hours": args.hours,
            "sources_total": len(results),
            "sources_ok": ok_count,
            "total_articles": total_tweets,
            "sources": results,
        }
```

- [ ] **Step 5: Update argparse choices and help**

In `scripts/fetch-twitter.py`, change backend choices:

```python
choices=["opencli", "official", "twitterapiio", "getxapi", "auto"],
```

Use this help text:

```python
help="Twitter backend (overrides TWITTER_API_BACKEND env var). "
     "auto = opencli first, then getxapi, twitterapiio, official"
```

Update parser description to:

```python
description="Fetch recent tweets from Twitter/X KOL accounts. "
            "Supports OpenCLI, GetXAPI, twitterapi.io, and official X API v2 backends.",
```

- [ ] **Step 6: Update pipeline CLI choices**

In `scripts/run-pipeline.py`, change:

```python
parser.add_argument("--twitter-backend", choices=["official", "twitterapiio", "auto"], default=None, help="Twitter API backend to use")
```

to:

```python
parser.add_argument("--twitter-backend", choices=["opencli", "getxapi", "official", "twitterapiio", "auto"], default=None, help="Twitter backend to use")
```

- [ ] **Step 7: Update smoke test script help and credential gate**

In `scripts/test-pipeline.sh`, change the help block backend section to:

```text
  --twitter-backend NAME
                    Force a specific Twitter backend
                    Values: opencli, getxapi, official, twitterapiio, auto
                    opencli     = OpenCLI browser-backed X/Twitter adapter
                    getxapi     = GetXAPI (needs GETX_API_KEY)
                    official    = X API v2 (needs X_BEARER_TOKEN)
                    twitterapiio = twitterapi.io (needs TWITTERAPI_IO_KEY)
                    auto        = try opencli first, then API fallbacks
```

Replace the Twitter credential gate with:

```bash
    if [ -n "$OPENCLI_BIN" ] || command -v opencli >/dev/null 2>&1 || [ -n "$GETX_API_KEY" ] || [ -n "$X_BEARER_TOKEN" ] || [ -n "$TWITTERAPI_IO_KEY" ]; then
        run_step "fetch-twitter" python3 "$SCRIPT_DIR/fetch-twitter.py" "${TWITTER_ARGS[@]}"
        validate_json "$OUTDIR/twitter.json" "twitter"
    else
        echo "⏭  fetch-twitter (no opencli or Twitter API credentials)"
        SKIPPED=$((SKIPPED + 1))
    fi
```

Update environment help:

```text
  OPENCLI_BIN        Optional path to OpenCLI executable
  GETX_API_KEY       GetXAPI key (for --backend getxapi)
  X_BEARER_TOKEN     Official X API v2 bearer token (for --backend official)
  TWITTERAPI_IO_KEY  twitterapi.io API key (for --backend twitterapiio)
  TWITTER_API_BACKEND Default twitter backend if --backend not given (auto|opencli|getxapi|twitterapiio|official)
```

- [ ] **Step 8: Run backend chain and parser tests**

Run:

```bash
python3 -m unittest tests.test_fetch_twitter_opencli.TestBackendChain -v
python3 scripts/fetch-twitter.py --help >/tmp/follow-news-fetch-twitter-help.txt
python3 scripts/run-pipeline.py --help >/tmp/follow-news-run-pipeline-help.txt
```

Expected: first command PASS; help commands exit 0.

- [ ] **Step 9: Run full tests**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 10: Commit backend chain and CLI changes**

```bash
git add scripts/fetch-twitter.py scripts/run-pipeline.py scripts/test-pipeline.sh tests/test_fetch_twitter_opencli.py
git commit -m "feat: prefer OpenCLI in twitter backend auto mode"
```

## Task 8: Add Merge Compatibility Fixture Test

**Files:**
- Modify: `tests/test_fetch_twitter_opencli.py`
- Test: `tests/test_fetch_twitter_opencli.py`

- [ ] **Step 1: Add merge compatibility test**

Append this code to `tests/test_fetch_twitter_opencli.py`:

```python
class TestOpenCliMergeCompatibility(unittest.TestCase):
    def test_opencli_articles_keep_existing_merge_shape(self):
        import importlib.util

        merge_spec = importlib.util.spec_from_file_location(
            "merge_sources",
            SCRIPTS_DIR / "merge-sources.py",
        )
        merge_mod = importlib.util.module_from_spec(merge_spec)
        merge_spec.loader.exec_module(merge_mod)

        source = {
            "source_id": "sama-twitter",
            "source_type": "twitter",
            "name": "Sam Altman",
            "handle": "sama",
            "priority": True,
            "topics": ["llm"],
            "status": "ok",
            "attempts": 1,
            "count": 1,
            "articles": [],
        }
        config_source = {
            "id": "sama-twitter",
            "type": "twitter",
            "name": "Sam Altman",
            "handle": "sama",
            "enabled": True,
            "priority": True,
            "topics": ["llm"],
        }
        article = fetch_twitter.normalize_opencli_tweet(
            {
                "id": "123",
                "author": "sama",
                "text": "A high-signal tweet.",
                "created_at": "2026-05-08T05:00:00Z",
                "likes": 1000,
                "retweets": 20,
                "replies": 3,
                "views": 5000,
                "is_retweet": False,
            },
            config_source,
            utc("2026-05-08T00:00:00Z"),
        )
        article["source_type"] = "twitter"

        score = merge_mod.calculate_base_score(article, source)

        self.assertIn("title", article)
        self.assertIn("link", article)
        self.assertIn("date", article)
        self.assertIn("metrics", article)
        self.assertGreaterEqual(score, 8)
```

- [ ] **Step 2: Run the compatibility test**

Run:

```bash
python3 -m unittest tests.test_fetch_twitter_opencli.TestOpenCliMergeCompatibility -v
```

Expected: PASS.

- [ ] **Step 3: Run full tests**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 4: Commit compatibility test**

```bash
git add tests/test_fetch_twitter_opencli.py
git commit -m "test: verify OpenCLI output merges as twitter articles"
```

## Task 9: Update OpenClaw Skill and User Docs

**Files:**
- Modify: `SKILL.md`
- Modify: `README.md`
- Modify: `README_CN.md`
- Modify: `references/digest-prompt.md`
- Modify: `tests/test_config.py`
- Test: `tests/test_config.py`

- [ ] **Step 1: Add doc synchronization tests**

In `tests/test_config.py`, add this method to `TestReadmeCounts`:

```python
    def test_twitter_backend_docs_include_opencli(self):
        readme_en = README_EN.read_text(encoding="utf-8")
        readme_zh = README_ZH.read_text(encoding="utf-8")
        skill = (Path(__file__).parent.parent / "SKILL.md").read_text(encoding="utf-8")

        for content in (readme_en, readme_zh, skill):
            self.assertIn("opencli", content.lower())
            self.assertIn("getxapi", content.lower())
            self.assertIn("twitterapiio", content.lower())
            self.assertIn("official", content.lower())

        self.assertIn("OPENCLI_BIN", skill)
```

- [ ] **Step 2: Run docs test to verify it fails**

Run:

```bash
python3 -m unittest tests.test_config.TestReadmeCounts.test_twitter_backend_docs_include_opencli -v
```

Expected: FAIL because docs do not yet mention `opencli` and `OPENCLI_BIN`.

- [ ] **Step 3: Update `SKILL.md` metadata and env**

In `SKILL.md`, change optional bins:

```yaml
    optionalBins: ["opencli", "mail", "msmtp", "gog", "gh", "openssl", "weasyprint"]
```

Change `TWITTER_API_BACKEND` env description:

```yaml
  - name: TWITTER_API_BACKEND
    required: false
    description: "Twitter backend: 'auto', 'opencli', 'getxapi', 'twitterapiio', or 'official' (default: auto; auto tries OpenCLI first)"
```

Add this env entry after `TWITTER_API_BACKEND`:

```yaml
  - name: OPENCLI_BIN
    required: false
    description: Optional path to the OpenCLI executable. Used when OpenCLI is not available on PATH.
```

Update Quick Start environment variables:

```markdown
   - `TWITTER_API_BACKEND` - Twitter backend: auto|opencli|getxapi|twitterapiio|official (optional, default: auto)
   - `OPENCLI_BIN` - OpenCLI executable path override (optional)
   - `GETX_API_KEY` - GetXAPI key for Twitter/X fallback (optional)
   - `TWITTERAPI_IO_KEY` - twitterapi.io API key for Twitter/X fallback (optional)
   - `X_BEARER_TOKEN` - Twitter/X official API bearer token for final fallback (optional)
```

Add this paragraph after Quick Start step 2:

```markdown
   OpenCLI is the preferred Twitter/X backend in `auto` mode. In OpenClaw environments where `jackwener/opencli` is installed, the agent should use that skill to validate `opencli doctor`, browser bridge state, and X login before asking for API keys.
```

- [ ] **Step 4: Update README environment sections**

In `README.md`, replace the Twitter environment block with:

```markdown
# Twitter/X Backend (auto priority: opencli > getxapi > twitterapiio > official)
export TWITTER_API_BACKEND="auto"  # auto|opencli|getxapi|twitterapiio|official
export OPENCLI_BIN="/path/to/opencli"  # optional; defaults to opencli on PATH
export GETX_API_KEY="..."        # GetXAPI fallback
export TWITTERAPI_IO_KEY="..."   # twitterapi.io fallback
export X_BEARER_TOKEN="..."      # Official X API v2 fallback
```

Add this paragraph below that block:

```markdown
OpenCLI is preferred because it can reuse an authenticated Chrome/Chromium session instead of requiring Twitter API credentials. API backends remain available for CI, headless machines, or users who already configured API keys.
```

In `README_CN.md`, replace the Twitter environment block with:

```markdown
# Twitter/X 后端（自动优先级：opencli > getxapi > twitterapiio > official）
export TWITTER_API_BACKEND="auto"  # auto|opencli|getxapi|twitterapiio|official
export OPENCLI_BIN="/path/to/opencli"  # 可选；默认使用 PATH 上的 opencli
export GETX_API_KEY="..."        # GetXAPI fallback
export TWITTERAPI_IO_KEY="..."   # twitterapi.io fallback
export X_BEARER_TOKEN="..."      # Twitter/X 官方 API v2 fallback
```

Add this paragraph below that block:

```markdown
OpenCLI 是默认优先后端，因为它可以复用已经登录的 Chrome/Chromium 会话，不再强制要求 Twitter API 凭据。CI、无浏览器环境，或已经配置 API key 的用户仍可通过 API 后端 fallback。
```

- [ ] **Step 5: Update digest prompt with OpenClaw agent guidance**

In `references/digest-prompt.md`, add this section after the Data Collection Pipeline command block:

```markdown
### Twitter/X Backend Guidance

Twitter/X uses `TWITTER_API_BACKEND=auto` by default. Auto mode tries OpenCLI first, then API fallbacks. If the `jackwener/opencli` skill is available in OpenClaw and Twitter data is missing, use that skill to validate `opencli doctor`, browser bridge connectivity, and X login state before asking the user for API credentials.
```

- [ ] **Step 6: Run docs tests**

Run:

```bash
python3 -m unittest tests.test_config.TestReadmeCounts -v
```

Expected: PASS.

- [ ] **Step 7: Run full tests**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 8: Commit docs**

```bash
git add SKILL.md README.md README_CN.md references/digest-prompt.md tests/test_config.py
git commit -m "docs: document OpenCLI twitter backend"
```

## Task 10: Manual Validation and Final Review

**Files:**
- Modify: none
- Test: full repository

- [ ] **Step 1: Confirm no old backend docs remain**

Run:

```bash
rg -n "auto priority: getxapi|auto = getxapi|official\\|twitterapiio\\|auto|twitterapiio first" README.md README_CN.md SKILL.md scripts tests references
```

Expected: no output.

- [ ] **Step 2: Run full unit tests**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 3: Validate CLI help**

Run:

```bash
python3 scripts/fetch-twitter.py --help | rg "opencli|getxapi|twitterapiio|official|auto"
python3 scripts/run-pipeline.py --help | rg "opencli|getxapi|twitterapiio|official|auto"
./scripts/test-pipeline.sh --help | rg "opencli|getxapi|twitterapiio|official|auto"
```

Expected: each command prints backend help including all five backend names.

- [ ] **Step 4: Validate explicit OpenCLI empty-result behavior when OpenCLI is unavailable**

Run in an environment where `opencli` is not on PATH:

```bash
env -u OPENCLI_BIN PATH="/usr/bin:/bin" python3 scripts/fetch-twitter.py \
  --backend opencli \
  --defaults config/defaults \
  --hours 1 \
  --output /tmp/follow-news-opencli-missing.json \
  --force \
  --verbose
python3 -m json.tool /tmp/follow-news-opencli-missing.json | rg "opencli_missing|backend_diagnostics|total_articles"
```

Expected: command exits 0, output contains `opencli_missing`, `backend_diagnostics`, and `"total_articles": 0`.

- [ ] **Step 5: Validate auto fallback with no credentials**

Run:

```bash
env -u OPENCLI_BIN -u GETX_API_KEY -u TWITTERAPI_IO_KEY -u X_BEARER_TOKEN PATH="/usr/bin:/bin" python3 scripts/fetch-twitter.py \
  --backend auto \
  --defaults config/defaults \
  --hours 1 \
  --output /tmp/follow-news-auto-no-backend.json \
  --force \
  --verbose
python3 -m json.tool /tmp/follow-news-auto-no-backend.json | rg "backend_diagnostics|total_articles"
```

Expected: command exits 0, output contains `backend_diagnostics` and `"total_articles": 0`.

- [ ] **Step 6: Validate real OpenCLI path when available**

Run only on a local machine where OpenCLI is installed, Chrome/Chromium has the Browser Bridge extension, and X is logged in:

```bash
python3 scripts/fetch-twitter.py \
  --backend opencli \
  --defaults config/defaults \
  --hours 24 \
  --output /tmp/follow-news-twitter-opencli.json \
  --verbose \
  --force
python3 -m json.tool /tmp/follow-news-twitter-opencli.json | rg '"backend": "opencli"|"total_articles"|"sources_ok"'
```

Expected: command exits 0. If X login is valid, output has `"backend": "opencli"` and nonzero `sources_ok`. If X login is invalid, output has `backend_diagnostics` with `opencli_auth_required`.

- [ ] **Step 7: Inspect final diff**

Run:

```bash
git status --short
git diff --stat HEAD
git diff HEAD -- scripts/fetch-twitter.py tests/test_fetch_twitter_opencli.py README.md README_CN.md SKILL.md references/digest-prompt.md | sed -n '1,260p'
```

Expected: only OpenCLI backend, docs, and tests are changed.

- [ ] **Step 8: Commit final validation notes if any files changed**

If Step 7 shows no uncommitted files, do not create an empty commit. If final fixes were made, run:

```bash
git add scripts/fetch-twitter.py scripts/run-pipeline.py scripts/test-pipeline.sh tests/test_fetch_twitter_opencli.py README.md README_CN.md SKILL.md references/digest-prompt.md tests/test_config.py
git commit -m "chore: finalize OpenCLI twitter backend"
```

Expected: repository has no uncommitted changes after the final commit.

## Self-Review

- Spec coverage:
  - OpenCLI first in `auto`: Task 7.
  - Explicit `opencli` without API fallback: Task 7 tests and implementation.
  - Existing JSON shape preserved: Tasks 1, 2, and 8.
  - API fallback retained: Task 7.
  - OpenClaw `jackwener/opencli` guidance: Task 9.
  - Topic search reserved but not enabled: Task 2 helper boundary and no task connects `topics.json` `twitter_queries`.
  - RSS/Web/GitHub/Reddit unchanged: File structure limits and Task 10 diff inspection.
- Placeholder scan:
  - No incomplete marker, incomplete step, or missing command is intentionally present.
- Type consistency:
  - `OpenCliBackendError.code`, `OpenCliBackendError.message`, `normalize_opencli_tweet`, `extract_opencli_tweet_records`, `resolve_opencli_bin`, `opencli_has_twitter_tweets`, `get_backend_order`, and `fetch_with_backend_chain` names match across tests and implementation steps.
