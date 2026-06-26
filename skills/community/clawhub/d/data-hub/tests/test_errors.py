import pytest
from pydantic import ValidationError

from data_hub.errors import (
    format_invalid_namespace_error,
    format_not_found_error,
    format_permission_error,
    format_validation_error,
)
from data_hub.models import MarketDataModel


class TestFormatValidationError:
    def test_contains_field_info(self):
        try:
            MarketDataModel(last_price="bad")
        except ValidationError as e:
            result = format_validation_error(e)
        assert "[VALIDATION_ERROR]" in result
        assert "last_price" in result
        assert "Please fix and retry" in result

    def test_multiple_errors(self):
        try:
            MarketDataModel(last_price=-1, volume_24h=-1)
        except ValidationError as e:
            result = format_validation_error(e)
        assert "[VALIDATION_ERROR]" in result


class TestFormatPermissionError:
    def test_output(self):
        result = format_permission_error("Analyst_Officer", "market_state")
        assert "[PERMISSION_DENIED]" in result
        assert "Analyst_Officer" in result
        assert "Default_Orchestrator" in result


class TestFormatNotFoundError:
    def test_output(self):
        result = format_not_found_error("market_state", "BTC_USDT")
        assert "[NOT_FOUND]" in result
        assert "BTC_USDT" in result


class TestFormatInvalidNamespaceError:
    def test_output(self):
        result = format_invalid_namespace_error("bad_ns")
        assert "[INVALID_NAMESPACE]" in result
        assert "bad_ns" in result
