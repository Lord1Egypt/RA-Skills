from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


ParamType = Literal["string", "date", "select", "integer", "number", "boolean"]
ExportFormat = Literal["csv", "json", "xlsx"]
SnapshotMode = Literal["filter_row", "latest_row", "first_row", "top_n"]


class IndicatorParam(BaseModel):
    name: str
    label: str
    type: ParamType = "string"
    required: bool = False
    default: Any | None = None
    placeholder: str | None = None
    description: str | None = None
    options: list[str] | None = None


class Indicator(BaseModel):
    id: str
    level1: str
    level2: str
    level3: str
    name: str
    ak_function: str
    source: str = ""
    source_name: str = ""
    update_frequency: str = ""
    description: str
    docs_url: str
    params: list[IndicatorParam] = Field(default_factory=list)
    result_notes: str | None = None


class IndicatorSummary(BaseModel):
    id: str
    level1: str
    level2: str
    level3: str
    name: str
    source: str = ""
    source_name: str = ""
    update_frequency: str = ""
    description: str
    docs_url: str


class SourceSummary(BaseModel):
    source: str
    source_name: str
    indicator_count: int


class RunRequest(BaseModel):
    indicator_id: str
    params: dict[str, Any] = Field(default_factory=dict)
    refresh: bool = False


class RunResponse(BaseModel):
    task_id: str
    indicator_id: str
    indicator_name: str
    row_count: int
    column_count: int
    columns: list[str]
    preview: list[dict[str, Any]]
    created_at: datetime
    expires_at: datetime


class PreviewResponse(BaseModel):
    task_id: str
    row_count: int
    column_count: int
    columns: list[str]
    preview: list[dict[str, Any]]
    created_at: datetime
    expires_at: datetime


class ErrorResponse(BaseModel):
    detail: str


class SnapshotCardConfig(BaseModel):
    title: str
    ak_function: str
    params: dict[str, Any] = Field(default_factory=dict)
    mode: SnapshotMode = "filter_row"
    filter_column: str | None = None
    filter_value: str | int | float | None = None
    value_field: str
    change_field: str | None = None
    unit: str = ""
    decimals: int = 2
    description: str | None = None


class SectorSnapshotConfig(BaseModel):
    cards: list[SnapshotCardConfig] = Field(default_factory=list)


class Sector(BaseModel):
    id: str
    name: str
    short_name: str
    description: str
    accent: str = "#1e6ee8"
    indicator_ids: list[str] = Field(default_factory=list)
    snapshot: SectorSnapshotConfig = Field(default_factory=SectorSnapshotConfig)


class SectorSummary(BaseModel):
    id: str
    name: str
    short_name: str
    description: str
    accent: str
    indicator_count: int


class SnapshotCard(BaseModel):
    title: str
    value: float | None = None
    value_display: str
    change: float | None = None
    change_display: str | None = None
    unit: str = ""
    decimals: int = 2
    description: str | None = None
    error: str | None = None


class SectorSnapshot(BaseModel):
    sector_id: str
    generated_at: datetime
    cards: list[SnapshotCard]


# ─── AI 智能取数 ───

AIPlanAction = Literal["run", "collect", "clarify", "reject", "not_configured", "error"]


class AIConfigUpdate(BaseModel):
    base_url: str
    model: str
    # Empty means "keep the existing key" when a config is already stored.
    api_key: str = ""


class AIConfigPublic(BaseModel):
    """Never exposes the raw api_key; only whether one is stored."""

    configured: bool
    base_url: str = ""
    model: str = ""
    has_key: bool = False


class AIChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class AIPlanRequest(BaseModel):
    messages: list[AIChatMessage] = Field(default_factory=list)


class AICandidate(BaseModel):
    id: str
    name: str
    level1: str = ""
    description: str = ""


class AIPlanResponse(BaseModel):
    action: AIPlanAction
    reply: str = ""
    indicator_id: str | None = None
    indicator_name: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)
    candidates: list[AICandidate] = Field(default_factory=list)
    # When action == "collect": the core parameters the user still needs to
    # provide, rendered as interactive inputs on the frontend. `params` holds
    # the values the model already auto-filled (or suggested, editable).
    form: list[IndicatorParam] = Field(default_factory=list)
    # Short one-tap replies (e.g. ["港股", "美股"]) rendered as buttons; clicking
    # one sends it back as the next user message. Used for market disambiguation
    # and other quick choices.
    quick_replies: list[str] = Field(default_factory=list)
