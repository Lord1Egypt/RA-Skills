"""Persistent financial model — aggregates, saves, and summarises all connector data."""
import json
import logging
import os
import tempfile
from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from pydantic import BaseModel

from engine.models import (
    Anomaly,
    FinancialRecord,
    FinancialSummary,
    Recommendation,
    SpendCategory,
)
from engine.utils import format_currency, format_percent

logger = logging.getLogger(__name__)

_DEFAULT_STATE_DIR = Path.home() / ".token-economy-intel"
_DEFAULT_STATE_FILE = _DEFAULT_STATE_DIR / "model.json"


class _QueryEntry(BaseModel):
    timestamp: datetime
    query: str


class _ModelState(BaseModel):
    """Serialisable internal state."""

    records: list[FinancialRecord] = []
    connected_accounts: list[str] = []
    query_history: list[_QueryEntry] = []
    last_updated: datetime = datetime(2000, 1, 1)


class FinancialModelManager:
    """Central financial model — loads, updates, persists, and summarises.

    Usage:
        mgr = FinancialModelManager()          # uses default path
        mgr.load()                             # reads JSON (no-op if missing)
        mgr.add_records(records, "openai")     # merge new data
        mgr.save()                             # atomic write
        summary = mgr.get_summary()
    """

    def __init__(self, state_path: str | Path | None = None) -> None:
        self._path = Path(state_path) if state_path else _DEFAULT_STATE_FILE
        self._state = _ModelState()

    # ── Persistence ─────────────────────────────────────────────

    def load(self) -> None:
        """Load state from JSON file. No-op if file doesn't exist."""
        if not self._path.exists():
            logger.info("No existing model at %s — starting fresh", self._path)
            return
        try:
            raw = self._path.read_text(encoding="utf-8")
            self._state = _ModelState.model_validate_json(raw)
            logger.info(
                "Loaded model: %d records, last updated %s",
                len(self._state.records),
                self._state.last_updated.isoformat(),
            )
        except (json.JSONDecodeError, ValueError) as exc:
            logger.error("Corrupt model file %s: %s — starting fresh", self._path, exc)
            self._state = _ModelState()

    def save(self) -> None:
        """Atomic save: write to temp file in the same directory, then rename."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._state.last_updated = datetime.now()

        data = self._state.model_dump_json(indent=2)
        fd, tmp_path = tempfile.mkstemp(
            dir=self._path.parent, suffix=".tmp", prefix=".model_"
        )
        try:
            os.write(fd, data.encode("utf-8"))
            os.close(fd)
            os.replace(tmp_path, self._path)
            logger.info("Saved model to %s (%d records)", self._path, len(self._state.records))
        except OSError:
            os.close(fd) if not os.get_inheritable(fd) else None
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise

    # ── Record management ───────────────────────────────────────

    def add_records(
        self, records: list[FinancialRecord], account_name: str
    ) -> int:
        """Merge new records into the model. Returns count of new records added.

        Deduplicates by (record_date, amount, provider, source, model).
        """
        existing_keys = {_record_key(r) for r in self._state.records}
        new_records = [r for r in records if _record_key(r) not in existing_keys]

        self._state.records.extend(new_records)
        if account_name not in self._state.connected_accounts:
            self._state.connected_accounts.append(account_name)
        self._state.last_updated = datetime.now()

        return len(new_records)

    def record_query(self, query: str) -> None:
        """Track a user query for improving future recommendations."""
        self._state.query_history.append(
            _QueryEntry(timestamp=datetime.now(), query=query)
        )
        # Keep last 200 queries
        if len(self._state.query_history) > 200:
            self._state.query_history = self._state.query_history[-200:]

    @property
    def records(self) -> list[FinancialRecord]:
        return self._state.records

    @property
    def query_history(self) -> list[_QueryEntry]:
        return self._state.query_history

    # ── Summaries ───────────────────────────────────────────────

    def get_summary(self) -> FinancialSummary:
        """Build a FinancialSummary from current state."""
        records = self._state.records
        now = datetime.now()
        thirty_days_ago = (now - timedelta(days=30)).date()

        recent = [r for r in records if r.record_date >= thirty_days_ago]

        # Spend by category (costs are negative)
        spend_by_cat: dict[str, Decimal] = defaultdict(Decimal)
        spend_by_prov: dict[str, Decimal] = defaultdict(Decimal)
        revenue = Decimal("0")
        crypto = Decimal("0")

        for r in recent:
            if r.category == SpendCategory.REVENUE:
                revenue += r.amount
            elif r.category == SpendCategory.CRYPTO_HOLDINGS:
                crypto += r.amount
            else:
                spend_by_cat[r.category.value] += abs(r.amount)
                spend_by_prov[r.provider.value] += abs(r.amount)

        total_spend = sum(spend_by_cat.values())

        # Date coverage
        if records:
            earliest = min(r.record_date for r in records)
            latest = max(r.record_date for r in records)
            coverage_days = (latest - earliest).days + 1
        else:
            coverage_days = 0

        return FinancialSummary(
            last_updated=self._state.last_updated,
            total_monthly_spend=total_spend,
            spend_by_category=dict(spend_by_cat),
            spend_by_provider=dict(spend_by_prov),
            revenue_monthly=revenue if revenue > 0 else None,
            crypto_holdings_usd=crypto if crypto > 0 else None,
            connected_accounts=list(self._state.connected_accounts),
            data_coverage_days=coverage_days,
            record_count=len(records),
        )

    def get_context_for_llm(self) -> str:
        """Return a concise text summary for inclusion in an LLM system prompt."""
        s = self.get_summary()
        lines = [
            "## Token Economy Financial Context",
            f"Last updated: {s.last_updated:%Y-%m-%d %H:%M}",
            f"Data coverage: {s.data_coverage_days} days, {s.record_count} records",
            f"Connected: {', '.join(s.connected_accounts) or 'none'}",
            "",
            f"Monthly spend: {format_currency(s.total_monthly_spend)}",
        ]

        if s.spend_by_category:
            lines.append("Spend by category:")
            for cat, amt in sorted(
                s.spend_by_category.items(), key=lambda x: x[1], reverse=True
            ):
                lines.append(f"  - {cat}: {format_currency(amt)}")

        if s.spend_by_provider:
            lines.append("Spend by provider:")
            for prov, amt in sorted(
                s.spend_by_provider.items(), key=lambda x: x[1], reverse=True
            ):
                lines.append(f"  - {prov}: {format_currency(amt)}")

        if s.revenue_monthly is not None:
            lines.append(f"Monthly revenue: {format_currency(s.revenue_monthly)}")
            if s.total_monthly_spend > 0:
                margin = float(
                    (s.revenue_monthly - s.total_monthly_spend) / s.revenue_monthly * 100
                )
                lines.append(f"Gross margin: {format_percent(margin)}")

        if s.crypto_holdings_usd is not None:
            lines.append(f"Crypto holdings: {format_currency(s.crypto_holdings_usd)}")

        if s.anomalies:
            lines.append(f"Active anomalies: {len(s.anomalies)}")
            for a in s.anomalies[:3]:
                lines.append(f"  - [{a.severity}] {a.description}")

        if s.recommendations:
            lines.append(f"Recommendations: {len(s.recommendations)}")
            for r in s.recommendations[:3]:
                lines.append(f"  - {r.description}")

        return "\n".join(lines)

    # ── Reset ───────────────────────────────────────────────────

    def reset(self) -> None:
        """Clear all state (for testing). Does NOT delete the file."""
        self._state = _ModelState()

    def delete_state_file(self) -> None:
        """Delete the persisted state file (for testing)."""
        if self._path.exists():
            self._path.unlink()


def _record_key(r: FinancialRecord) -> tuple:
    return (r.record_date, r.amount, r.provider, r.source, r.model)
