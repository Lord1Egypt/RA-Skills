"""
Tests for the annual fee renewal tracker:
  - db.get_renewal_schedule()
  - CLI: fleece cards fee-date
  - CLI: fleece cards renewal
  - CLI: fleece cards add --fee-date
"""
import datetime
import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from cli import app

runner = CliRunner()


# ---------------------------------------------------------------------------
# Fixture: isolated temp database
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    """Point db.DB_PATH at a fresh temp file for each test."""
    import db
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test_fleece.db")
    db.init_db()
    return tmp_path / "test_fleece.db"


def _add_card(name: str, annual_fee: str = "$95", fee_date: str = "") -> None:
    import db, datetime
    db.add_card({
        "name": name,
        "annual_fee": annual_fee,
        "date_added": datetime.date.today().isoformat(),
        "fee_date": fee_date,
    })


# ===========================================================================
# db.get_renewal_schedule()
# ===========================================================================

class TestGetRenewalSchedule:
    def test_empty_when_no_cards(self):
        import db
        assert db.get_renewal_schedule() == []

    def test_empty_when_no_fee_dates_set(self):
        import db
        _add_card("Amex Gold")
        assert db.get_renewal_schedule() == []

    def test_returns_card_with_fee_date(self):
        import db
        # Use a future date guaranteed to be in the future
        future = (datetime.date.today() + datetime.timedelta(days=30)).strftime("%m-%d")
        _add_card("Chase Sapphire Preferred", fee_date=future)
        schedule = db.get_renewal_schedule()
        assert len(schedule) == 1
        assert schedule[0]["name"] == "Chase Sapphire Preferred"
        assert schedule[0]["days_until"] == 30

    def test_past_date_rolls_to_next_year(self):
        import db
        # Use yesterday's MM-DD — should roll forward ~365 days
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m-%d")
        _add_card("Amex Platinum", fee_date=yesterday)
        schedule = db.get_renewal_schedule()
        assert len(schedule) == 1
        assert schedule[0]["days_until"] >= 364

    def test_sorted_ascending_by_days(self):
        import db
        today = datetime.date.today()
        soon = (today + datetime.timedelta(days=10)).strftime("%m-%d")
        later = (today + datetime.timedelta(days=60)).strftime("%m-%d")
        _add_card("Card A", fee_date=later)
        _add_card("Card B", fee_date=soon)
        schedule = db.get_renewal_schedule()
        assert schedule[0]["name"] == "Card B"
        assert schedule[1]["name"] == "Card A"
        assert schedule[0]["days_until"] < schedule[1]["days_until"]

    def test_skips_cards_without_fee_date(self):
        import db
        future = (datetime.date.today() + datetime.timedelta(days=20)).strftime("%m-%d")
        _add_card("Card With Date", fee_date=future)
        _add_card("Card No Date")
        schedule = db.get_renewal_schedule()
        assert len(schedule) == 1
        assert schedule[0]["name"] == "Card With Date"

    def test_next_renewal_is_iso_date_string(self):
        import db
        future = (datetime.date.today() + datetime.timedelta(days=15)).strftime("%m-%d")
        _add_card("Citi Double Cash", fee_date=future)
        schedule = db.get_renewal_schedule()
        # Should be parseable as an ISO date
        datetime.date.fromisoformat(schedule[0]["next_renewal"])


# ===========================================================================
# CLI: cards fee-date
# ===========================================================================

class TestCardsFeeDate:
    def test_sets_fee_date(self):
        _add_card("Amex Gold")
        result = runner.invoke(app, ["cards", "fee-date", "Amex Gold", "03-15"])
        assert result.exit_code == 0
        assert "Amex Gold" in result.output
        assert "03-15" in result.output

    def test_partial_name_match(self):
        _add_card("Chase Sapphire Preferred")
        result = runner.invoke(app, ["cards", "fee-date", "sapphire", "06-01"])
        assert result.exit_code == 0
        assert "Chase Sapphire Preferred" in result.output

    def test_ambiguous_match_exits_1(self):
        _add_card("Chase Sapphire Preferred")
        _add_card("Chase Sapphire Reserve")
        result = runner.invoke(app, ["cards", "fee-date", "sapphire", "06-01"])
        assert result.exit_code == 1

    def test_no_match_exits_1(self):
        result = runner.invoke(app, ["cards", "fee-date", "nonexistent", "01-01"])
        assert result.exit_code == 1

    def test_invalid_format_exits_1(self):
        _add_card("Amex Gold")
        result = runner.invoke(app, ["cards", "fee-date", "Amex Gold", "January 15"])
        assert result.exit_code == 1

    def test_invalid_date_value_exits_1(self):
        _add_card("Amex Gold")
        result = runner.invoke(app, ["cards", "fee-date", "Amex Gold", "99-99"])
        assert result.exit_code == 1

    def test_json_output(self):
        _add_card("Amex Gold")
        result = runner.invoke(app, ["cards", "fee-date", "Amex Gold", "01-15", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["ok"] is True
        assert data["fee_date"] == "01-15"
        assert data["card"] == "Amex Gold"

    def test_date_persisted_in_db(self):
        import db
        _add_card("Citi Double Cash")
        runner.invoke(app, ["cards", "fee-date", "Citi Double Cash", "07-20"])
        card = db.get_card("Citi Double Cash")
        assert card["fee_date"] == "07-20"


# ===========================================================================
# CLI: cards renewal
# ===========================================================================

class TestCardsRenewal:
    def test_no_cards_shows_empty_message(self):
        result = runner.invoke(app, ["cards", "renewal"])
        assert result.exit_code == 0
        assert "No cards" in result.output

    def test_card_without_fee_date_appears_in_no_date_list(self):
        _add_card("Amex Gold")
        result = runner.invoke(app, ["cards", "renewal"])
        assert result.exit_code == 0
        assert "Amex Gold" in result.output
        assert "fee date" in result.output.lower()

    def test_card_with_fee_date_appears_in_schedule(self):
        future = (datetime.date.today() + datetime.timedelta(days=45)).strftime("%m-%d")
        _add_card("Chase Sapphire Preferred", fee_date=future)
        result = runner.invoke(app, ["cards", "renewal"])
        assert result.exit_code == 0
        assert "Chase Sapphire Preferred" in result.output
        assert "45d" in result.output

    def test_days_filter_excludes_far_renewals(self):
        future = (datetime.date.today() + datetime.timedelta(days=90)).strftime("%m-%d")
        _add_card("Amex Gold", fee_date=future)
        result = runner.invoke(app, ["cards", "renewal", "--days", "30"])
        assert result.exit_code == 0
        assert "No upcoming renewals" in result.output

    def test_days_filter_includes_near_renewals(self):
        future = (datetime.date.today() + datetime.timedelta(days=20)).strftime("%m-%d")
        _add_card("Amex Gold", fee_date=future)
        result = runner.invoke(app, ["cards", "renewal", "--days", "30"])
        assert result.exit_code == 0
        assert "Amex Gold" in result.output

    def test_json_output_shape(self):
        future = (datetime.date.today() + datetime.timedelta(days=10)).strftime("%m-%d")
        _add_card("Citi Double Cash", fee_date=future)
        _add_card("Capital One Venture")
        result = runner.invoke(app, ["cards", "renewal", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["ok"] is True
        assert data["command"] == "renewal"
        assert len(data["schedule"]) == 1
        assert data["schedule"][0]["name"] == "Citi Double Cash"
        assert "no_date_set" in data
        assert "Capital One Venture" in data["no_date_set"]

    def test_schedule_sorted_by_days_ascending(self):
        today = datetime.date.today()
        soon  = (today + datetime.timedelta(days=5)).strftime("%m-%d")
        later = (today + datetime.timedelta(days=50)).strftime("%m-%d")
        _add_card("Card Soon",  fee_date=soon)
        _add_card("Card Later", fee_date=later)
        result = runner.invoke(app, ["cards", "renewal", "--json"])
        data = json.loads(result.output)
        names = [c["name"] for c in data["schedule"]]
        assert names == ["Card Soon", "Card Later"]


# ===========================================================================
# CLI: cards add --fee-date
# ===========================================================================

class TestCardsAddWithFeeDate:
    def test_add_with_fee_date_stores_it(self):
        import db
        result = runner.invoke(app, [
            "cards", "add", "Amex Platinum", "--fee", "$695", "--fee-date", "02-28"
        ])
        assert result.exit_code == 0
        card = db.get_card("Amex Platinum")
        assert card["fee_date"] == "02-28"

    def test_add_without_fee_date_stores_empty(self):
        import db
        result = runner.invoke(app, ["cards", "add", "Citi Double Cash"])
        assert result.exit_code == 0
        card = db.get_card("Citi Double Cash")
        assert card["fee_date"] == ""
