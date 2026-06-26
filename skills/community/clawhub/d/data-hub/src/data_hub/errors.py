from pydantic import ValidationError

from .constants import WRITE_PERMISSIONS


def format_validation_error(error: ValidationError) -> str:
    details = []
    for e in error.errors():
        field = ".".join(str(loc) for loc in e["loc"])
        msg = e["msg"]
        details.append(f"field '{field}': {msg}")
    joined = "; ".join(details)
    return f"[VALIDATION_ERROR] {joined}. Please fix and retry."


def format_permission_error(agent_id: str, namespace: str) -> str:
    expected = WRITE_PERMISSIONS.get(namespace, "unknown")
    return (
        f"[PERMISSION_DENIED] Agent '{agent_id}' is not authorized to write to "
        f"'{namespace}'. Only '{expected}' can write here."
    )


def format_not_found_error(namespace: str, key: str) -> str:
    return f"[NOT_FOUND] No data found for key '{key}' in namespace '{namespace}'."


def format_invalid_namespace_error(namespace: str) -> str:
    return f"[INVALID_NAMESPACE] '{namespace}' is not a valid namespace."
