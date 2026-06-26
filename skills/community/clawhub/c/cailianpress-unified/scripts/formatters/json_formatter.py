"""JSON output formatter for CLS query results."""

from cls_service import ClsQueryResult


def format_as_json(result: ClsQueryResult) -> str:
    """Return raw dict for JSON serialization."""
    return result.to_dict()
