"""
FormatGate API — FastAPI application.

Single endpoint: POST /v1/convert
Converts between JSON, YAML, and TOML formats.
"""

import json
from typing import Any

import tomllib
import yaml
from fastapi import FastAPI

from .models import ConvertRequest, ConvertResponse

app = FastAPI(
    title="FormatGate API",
    description="JSON, YAML, and TOML format conversion for AI agents.",
    version="0.1.0",
)


def _parse(content: str, fmt: str) -> Any:
    """Parse content from the given format."""
    if fmt == "json":
        return json.loads(content)
    elif fmt == "yaml":
        return yaml.safe_load(content)
    elif fmt == "toml":
        return tomllib.loads(content)
    raise ValueError(f"Unsupported format: {fmt}")


def _serialize(data: Any, fmt: str) -> str:
    """Serialize data to the given format."""
    if fmt == "json":
        return json.dumps(data, indent=2, default=str)
    elif fmt == "yaml":
        return yaml.dump(data, default_flow_style=False, sort_keys=False)
    elif fmt == "toml":
        # tomllib is read-only in stdlib; use a simple TOML writer
        return _to_toml(data)
    raise ValueError(f"Unsupported format: {fmt}")


def _to_toml(data: Any, prefix: str = "") -> str:
    """Simple TOML serializer for flat/nested dicts."""
    lines: list[str] = []
    tables: list[tuple[str, dict]] = []

    if not isinstance(data, dict):
        raise ValueError("TOML requires a top-level table (dict)")

    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            tables.append((full_key, value))
        elif isinstance(value, list):
            items = ", ".join(json.dumps(v) for v in value)
            lines.append(f"{key} = [{items}]")
        elif isinstance(value, bool):
            lines.append(f"{key} = {str(value).lower()}")
        elif isinstance(value, (int, float)):
            lines.append(f"{key} = {value}")
        elif isinstance(value, str):
            lines.append(f'{key} = {json.dumps(value)}')
        else:
            lines.append(f'{key} = {json.dumps(str(value))}')

    for table_key, table_data in tables:
        lines.append(f"\n[{table_key}]")
        lines.append(_to_toml(table_data, prefix=table_key))

    return "\n".join(lines)


@app.post("/v1/convert", response_model=ConvertResponse)
async def convert(request: ConvertRequest) -> ConvertResponse:
    """Convert content between JSON, YAML, and TOML."""
    try:
        data = _parse(request.content, request.input_format)
        result = _serialize(data, request.output_format)
        return ConvertResponse(
            success=True,
            result=result,
            input_format=request.input_format,
            output_format=request.output_format,
        )
    except Exception as e:
        return ConvertResponse(
            success=False,
            error=str(e),
            input_format=request.input_format,
            output_format=request.output_format,
        )
