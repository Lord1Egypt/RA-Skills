#!/usr/bin/env python3
import argparse
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
from urllib.parse import urljoin, urlparse

try:
    from i18n import add_locale_argument, t
except ModuleNotFoundError:  # Imported by the repository test suite.
    from scripts.i18n import add_locale_argument, t


ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT_SCRIPT = ROOT / "scripts" / "design-contract.py"
VISUAL_DIFF_SCRIPT = ROOT / "scripts" / "visual-diff.py"
ACCESSIBLE_NAME_RULES = {
    "aria-command-name",
    "aria-input-field-name",
    "button-name",
    "input-button-name",
    "label",
    "link-name",
    "select-name",
}


def load_module(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_sync_playwright():
    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError:
        pw_python = shutil.which("pw-python")
        if pw_python and pathlib.Path(sys.executable).name != "pw-python":
            os.execvp(pw_python, [pw_python, *sys.argv])
        raise RuntimeError(
            "Playwright is required. Install playwright or run with an environment that provides pw-python."
        )
    return sync_playwright


def normalize_target(target: str) -> str:
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https", "file"}:
        return target
    return pathlib.Path(target).expanduser().resolve().as_uri()


def join_target(base: str, path: str) -> str:
    if urlparse(path).scheme in {"http", "https", "file"}:
        return path
    if base.startswith("file:"):
        path_parts = urlparse(path)
        base_parts = urlparse(base)
        if path_parts.path in {"", "/"}:
            return base_parts._replace(query=path_parts.query, fragment=path_parts.fragment).geturl()
        base_path = pathlib.Path(base_parts.path)
        file_url = (base_path.parent / path_parts.path.lstrip("/")).resolve().as_uri()
        return urlparse(file_url)._replace(query=path_parts.query, fragment=path_parts.fragment).geturl()
    return urljoin(base.rstrip("/") + "/", path.lstrip("/"))


def viewport_height(width: int) -> int:
    if width <= 480:
        return 844
    if width <= 1100:
        return 768
    return 900


def resolve_axe_script(project_root: pathlib.Path, explicit: str | None) -> pathlib.Path | None:
    candidates = []
    if explicit:
        candidates.append(pathlib.Path(explicit).expanduser())
    candidates.extend(
        [
            project_root / "node_modules" / "axe-core" / "axe.min.js",
            project_root / "node_modules" / "axe-core" / "axe.js",
        ]
    )
    return next((path.resolve() for path in candidates if path.is_file()), None)


def resolve_command(explicit: str | None, fallback: str) -> str | None:
    if explicit:
        candidate = pathlib.Path(explicit).expanduser()
        if candidate.parent != pathlib.Path(".") or "/" in explicit:
            return str(candidate.resolve()) if candidate.is_file() and os.access(candidate, os.X_OK) else None
        return shutil.which(explicit)
    return shutil.which(fallback)


def run_step(page, step: dict, target: str) -> str | None:
    action = step["action"]
    selector = step.get("selector")
    value = step.get("value", "")
    timeout = step.get("timeoutMs", 5000)
    if action == "goto":
        page.goto(join_target(target, value), wait_until="networkidle", timeout=timeout)
    elif action == "click":
        page.locator(selector).click(timeout=timeout)
    elif action == "fill":
        page.locator(selector).fill(value, timeout=timeout)
    elif action == "press":
        page.locator(selector).press(value, timeout=timeout)
    elif action == "expect-visible":
        page.locator(selector).wait_for(state="visible", timeout=timeout)
    elif action == "expect-hidden":
        page.locator(selector).wait_for(state="hidden", timeout=timeout)
    elif action == "expect-text":
        actual = page.locator(selector).inner_text(timeout=timeout)
        if value not in actual:
            raise AssertionError(f"Expected {selector} to contain {value!r}; got {actual!r}")
    elif action == "expect-url":
        if not re.search(value, page.url):
            raise AssertionError(f"Expected URL /{value}/; got {page.url}")
    elif action == "screenshot":
        return step.get("name") or "checkpoint"
    else:
        raise ValueError(f"Unsupported flow action: {action}")


def browser_metrics(page) -> dict:
    return page.evaluate(
        """
        () => {
          const nav = performance.getEntriesByType('navigation')[0];
          const resources = performance.getEntriesByType('resource');
          const root = document.documentElement;
          return {
            loadMs: nav ? Math.round(nav.loadEventEnd || nav.duration) : 0,
            transferBytes: resources.reduce((sum, item) => sum + (item.transferSize || 0), nav && nav.transferSize || 0),
            requests: resources.length + 1,
            horizontalOverflow: root.scrollWidth > root.clientWidth + 1,
            reducedMotionActive: matchMedia('(prefers-reduced-motion: reduce)').matches
          };
        }
        """
    )


def run_axe(page, axe_script: pathlib.Path) -> dict:
    page.add_script_tag(path=str(axe_script))
    return page.evaluate(
        """
        async () => {
          const result = await axe.run(document, {resultTypes: ['violations']});
          return {
            count: result.violations.length,
            violations: result.violations.map(item => ({
              id: item.id,
              impact: item.impact,
              nodes: item.nodes.length,
              help: item.help
            }))
          };
        }
        """
    )


def accessible_name_violations(axe_result: dict) -> list[str]:
    return sorted(
        violation["id"]
        for violation in axe_result.get("violations", [])
        if violation.get("id") in ACCESSIBLE_NAME_RULES
    )


def run_lighthouse(command: str, target: str, output_path: pathlib.Path) -> dict:
    try:
        result = subprocess.run(
            [
                command,
                target,
                "--quiet",
                "--output=json",
                f"--output-path={output_path}",
                "--chrome-flags=--headless --no-sandbox --disable-gpu",
            ],
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"available": False, "passed": False, "error": str(exc)}
    if result.returncode != 0:
        return {"available": True, "passed": False, "error": result.stderr.strip() or result.stdout.strip()}
    report = json.loads(output_path.read_text(encoding="utf-8"))
    score = report.get("categories", {}).get("performance", {}).get("score")
    return {"available": True, "passed": True, "score": score, "report": str(output_path)}


def compare_visual(
    baseline: pathlib.Path,
    current: pathlib.Path,
    diff: pathlib.Path,
    max_ratio: float,
) -> dict:
    module = load_module("visual_diff", VISUAL_DIFF_SCRIPT)
    result = module.compare_images(baseline, current, diff)
    result["passed"] = result["comparable"] and result["ratio"] <= max_ratio
    return result


def verify(args: argparse.Namespace) -> tuple[dict, int]:
    contract_module = load_module("design_contract", CONTRACT_SCRIPT)
    contract_path = pathlib.Path(args.contract).expanduser().resolve()
    project_root = pathlib.Path(args.project_root).expanduser().resolve()
    errors, engine = contract_module.validate_contract(
        contract_path,
        project_root,
        require_approved=not args.allow_draft,
    )
    if errors:
        return {"passed": False, "contractEngine": engine, "errors": errors}, 1
    contract = contract_module.load_json(contract_path)

    target = normalize_target(args.target)
    out_dir = pathlib.Path(args.out).expanduser().resolve()
    screenshot_dir = out_dir / "screenshots"
    diff_dir = out_dir / "diffs"
    out_dir.mkdir(parents=True, exist_ok=True)
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    axe_script = resolve_axe_script(project_root, args.axe_script)
    lighthouse_command = resolve_command(args.lighthouse_command, "lighthouse")
    report = {
        "passed": True,
        "contractEngine": engine,
        "target": target,
        "tools": {
            "playwright": True,
            "axe": str(axe_script) if axe_script else None,
            "lighthouse": lighthouse_command,
        },
        "flows": [],
        "errors": [],
        "warnings": [],
    }
    if not axe_script:
        message = "axe-core not found; install axe-core or pass --axe-script"
        (report["warnings"] if args.allow_missing_tools else report["errors"]).append(message)
    if not lighthouse_command and target.startswith(("http://", "https://")):
        message = "Lighthouse not found; install lighthouse or pass --lighthouse-command"
        (report["warnings"] if args.allow_missing_tools else report["errors"]).append(message)

    keyboard_flow_present = any(
        step.get("action") == "press"
        for flow in contract["flows"]
        for step in flow.get("steps", [])
    )
    if contract["accessibility"]["keyboardComplete"] and not keyboard_flow_present:
        report["errors"].append("keyboardComplete requires at least one press step")

    sync_playwright = load_sync_playwright()
    browser_executable = args.chromium if args.chromium and pathlib.Path(args.chromium).is_file() else None
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=browser_executable)
        for width in contract["breakpoints"]:
            context = browser.new_context(
                viewport={"width": width, "height": viewport_height(width)},
                reduced_motion="reduce" if contract["accessibility"]["reducedMotion"] else "no-preference",
            )
            for flow in contract["flows"]:
                page = context.new_page()
                console_errors = []
                page_errors = []
                page.on("console", lambda message, bucket=console_errors: bucket.append(message.text) if message.type == "error" else None)
                page.on("pageerror", lambda error, bucket=page_errors: bucket.append(str(error)))
                flow_report = {"id": flow["id"], "width": width, "passed": True, "errors": []}
                try:
                    page.goto(join_target(target, flow["start"]), wait_until="networkidle", timeout=args.timeout_ms)
                    for step_index, step in enumerate(flow.get("steps", [])):
                        checkpoint = run_step(page, step, target)
                        if checkpoint:
                            safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "-", checkpoint).strip("-") or "checkpoint"
                            checkpoint_path = screenshot_dir / (
                                f"{flow['id']}-{width}-{step_index}-{safe_name}.png"
                            )
                            page.screenshot(path=str(checkpoint_path), full_page=True)
                            flow_report.setdefault("checkpoints", []).append(str(checkpoint_path))
                    screenshot_name = f"{flow['id']}-{width}.png"
                    screenshot_path = screenshot_dir / screenshot_name
                    page.screenshot(path=str(screenshot_path), full_page=True)
                    flow_report["screenshot"] = str(screenshot_path)
                    flow_report["metrics"] = browser_metrics(page)
                    flow_report["consoleErrors"] = console_errors + page_errors
                    if axe_script:
                        flow_report["axe"] = run_axe(page, axe_script)

                    baseline_value = contract.get("visualBaselines", {}).get(f"{flow['id']}@{width}")
                    if baseline_value:
                        baseline = (project_root / baseline_value).resolve()
                        if not baseline.is_file():
                            flow_report["errors"].append(f"visual baseline not found: {baseline_value}")
                        else:
                            flow_report["visualDiff"] = compare_visual(
                                baseline,
                                screenshot_path,
                                diff_dir / screenshot_name,
                                contract["performance"]["maxVisualDiffRatio"],
                            )
                except Exception as exc:
                    flow_report["errors"].append(str(exc))
                finally:
                    page.close()

                metrics = flow_report.get("metrics", {})
                budgets = contract["performance"]
                if metrics.get("loadMs", 0) > budgets["maxLoadMs"]:
                    flow_report["errors"].append("load time budget exceeded")
                if metrics.get("transferBytes", 0) > budgets["maxTransferBytes"]:
                    flow_report["errors"].append("transfer budget exceeded")
                if metrics.get("requests", 0) > budgets["maxRequests"]:
                    flow_report["errors"].append("request budget exceeded")
                if metrics.get("horizontalOverflow"):
                    flow_report["errors"].append("horizontal overflow detected")
                if contract["accessibility"]["reducedMotion"] and not metrics.get("reducedMotionActive"):
                    flow_report["errors"].append("reduced-motion media preference was not active")
                if len(flow_report.get("consoleErrors", [])) > budgets["maxConsoleErrors"]:
                    flow_report["errors"].append("console error budget exceeded")
                if flow_report.get("axe", {}).get("count", 0) > contract["accessibility"]["maxAxeViolations"]:
                    flow_report["errors"].append("axe violation budget exceeded")
                if contract["accessibility"]["requireAccessibleNames"] and flow_report.get("axe"):
                    name_violations = accessible_name_violations(flow_report["axe"])
                    if name_violations:
                        flow_report["errors"].append(
                            f"accessible name requirement failed: {', '.join(name_violations)}"
                        )
                if flow_report.get("visualDiff") and not flow_report["visualDiff"]["passed"]:
                    flow_report["errors"].append("visual difference budget exceeded")
                flow_report["passed"] = not flow_report["errors"]
                report["flows"].append(flow_report)
            context.close()
        browser.close()

    if lighthouse_command and target.startswith(("http://", "https://")):
        lighthouse = run_lighthouse(lighthouse_command, target, out_dir / "lighthouse.json")
        if lighthouse.get("score") is not None:
            lighthouse["passed"] = lighthouse["score"] >= contract["performance"]["minLighthouseScore"]
        if not lighthouse.get("passed"):
            report["errors"].append("Lighthouse performance budget failed")
        report["lighthouse"] = lighthouse
    elif target.startswith("file:"):
        report["warnings"].append("Lighthouse skipped for file target; use an HTTP preview for release verification")

    if any(not flow["passed"] for flow in report["flows"]):
        report["errors"].append("one or more interaction flows failed")
    report["passed"] = not report["errors"]
    report_path = out_dir / "report.json"
    report["report"] = str(report_path)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report, 0 if report["passed"] else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=t("Run contract-driven frontend interaction and production QA."))
    add_locale_argument(parser)
    parser.add_argument("target", help=t("HTTP(S) URL or local HTML path"))
    parser.add_argument("--contract", default=".codex/design-guide/design-contract.json")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--out", default=".codex/design-guide/verification")
    parser.add_argument("--axe-script")
    parser.add_argument("--lighthouse-command")
    parser.add_argument("--chromium", default="/usr/bin/chromium")
    parser.add_argument("--timeout-ms", type=int, default=10000)
    parser.add_argument("--allow-draft", action="store_true")
    parser.add_argument("--allow-missing-tools", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report, code = verify(args)
    except (RuntimeError, ValueError) as exc:
        print(t("verify-ui failed: {error}", args.locale, error=exc), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
