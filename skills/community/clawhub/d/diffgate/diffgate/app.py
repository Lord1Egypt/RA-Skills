"""
DiffGate API — FastAPI application.

Single endpoint: POST /v1/diff
Compares two texts and returns unified diff with similarity score.
"""

import difflib
from decimal import ROUND_HALF_UP, Decimal

from fastapi import FastAPI

from .models import Change, DiffRequest, DiffResponse

app = FastAPI(
    title="DiffGate API",
    description="Stateless text diff and similarity scoring for AI agents.",
    version="0.1.0",
)


@app.post("/v1/diff", response_model=DiffResponse)
async def diff_texts(request: DiffRequest) -> DiffResponse:
    """Compare two texts and return diff with similarity score."""
    lines_a = request.text_a.splitlines(keepends=True)
    lines_b = request.text_b.splitlines(keepends=True)

    # Compute similarity using SequenceMatcher
    matcher = difflib.SequenceMatcher(None, lines_a, lines_b)
    ratio = matcher.ratio()

    if not lines_a and not lines_b:
        similarity = Decimal("1")
    else:
        similarity = Decimal(str(ratio)).quantize(
            Decimal("0.0001"), rounding=ROUND_HALF_UP
        )

    # Extract changes from unified diff
    changes: list[Change] = []
    additions = 0
    deletions = 0

    for line in difflib.unified_diff(lines_a, lines_b, lineterm=""):
        if line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
            continue
        if line.startswith("+"):
            additions += 1
            changes.append(Change(type="add", content=line[1:]))
        elif line.startswith("-"):
            deletions += 1
            changes.append(Change(type="delete", content=line[1:]))

    return DiffResponse(
        similarity=similarity,
        additions=additions,
        deletions=deletions,
        changes=changes,
    )
