from ..constants import INDICATOR_WINDOW_SIZE


def _validate_indicators(data: dict) -> str | None:
    if not isinstance(data, dict):
        return "[VALIDATION_ERROR] Expected dict for indicators data. Please fix and retry."
    for key, values in data.items():
        if not isinstance(key, str):
            return f"[VALIDATION_ERROR] Indicator key must be string, got {type(key).__name__}. Please fix and retry."
        if not isinstance(values, list):
            return f"[VALIDATION_ERROR] Indicator '{key}' values must be a list, got {type(values).__name__}. Please fix and retry."
        for i, v in enumerate(values):
            if not isinstance(v, (int, float)):
                return f"[VALIDATION_ERROR] Indicator '{key}' value at index {i} must be float, got {type(v).__name__}. Please fix and retry."
    return None


def push(memory: dict, symbol: str, data: dict) -> tuple[dict, str | None]:
    error = _validate_indicators(data)
    if error is not None:
        return memory, error

    indicators = memory.get("indicators", {})
    existing = indicators.get(symbol, {})

    merged = {**existing}
    for key, new_values in data.items():
        old_values = merged.get(key, [])
        combined = [*old_values, *new_values]
        merged[key] = combined[-INDICATOR_WINDOW_SIZE:]

    new_indicators = {**indicators, symbol: merged}
    return {**memory, "indicators": new_indicators}, None


def get(memory: dict, symbol: str) -> dict | None:
    return memory.get("indicators", {}).get(symbol)
