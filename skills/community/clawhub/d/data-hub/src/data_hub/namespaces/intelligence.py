from pydantic import ValidationError

from ..errors import format_validation_error
from ..models import IntelligenceModel


def push(memory: dict, symbol: str, data: dict) -> tuple[dict, str | None]:
    try:
        validated = IntelligenceModel(**data)
    except ValidationError as e:
        return memory, format_validation_error(e)

    intel = memory.get("intelligence", {})
    new_intel = {**intel, symbol: validated.model_dump()}
    return {**memory, "intelligence": new_intel}, None


def get(memory: dict, symbol: str) -> dict | None:
    return memory.get("intelligence", {}).get(symbol)
