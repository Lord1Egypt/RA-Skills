"""Engram Web UI — lightweight HTTP server for visual Engram management."""

from __future__ import annotations

import json
import webbrowser
from dataclasses import asdict
from pathlib import Path
from typing import Any

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from engram_server.loader import EngramLoader

STATIC_DIR = Path(__file__).parent / "static"


def _json(data: Any, status: int = 200) -> JSONResponse:
    return JSONResponse(data, status_code=status)


def _build_loader(packs_dir: Path) -> EngramLoader:
    configured = Path(packs_dir).expanduser().resolve()
    project_engram = (Path.cwd().resolve() / ".claude" / "engram").resolve()

    # Web UI should focus on the current project workspace when available.
    if project_engram.is_dir():
        return EngramLoader(packs_dir=[project_engram], default_packs_dir=project_engram)

    return EngramLoader(packs_dir=[configured], default_packs_dir=configured)


# ---------------------------------------------------------------------------
# API route handlers
# ---------------------------------------------------------------------------

async def api_list_engrams(request: Request) -> JSONResponse:
    loader: EngramLoader = request.app.state.loader
    return _json(loader.list_engrams())


async def api_get_engram(request: Request) -> JSONResponse:
    loader: EngramLoader = request.app.state.loader
    name = request.path_params["name"]
    info = loader.get_engram_info(name)
    if info is None:
        return _json({"error": f"Engram not found: {name}"}, 404)
    return _json(info)


async def api_list_files(request: Request) -> JSONResponse:
    loader: EngramLoader = request.app.state.loader
    name = request.path_params["name"]
    engram_dir = loader._resolve_engram_dir(name)
    if engram_dir is None:
        return _json({"error": f"Engram not found: {name}"}, 404)

    files: list[dict[str, str]] = []
    for p in sorted(engram_dir.rglob("*")):
        if p.is_file() and not p.name.startswith("."):
            rel = str(p.relative_to(engram_dir))
            files.append({"path": rel, "name": p.name})
    return _json(files)


async def api_read_file(request: Request) -> Response:
    loader: EngramLoader = request.app.state.loader
    name = request.path_params["name"]
    file_path = request.path_params["path"]
    content = loader.load_file(name, file_path)
    if content is None:
        return _json({"error": "File not found"}, 404)
    return Response(content, media_type="text/plain; charset=utf-8")


async def api_write_file(request: Request) -> JSONResponse:
    loader: EngramLoader = request.app.state.loader
    name = request.path_params["name"]
    file_path = request.path_params["path"]
    body = await request.json()
    content = body.get("content", "")
    ok = loader.write_file(name, file_path, content)
    if not ok:
        return _json({"error": "Write failed"}, 400)
    return _json({"ok": True})


async def api_delete_memory(request: Request) -> JSONResponse:
    loader: EngramLoader = request.app.state.loader
    name = request.path_params["name"]
    body = await request.json()
    category = body.get("category", "")
    summary = body.get("summary", "")
    ok = loader.delete_memory(name, category, summary)
    if not ok:
        return _json({"error": "Memory entry not found"}, 404)
    return _json({"ok": True, "deleted": summary})


async def api_stats(request: Request) -> JSONResponse:
    from engram_server.stats import gather_stats

    loader: EngramLoader = request.app.state.loader
    report = gather_stats(loader)
    return _json(asdict(report))


async def api_lint(request: Request) -> JSONResponse:
    from engram_server.lint import lint_engram

    loader: EngramLoader = request.app.state.loader
    name = request.path_params["name"]
    engram_dir = loader._resolve_engram_dir(name)
    if engram_dir is None:
        return _json({"error": f"Engram not found: {name}"}, 404)
    messages = lint_engram(engram_dir)
    return _json([
        {"level": m.level, "file": m.file_path, "message": m.message}
        for m in messages
    ])


# ---------------------------------------------------------------------------
# SPA fallback — serve index.html for non-API, non-static paths
# ---------------------------------------------------------------------------

async def _spa_fallback(request: Request) -> Response:
    index = STATIC_DIR / "index.html"
    if not index.exists():
        return Response("Web UI not found. Static files missing.", status_code=500)
    return Response(index.read_text(encoding="utf-8"), media_type="text/html")


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

def create_web_app(packs_dir: Path) -> Starlette:
    loader = _build_loader(packs_dir)

    api_routes = [
        Route("/engrams", api_list_engrams),
        Route("/engrams/{name}", api_get_engram),
        Route("/engrams/{name}/files", api_list_files),
        Route("/engrams/{name}/files/{path:path}", api_read_file, methods=["GET"]),
        Route("/engrams/{name}/files/{path:path}", api_write_file, methods=["PUT"]),
        Route("/engrams/{name}/memory", api_delete_memory, methods=["DELETE"]),
        Route("/engrams/{name}/lint", api_lint),
        Route("/stats", api_stats),
    ]

    routes: list = [Mount("/api", routes=api_routes)]

    if STATIC_DIR.exists():
        routes.append(Mount("/static", app=StaticFiles(directory=str(STATIC_DIR))))

    # SPA fallback must be last
    routes.append(Route("/{path:path}", _spa_fallback))
    routes.append(Route("/", _spa_fallback))

    app = Starlette(routes=routes)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    app.state.loader = loader
    return app


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_ui(packs_dir: Path, port: int = 9470, open_browser: bool = True) -> None:
    import uvicorn

    app = create_web_app(packs_dir)
    url = f"http://localhost:{port}"
    print(f"Engram UI running at {url}")

    if open_browser:
        webbrowser.open(url)

    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")
