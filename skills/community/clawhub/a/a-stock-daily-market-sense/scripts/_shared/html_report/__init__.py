"""Project-wide HTML report renderer.

Skills produce a Markdown research note and an optional JSON evidence pack,
then call ``HtmlReportBuilder`` to wrap them in a self-contained HTML page
with a chosen style theme. Domain charts (valuation bands, K-lines, …) are
contributed by each skill as ``ChartHook`` payloads + JS bodies that draw
themselves using the shared chart kit (``window.CK``).

The thin per-skill entrypoint is built from three reusable pieces:
- ``render_report`` / ``RenderJob`` — the shared CLI orchestration.
- ``PillDecoration`` / ``HeroDecoration`` — data-driven UI decorations.
- ``ChartHook`` + ``window.CK`` (chart kit) — chart contributions.
"""

from .builder import HtmlReportBuilder, list_themes
from .chart_hook import ChartHook
from .chartkit import chartkit_js
from .cli import RenderJob, render_report
from .decorations import (
    CollapsibleUpdatesDecoration,
    HeroDecoration,
    PillDecoration,
    TimelineDecoration,
)
from .markdown_engine import render_markdown
from .text_validator import validate_text_preserved

__all__ = [
    "HtmlReportBuilder",
    "ChartHook",
    "RenderJob",
    "render_report",
    "PillDecoration",
    "HeroDecoration",
    "CollapsibleUpdatesDecoration",
    "TimelineDecoration",
    "chartkit_js",
    "list_themes",
    "render_markdown",
    "validate_text_preserved",
]
