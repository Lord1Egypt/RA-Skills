#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def load_plan(plan_path: str) -> dict:
    if plan_path == "-":
        return json.load(sys.stdin)
    with open(plan_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_step(page, step: dict) -> dict:
    action = step.get("action")
    if action == "goto":
        url = step["url"]
        wait_until = step.get("wait_until", "domcontentloaded")
        page.goto(url, wait_until=wait_until)
        return {"action": action, "ok": True, "url": page.url}

    if action == "click":
        page.locator(step["selector"]).first.click(timeout=step.get("timeout_ms", 10000))
        return {"action": action, "ok": True}

    if action == "fill":
        page.locator(step["selector"]).first.fill(step.get("text", ""), timeout=step.get("timeout_ms", 10000))
        return {"action": action, "ok": True}

    if action == "type":
        page.locator(step["selector"]).first.type(
            step.get("text", ""),
            delay=step.get("delay_ms", 50),
            timeout=step.get("timeout_ms", 10000),
        )
        return {"action": action, "ok": True}

    if action == "press":
        page.keyboard.press(step["key"])
        return {"action": action, "ok": True}

    if action == "wait":
        page.wait_for_timeout(step.get("ms", 1000))
        return {"action": action, "ok": True}

    if action == "wait_for_selector":
        page.locator(step["selector"]).first.wait_for(timeout=step.get("timeout_ms", 10000))
        return {"action": action, "ok": True}

    if action == "screenshot":
        path = step.get("path", "/tmp/firefox-openclaw-step.png")
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=path, full_page=step.get("full_page", False))
        return {"action": action, "ok": True, "path": path}

    if action == "content":
        text = page.locator(step["selector"]).first.inner_text(timeout=step.get("timeout_ms", 10000))
        return {"action": action, "ok": True, "text": text}

    raise ValueError(f"Unsupported action: {action}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run structured Firefox automation steps with Playwright.")
    parser.add_argument("--plan", required=True, help="Path to JSON plan file, or '-' for stdin")
    parser.add_argument("--display", default=os.environ.get("DISPLAY", ":1"))
    parser.add_argument("--profile-dir", default="/root/snap/firefox/common/.mozilla/firefox/kp5hskbz.default")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--output", default="-", help="Where to write JSON results, '-' for stdout")
    args = parser.parse_args()

    plan = load_plan(args.plan)
    os.environ["DISPLAY"] = args.display

    needs_gui = bool(plan.get("needs_gui", False))
    gui_reason = str(plan.get("gui_reason", "")).strip()
    allowed_reasons = {
        "login",
        "captcha",
        "mfa",
        "visual_verification",
        "site_only_action",
    }

    if not needs_gui:
        result = {
            "ok": True,
            "skipped": True,
            "reason": "GUI launch blocked by policy: set needs_gui=true in plan.",
        }
        payload = json.dumps(result, ensure_ascii=True, indent=2)
        if args.output == "-":
            print(payload)
        else:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(payload + "\n")
        return 0

    if gui_reason not in allowed_reasons:
        result = {
            "ok": False,
            "skipped": True,
            "reason": "Invalid or missing gui_reason.",
            "allowed_gui_reasons": sorted(allowed_reasons),
        }
        payload = json.dumps(result, ensure_ascii=True, indent=2)
        if args.output == "-":
            print(payload)
        else:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(payload + "\n")
        return 3

    profile_dir = plan.get("profile_dir", args.profile_dir)
    headless = bool(plan.get("headless", args.headless))
    initial_url = plan.get("url", "about:blank")
    steps = plan.get("steps", [])

    Path(profile_dir).mkdir(parents=True, exist_ok=True)

    results = {"ok": True, "display": args.display, "profile_dir": profile_dir, "steps": []}

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=headless)
        context = browser.new_context()

        # Inject cookies from file if provided in plan
        cookies_path = plan.get("cookies_path")
        if cookies_path and os.path.exists(cookies_path):
            import json as _json
            with open(cookies_path) as cf:
                cookie_data = _json.load(cf)
            context.add_cookies(cookie_data.get("cookies", []))

        page = context.new_page()
        page.goto(initial_url)
        for step in steps:
            try:
                step_result = run_step(page, step)
                results["steps"].append(step_result)
            except Exception as exc:
                results["ok"] = False
                results["steps"].append(
                    {"action": step.get("action"), "ok": False, "error": str(exc), "url": page.url}
                )
                break

        results["final_url"] = page.url

        # Validate: take a final confirmation screenshot before closing
        validation_path = plan.get("validation_screenshot", "/tmp/firefox-openclaw-validate.png")
        page.screenshot(path=validation_path)
        results["validation_screenshot"] = validation_path

        # Wait before closing - give time to confirm result is correct
        close_delay_ms = plan.get("close_delay_ms", 3000)
        page.wait_for_timeout(close_delay_ms)

        if plan.get("storage_state_path"):
            context.storage_state(path=plan["storage_state_path"])
        context.close()
        browser.close()

    payload = json.dumps(results, ensure_ascii=True, indent=2)
    if args.output == "-":
        print(payload)
    else:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(payload + "\n")

    return 0 if results["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
