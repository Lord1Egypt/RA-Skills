#!/usr/bin/env python3
"""Steel Browser skill wrapper.

CLI-first browser automation for Steel.
- Default runtime: Steel CLI (`steel` or `npx @steel-dev/cli`)
- Optional runtime: Python Playwright + Steel SDK plan runner
- Runtime choice: auto | cli | node | python
"""

from __future__ import print_function

import argparse
import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from urllib.parse import urlparse


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ENV_CANDIDATES = [
    Path.cwd() / ".env",
    SKILL_DIR / ".env",
]
SUPPORTED_PYTHON_ACTIONS = [
    "goto",
    "wait_for_load_state",
    "wait_for_selector",
    "wait_for_text",
    "click",
    "fill",
    "type",
    "press",
    "select",
    "hover",
    "eval",
    "extract_text",
    "extract_html",
    "screenshot",
    "get_title",
    "get_url",
    "scroll",
]


class SkillError(Exception):
    pass


def _parse_env_file(path):
    loaded = {}
    if not path:
        return loaded
    env_path = Path(path).expanduser()
    if not env_path.exists():
        return loaded
    with env_path.open("r") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export "):].strip()
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("\"'")
            loaded[key] = value
    return loaded


def _load_env(env_file=None):
    merged = dict(os.environ)
    chosen = None

    candidates = []
    if env_file:
        candidates.append(Path(env_file).expanduser())
    env_from_var = os.environ.get("STEEL_BROWSER_ENV_FILE")
    if env_from_var:
        candidates.append(Path(env_from_var).expanduser())
    candidates.extend(DEFAULT_ENV_CANDIDATES)

    for candidate in candidates:
        if candidate.exists():
            chosen = candidate
            loaded = _parse_env_file(candidate)
            for key, value in loaded.items():
                merged.setdefault(key, value)
            break

    return merged, chosen


def _command_exists(name):
    return shutil.which(name) is not None


def _resolve_cli_command(runtime):
    forced_bin = os.environ.get("STEEL_BROWSER_CLI_BIN")
    if forced_bin:
        return [forced_bin], "forced-bin"

    if runtime == "node":
        if _command_exists("npx"):
            return ["npx", "--yes", "@steel-dev/cli"], "npx"
        raise SkillError("runtime=node requires `npx` (or set STEEL_BROWSER_CLI_BIN)")

    if runtime in ("auto", "cli"):
        if _command_exists("steel"):
            return ["steel"], "steel"
        if _command_exists("npx"):
            return ["npx", "--yes", "@steel-dev/cli"], "npx"
        raise SkillError("Steel CLI not found. Install `steel` or make `npx` available.")

    raise SkillError("runtime `%s` is not a CLI runtime" % runtime)


def _run_subprocess(command, env):
    completed = subprocess.run(
        command,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if completed.stdout:
        sys.stdout.write(completed.stdout)
    if completed.stderr:
        sys.stderr.write(completed.stderr)
    return completed.returncode


def _append_common_cli_flags(command, session=None, local=False, api_url=None, json_output=False):
    existing = set(command)
    if session and "--session" not in existing:
        command.extend(["--session", session])
    if local and "--local" not in existing and "-l" not in existing:
        command.append("--local")
    if api_url and "--api-url" not in existing:
        command.extend(["--api-url", api_url])
    if json_output and "--json" not in existing:
        command.append("--json")
    return command


def _derive_site_keys(url, explicit_site=None):
    keys = []
    if explicit_site:
        keys.append(explicit_site)
    if url:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        if hostname:
            parts = hostname.split(".")
            keys.append(hostname)
            if len(parts) >= 2:
                keys.append(parts[-2] + "." + parts[-1])
                keys.append(parts[-2])
    unique = []
    for item in keys:
        if item and item not in unique:
            unique.append(item)
    return unique


def _normalize_cookie(cookie, fallback_domain=None):
    normalized = {
        "name": cookie.get("name"),
        "value": cookie.get("value"),
        "path": cookie.get("path", "/"),
        "secure": bool(cookie.get("secure", False)),
        "httpOnly": bool(cookie.get("httpOnly", False)),
    }
    if cookie.get("domain"):
        normalized["domain"] = cookie.get("domain")
    elif fallback_domain:
        normalized["domain"] = fallback_domain

    same_site = cookie.get("sameSite") or cookie.get("same_site")
    if same_site == "no_restriction":
        normalized["sameSite"] = "None"
    elif same_site in ("Strict", "Lax", "None"):
        normalized["sameSite"] = same_site

    if "expires" in cookie and cookie.get("expires") is not None:
        normalized["expires"] = cookie.get("expires")
    return normalized


def _load_cookies(cookies_file, url=None, site=None):
    if not cookies_file:
        return []
    cookie_path = Path(cookies_file).expanduser()
    if not cookie_path.exists():
        raise SkillError("cookies file not found: %s" % cookie_path)

    with cookie_path.open("r") as handle:
        raw = json.load(handle)

    derived_keys = _derive_site_keys(url, site)
    fallback_domain = None
    parsed = urlparse(url or "")
    if parsed.hostname:
        fallback_domain = "." + parsed.hostname.lstrip(".")

    if isinstance(raw, list):
        cookies = []
        for cookie in raw:
            domain = cookie.get("domain", "")
            if not derived_keys or any(key in domain for key in derived_keys):
                cookies.append(_normalize_cookie(cookie, fallback_domain=fallback_domain))
        return cookies

    if isinstance(raw, dict):
        if isinstance(raw.get("cookies"), list):
            return [_normalize_cookie(cookie, fallback_domain=fallback_domain) for cookie in raw["cookies"]]

        for key in derived_keys:
            if key not in raw:
                continue
            cookie_blob = raw[key]
            if isinstance(cookie_blob, list):
                return [_normalize_cookie(cookie, fallback_domain=fallback_domain) for cookie in cookie_blob]
            if isinstance(cookie_blob, str):
                parsed_cookies = []
                for part in cookie_blob.split(";"):
                    if "=" not in part:
                        continue
                    name, value = part.strip().split("=", 1)
                    parsed_cookies.append({
                        "name": name,
                        "value": value,
                        "domain": fallback_domain or ("." + key.lstrip(".")),
                        "path": "/",
                    })
                return parsed_cookies

    return []


def _python_runtime_report(env):
    report = {
        "current_executable": sys.executable,
        "current_modules": {},
        "configured_python_bin": env.get("STEEL_BROWSER_PYTHON_BIN") or os.environ.get("STEEL_BROWSER_PYTHON_BIN"),
        "configured_python_bin_ok": None,
    }

    for module_name in ("playwright", "steel"):
        try:
            __import__(module_name)
            report["current_modules"][module_name] = True
        except Exception:
            report["current_modules"][module_name] = False

    alt = report["configured_python_bin"]
    if alt:
        alt_path = Path(alt).expanduser()
        report["configured_python_bin_ok"] = alt_path.exists()
    return report


def cmd_doctor(args, env, env_path):
    cli_auto = None
    cli_source = None
    cli_error = None
    try:
        cli_auto, cli_source = _resolve_cli_command("auto")
    except Exception as exc:
        cli_error = str(exc)

    report = {
        "skill_dir": str(SKILL_DIR),
        "cwd": os.getcwd(),
        "env_file": str(env_path) if env_path else None,
        "steel_api_key_present": bool(env.get("STEEL_API_KEY")),
        "steel_browser_api_url": env.get("STEEL_BROWSER_API_URL") or env.get("STEEL_LOCAL_API_URL"),
        "cookies_file": env.get("STEEL_BROWSER_COOKIES_FILE"),
        "commands": {
            "steel": shutil.which("steel"),
            "npx": shutil.which("npx"),
            "node": shutil.which("node"),
            "python3": shutil.which("python3"),
        },
        "cli_runtime": {
            "default_command": cli_auto,
            "source": cli_source,
            "error": cli_error,
        },
        "python_runtime": _python_runtime_report(env),
        "supported_python_actions": SUPPORTED_PYTHON_ACTIONS,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


def _cli_mode_flags(args):
    flags = []
    if getattr(args, "local", False):
        flags.append("--local")
    if getattr(args, "api_url", None):
        flags.extend(["--api-url", args.api_url])
    if getattr(args, "json", False):
        flags.append("--json")
    return flags


def cmd_scrape(args, env):
    base, _ = _resolve_cli_command(args.runtime)
    command = list(base) + ["scrape", args.url]
    if args.format:
        command.extend(["--format", args.format])
    if args.delay is not None:
        command.extend(["--delay", str(args.delay)])
    if args.pdf:
        command.append("--pdf")
    if args.screenshot:
        command.append("--screenshot")
    if args.use_proxy:
        command.append("--use-proxy")
    if args.region:
        command.extend(["--region", args.region])
    command.extend(_cli_mode_flags(args))
    return _run_subprocess(command, env)


def cmd_screenshot(args, env):
    base, _ = _resolve_cli_command(args.runtime)
    command = list(base) + ["screenshot", args.url]
    if args.delay is not None:
        command.extend(["--delay", str(args.delay)])
    if args.full_page:
        command.append("--full-page")
    if args.use_proxy:
        command.append("--use-proxy")
    if args.region:
        command.extend(["--region", args.region])
    command.extend(_cli_mode_flags(args))
    return _run_subprocess(command, env)


def cmd_pdf(args, env):
    base, _ = _resolve_cli_command(args.runtime)
    command = list(base) + ["pdf", args.url]
    if args.delay is not None:
        command.extend(["--delay", str(args.delay)])
    if args.use_proxy:
        command.append("--use-proxy")
    if args.region:
        command.extend(["--region", args.region])
    command.extend(_cli_mode_flags(args))
    return _run_subprocess(command, env)


def cmd_start_session(args, env):
    base, _ = _resolve_cli_command(args.runtime)
    command = list(base) + ["browser", "start", "--session", args.session]
    if args.stealth:
        command.append("--stealth")
    if args.proxy:
        command.extend(["--proxy", args.proxy])
    if args.session_timeout is not None:
        command.extend(["--session-timeout", str(args.session_timeout)])
    if args.session_solve_captcha:
        command.append("--session-solve-captcha")
    if args.profile:
        command.extend(["--profile", args.profile])
    if args.update_profile:
        command.append("--update-profile")
    if args.namespace:
        command.extend(["--namespace", args.namespace])
    if args.credentials:
        command.append("--credentials")
    command.extend(_cli_mode_flags(args))
    return _run_subprocess(command, env)


def cmd_stop_session(args, env):
    base, _ = _resolve_cli_command(args.runtime)
    command = list(base) + ["browser", "stop"]
    if args.all:
        command.append("--all")
    elif args.session:
        command.extend(["--session", args.session])
    else:
        raise SkillError("stop-session requires --session or --all")
    command.extend(_cli_mode_flags(args))
    return _run_subprocess(command, env)


def cmd_sessions(args, env):
    base, _ = _resolve_cli_command(args.runtime)
    command = list(base) + ["browser", "sessions"]
    command.extend(_cli_mode_flags(args))
    return _run_subprocess(command, env)


def cmd_live(args, env):
    base, _ = _resolve_cli_command(args.runtime)
    command = list(base) + ["browser", "live", "--session", args.session]
    command.extend(_cli_mode_flags(args))
    return _run_subprocess(command, env)


def cmd_browser(args, env):
    base, _ = _resolve_cli_command(args.runtime)
    browser_args = list(args.browser_args or [])
    if browser_args and browser_args[0] == "--":
        browser_args = browser_args[1:]
    if not browser_args:
        raise SkillError("browser requires passthrough arguments after `--`")
    command = list(base) + ["browser"] + browser_args
    _append_common_cli_flags(
        command,
        session=args.session,
        local=args.local,
        api_url=args.api_url,
        json_output=args.json,
    )
    return _run_subprocess(command, env)


def _maybe_reexec_python(args, env):
    configured = env.get("STEEL_BROWSER_PYTHON_BIN") or os.environ.get("STEEL_BROWSER_PYTHON_BIN")
    if not configured:
        return None
    configured_path = Path(configured).expanduser()
    if not configured_path.exists():
        return None

    try:
        import playwright  # noqa: F401
        import steel  # noqa: F401
        return None
    except Exception:
        pass

    current = Path(sys.executable).resolve()
    target = configured_path.resolve()
    if current == target:
        return None

    command = [str(target)] + sys.argv
    return subprocess.call(command, env=env)


async def _run_python_plan_async(args, env):
    try:
        from steel import AsyncSteel
        from playwright.async_api import async_playwright
    except Exception as exc:
        raise SkillError(
            "Python runtime requires `steel` and `playwright`. "
            "Install them in the active interpreter or set STEEL_BROWSER_PYTHON_BIN. (%s)" % exc
        )

    api_key = env.get("STEEL_API_KEY")
    if not api_key:
        raise SkillError("STEEL_API_KEY is required for the Python runtime")

    plan_path = Path(args.plan_file).expanduser()
    if not plan_path.exists():
        raise SkillError("plan file not found: %s" % plan_path)

    with plan_path.open("r") as handle:
        plan = json.load(handle)

    session_label = args.session or plan.get("session_name") or ("steel-skill-" + uuid.uuid4().hex[:8])
    custom_session_id = plan.get("session_id") or str(uuid.uuid4())
    use_proxy = bool(args.use_proxy or plan.get("use_proxy"))
    solve_captcha = bool(args.solve_captcha or plan.get("solve_captcha"))
    start_url = args.url or plan.get("url")
    cookies_file = args.cookies_file or env.get("STEEL_BROWSER_COOKIES_FILE")
    site = args.site or plan.get("site")

    client = AsyncSteel(steel_api_key=api_key)
    session = None
    playwright = None
    browser = None
    context = None
    page = None
    results = []

    try:
        create_kwargs = {
            "session_id": custom_session_id,
        }
        if use_proxy:
            create_kwargs["use_proxy"] = True
        if solve_captcha:
            create_kwargs["solve_captcha"] = True

        session = await client.sessions.create(**create_kwargs)
        playwright = await async_playwright().start()
        cdp_url = "wss://connect.steel.dev?apiKey=%s&sessionId=%s" % (api_key, session.id)
        browser = await playwright.chromium.connect_over_cdp(cdp_url)
        if browser.contexts:
            context = browser.contexts[0]
        else:
            context = await browser.new_context()

        cookies = _load_cookies(cookies_file, url=start_url, site=site) if cookies_file else []
        if cookies:
            await context.add_cookies(cookies)

        page = await context.new_page()
        if start_url:
            await page.goto(start_url, wait_until="domcontentloaded", timeout=args.timeout)

        steps = plan.get("steps", [])
        for index, step in enumerate(steps):
            action = step.get("action")
            if action not in SUPPORTED_PYTHON_ACTIONS:
                raise SkillError("unsupported Python plan action at step %s: %s" % (index, action))

            if action == "goto":
                result = await page.goto(
                    step["url"],
                    wait_until=step.get("wait_until", "domcontentloaded"),
                    timeout=step.get("timeout", args.timeout),
                )
                results.append({
                    "step": index,
                    "action": action,
                    "status": result.status if result else None,
                    "url": page.url,
                })
            elif action == "wait_for_load_state":
                await page.wait_for_load_state(step.get("state", "networkidle"), timeout=step.get("timeout", args.timeout))
                results.append({"step": index, "action": action, "state": step.get("state", "networkidle")})
            elif action == "wait_for_selector":
                await page.wait_for_selector(
                    step["selector"],
                    state=step.get("state", "visible"),
                    timeout=step.get("timeout", args.timeout),
                )
                results.append({"step": index, "action": action, "selector": step["selector"]})
            elif action == "wait_for_text":
                target_text = step["text"]
                await page.wait_for_function(
                    "(needle) => document.body && document.body.innerText.includes(needle)",
                    target_text,
                    timeout=step.get("timeout", args.timeout),
                )
                results.append({"step": index, "action": action, "text": target_text})
            elif action == "click":
                await page.click(step["selector"], timeout=step.get("timeout", args.timeout))
                results.append({"step": index, "action": action, "selector": step["selector"]})
            elif action == "fill":
                await page.fill(step["selector"], step.get("value", ""), timeout=step.get("timeout", args.timeout))
                results.append({"step": index, "action": action, "selector": step["selector"]})
            elif action == "type":
                await page.type(
                    step["selector"],
                    step.get("value", ""),
                    delay=step.get("delay_ms", 50),
                    timeout=step.get("timeout", args.timeout),
                )
                results.append({"step": index, "action": action, "selector": step["selector"]})
            elif action == "press":
                selector = step.get("selector")
                if selector:
                    await page.focus(selector, timeout=step.get("timeout", args.timeout))
                await page.keyboard.press(step["key"])
                results.append({"step": index, "action": action, "key": step["key"], "selector": selector})
            elif action == "select":
                values = step.get("values")
                if values is None:
                    values = [step.get("value")]
                await page.select_option(step["selector"], values, timeout=step.get("timeout", args.timeout))
                results.append({"step": index, "action": action, "selector": step["selector"], "values": values})
            elif action == "hover":
                await page.hover(step["selector"], timeout=step.get("timeout", args.timeout))
                results.append({"step": index, "action": action, "selector": step["selector"]})
            elif action == "eval":
                value = await page.evaluate(step["script"])
                results.append({"step": index, "action": action, "result": value})
            elif action == "extract_text":
                selector = step.get("selector", "body")
                locator = page.locator(selector).first
                text = await locator.inner_text(timeout=step.get("timeout", args.timeout))
                max_chars = step.get("max_chars", 8000)
                results.append({"step": index, "action": action, "selector": selector, "text": text[:max_chars]})
            elif action == "extract_html":
                selector = step.get("selector", "body")
                locator = page.locator(selector).first
                html = await locator.inner_html(timeout=step.get("timeout", args.timeout))
                max_chars = step.get("max_chars", 8000)
                results.append({"step": index, "action": action, "selector": selector, "html": html[:max_chars]})
            elif action == "screenshot":
                output = step.get("output")
                if not output:
                    raise SkillError("screenshot step requires `output`")
                output_path = str(Path(output).expanduser())
                selector = step.get("selector")
                if selector:
                    await page.locator(selector).first.screenshot(path=output_path)
                else:
                    await page.screenshot(path=output_path, full_page=bool(step.get("full_page", False)))
                results.append({"step": index, "action": action, "output": output_path})
            elif action == "get_title":
                results.append({"step": index, "action": action, "title": await page.title()})
            elif action == "get_url":
                results.append({"step": index, "action": action, "url": page.url})
            elif action == "scroll":
                x = step.get("x", 0)
                y = step.get("y", 800)
                await page.mouse.wheel(x, y)
                results.append({"step": index, "action": action, "x": x, "y": y})

        payload = {
            "runtime": "python",
            "session_name": session_label,
            "session_id": session.id,
            "url": page.url if page else start_url,
            "results": results,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    finally:
        if browser is not None:
            await browser.close()
        if playwright is not None:
            await playwright.stop()
        if session is not None:
            await client.sessions.release(session.id)


def cmd_run_python_plan(args, env):
    reexec_code = _maybe_reexec_python(args, env)
    if reexec_code is not None:
        return reexec_code

    import asyncio

    return asyncio.run(_run_python_plan_async(args, env))


def build_parser():
    parser = argparse.ArgumentParser(description="Steel Browser skill wrapper")
    parser.add_argument("--env-file", help="Optional env file to load before running")

    subparsers = parser.add_subparsers(dest="command")

    doctor = subparsers.add_parser("doctor", help="Report runtime and env availability")
    doctor.set_defaults(handler="doctor")

    def add_cli_runtime(subparser):
        subparser.add_argument("--runtime", choices=["auto", "cli", "node"], default="auto")
        subparser.add_argument("--local", action="store_true", help="Use local Steel runtime")
        subparser.add_argument("--api-url", help="Explicit self-hosted API URL")
        subparser.add_argument("--json", action="store_true", help="Request JSON output when supported")

    scrape = subparsers.add_parser("scrape", help="Run `steel scrape`")
    scrape.add_argument("--url", required=True)
    scrape.add_argument("--format", help="Comma-separated formats: html,readability,cleaned_html,markdown")
    scrape.add_argument("--delay", type=int)
    scrape.add_argument("--pdf", action="store_true")
    scrape.add_argument("--screenshot", action="store_true")
    scrape.add_argument("--use-proxy", action="store_true")
    scrape.add_argument("--region")
    add_cli_runtime(scrape)
    scrape.set_defaults(handler="scrape")

    screenshot = subparsers.add_parser("screenshot", help="Run `steel screenshot`")
    screenshot.add_argument("--url", required=True)
    screenshot.add_argument("--delay", type=int)
    screenshot.add_argument("--full-page", action="store_true")
    screenshot.add_argument("--use-proxy", action="store_true")
    screenshot.add_argument("--region")
    add_cli_runtime(screenshot)
    screenshot.set_defaults(handler="screenshot")

    pdf = subparsers.add_parser("pdf", help="Run `steel pdf`")
    pdf.add_argument("--url", required=True)
    pdf.add_argument("--delay", type=int)
    pdf.add_argument("--use-proxy", action="store_true")
    pdf.add_argument("--region")
    add_cli_runtime(pdf)
    pdf.set_defaults(handler="pdf")

    start_session = subparsers.add_parser("start-session", help="Run `steel browser start`")
    start_session.add_argument("--session", required=True)
    start_session.add_argument("--stealth", action="store_true")
    start_session.add_argument("--proxy")
    start_session.add_argument("--session-timeout", type=int)
    start_session.add_argument("--session-solve-captcha", action="store_true")
    start_session.add_argument("--profile")
    start_session.add_argument("--update-profile", action="store_true")
    start_session.add_argument("--namespace")
    start_session.add_argument("--credentials", action="store_true")
    add_cli_runtime(start_session)
    start_session.set_defaults(handler="start-session")

    stop_session = subparsers.add_parser("stop-session", help="Run `steel browser stop`")
    stop_session.add_argument("--session")
    stop_session.add_argument("--all", action="store_true")
    add_cli_runtime(stop_session)
    stop_session.set_defaults(handler="stop-session")

    sessions = subparsers.add_parser("sessions", help="Run `steel browser sessions`")
    add_cli_runtime(sessions)
    sessions.set_defaults(handler="sessions")

    live = subparsers.add_parser("live", help="Run `steel browser live`")
    live.add_argument("--session", required=True)
    add_cli_runtime(live)
    live.set_defaults(handler="live")

    browser = subparsers.add_parser("browser", help="Pass through to `steel browser ...`")
    browser.add_argument("--runtime", choices=["auto", "cli", "node"], default="auto")
    browser.add_argument("--session")
    browser.add_argument("--local", action="store_true")
    browser.add_argument("--api-url")
    browser.add_argument("--json", action="store_true")
    browser.add_argument("browser_args", nargs=argparse.REMAINDER)
    browser.set_defaults(handler="browser")

    python_plan = subparsers.add_parser("run-python-plan", help="Execute a JSON plan with Steel SDK + Playwright")
    python_plan.add_argument("--plan-file", required=True)
    python_plan.add_argument("--url", help="Optional start URL override")
    python_plan.add_argument("--session", help="Optional named session override")
    python_plan.add_argument("--site", help="Cookie lookup key override")
    python_plan.add_argument("--cookies-file", help="Cookie JSON file (or STEEL_BROWSER_COOKIES_FILE)")
    python_plan.add_argument("--use-proxy", action="store_true")
    python_plan.add_argument("--solve-captcha", action="store_true")
    python_plan.add_argument("--timeout", type=int, default=30000)
    python_plan.set_defaults(handler="run-python-plan")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1

    env, env_path = _load_env(args.env_file)

    try:
        if args.handler == "doctor":
            return cmd_doctor(args, env, env_path)
        if args.handler == "scrape":
            return cmd_scrape(args, env)
        if args.handler == "screenshot":
            return cmd_screenshot(args, env)
        if args.handler == "pdf":
            return cmd_pdf(args, env)
        if args.handler == "start-session":
            return cmd_start_session(args, env)
        if args.handler == "stop-session":
            return cmd_stop_session(args, env)
        if args.handler == "sessions":
            return cmd_sessions(args, env)
        if args.handler == "live":
            return cmd_live(args, env)
        if args.handler == "browser":
            return cmd_browser(args, env)
        if args.handler == "run-python-plan":
            return cmd_run_python_plan(args, env)
        raise SkillError("unknown handler: %s" % args.handler)
    except SkillError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
