"""CLI entry point — all sparki subcommands."""

import asyncio
import json
from pathlib import Path
from typing import Annotated, Any, Optional

import httpx
import typer

from sparki_cli.client import SparkiClient
from sparki_cli.config import Config, DEFAULT_CONFIG_DIR
from sparki_cli.constants import (
    ALLOWED_EXTENSIONS,
    MAX_FILES_PER_UPLOAD,
    MAX_UPLOAD_SIZE,
    EditMode,
    VALID_DURATION_RANGES,
    TELEGRAM_FILE_SIZE_LIMIT,
    validate_style,
    style_to_payload,
    DEFAULT_ASSET_POLL_INTERVAL,
    DEFAULT_ASSET_POLL_TIMEOUT,
    DEFAULT_PROJECT_POLL_INTERVAL,
    DEFAULT_PROJECT_POLL_TIMEOUT,
)
from sparki_cli.output import log, print_error, print_success

app = typer.Typer(add_completion=False)


def get_config_dir() -> Path:
    """Return the config directory path. Extracted for test monkeypatching."""
    return DEFAULT_CONFIG_DIR


def _load_config() -> Config:
    """Load configuration using the (possibly monkeypatched) config dir."""
    return Config(config_dir=get_config_dir())


def _require_auth() -> tuple[Config, SparkiClient] | None:
    """Load config and return (Config, SparkiClient), or print AUTH_FAILED and return None."""
    cfg = _load_config()
    if not cfg.api_key:
        print_error("AUTH_FAILED")
        return None
    client = SparkiClient(base_url=cfg.base_url, api_key=cfg.api_key)
    return cfg, client


def _validate_files(files: list[Path]) -> list[Path] | None:
    """Validate file existence, format, and size. Returns list or None on error."""
    if len(files) > MAX_FILES_PER_UPLOAD:
        print_error("UPLOAD_FAILED", f"Too many files: max {MAX_FILES_PER_UPLOAD} allowed, got {len(files)}")
        return None
    for f in files:
        if not f.exists():
            print_error("UPLOAD_FAILED", f"File not found: {f}")
            return None
        ext = f.suffix.lstrip(".").lower()
        if ext not in ALLOWED_EXTENSIONS:
            print_error("INVALID_FILE_FORMAT")
            return None
        if f.stat().st_size > MAX_UPLOAD_SIZE:
            print_error("FILE_TOO_LARGE")
            return None
    return files


def _history_file() -> Path:
    """Return the path to the local project history file."""
    return get_config_dir() / "sparki_history.json"


def _load_history() -> list[dict]:
    """Load locally tracked project IDs."""
    hf = _history_file()
    if hf.exists():
        return json.loads(hf.read_text())
    return []


def _save_project(task_id: str, mode: str = "", style: str = "") -> None:
    """Track a project ID locally for history lookups."""
    from datetime import datetime, timezone
    history = _load_history()
    history.insert(0, {
        "task_id": task_id,
        "mode": mode,
        "style": style,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    history = history[:100]
    hf = _history_file()
    hf.parent.mkdir(parents=True, exist_ok=True)
    hf.write_text(json.dumps(history, indent=2))


def _extract_result_url(data: dict[str, Any]) -> str | None:
    """Extract result URL from project status response data."""
    materials = data.get("materials", data.get("outputResultAssets",
                data.get("output_result_assets", [])))
    if not materials:
        return None
    item = materials[0]
    if isinstance(item, dict):
        return (item.get("url") or item.get("download_url")
                or item.get("downloadUrl"))
    if isinstance(item, str):
        return item
    return None


def _run_async(coro_fn):
    """Run an async function, catching httpx errors as NETWORK_ERROR."""
    try:
        asyncio.run(coro_fn())
    except (httpx.HTTPError, httpx.StreamError) as e:
        print_error("NETWORK_ERROR", str(e))


@app.command()
def setup(
    api_key: Annotated[str, typer.Option("--api-key", help="Your Sparki API key")],
    base_url: Annotated[Optional[str], typer.Option("--base-url", help="Override the Sparki API base URL")] = None,
) -> None:
    """Save API key and validate it against the Sparki backend."""

    async def _run() -> None:
        cfg = _load_config()
        effective_base_url = base_url or cfg.base_url
        client = SparkiClient(base_url=effective_base_url, api_key=api_key)
        valid = await client.validate_key()
        if not valid:
            print_error("AUTH_FAILED")
            return
        cfg.save(api_key=api_key, base_url=base_url)
        log("Welcome to Sparki! Configuration saved.")
        print_success({"message": "API key saved successfully",
                        "config_dir": str(get_config_dir())})

    _run_async(_run)


@app.command()
def upload(
    file: Annotated[list[Path], typer.Option("--file", help="Video file(s) to upload")],
) -> None:
    """Upload one or more video files to Sparki."""

    auth = _require_auth()
    if auth is None:
        return
    _, client = auth

    validated = _validate_files(file)
    if validated is None:
        return

    async def _run() -> None:
        assets = []
        for f in validated:
            log(f"Uploading {f.name}...")
            resp = await client.upload_asset(f)
            if resp.get("code") != 200:
                print_error("UPLOAD_FAILED", resp.get("message"))
                return
            assets.append(resp["data"])
        print_success({"assets": assets})

    _run_async(_run)


@app.command(name="upload-tg")
def upload_tg() -> None:
    """Return the configured Telegram upload link."""
    auth = _require_auth()
    if auth is None:
        return
    cfg, _ = auth
    print_success({"upload_tg": cfg.upload_tg})


@app.command()
def assets(
    limit: Annotated[int, typer.Option("--limit", help="Max number of assets to return")] = 20,
) -> None:
    """List uploaded assets."""

    auth = _require_auth()
    if auth is None:
        return
    _, client = auth

    async def _run() -> None:
        resp = await client.list_assets(page_size=limit)
        if resp.get("code") != 200:
            print_error("NETWORK_ERROR", resp.get("message"))
            return
        print_success(resp["data"])

    _run_async(_run)


@app.command()
def edit(
    object_key: Annotated[list[str], typer.Option("--object-key", help="Asset object key(s) to edit")],
    mode: Annotated[str, typer.Option("--mode", help="Edit mode: style-guided, prompt-driven")],
    style: Annotated[Optional[str], typer.Option("--style", help="Style for style-guided mode (e.g. vlog/daily)")] = None,
    prompt: Annotated[Optional[str], typer.Option("--prompt", help="Text prompt for prompt-driven mode")] = None,
    aspect_ratio: Annotated[str, typer.Option("--aspect-ratio", help="Output aspect ratio")] = "9:16",
    duration_range: Annotated[Optional[str], typer.Option("--duration-range", help="Duration range (e.g. 30s~60s)")] = None,
) -> None:
    """Create a new edit project for uploaded assets."""

    auth = _require_auth()
    if auth is None:
        return
    _, client = auth

    if duration_range and duration_range not in VALID_DURATION_RANGES:
        print_error("INVALID_MODE", f"Invalid duration range: {duration_range}")
        return

    if mode == EditMode.STYLE_GUIDED:
        if not style or not validate_style(style):
            print_error("INVALID_STYLE")
            return
        payload = style_to_payload(style)
        tags = payload["tags"]
        agent_type = payload["agent_type"]
        user_input = prompt or payload.get("default_prompt", "")
    elif mode == EditMode.PROMPT_DRIVEN:
        if not prompt:
            print_error("INVALID_MODE")
            return
        tags = []
        agent_type = None
        user_input = prompt
    else:
        print_error("INVALID_MODE")
        return

    async def _run() -> None:
        resp = await client.create_project(
            object_keys=object_key,
            tags=tags,
            user_input=user_input,
            aspect_ratio=aspect_ratio,
            agent_type=agent_type,
            duration_range=duration_range,
        )
        if resp.get("code") != 200:
            print_error("NETWORK_ERROR", resp.get("message"))
            return
        data = resp["data"]
        task_id = data.get("task_id", data.get("taskId", ""))
        _save_project(task_id, mode=mode, style=style or "")
        print_success(data)

    _run_async(_run)


@app.command()
def status(
    task_id: Annotated[str, typer.Option("--task-id", help="Project ID to check")],
) -> None:
    """Check the status of an edit project."""

    auth = _require_auth()
    if auth is None:
        return
    _, client = auth

    async def _run() -> None:
        resp = await client.get_project_status(task_id)
        if resp.get("code") != 200:
            print_error("TASK_NOT_FOUND", resp.get("message"))
            return
        print_success(resp["data"])

    _run_async(_run)


@app.command()
def download(
    task_id: Annotated[str, typer.Option("--task-id", help="Project ID to download")],
    output: Annotated[Optional[Path], typer.Option("--output", help="Output file path")] = None,
) -> None:
    """Download the result of a completed edit project."""

    auth = _require_auth()
    if auth is None:
        return
    cfg, client = auth

    async def _run() -> None:
        resp = await client.get_project_status(task_id)
        if resp.get("code") != 200:
            print_error("TASK_NOT_FOUND", resp.get("message"))
            return
        data = resp["data"]
        task_status = data.get("status", "").upper()
        if task_status != "COMPLETED":
            print_error("TASK_NOT_FOUND",
                        f"Project {task_id} is not completed (status: {data.get('status')})")
            return
        result_url = _extract_result_url(data)
        if not result_url:
            print_error("NETWORK_ERROR", "No result URL available")
            return
        out_path = output or cfg.default_output_dir / f"{task_id}.mp4"
        file_size = await client.download_result(result_url, out_path)
        delivery_hint = ("telegram_direct" if file_size <= TELEGRAM_FILE_SIZE_LIMIT
                         else "link_only")
        print_success({
            "task_id": task_id,
            "file_path": str(out_path),
            "file_size": file_size,
            "result_url": result_url,
            "delivery_hint": delivery_hint,
        })

    _run_async(_run)


@app.command()
def history(
    limit: Annotated[int, typer.Option("--limit", help="Number of projects to return")] = 20,
    status: Annotated[Optional[str], typer.Option("--status", help="Filter by status (or 'all')")] = "all",
) -> None:
    """List recent edit projects."""

    auth = _require_auth()
    if auth is None:
        return
    _, client = auth

    async def _run() -> None:
        local_history = _load_history()
        if not local_history:
            print_success({"projects": [], "total": 0})
            return
        entries = local_history[:limit]
        projects = []
        for entry in entries:
            tid = entry["task_id"]
            resp = await client.get_project_status(tid)
            if resp.get("code") == 200:
                projects.append(resp["data"])

        if status and status != "all":
            projects = [p for p in projects
                        if p.get("status", "").upper() == status.upper()]

        print_success({"projects": projects, "total": len(projects)})

    _run_async(_run)


@app.command()
def run(
    file: Annotated[list[Path], typer.Option("--file", help="Video file(s) to upload and edit")],
    mode: Annotated[str, typer.Option("--mode", help="Edit mode: style-guided, prompt-driven")],
    style: Annotated[Optional[str], typer.Option("--style", help="Style for style-guided mode")] = None,
    prompt: Annotated[Optional[str], typer.Option("--prompt", help="Text prompt for prompt-driven mode")] = None,
    aspect_ratio: Annotated[str, typer.Option("--aspect-ratio", help="Output aspect ratio")] = "9:16",
    duration_range: Annotated[Optional[str], typer.Option("--duration-range", help="Duration range")] = None,
    output: Annotated[Optional[Path], typer.Option("--output", help="Output file path")] = None,
    poll_interval: Annotated[int, typer.Option("--poll-interval", help="Seconds between project status polls")] = DEFAULT_PROJECT_POLL_INTERVAL,
    timeout: Annotated[int, typer.Option("--timeout", help="Max seconds to wait for completion")] = DEFAULT_PROJECT_POLL_TIMEOUT,
) -> None:
    """End-to-end workflow: upload -> edit -> poll -> download."""

    auth = _require_auth()
    if auth is None:
        return
    cfg, client = auth

    # Validate duration range
    if duration_range and duration_range not in VALID_DURATION_RANGES:
        print_error("INVALID_MODE", f"Invalid duration range: {duration_range}")
        return

    # Validate mode/style
    if mode == EditMode.STYLE_GUIDED:
        if not style or not validate_style(style):
            print_error("INVALID_STYLE")
            return
        payload = style_to_payload(style)
        tags = payload["tags"]
        agent_type = payload["agent_type"]
        user_input = prompt or payload.get("default_prompt", "")
    elif mode == EditMode.PROMPT_DRIVEN:
        if not prompt:
            print_error("INVALID_MODE")
            return
        tags = []
        agent_type = None
        user_input = prompt
    else:
        print_error("INVALID_MODE")
        return

    validated = _validate_files(file)
    if validated is None:
        return

    async def _run() -> None:
        import time

        # Step 1: Upload all files
        object_keys = []
        for f in validated:
            log(f"Uploading {f.name}...")
            resp = await client.upload_asset(f)
            if resp.get("code") != 200:
                print_error("UPLOAD_FAILED", resp.get("message"))
                return
            object_key = resp["data"]["object_key"]

            # Poll for asset processing
            log(f"Waiting for processing: {object_key}")
            asset_start = time.monotonic()
            while True:
                if time.monotonic() - asset_start >= DEFAULT_ASSET_POLL_TIMEOUT:
                    print_error("RENDER_TIMEOUT", "Asset processing timed out")
                    return
                try:
                    status_resp = await client.get_asset_status(object_key)
                except httpx.HTTPError as exc:
                    log(f"Asset status check failed ({exc}), retrying...")
                    await asyncio.sleep(DEFAULT_ASSET_POLL_INTERVAL)
                    continue
                asset_status = status_resp.get("data", {}).get("status") if status_resp.get("data") else None
                if asset_status == 1:
                    break
                if asset_status == -2:
                    print_error("UPLOAD_FAILED", f"Asset processing failed: {object_key}")
                    return
                await asyncio.sleep(DEFAULT_ASSET_POLL_INTERVAL)
            object_keys.append(object_key)

        # Step 2: Create project
        log("Creating edit project...")
        proj_resp = await client.create_project(
            object_keys=object_keys,
            tags=tags,
            user_input=user_input,
            aspect_ratio=aspect_ratio,
            agent_type=agent_type,
            duration_range=duration_range,
        )
        if proj_resp.get("code") != 200:
            print_error("NETWORK_ERROR", proj_resp.get("message"))
            return
        data = proj_resp["data"]
        task_id = data.get("task_id", data.get("taskId", ""))
        _save_project(task_id, mode=mode, style=style or "")

        # Step 3: Poll for project completion
        proj_start = time.monotonic()
        while True:
            elapsed = time.monotonic() - proj_start
            if elapsed >= timeout:
                print_error("RENDER_TIMEOUT")
                return
            try:
                status_resp = await client.get_project_status(task_id)
            except httpx.HTTPError as exc:
                log(f"Project status check failed ({exc}), retrying...")
                await asyncio.sleep(poll_interval)
                continue
            if status_resp.get("code") != 200:
                print_error("TASK_NOT_FOUND", status_resp.get("message"))
                return
            proj_data = status_resp["data"]
            task_status = proj_data.get("status", "")
            log(f"Project {task_id} status: {task_status}")
            if task_status.upper() in ("COMPLETED",):
                break
            if task_status.upper() in ("FAILED", "CANCEL"):
                print_error("NETWORK_ERROR", f"Project failed: {task_id}")
                return
            await asyncio.sleep(poll_interval)

        # Step 4: Download result
        result_url = _extract_result_url(proj_data)
        if not result_url:
            print_error("NETWORK_ERROR", "No result URL available")
            return
        out_path = output or cfg.default_output_dir / f"{task_id}.mp4"
        file_size = await client.download_result(result_url, out_path)
        delivery_hint = ("telegram_direct" if file_size <= TELEGRAM_FILE_SIZE_LIMIT
                         else "link_only")

        print_success({
            "task_id": task_id,
            "status": task_status,
            "file_path": str(out_path),
            "file_size": file_size,
            "result_url": result_url,
            "delivery_hint": delivery_hint,
        })

    _run_async(_run)
