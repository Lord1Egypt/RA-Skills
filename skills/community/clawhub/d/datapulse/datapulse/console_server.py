"""Local browser console for the DataPulse intelligence center."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Callable

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, Response
from pydantic import BaseModel, ConfigDict, Field

from datapulse.console_deck import build_mission_deck_suggestions
from datapulse.console_markup import render_console_html
from datapulse.reader import DataPulseReader

CONSOLE_TITLE = "DataPulse Command Chamber"
BRAND_SOURCE_PATH = Path(__file__).resolve().parent.parent / "docs" / "形象.jpg"
BRAND_HERO_PATH = Path(__file__).resolve().parent.parent / "docs" / "assets" / "datapulse-command-chamber-hero.jpg"
BRAND_SQUARE_PATH = Path(__file__).resolve().parent.parent / "docs" / "assets" / "datapulse-command-chamber-square.jpg"
BRAND_ICON_PATH = Path(__file__).resolve().parent.parent / "docs" / "assets" / "datapulse-command-chamber-icon.png"


class WatchCreateRequest(BaseModel):
    name: str
    query: str
    platforms: list[str] | None = None
    sites: list[str] | None = None
    schedule: str = "manual"
    min_confidence: float = 0.0
    top_n: int = 5
    alert_rules: list[dict[str, Any]] | None = None


class WatchUpdateRequest(BaseModel):
    name: str | None = None
    query: str | None = None
    platforms: list[str] | None = None
    sites: list[str] | None = None
    schedule: str | None = None
    min_confidence: float | None = None
    top_n: int | None = None
    alert_rules: list[dict[str, Any]] | None = None
    enabled: bool | None = None


class WatchAlertRuleRequest(BaseModel):
    alert_rules: list[dict[str, Any]] | None = None


class WatchDeckSuggestionRequest(BaseModel):
    name: str = ""
    query: str = ""
    schedule: str = ""
    platform: str = ""
    domain: str = ""
    route: str = ""
    keyword: str = ""
    min_score: str = ""
    min_confidence: str = ""


class RunDueRequest(BaseModel):
    limit: int = Field(default=0, ge=0)


class TriageStateRequest(BaseModel):
    state: str
    note: str = ""
    actor: str = "console"
    duplicate_of: str | None = None


class TriageNoteRequest(BaseModel):
    note: str
    author: str = "console"


class StoryUpdateRequest(BaseModel):
    title: str | None = None
    summary: str | None = None
    status: str | None = None


class StoryCreateRequest(BaseModel):
    title: str
    summary: str = ""
    status: str = "active"
    model_config = ConfigDict(extra="allow")


class StoryFromTriageRequest(BaseModel):
    item_ids: list[str]
    title: str | None = None
    summary: str = ""
    status: str = "monitoring"


class AlertRouteCreateRequest(BaseModel):
    name: str
    channel: str
    description: str | None = None
    webhook_url: str | None = None
    authorization: str | None = None
    headers: dict[str, str] | None = None
    feishu_webhook: str | None = None
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    timeout_seconds: float | None = Field(default=None, gt=0)


class AlertRouteUpdateRequest(BaseModel):
    channel: str | None = None
    description: str | None = None
    webhook_url: str | None = None
    authorization: str | None = None
    headers: dict[str, str] | None = None
    feishu_webhook: str | None = None
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    timeout_seconds: float | None = Field(default=None, gt=0)


def create_app(reader_factory: Callable[[], DataPulseReader] = DataPulseReader) -> FastAPI:
    app = FastAPI(title=CONSOLE_TITLE, version="0.8.0")

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        return render_console_html(CONSOLE_TITLE)

    @app.get("/brand/source")
    def brand_source() -> FileResponse:
        if not BRAND_SOURCE_PATH.exists():
            raise HTTPException(status_code=404, detail="brand source not found")
        return FileResponse(BRAND_SOURCE_PATH, media_type="image/jpeg")

    @app.get("/brand/hero")
    def brand_hero() -> FileResponse:
        if not BRAND_HERO_PATH.exists():
            raise HTTPException(status_code=404, detail="brand hero not found")
        return FileResponse(BRAND_HERO_PATH, media_type="image/jpeg")

    @app.get("/brand/square")
    def brand_square() -> FileResponse:
        if not BRAND_SQUARE_PATH.exists():
            raise HTTPException(status_code=404, detail="brand square not found")
        return FileResponse(BRAND_SQUARE_PATH, media_type="image/jpeg")

    @app.get("/brand/icon")
    def brand_icon() -> FileResponse:
        if not BRAND_ICON_PATH.exists():
            raise HTTPException(status_code=404, detail="brand icon not found")
        return FileResponse(BRAND_ICON_PATH, media_type="image/png")

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/readyz")
    def readyz() -> dict[str, str]:
        return {"status": "ready"}

    @app.get("/api/overview")
    def overview() -> dict[str, Any]:
        reader = reader_factory()
        watches = reader.list_watches(include_disabled=True)
        alerts = reader.list_alerts(limit=20)
        routes = reader.list_alert_routes()
        status = reader.watch_status_snapshot()
        stories = reader.list_stories(limit=5000, min_items=0)
        return {
            "enabled_watches": sum(1 for watch in watches if watch.get("enabled", True)),
            "disabled_watches": sum(1 for watch in watches if not watch.get("enabled", True)),
            "due_watches": sum(1 for watch in watches if watch.get("is_due")),
            "story_count": len(stories),
            "alert_count": len(alerts),
            "route_count": len(routes),
            "triage_open_count": reader.triage_stats().get("open_count", 0),
            "daemon_state": status.get("state", "idle"),
            "daemon_heartbeat_at": status.get("heartbeat_at", ""),
        }

    @app.get("/api/watches")
    def list_watches(include_disabled: bool = False) -> list[dict[str, Any]]:
        return reader_factory().list_watches(include_disabled=include_disabled)

    @app.get("/api/watches/{identifier}")
    def show_watch(identifier: str) -> dict[str, Any]:
        payload = reader_factory().show_watch(identifier)
        if payload is None:
            raise HTTPException(status_code=404, detail=f"Watch mission not found: {identifier}")
        return payload

    @app.get("/api/watches/{identifier}/results")
    def watch_results(identifier: str, limit: int = 10, min_confidence: float = 0.0) -> list[dict[str, Any]]:
        payload = reader_factory().list_watch_results(identifier, limit=limit, min_confidence=min_confidence)
        if payload is None:
            raise HTTPException(status_code=404, detail=f"Watch mission not found: {identifier}")
        return payload

    @app.post("/api/watches")
    def create_watch(payload: WatchCreateRequest) -> dict[str, Any]:
        return reader_factory().create_watch(**payload.model_dump())

    @app.put("/api/watches/{identifier}")
    def update_watch(identifier: str, payload: WatchUpdateRequest) -> dict[str, Any]:
        try:
            mission = reader_factory().update_watch(identifier, **payload.model_dump())
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if mission is None:
            raise HTTPException(status_code=404, detail=f"Watch mission not found: {identifier}")
        return mission

    @app.post("/api/console/deck/suggestions")
    def mission_deck_suggestions(payload: WatchDeckSuggestionRequest) -> dict[str, Any]:
        return build_mission_deck_suggestions(reader_factory(), payload.model_dump())

    @app.put("/api/watches/{identifier}/alert-rules")
    def set_watch_alert_rules(identifier: str, payload: WatchAlertRuleRequest) -> dict[str, Any]:
        mission = reader_factory().set_watch_alert_rules(identifier, alert_rules=payload.alert_rules)
        if mission is None:
            raise HTTPException(status_code=404, detail=f"Watch mission not found: {identifier}")
        return mission

    @app.post("/api/watches/run-due")
    async def run_due_watches(payload: RunDueRequest) -> dict[str, Any]:
        return await reader_factory().run_due_watches(limit=payload.limit or None)

    @app.post("/api/watches/{identifier}/run")
    async def run_watch(identifier: str) -> dict[str, Any]:
        try:
            return await reader_factory().run_watch(identifier)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.post("/api/watches/{identifier}/disable")
    def disable_watch(identifier: str) -> dict[str, Any]:
        payload = reader_factory().disable_watch(identifier)
        if payload is None:
            raise HTTPException(status_code=404, detail=f"Watch mission not found: {identifier}")
        return payload

    @app.post("/api/watches/{identifier}/enable")
    def enable_watch(identifier: str) -> dict[str, Any]:
        payload = reader_factory().enable_watch(identifier)
        if payload is None:
            raise HTTPException(status_code=404, detail=f"Watch mission not found: {identifier}")
        return payload

    @app.delete("/api/watches/{identifier}")
    def delete_watch(identifier: str) -> dict[str, Any]:
        payload = reader_factory().delete_watch(identifier)
        if payload is None:
            raise HTTPException(status_code=404, detail=f"Watch mission not found: {identifier}")
        return payload

    @app.get("/api/alerts")
    def list_alerts(limit: int = 20, mission_id: str = "") -> list[dict[str, Any]]:
        return reader_factory().list_alerts(limit=limit, mission_id=mission_id or None)

    @app.get("/api/alert-routes")
    def list_alert_routes() -> list[dict[str, Any]]:
        return reader_factory().list_alert_routes()

    @app.post("/api/alert-routes")
    def create_alert_route(payload: AlertRouteCreateRequest) -> dict[str, Any]:
        try:
            return reader_factory().create_alert_route(**payload.model_dump(exclude_none=True))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.put("/api/alert-routes/{identifier}")
    def update_alert_route(identifier: str, payload: AlertRouteUpdateRequest) -> dict[str, Any]:
        try:
            route = reader_factory().update_alert_route(identifier, **payload.model_dump(exclude_none=True))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if route is None:
            raise HTTPException(status_code=404, detail=f"Alert route not found: {identifier}")
        return route

    @app.delete("/api/alert-routes/{identifier}")
    def delete_alert_route(identifier: str) -> dict[str, Any]:
        route = reader_factory().delete_alert_route(identifier)
        if route is None:
            raise HTTPException(status_code=404, detail=f"Alert route not found: {identifier}")
        return route

    @app.get("/api/alert-routes/health")
    def alert_route_health(limit: int = 100) -> list[dict[str, Any]]:
        return reader_factory().alert_route_health(limit=limit)

    @app.get("/api/watch-status")
    def watch_status() -> dict[str, Any]:
        return reader_factory().watch_status_snapshot()

    @app.get("/api/ops")
    def ops_snapshot() -> dict[str, Any]:
        return reader_factory().ops_snapshot()

    @app.get("/api/ops/scorecard")
    def ops_scorecard() -> dict[str, Any]:
        return reader_factory().governance_scorecard_snapshot()

    @app.get("/api/stories")
    def list_stories(limit: int = 8, min_items: int = 0) -> list[dict[str, Any]]:
        return reader_factory().list_stories(limit=limit, min_items=min_items)

    @app.post("/api/stories")
    def create_story(payload: StoryCreateRequest) -> dict[str, Any]:
        try:
            return reader_factory().create_story(**payload.model_dump(exclude_none=True))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/api/stories/from-triage")
    def create_story_from_triage(payload: StoryFromTriageRequest) -> dict[str, Any]:
        try:
            return reader_factory().create_story_from_triage(**payload.model_dump(exclude_none=True))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/api/stories/{identifier}")
    def show_story(identifier: str) -> dict[str, Any]:
        story = reader_factory().show_story(identifier)
        if story is None:
            raise HTTPException(status_code=404, detail=f"Story not found: {identifier}")
        return story

    @app.put("/api/stories/{identifier}")
    def update_story(identifier: str, payload: StoryUpdateRequest) -> dict[str, Any]:
        try:
            story = reader_factory().update_story(identifier, **payload.model_dump())
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if story is None:
            raise HTTPException(status_code=404, detail=f"Story not found: {identifier}")
        return story

    @app.delete("/api/stories/{identifier}")
    def delete_story(identifier: str) -> dict[str, Any]:
        story = reader_factory().delete_story(identifier)
        if story is None:
            raise HTTPException(status_code=404, detail=f"Story not found: {identifier}")
        return story

    @app.get("/api/stories/{identifier}/graph")
    def story_graph(identifier: str, entity_limit: int = 12, relation_limit: int = 24) -> dict[str, Any]:
        graph = reader_factory().story_graph(
            identifier,
            entity_limit=entity_limit,
            relation_limit=relation_limit,
        )
        if graph is None:
            raise HTTPException(status_code=404, detail=f"Story not found: {identifier}")
        return graph

    @app.get("/api/stories/{identifier}/export")
    def export_story(identifier: str, format: str = "markdown") -> Response:
        output_format = str(format or "markdown").strip().lower() or "markdown"
        if output_format not in {"markdown", "md", "json"}:
            raise HTTPException(status_code=400, detail=f"Unsupported story export format: {format}")
        payload = reader_factory().export_story(identifier, output_format=output_format)
        if payload is None:
            raise HTTPException(status_code=404, detail=f"Story not found: {identifier}")
        media_type = "application/json" if output_format == "json" else "text/markdown"
        return Response(content=payload, media_type=media_type)

    @app.get("/api/triage")
    def triage_list(limit: int = 20, state: list[str] | None = None, include_closed: bool = False) -> list[dict[str, Any]]:
        return reader_factory().triage_list(limit=limit, states=state, include_closed=include_closed)

    @app.get("/api/triage/stats")
    def triage_stats() -> dict[str, Any]:
        return reader_factory().triage_stats()

    @app.get("/api/triage/{item_id}/explain")
    def triage_explain(item_id: str, limit: int = 5) -> dict[str, Any]:
        payload = reader_factory().triage_explain(item_id, limit=limit)
        if payload is None:
            raise HTTPException(status_code=404, detail=f"Triage item not found: {item_id}")
        return payload

    @app.post("/api/triage/{item_id}/state")
    def triage_update(item_id: str, payload: TriageStateRequest) -> dict[str, Any]:
        try:
            item = reader_factory().triage_update(item_id, **payload.model_dump())
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if item is None:
            raise HTTPException(status_code=404, detail=f"Triage item not found: {item_id}")
        return item

    @app.post("/api/triage/{item_id}/note")
    def triage_note(item_id: str, payload: TriageNoteRequest) -> dict[str, Any]:
        item = reader_factory().triage_note(item_id, **payload.model_dump())
        if item is None:
            raise HTTPException(status_code=404, detail=f"Triage item not found: {item_id}")
        return item

    @app.delete("/api/triage/{item_id}")
    def triage_delete(item_id: str) -> dict[str, Any]:
        item = reader_factory().triage_delete(item_id)
        if item is None:
            raise HTTPException(status_code=404, detail=f"Triage item not found: {item_id}")
        return item

    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch the DataPulse browser console.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8765, help="Bind port (default 8765)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for local development")
    args = parser.parse_args()

    import uvicorn

    uvicorn.run("datapulse.console_server:create_app", host=args.host, port=args.port, reload=args.reload, factory=True)


if __name__ == "__main__":
    main()
