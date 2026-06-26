import asyncio
import time

from .constants import (
    NAMESPACE_INDICATORS,
    NAMESPACE_INTELLIGENCE,
    NAMESPACE_MARKET_STATE,
    NAMESPACE_RISK_AUDIT,
    RISK_AUDIT_KEY,
    VALID_NAMESPACES,
    WRITE_PERMISSIONS,
)
from .errors import (
    format_invalid_namespace_error,
    format_not_found_error,
    format_permission_error,
)
from .janitor import expire_intelligence, mark_stale_market_data
from .namespaces import indicators, intelligence, market_state, risk_audit


class DataHub:
    def __init__(self, snapshot_path: str | None = None):
        self._memory: dict = {
            NAMESPACE_MARKET_STATE: {},
            NAMESPACE_INDICATORS: {},
            NAMESPACE_INTELLIGENCE: {},
            NAMESPACE_RISK_AUDIT: {},
        }
        self._lock = asyncio.Lock()
        self._snapshot_path = snapshot_path

    async def push_data(
        self, agent_id: str, category: str, key: str, data: dict
    ) -> dict:
        if category not in VALID_NAMESPACES:
            return {"success": False, "error": format_invalid_namespace_error(category)}

        expected_agent = WRITE_PERMISSIONS[category]
        if agent_id != expected_agent:
            return {"success": False, "error": format_permission_error(agent_id, category)}

        async with self._lock:
            new_memory, error = self._do_push(category, key, data)

        if error is not None:
            return {"success": False, "error": error}

        self._memory = new_memory

        if category == NAMESPACE_RISK_AUDIT and self._snapshot_path:
            snapshot_data = new_memory.get(NAMESPACE_RISK_AUDIT, {}).get(RISK_AUDIT_KEY)
            if snapshot_data is not None:
                snapshot_err = risk_audit.save_snapshot(snapshot_data, self._snapshot_path)
                if snapshot_err is not None:
                    return {"success": True, "warning": snapshot_err}

        return {"success": True}

    async def get_data(self, category: str, key: str) -> dict:
        if category not in VALID_NAMESPACES:
            return {"success": False, "error": format_invalid_namespace_error(category)}

        async with self._lock:
            data = self._do_get(category, key)

        if data is None:
            return {"success": False, "error": format_not_found_error(category, key)}

        return {"success": True, "data": data}

    async def get_summary(self) -> dict:
        now = time.time()

        async with self._lock:
            cleaned_memory = self._clean(now)
            self._memory = cleaned_memory
            summary = {
                NAMESPACE_MARKET_STATE: {**cleaned_memory[NAMESPACE_MARKET_STATE]},
                NAMESPACE_INDICATORS: {**cleaned_memory[NAMESPACE_INDICATORS]},
                NAMESPACE_INTELLIGENCE: {**cleaned_memory[NAMESPACE_INTELLIGENCE]},
                NAMESPACE_RISK_AUDIT: {**cleaned_memory[NAMESPACE_RISK_AUDIT]},
            }

        return {"success": True, "data": summary}

    def _do_push(self, category: str, key: str, data: dict) -> tuple[dict, str | None]:
        if category == NAMESPACE_MARKET_STATE:
            return market_state.push(self._memory, key, data)
        if category == NAMESPACE_INDICATORS:
            return indicators.push(self._memory, key, data)
        if category == NAMESPACE_INTELLIGENCE:
            return intelligence.push(self._memory, key, data)
        if category == NAMESPACE_RISK_AUDIT:
            return risk_audit.push(self._memory, data)
        return self._memory, format_invalid_namespace_error(category)

    def _do_get(self, category: str, key: str) -> dict | None:
        if category == NAMESPACE_MARKET_STATE:
            return market_state.get(self._memory, key)
        if category == NAMESPACE_INDICATORS:
            return indicators.get(self._memory, key)
        if category == NAMESPACE_INTELLIGENCE:
            return intelligence.get(self._memory, key)
        if category == NAMESPACE_RISK_AUDIT:
            return risk_audit.get(self._memory)
        return None

    def _clean(self, now: float) -> dict:
        cleaned_market = {
            symbol: mark_stale_market_data(data, now)
            for symbol, data in self._memory[NAMESPACE_MARKET_STATE].items()
        }
        cleaned_intel = {
            symbol: expire_intelligence(data, now)
            for symbol, data in self._memory[NAMESPACE_INTELLIGENCE].items()
        }
        return {
            **self._memory,
            NAMESPACE_MARKET_STATE: cleaned_market,
            NAMESPACE_INTELLIGENCE: cleaned_intel,
        }
