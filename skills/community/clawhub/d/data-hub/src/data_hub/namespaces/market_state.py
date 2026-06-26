from pydantic import ValidationError

from ..errors import format_validation_error
from ..models import MarketDataModel


def push(memory: dict, symbol: str, data: dict) -> tuple[dict, str | None]:
    try:
        validated = MarketDataModel(**data)
    except ValidationError as e:
        return memory, format_validation_error(e)

    market = memory.get("market_state", {})
    new_market = {**market, symbol: validated.model_dump()}
    return {**memory, "market_state": new_market}, None


def get(memory: dict, symbol: str) -> dict | None:
    return memory.get("market_state", {}).get(symbol)
