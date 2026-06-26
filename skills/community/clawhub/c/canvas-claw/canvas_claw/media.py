from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from canvas_claw.client import CanvasClawClient
from canvas_claw.errors import CanvasClawError


@dataclass(frozen=True)
class ResolvedMediaInput:
    kind: str
    value: str
    path: Path | None = None


def classify_media_input(raw: str) -> ResolvedMediaInput:
    candidate = raw.strip()
    if candidate.startswith("http://") or candidate.startswith("https://"):
        return ResolvedMediaInput(kind="url", value=candidate)

    path = Path(candidate).expanduser()
    if path.exists() and path.is_file():
        return ResolvedMediaInput(kind="file", value=str(path), path=path)

    raise CanvasClawError(f"Unsupported media input: {raw}")


def materialize_input(client: CanvasClawClient, raw: str, media_type: str) -> str:
    resolved = classify_media_input(raw)
    if resolved.kind == "url":
        return resolved.value
    assert resolved.path is not None
    response = client.materialize_binary(
        media_type=media_type,
        filename=resolved.path.name,
        content=resolved.path.read_bytes(),
        content_type="application/octet-stream",
    )
    public_url = str(response.get("public_url") or "").strip()
    if not public_url:
        raise CanvasClawError("Materialized asset response missing public_url")
    return public_url


def materialize_many(client: CanvasClawClient, values: list[str], media_type: str) -> list[str]:
    return [materialize_input(client, value, media_type) for value in values]
