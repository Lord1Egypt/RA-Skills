#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import time
import urllib.parse
import urllib.request
import base64
import re
from pathlib import Path
from typing import Any


MIDJOURNEY_TAB_URL = "https://alpha.midjourney.com/imagine"
SCRIPT_DIR = Path(__file__).resolve().parent
CDP_PORT = int(os.getenv("MJ_CDP_PORT", "9222"))
CDP_PROFILE_DIR = os.getenv("MJ_CDP_PROFILE_DIR", str(SCRIPT_DIR.parent / ".chrome-cdp-profile"))
CHROME_APP = os.getenv("MJ_CHROME_APP", "").strip()
CHROME_PROXY = os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY") or ""
JOB_TILE_RE = re.compile(r"/(?P<tile>\d+_\d+)(?:_[^/?]+)?\.(?:png|jpe?g|webp)(?:\?|$)", re.IGNORECASE)
BROWSER_BACKEND = os.getenv("MJ_BROWSER_BACKEND", "auto").strip().lower()


def _json_version_url() -> str:
    return f"http://127.0.0.1:{CDP_PORT}/json/version"


def _check_cdp_ready() -> bool:
    try:
        with urllib.request.urlopen(_json_version_url(), timeout=1) as response:
            return response.status == 200
    except Exception:
        return False


def _chrome_launch_args(url: str) -> list[str]:
    args = [
        f"--remote-debugging-port={CDP_PORT}",
        f"--user-data-dir={CDP_PROFILE_DIR}",
        "--new-window",
    ]
    if CHROME_PROXY:
        args.append(f"--proxy-server={CHROME_PROXY}")
    args.append(url)
    return args


def _dedupe_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def _chrome_binary_candidates() -> list[str]:
    system = platform.system()
    configured = CHROME_APP
    if system == "Darwin":
        return _dedupe_strings(
            [
                configured,
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Google Chrome.app",
            ]
        )
    if system == "Windows":
        return _dedupe_strings(
            [
                configured,
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                "chrome.exe",
            ]
        )
    return _dedupe_strings(
        [
            configured,
            shutil.which("google-chrome") or "",
            shutil.which("chromium") or "",
            shutil.which("chromium-browser") or "",
            shutil.which("chrome") or "",
        ]
    )


def _launch_chrome(command: list[str], *, use_open: bool) -> tuple[bool, str]:
    try:
        if use_open:
            completed = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            if completed.returncode != 0:
                return False, completed.stderr.strip() or "open returned non-zero exit status"
            return True, ""

        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
        return True, ""
    except FileNotFoundError as exc:
        return False, str(exc)
    except Exception as exc:
        return False, str(exc)


def _launch_debug_chrome(url: str) -> None:
    system = platform.system()
    launch_args = _chrome_launch_args(url)
    errors: list[str] = []
    for candidate in _chrome_binary_candidates():
        use_open = system == "Darwin" and candidate.endswith(".app")
        if use_open:
            command = ["open", "-na", candidate, "--args", *launch_args]
        else:
            command = [candidate, *launch_args]
        ok, error = _launch_chrome(command, use_open=use_open)
        if ok:
            return
        errors.append(f"{candidate}: {error}")

    raise RuntimeError(
        "Failed to launch Chrome debug session. Set MJ_CHROME_APP to your Chrome executable or app path. "
        + " | ".join(errors)
    )


def ensure_debug_chrome(url: str = MIDJOURNEY_TAB_URL) -> None:
    if _check_cdp_ready():
        return

    Path(CDP_PROFILE_DIR).mkdir(parents=True, exist_ok=True)
    _launch_debug_chrome(url)

    deadline = time.time() + 15
    while time.time() < deadline:
        if _check_cdp_ready():
            return
        time.sleep(0.5)
    raise RuntimeError("Chrome DevTools endpoint did not become ready")


def _run_cdp_fetch(
    url: str,
    *,
    page_url: str,
    method: str,
    headers: dict[str, str] | None,
    payload: dict[str, Any] | None,
    timeout_seconds: float,
) -> Any:
    ensure_debug_chrome()
    command = [
        "node",
        str(SCRIPT_DIR / "mj_cdp_fetch.mjs"),
        "--debug-port",
        str(CDP_PORT),
        "--page-url",
        page_url,
        "--request-url",
        url,
        "--method",
        method,
        "--headers-json",
        json.dumps(headers or {}),
        "--timeout-seconds",
        str(timeout_seconds),
    ]
    cookie = os.getenv("MJ_COOKIE", "")
    if cookie:
        command.extend(["--cookie-header", cookie])
    if payload is not None:
        command.extend(["--payload-json", json.dumps(payload)])

    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "CDP fetch failed")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"CDP fetch returned invalid JSON: {completed.stdout[:500]}") from exc


def _playwright_available() -> bool:
    package_json = SCRIPT_DIR.parent / "package.json"
    node_modules = SCRIPT_DIR.parent / "node_modules" / "playwright-core"
    return package_json.exists() and node_modules.exists()


def _should_use_playwright() -> bool:
    if BROWSER_BACKEND == "playwright":
        return True
    if BROWSER_BACKEND == "cdp":
        return False
    return _playwright_available()


def _run_playwright_bridge(
    mode: str,
    *,
    page_url: str,
    timeout_seconds: float,
    request_url: str | None = None,
    method: str | None = None,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    expression: str | None = None,
    force_navigate: bool = False,
) -> Any:
    ensure_debug_chrome(page_url)
    command = [
        "node",
        str(SCRIPT_DIR / "mj_playwright_bridge.mjs"),
        "--mode",
        mode,
        "--debug-port",
        str(CDP_PORT),
        "--page-url",
        page_url,
        "--timeout-seconds",
        str(timeout_seconds),
        "--force-navigate",
        "true" if force_navigate else "false",
    ]
    if request_url:
        command.extend(["--request-url", request_url])
    if method:
        command.extend(["--method", method])
    if headers is not None:
        command.extend(["--headers-json", json.dumps(headers)])
    if payload is not None:
        command.extend(["--payload-json", json.dumps(payload)])
    if expression is not None:
        command.extend(["--expression", expression])

    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or f"Playwright {mode} failed")
    if mode == "fetch":
        try:
            return json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Playwright fetch returned invalid JSON: {completed.stdout[:500]}") from exc
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Playwright eval returned invalid JSON: {completed.stdout[:500]}") from exc


def browser_eval_json(
    expression: str,
    *,
    page_url: str = MIDJOURNEY_TAB_URL,
    timeout_seconds: float = 30.0,
    force_navigate: bool = False,
) -> Any:
    if _should_use_playwright():
        try:
            return _run_playwright_bridge(
                "eval",
                page_url=page_url,
                timeout_seconds=timeout_seconds,
                expression=expression,
                force_navigate=force_navigate,
            )
        except Exception:
            if BROWSER_BACKEND == "playwright":
                raise

    ensure_debug_chrome(page_url)
    command = [
        "node",
        str(SCRIPT_DIR / "mj_cdp_eval.mjs"),
        "--debug-port",
        str(CDP_PORT),
        "--page-url",
        page_url,
        "--expression",
        expression,
        "--timeout-seconds",
        str(timeout_seconds),
        "--force-navigate",
        "true" if force_navigate else "false",
    ]
    cookie = os.getenv("MJ_COOKIE", "")
    if cookie:
        command.extend(["--cookie-header", cookie])
    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "CDP eval failed")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"CDP eval returned invalid JSON: {completed.stdout[:500]}") from exc


def _run_osascript(script: str) -> str:
    completed = subprocess.run(
        ["osascript", "-e", script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "osascript failed")
    return completed.stdout.strip()


def ensure_midjourney_tab(url: str = MIDJOURNEY_TAB_URL) -> None:
    script = f'''
tell application "Google Chrome"
    activate
    set foundTab to false
    repeat with wi from 1 to count of windows
        set w to window wi
        repeat with ti from 1 to count of tabs of w
            set t to tab ti of w
            if URL of t contains "alpha.midjourney.com" then
                set active tab index of w to ti
                set index of w to 1
                set foundTab to true
                exit repeat
            end if
        end repeat
        if foundTab then exit repeat
    end repeat
    if not foundTab then
        if (count of windows) = 0 then
            make new window
        end if
        tell window 1
            set newTab to make new tab with properties {{URL:"{url}"}}
            set active tab index to (index of newTab)
        end tell
    end if
end tell
'''
    _run_osascript(script)


def execute_js(js_code: str) -> str:
    normalized = " ".join(line.strip() for line in js_code.splitlines() if line.strip())
    escaped = normalized.replace("\\", "\\\\").replace('"', '\\"')
    script = f'''
tell application "Google Chrome"
    tell active tab of front window to execute javascript "{escaped}"
end tell
'''
    return _run_osascript(script)


def _run_applescript_fetch(
    url: str,
    *,
    page_url: str,
    method: str,
    headers: dict[str, str] | None,
    payload: dict[str, Any] | None,
    timeout_seconds: float,
) -> Any:
    ensure_midjourney_tab(page_url)
    token = f"codex_{int(time.time() * 1000)}"
    request_init = {
        "method": method,
        "headers": headers or {},
        "credentials": "include",
    }
    if payload is not None:
        request_init["body"] = json.dumps(payload)

    js = f"""
(() => {{
  const token = {json.dumps(token)};
  window.__codexFetchState = window.__codexFetchState || {{}};
  window.__codexFetchState[token] = {{ status: "pending" }};
  fetch({json.dumps(url)}, {json.dumps(request_init)})
    .then(async (resp) => {{
      const text = await resp.text();
      window.__codexFetchState[token] = {{ status: "done", ok: resp.ok, statusCode: resp.status, text }};
    }})
    .catch((err) => {{
      window.__codexFetchState[token] = {{ status: "error", error: String(err) }};
    }});
  return token;
}})();
"""
    execute_js(js)

    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        state_raw = execute_js(
            f'JSON.stringify((window.__codexFetchState && window.__codexFetchState[{json.dumps(token)}]) || null)'
        )
        if not state_raw or state_raw == "null":
            time.sleep(0.5)
            continue
        state = json.loads(state_raw)
        if state.get("status") == "pending":
            time.sleep(0.5)
            continue
        if state.get("status") == "error":
            raise RuntimeError(state.get("error", "browser fetch failed"))
        text = state.get("text", "")
        if not state.get("ok", False):
            raise RuntimeError(f"browser fetch HTTP {state.get('statusCode')}: {text[:500]}")
        return json.loads(text)

    raise RuntimeError(f"browser fetch timed out after {timeout_seconds} seconds")


def browser_fetch_json(
    url: str,
    *,
    page_url: str = MIDJOURNEY_TAB_URL,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    timeout_seconds: float = 60.0,
) -> Any:
    if _should_use_playwright():
        try:
            return _run_playwright_bridge(
                "fetch",
                page_url=page_url,
                timeout_seconds=timeout_seconds,
                request_url=url,
                method=method,
                headers=headers or {},
                payload=payload,
            )
        except Exception as playwright_error:
            if BROWSER_BACKEND == "playwright":
                raise RuntimeError(f"browser transport failed via Playwright ({playwright_error})") from playwright_error
    try:
        return _run_cdp_fetch(
            url,
            page_url=page_url,
            method=method,
            headers=headers,
            payload=payload,
            timeout_seconds=timeout_seconds,
        )
    except Exception as cdp_error:
        if platform.system() != "Darwin":
            raise RuntimeError(f"browser transport failed via CDP ({cdp_error})") from cdp_error
        try:
            return _run_applescript_fetch(
                url,
                page_url=page_url,
                method=method,
                headers=headers,
                payload=payload,
                timeout_seconds=timeout_seconds,
            )
        except Exception as applescript_error:
            raise RuntimeError(
                f"browser transport failed via CDP ({cdp_error}) and AppleScript ({applescript_error})"
            ) from applescript_error


def browser_fetch_imagine_feed(
    *,
    user_id: str,
    csrf_protection: str,
    page_size: int = 1000,
    cursor: str | None = None,
    page_url: str = MIDJOURNEY_TAB_URL,
    timeout_seconds: float = 60.0,
) -> dict[str, Any]:
    params = {
        "user_id": user_id,
        "page_size": str(page_size),
    }
    if cursor:
        params["cursor"] = cursor
    url = f"https://alpha.midjourney.com/api/imagine?{urllib.parse.urlencode(params)}"
    response = browser_fetch_json(
        url,
        page_url=page_url,
        headers={
            "accept": "*/*",
            "content-type": "application/json",
            "x-csrf-protection": csrf_protection,
        },
        timeout_seconds=timeout_seconds,
    )
    if not isinstance(response, dict):
        raise RuntimeError(f"Unexpected imagine feed response type: {type(response).__name__}")
    return response


def wait_for_imagine_feed_jobs(
    job_ids: list[str],
    *,
    user_id: str,
    csrf_protection: str,
    attempts: int = 20,
    interval_seconds: float = 3.0,
    page_size: int = 1000,
    page_url: str = MIDJOURNEY_TAB_URL,
    timeout_seconds: float = 60.0,
) -> dict[str, Any]:
    wanted_job_ids = [job_id.strip() for job_id in job_ids if job_id and job_id.strip()]
    history: list[dict[str, Any]] = []
    last_response: dict[str, Any] | None = None
    found_rows: dict[str, dict[str, Any]] = {}

    for attempt in range(1, max(1, attempts) + 1):
        response = browser_fetch_imagine_feed(
            user_id=user_id,
            csrf_protection=csrf_protection,
            page_size=page_size,
            page_url=page_url,
            timeout_seconds=timeout_seconds,
        )
        last_response = response
        rows = response.get("data", []) if isinstance(response, dict) else []
        if isinstance(rows, list):
            for row in rows:
                if not isinstance(row, dict):
                    continue
                job_id = str(row.get("id", "")).strip()
                if job_id in wanted_job_ids:
                    found_rows[job_id] = row
        history.append(
            {
                "attempt": attempt,
                "found_job_ids": sorted(found_rows.keys()),
                "row_count": len(rows) if isinstance(rows, list) else None,
            }
        )
        if all(job_id in found_rows for job_id in wanted_job_ids):
            return {
                "done": True,
                "attempts": attempt,
                "history": history,
                "jobs": found_rows,
                "response": response,
            }
        if attempt < attempts:
            time.sleep(interval_seconds)

    return {
        "done": False,
        "attempts": max(1, attempts),
        "history": history,
        "jobs": found_rows,
        "response": last_response,
    }


def watch_job_results(
    job_ids: list[str],
    *,
    page_url: str = MIDJOURNEY_TAB_URL,
    min_count: int = 4,
    timeout_seconds: float = 90.0,
) -> dict[str, Any]:
    wanted_job_ids = [job_id.strip() for job_id in job_ids if job_id and job_id.strip()]
    if not wanted_job_ids:
        return {
            "done": True,
            "elapsed_seconds": 0.0,
            "min_count": min_count,
            "jobs": {},
        }

    ensure_debug_chrome(page_url)
    command = [
        "node",
        str(SCRIPT_DIR / "mj_cdp_watch_results.mjs"),
        "--debug-port",
        str(CDP_PORT),
        "--page-url",
        page_url,
        "--job-ids-json",
        json.dumps(wanted_job_ids),
        "--timeout-seconds",
        str(timeout_seconds),
        "--min-count",
        str(max(1, min_count)),
    ]
    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "CDP watch failed")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"CDP watch returned invalid JSON: {completed.stdout[:500]}") from exc


def build_prompt_card_probe(prompt_text: str) -> str:
    prompt_json = json.dumps(prompt_text.strip().lower())
    return f"""
(() => {{
  const normalize = (value) => (value || '').replace(/\\s+/g, ' ').trim().toLowerCase();
  const extractUrls = (root) => {{
    const urls = [];
    const seen = new Set();
    const urlPattern = /https?:\\/\\/[^"' )]+cdn\\.midjourney\\.com[^"' )]+/ig;
    const pushUrl = (raw) => {{
      if (!raw) return;
      const cleaned = raw.replace(/^url\\(["']?/, '').replace(/["']?\\)$/, '');
      if (!cleaned.includes('cdn.midjourney.com') || seen.has(cleaned)) return;
      seen.add(cleaned);
      urls.push(cleaned);
    }};
    const nodes = [root, ...Array.from(root.querySelectorAll('*'))];
    for (const node of nodes) {{
      const styleAttr = (node.getAttribute && node.getAttribute('style')) || '';
      if (styleAttr.includes('cdn.midjourney.com')) {{
        const matches = styleAttr.match(urlPattern) || [];
        for (const match of matches) pushUrl(match);
      }}
      const computed = window.getComputedStyle ? getComputedStyle(node) : null;
      const bg = computed ? (computed.backgroundImage || '') : '';
      if (bg.includes('cdn.midjourney.com')) {{
        const matches = bg.match(urlPattern) || [];
        for (const match of matches) pushUrl(match);
      }}
      if (node.tagName === 'IMG') {{
        pushUrl(node.currentSrc || node.src || '');
      }}
    }}
    return urls;
  }};
  const promptNeedle = {prompt_json};
  const promptBase = normalize(promptNeedle.replace(/--.*$/, ''));
  const allNodes = Array.from(document.querySelectorAll('div,article,section,li,a,span,p,h1,h2,h3,h4'));
  const candidates = [];
  for (const node of allNodes) {{
    const text = normalize(node.innerText || '');
    if (!text) continue;
    if (!(text.includes(promptNeedle) || (promptBase && text.includes(promptBase)))) continue;
    let current = node;
    for (let depth = 0; depth < 6 && current; depth += 1) {{
      const imageUrls = extractUrls(current);
      candidates.push({{
        text: (current.innerText || '').trim().slice(0, 500),
        imageUrls,
        imageCount: imageUrls.length,
        htmlLength: (current.innerHTML || '').length,
        textLength: text.length,
        depth,
      }});
      current = current.parentElement;
    }}
  }}
  candidates.sort((a, b) => b.imageCount - a.imageCount || a.depth - b.depth || a.textLength - b.textLength || b.htmlLength - a.htmlLength);
  return {{
    promptNeedle,
    promptBase,
    candidateCount: candidates.length,
    candidates: candidates.slice(0, 5),
    best: candidates[0] || null,
  }};
}})()
"""


def build_job_asset_probe(job_id: str) -> str:
    job_id_json = json.dumps(job_id.strip())
    return f"""
(() => {{
  const jobId = {job_id_json};
  const urls = performance.getEntriesByType('resource')
    .map((entry) => entry.name)
    .filter((name) => name.includes(jobId) && name.includes('cdn.midjourney.com'))
    .filter((name) => /\\.(png|jpe?g|webp)(\\?|$)/i.test(name));
  return {{
    jobId,
    count: Array.from(new Set(urls)).length,
    urls: Array.from(new Set(urls)),
    title: document.title,
    bodySample: (document.body && document.body.innerText ? document.body.innerText.slice(0, 400) : ''),
  }};
}})()
"""


def build_multi_job_asset_probe(job_ids: list[str]) -> str:
    jobs_json = json.dumps([job_id.strip() for job_id in job_ids if job_id.strip()])
    return f"""
(() => {{
  const jobIds = {jobs_json};
  const resourceUrls = performance.getEntriesByType('resource')
    .map((entry) => entry.name)
    .filter((name) => name.includes('cdn.midjourney.com'))
    .filter((name) => /\\.(png|jpe?g|webp)(\\?|$)/i.test(name));
  const jobs = {{}};
  for (const jobId of jobIds) {{
    const urls = resourceUrls.filter((name) => name.includes(jobId));
    jobs[jobId] = {{
      jobId,
      count: Array.from(new Set(urls)).length,
      urls: Array.from(new Set(urls)),
    }};
  }}
  return {{
    jobIds,
    jobs,
    title: document.title,
    bodySample: (document.body && document.body.innerText ? document.body.innerText.slice(0, 400) : ''),
  }};
}})()
"""


def build_job_page_probe(job_id: str) -> str:
    job_id_json = json.dumps(job_id.strip())
    return f"""
new Promise((resolve) => {{
  const jobId = {job_id_json};
  const start = Date.now();
  const collect = () => {{
    const urls = [];
    const seen = new Set();
    const pushUrl = (raw) => {{
      const cleaned = String(raw || '').replace(/^url\\(["']?/, '').replace(/["']?\\)$/, '');
      if (!cleaned.includes(jobId) || seen.has(cleaned)) return;
      seen.add(cleaned);
      urls.push(cleaned);
    }};
    for (const el of Array.from(document.querySelectorAll('*'))) {{
      const styleAttr = (el.getAttribute && el.getAttribute('style')) || '';
      if (styleAttr.includes(jobId)) {{
        for (const match of styleAttr.match(/https?:\\/\\/[^"' )]+/ig) || []) pushUrl(match);
      }}
      const computed = window.getComputedStyle ? getComputedStyle(el) : null;
      const bg = computed ? (computed.backgroundImage || '') : '';
      if (bg.includes(jobId)) {{
        for (const match of bg.match(/https?:\\/\\/[^"' )]+/ig) || []) pushUrl(match);
      }}
      if (el.tagName === 'IMG') {{
        pushUrl(el.currentSrc || el.src || '');
      }}
    }}
    const body = (document.body && document.body.innerText) || '';
    if (urls.length >= 4 || Date.now() - start > 12000) {{
      resolve({{
        jobId,
        count: urls.length,
        urls,
        href: location.href,
        title: document.title,
        bodySample: body.slice(0, 800),
      }});
      return;
    }}
    setTimeout(collect, 500);
  }};
  collect();
}})()
"""


def build_job_cdn_probe(job_id: str) -> str:
    return f"""
(() => {{
  const jobId = {json.dumps(job_id)};
  const urls = ["0_0", "0_1", "0_2", "0_3"].map((tile) =>
    `https://cdn.midjourney.com/${{jobId}}/${{tile}}_640_N.webp?method=shortest`
  );
  const probe = async (url) => {{
    try {{
      const head = await fetch(url, {{ method: "HEAD", credentials: "omit" }});
      return {{
        ok: head.ok,
        url,
        status: head.status,
        contentType: head.headers.get("content-type"),
      }};
    }} catch (error) {{
      try {{
        const get = await fetch(url, {{ credentials: "omit" }});
        return {{
          ok: get.ok,
          url,
          status: get.status,
          contentType: get.headers.get("content-type"),
        }};
      }} catch (fallbackError) {{
        return {{ ok: false, url, error: String(fallbackError || error) }};
      }}
    }}
  }};
  return Promise.all(urls.map(probe)).then((results) => {{
    const ready = results.filter((item) => item.ok).map((item) => item.url);
    return {{
      jobId,
      count: ready.length,
      urls: ready,
      attempted: urls,
      results,
      href: location.href,
      title: document.title,
    }};
  }});
}})()
"""


def select_preferred_job_urls(urls: list[str]) -> list[str]:
    grouped: dict[str, str] = {}
    extras: list[str] = []

    def score(url: str) -> tuple[int, int]:
        lowered = url.lower()
        return (
            2 if lowered.endswith(".webp") or ".webp?" in lowered else 1 if lowered.endswith(".png") or ".png?" in lowered else 0,
            1 if "_n." in lowered or "_n.webp" in lowered or "_n?" in lowered else 0,
        )

    for url in urls:
        match = JOB_TILE_RE.search(url)
        if not match:
            if url not in extras:
                extras.append(url)
            continue
        tile = match.group("tile")
        current = grouped.get(tile)
        if current is None or score(url) > score(current):
            grouped[tile] = url

    ordered_tiles = sorted(grouped.items(), key=lambda item: tuple(int(part) for part in item[0].split("_")))
    ordered_urls = [url for _, url in ordered_tiles]
    for extra in extras:
        if extra not in ordered_urls:
            ordered_urls.append(extra)
    return ordered_urls


def wait_for_job_assets(
    job_id: str,
    *,
    page_url: str = MIDJOURNEY_TAB_URL,
    min_count: int = 4,
    attempts: int = 30,
    interval_seconds: float = 2.0,
    timeout_seconds: float = 30.0,
) -> dict[str, Any]:
    history: list[dict[str, Any]] = []
    result: dict[str, Any] | None = None
    for attempt in range(1, max(1, attempts) + 1):
        result = browser_eval_json(
            build_job_asset_probe(job_id),
            page_url=page_url,
            timeout_seconds=timeout_seconds,
        )
        count = int(result.get("count", 0)) if isinstance(result, dict) else 0
        history.append({"attempt": attempt, "count": count})
        if count >= max(1, min_count):
            result_urls = select_preferred_job_urls(list(result.get("urls") or []))
            return {
                "job_id": job_id,
                "done": True,
                "attempts": attempt,
                "history": history,
                "result_urls": result_urls,
                "page_probe": result,
                "min_count": min_count,
            }
        if attempt < attempts:
            time.sleep(interval_seconds)

    return {
        "job_id": job_id,
        "done": False,
        "attempts": attempts,
        "history": history,
        "result_urls": select_preferred_job_urls(list(result.get("urls") or [])) if isinstance(result, dict) else [],
        "page_probe": result,
        "min_count": min_count,
    }


def wait_for_job_page_assets(
    job_id: str,
    *,
    attempts: int = 12,
    interval_seconds: float = 3.0,
    timeout_seconds: float = 30.0,
) -> dict[str, Any]:
    page_url = f"https://alpha.midjourney.com/jobs/{job_id}?index=0"
    history: list[dict[str, Any]] = []
    result: dict[str, Any] | None = None
    for attempt in range(1, max(1, attempts) + 1):
        result = browser_eval_json(
            build_job_page_probe(job_id),
            page_url=page_url,
            timeout_seconds=timeout_seconds,
        )
        count = int(result.get("count", 0)) if isinstance(result, dict) else 0
        history.append({"attempt": attempt, "count": count})
        if count >= 4:
            result_urls = select_preferred_job_urls(list(result.get("urls") or []))
            return {
                "job_id": job_id,
                "done": True,
                "attempts": attempt,
                "history": history,
                "result_urls": result_urls,
                "page_probe": result,
                "source": "job_page",
                "min_count": 4,
            }
        if attempt < attempts:
            time.sleep(interval_seconds)

    return {
        "job_id": job_id,
        "done": False,
        "attempts": attempts,
        "history": history,
        "result_urls": select_preferred_job_urls(list(result.get("urls") or [])) if isinstance(result, dict) else [],
        "page_probe": result,
        "source": "job_page",
        "min_count": 4,
    }


def wait_for_job_cdn_assets(
    job_id: str,
    *,
    page_url: str = MIDJOURNEY_TAB_URL,
    attempts: int = 12,
    interval_seconds: float = 3.0,
    timeout_seconds: float = 30.0,
) -> dict[str, Any]:
    history: list[dict[str, Any]] = []
    result: dict[str, Any] | None = None
    for attempt in range(1, max(1, attempts) + 1):
        result = browser_eval_json(
            build_job_cdn_probe(job_id),
            page_url=page_url,
            timeout_seconds=timeout_seconds,
        )
        count = int(result.get("count", 0)) if isinstance(result, dict) else 0
        history.append({"attempt": attempt, "count": count})
        if count >= 4:
            result_urls = select_preferred_job_urls(list(result.get("urls") or []))
            return {
                "job_id": job_id,
                "done": True,
                "attempts": attempt,
                "history": history,
                "result_urls": result_urls,
                "page_probe": result,
                "source": "job_cdn",
                "min_count": 4,
            }
        if attempt < attempts:
            time.sleep(interval_seconds)

    return {
        "job_id": job_id,
        "done": False,
        "attempts": attempts,
        "history": history,
        "result_urls": select_preferred_job_urls(list(result.get("urls") or [])) if isinstance(result, dict) else [],
        "page_probe": result,
        "source": "job_cdn",
        "min_count": 4,
    }


def wait_for_job_assets_batch(
    job_ids: list[str],
    *,
    page_url: str = MIDJOURNEY_TAB_URL,
    min_count: int = 4,
    attempts: int = 30,
    interval_seconds: float = 2.0,
    timeout_seconds: float = 30.0,
) -> dict[str, Any]:
    wanted_job_ids = [job_id.strip() for job_id in job_ids if job_id and job_id.strip()]
    if not wanted_job_ids:
        return {
            "done": True,
            "attempts": 0,
            "history": [],
            "jobs": {},
            "min_count": min_count,
        }

    history: list[dict[str, Any]] = []
    result: dict[str, Any] | None = None
    for attempt in range(1, max(1, attempts) + 1):
        result = browser_eval_json(
            build_multi_job_asset_probe(wanted_job_ids),
            page_url=page_url,
            timeout_seconds=timeout_seconds,
        )
        jobs = result.get("jobs", {}) if isinstance(result, dict) else {}
        counts = {
            job_id: int((jobs.get(job_id) or {}).get("count", 0))
            for job_id in wanted_job_ids
        }
        history.append({"attempt": attempt, "counts": counts})
        if all(count >= max(1, min_count) for count in counts.values()):
            return {
                "done": True,
                "attempts": attempt,
                "history": history,
                "jobs": {
                    job_id: {
                        "job_id": job_id,
                        "done": counts.get(job_id, 0) >= max(1, min_count),
                        "attempts": attempt,
                        "result_urls": select_preferred_job_urls(list((jobs.get(job_id) or {}).get("urls") or [])),
                        "page_probe": jobs.get(job_id) or {},
                        "min_count": min_count,
                    }
                    for job_id in wanted_job_ids
                },
                "page_probe": result,
                "min_count": min_count,
            }
        if attempt < attempts:
            time.sleep(interval_seconds)

    jobs = result.get("jobs", {}) if isinstance(result, dict) else {}
    return {
        "done": False,
        "attempts": attempts,
        "history": history,
        "jobs": {
            job_id: {
                "job_id": job_id,
                "done": int((jobs.get(job_id) or {}).get("count", 0)) >= max(1, min_count),
                "attempts": attempts,
                "result_urls": select_preferred_job_urls(list((jobs.get(job_id) or {}).get("urls") or [])),
                "page_probe": jobs.get(job_id) or {},
                "min_count": min_count,
            }
            for job_id in wanted_job_ids
        },
        "page_probe": result,
        "min_count": min_count,
    }


def wait_for_prompt_card_assets(
    prompt_text: str,
    *,
    page_url: str = MIDJOURNEY_TAB_URL,
    min_count: int = 4,
    attempts: int = 30,
    interval_seconds: float = 2.0,
    timeout_seconds: float = 30.0,
) -> dict[str, Any]:
    history: list[dict[str, Any]] = []
    result: dict[str, Any] | None = None
    for attempt in range(1, max(1, attempts) + 1):
        result = browser_eval_json(
            build_prompt_card_probe(prompt_text),
            page_url=page_url,
            timeout_seconds=timeout_seconds,
        )
        best = result.get("best") or {} if isinstance(result, dict) else {}
        image_urls = list(best.get("imageUrls") or [])
        history.append(
            {
                "attempt": attempt,
                "candidate_count": int((result or {}).get("candidateCount", 0)) if isinstance(result, dict) else 0,
                "image_count": len(image_urls),
            }
        )
        if len(image_urls) >= max(1, min_count):
            return {
                "prompt_text": prompt_text,
                "done": True,
                "attempts": attempt,
                "history": history,
                "result_urls": image_urls,
                "page_probe": result,
                "min_count": min_count,
                "source": "prompt_card",
            }
        if attempt < attempts:
            time.sleep(interval_seconds)

    best = result.get("best") or {} if isinstance(result, dict) else {}
    return {
        "prompt_text": prompt_text,
        "done": False,
        "attempts": attempts,
        "history": history,
        "result_urls": list(best.get("imageUrls") or []),
        "page_probe": result,
        "min_count": min_count,
        "source": "prompt_card",
    }


def browser_convert_image_url(
    image_url: str,
    *,
    output_format: str = "png",
    page_url: str = MIDJOURNEY_TAB_URL,
    timeout_seconds: float = 60.0,
) -> dict[str, Any]:
    format_name = output_format.lower()
    if format_name != "png":
        raise RuntimeError(f"Unsupported browser conversion format: {output_format}")

    expr = f"""
(async () => {{
  try {{
    const resp = await fetch({json.dumps(image_url)});
    const blob = await resp.blob();
    const bmp = await createImageBitmap(blob);
    const canvas = document.createElement('canvas');
    canvas.width = bmp.width;
    canvas.height = bmp.height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(bmp, 0, 0);
    const dataUrl = canvas.toDataURL('image/png');
    return {{
      ok: true,
      width: bmp.width,
      height: bmp.height,
      dataBase64: dataUrl.split(',')[1],
      mimeType: 'image/png'
    }};
  }} catch (error) {{
    return {{
      ok: false,
      error: String(error)
    }};
  }}
}})()
"""
    result = browser_eval_json(expr, page_url=page_url, timeout_seconds=timeout_seconds)
    if not isinstance(result, dict) or not result.get("ok"):
        raise RuntimeError(f"Browser image conversion failed: {result}")
    data_base64 = result.get("dataBase64")
    if not isinstance(data_base64, str) or not data_base64:
        raise RuntimeError("Browser image conversion returned empty image data")
    return {
        "bytes": base64.b64decode(data_base64),
        "mime_type": result.get("mimeType", "image/png"),
        "width": result.get("width"),
        "height": result.get("height"),
    }


def browser_fetch_binary_url(
    url: str,
    *,
    page_url: str = MIDJOURNEY_TAB_URL,
    timeout_seconds: float = 60.0,
) -> dict[str, Any]:
    expr = f"""
(async () => {{
  try {{
    const resp = await fetch({json.dumps(url)});
    const buffer = await resp.arrayBuffer();
    const bytes = new Uint8Array(buffer);
    let binary = '';
    const chunkSize = 0x8000;
    for (let i = 0; i < bytes.length; i += chunkSize) {{
      binary += String.fromCharCode(...bytes.subarray(i, i + chunkSize));
    }}
    return {{
      ok: resp.ok,
      status: resp.status,
      mimeType: resp.headers.get('content-type') || '',
      dataBase64: btoa(binary),
      sizeBytes: bytes.length,
    }};
  }} catch (error) {{
    return {{
      ok: false,
      status: 0,
      error: String(error)
    }};
  }}
}})()
"""
    result = browser_eval_json(expr, page_url=page_url, timeout_seconds=timeout_seconds)
    if not isinstance(result, dict) or not result.get("ok"):
        raise RuntimeError(f"Browser binary fetch failed: {result}")
    data_base64 = result.get("dataBase64")
    if not isinstance(data_base64, str) or not data_base64:
        raise RuntimeError("Browser binary fetch returned empty data")
    return {
        "bytes": base64.b64decode(data_base64),
        "mime_type": result.get("mimeType") or None,
        "status": result.get("status"),
        "size_bytes": result.get("sizeBytes"),
    }


def browser_convert_image_bytes(
    image_bytes: bytes,
    *,
    input_mime_type: str = "image/webp",
    output_format: str = "png",
    page_url: str = MIDJOURNEY_TAB_URL,
    timeout_seconds: float = 60.0,
) -> dict[str, Any]:
    format_name = output_format.lower()
    if format_name != "png":
        raise RuntimeError(f"Unsupported browser conversion format: {output_format}")

    input_base64 = base64.b64encode(image_bytes).decode("ascii")
    expr = f"""
(async () => {{
  try {{
    const binary = atob({json.dumps(input_base64)});
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i += 1) {{
      bytes[i] = binary.charCodeAt(i);
    }}
    const blob = new Blob([bytes], {{ type: {json.dumps(input_mime_type)} }});
    const objectUrl = URL.createObjectURL(blob);
    const img = new Image();
    img.src = objectUrl;
    await img.decode();
    const canvas = document.createElement('canvas');
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const outputDataUrl = canvas.toDataURL('image/png');
    URL.revokeObjectURL(objectUrl);
    return {{
      ok: true,
      width: img.naturalWidth,
      height: img.naturalHeight,
      dataBase64: outputDataUrl.split(',')[1],
      mimeType: 'image/png'
    }};
  }} catch (error) {{
    return {{
      ok: false,
      error: String(error)
    }};
  }}
}})()
"""
    result = browser_eval_json(expr, page_url=page_url, timeout_seconds=timeout_seconds)
    if not isinstance(result, dict) or not result.get("ok"):
        raise RuntimeError(f"Browser image conversion failed: {result}")
    data_base64 = result.get("dataBase64")
    if not isinstance(data_base64, str) or not data_base64:
        raise RuntimeError("Browser image conversion returned empty image data")
    return {
        "bytes": base64.b64decode(data_base64),
        "mime_type": result.get("mimeType", "image/png"),
        "width": result.get("width"),
        "height": result.get("height"),
    }
