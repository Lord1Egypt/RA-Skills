"""Tests for SEK price conversion and FX rate handling (issue #81)."""

import pytest
from unittest.mock import patch, MagicMock
from datetime import date

from database_handler import DatabaseHandler
from data_parser import DataParser, DataParser as _DP
from calculate_stats import StatCalculator


# ---------------------------------------------------------------------------
# _to_sek_price: derive SEK per-share price from transaction row
# ---------------------------------------------------------------------------

class TestToSekPrice:
    """Tests for DataParser._to_sek_price static method."""

    def test_buy_with_courtage(self):
        # Buy 10 shares at 100 SEK each, courtage 50 SEK, total = -(1000 + 50)
        row = (date(2023, 1, 1), '1111', 'Köp', 'Asset A',
               10, 100.0, -1050.0, 50.0, 'SEK', 'TESTA',
               1, 'avanza', None)
        # sek_price = (abs(total) - courtage) / amount = (1050 - 50) / 10 = 100
        assert _DP._to_sek_price(row) == 100.0

    def test_sell_with_courtage(self):
        # Sell 5 shares at 150 SEK each, courtage 50 SEK, total = 750 - 50
        row = (date(2023, 1, 1), '1111', 'Sälj', 'Asset A',
               -5, 150.0, 700.0, 50.0, 'SEK', 'TESTA',
               1, 'avanza', None)
        # sek_price = (abs(total) + courtage) / abs(amount) = (700 + 50) / 5 = 150
        assert _DP._to_sek_price(row) == 150.0

    def test_buy_non_sek_derives_from_total(self):
        # Buy 32 units at 8.40 EUR, FX ~11.08, courtage 0
        # total (SEK) = -(8.40 * 32 * 11.08) = -2982.1
        row = (date(2023, 6, 15), '1111', 'Köp', 'EUR Fund',
               32, 8.40, -2982.1, 0.0, 'SEK', 'TESTE',
               1, 'avanza', None)
        # sek_price = 2982.1 / 32 = 93.19...
        result = _DP._to_sek_price(row)
        assert abs(result - 93.19) < 0.01

    def test_total_zero_returns_native(self):
        # Tillgångsinsättning: total = 0, can't derive SEK
        row = (date(2023, 1, 1), '1111', 'Tillgångsinsättning', 'Asset B',
               10, 50.0, 0.0, 0.0, 'SEK', 'TESTB',
               1, 'avanza', None)
        assert _DP._to_sek_price(row) == 50.0

    def test_zero_amount_returns_native(self):
        row = (date(2023, 1, 1), '1111', 'Köp', 'Asset A',
               0, 100.0, 0.0, 0.0, 'SEK', 'TESTA',
               1, 'avanza', None)
        assert _DP._to_sek_price(row) == 100.0

    def test_no_courtage_buy(self):
        row = (date(2023, 1, 1), '1111', 'Köp', 'Asset A',
               10, 100.0, -1000.0, 0.0, 'SEK', 'TESTA',
               1, 'avanza', None)
        assert _DP._to_sek_price(row) == 100.0


# ---------------------------------------------------------------------------
# update_prices: FX conversion for external prices
# ---------------------------------------------------------------------------

class TestUpdatePricesFx:
    """Tests that update_prices converts non-SEK prices and stores FX rates."""

    @patch('requests.get')
    @patch('requests.post')
    def test_non_sek_price_converted_to_sek(self, mock_post, mock_get, tmp_path):
        """A EUR-denominated instrument should have its price converted to SEK."""
        db_file = tmp_path / "test_fx.db"
        db = DatabaseHandler(str(db_file))
        db.connect()
        cur = db.get_cursor()
        cur.execute("INSERT INTO assets (asset, amount) VALUES ('EUR Fund', 10)")
        asset_id = cur.execute("SELECT asset_id FROM assets WHERE asset = 'EUR Fund'").fetchone()[0]
        db.commit()

        def mock_post_side_effect(url, headers=None, json=None, timeout=None):
            resp = MagicMock()
            resp.status_code = 200
            query = json.get("query", "")
            if "EUR Fund" in query:
                resp.json.return_value = {
                    "hits": [{
                        "type": "FUND",
                        "orderBookId": "123",
                        "price": {"last": "8,24", "currency": "EUR"}
                    }]
                }
            elif "EUR/SEK" in query:
                resp.json.return_value = {
                    "hits": [{
                        "type": "INDEX",
                        "subType": "Valuta",
                        "price": {"last": "11,05", "currency": None}
                    }]
                }
            else:
                resp.json.return_value = {"hits": []}
            return resp

        mock_post.side_effect = mock_post_side_effect
        # Block all detail GET requests so we test the search-level price
        mock_get.return_value = MagicMock(status_code=404)

        stat_calc = StatCalculator(db)
        stat_calc.update_prices(force=True)

        # latest_price should be 8.24 * 11.05 = 91.052
        price_row = cur.execute("SELECT latest_price FROM assets WHERE asset_id = ?", (asset_id,)).fetchone()
        assert price_row is not None
        assert abs(price_row[0] - 91.052) < 0.01

        # asset_prices should also have the SEK price
        ap = cur.execute("SELECT price FROM asset_prices WHERE asset_id = ?", (asset_id,)).fetchone()
        assert ap is not None
        assert abs(ap[0] - 91.052) < 0.01

        # exchange_rates should have the EUR rate
        er = cur.execute("SELECT rate FROM exchange_rates WHERE currency = 'EUR'").fetchone()
        assert er is not None
        assert abs(er[0] - 11.05) < 0.001

    @patch('requests.get')
    @patch('requests.post')
    def test_sek_price_not_converted(self, mock_post, mock_get, tmp_path):
        """A SEK-denominated instrument should not have any FX conversion applied."""
        db_file = tmp_path / "test_sek.db"
        db = DatabaseHandler(str(db_file))
        db.connect()
        cur = db.get_cursor()
        cur.execute("INSERT INTO assets (asset, amount) VALUES ('Swedish Stock', 5)")
        asset_id = cur.execute("SELECT asset_id FROM assets WHERE asset = 'Swedish Stock'").fetchone()[0]
        db.commit()

        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {
            "hits": [{
                "type": "STOCK",
                "orderBookId": "5431",
                "price": {"last": "150,00", "currency": "SEK"}
            }]
        }
        mock_post.return_value = resp
        mock_get.return_value = MagicMock(status_code=404)

        stat_calc = StatCalculator(db)
        stat_calc.update_prices(force=True)

        price_row = cur.execute("SELECT latest_price FROM assets WHERE asset_id = ?", (asset_id,)).fetchone()
        assert price_row[0] == 150.0

        # No exchange_rates rows should exist
        er_count = cur.execute("SELECT COUNT(*) FROM exchange_rates").fetchone()[0]
        assert er_count == 0

    @patch('requests.post')
    def test_null_currency_not_converted(self, mock_post, tmp_path):
        """Instruments where price.currency is null should not trigger FX conversion."""
        db_file = tmp_path / "test_null.db"
        db = DatabaseHandler(str(db_file))
        db.connect()
        cur = db.get_cursor()
        cur.execute("INSERT INTO assets (asset, amount) VALUES ('Mystery Fund', 5)")
        asset_id = cur.execute("SELECT asset_id FROM assets WHERE asset = 'Mystery Fund'").fetchone()[0]
        db.commit()

        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {
            "hits": [{
                "type": "FUND",
                "orderBookId": "999",
                "price": {"last": "200,00", "currency": None}
            }]
        }
        mock_post.return_value = resp

        stat_calc = StatCalculator(db)
        stat_calc.update_prices(force=True)

        price_row = cur.execute("SELECT latest_price FROM assets WHERE asset_id = ?", (asset_id,)).fetchone()
        assert price_row[0] == 200.0

    @patch('requests.post')
    def test_multiple_currencies_share_fx_cache(self, mock_post, tmp_path):
        """Two EUR instruments should only trigger one EUR/SEK fetch."""
        db_file = tmp_path / "test_multi_fx.db"
        db = DatabaseHandler(str(db_file))
        db.connect()
        cur = db.get_cursor()
        cur.execute("INSERT INTO assets (asset, amount) VALUES ('EUR Fund A', 10)")
        cur.execute("INSERT INTO assets (asset, amount) VALUES ('EUR Fund B', 5)")
        db.commit()

        fx_call_count = [0]

        def mock_post_side_effect(url, headers=None, json=None, timeout=None):
            resp = MagicMock()
            resp.status_code = 200
            query = json.get("query", "")
            if query.startswith("EUR/SEK"):
                fx_call_count[0] += 1
                resp.json.return_value = {
                    "hits": [{
                        "type": "INDEX",
                        "price": {"last": "11,00", "currency": None}
                    }]
                }
            else:
                resp.json.return_value = {
                    "hits": [{
                        "price": {"last": "10,00", "currency": "EUR"}
                    }]
                }
            return resp

        mock_post.side_effect = mock_post_side_effect

        stat_calc = StatCalculator(db)
        stat_calc.update_prices(force=True)

        # EUR/SEK should only have been fetched once despite two EUR assets
        assert fx_call_count[0] == 1

        # Both assets should have SEK price = 10.00 * 11.00 = 110.00
        prices = cur.execute("SELECT latest_price FROM assets ORDER BY asset").fetchall()
        assert abs(prices[0][0] - 110.0) < 0.01
        assert abs(prices[1][0] - 110.0) < 0.01


# ---------------------------------------------------------------------------
# One-time migration: rebuild transaction-sourced prices to SEK
# ---------------------------------------------------------------------------

class TestSekPriceMigration:
    """Tests that existing native-currency asset_prices rows are rebuilt to SEK."""

    def test_migration_converts_transaction_prices(self, tmp_path):
        """Pre-existing transaction-sourced prices should be converted to SEK."""
        db_file = tmp_path / "test_migration.db"
        db = DatabaseHandler(str(db_file))
        db.connect()
        cur = db.get_cursor()

        # Insert asset
        cur.execute("INSERT INTO assets (asset) VALUES ('Asset A')")
        asset_id = cur.execute("SELECT asset_id FROM assets WHERE asset = 'Asset A'").fetchone()[0]

        # Insert processed transactions
        # Buy: 10 shares at 100 SEK, courtage 50, total = -1050
        cur.execute("""
            INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, processed)
            VALUES ('2023-01-01', '1111', 'Köp', 'Asset A', 10, 100, -1050, 50, 'SEK', 'TESTA', 1)
        """)
        # Sell: -5 shares at 150 SEK, courtage 25, total = 725
        cur.execute("""
            INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, processed)
            VALUES ('2023-01-02', '1111', 'Sälj', 'Asset A', -5, 150, 725, 25, 'SEK', 'TESTA', 1)
        """)

        # Insert NATIVE prices (the bug state) into asset_prices
        cur.execute("INSERT INTO asset_prices (asset_id, price_date, price, source) VALUES (?, '2023-01-01', 100.0, 'transaction')", (asset_id,))
        cur.execute("INSERT INTO asset_prices (asset_id, price_date, price, source) VALUES (?, '2023-01-02', 150.0, 'transaction')", (asset_id,))
        db.commit()

        # Mark migration as NOT done
        cur.execute("DELETE FROM metadata WHERE key = 'sek_prices_migrated'")
        db.commit()

        # Re-run create_tables to trigger migration
        db.create_tables()

        # Check prices were converted to SEK
        prices = cur.execute(
            "SELECT price_date, price FROM asset_prices WHERE asset_id = ? ORDER BY price_date",
            (asset_id,)
        ).fetchall()

        # Buy: (abs(-1050) - 50) / 10 = 100.0 (unchanged since courtage-adjusted total matches)
        assert abs(prices[0][1] - 100.0) < 0.01
        # Sell: (725 + 25) / 5 = 150.0
        assert abs(prices[1][1] - 150.0) < 0.01

        # Migration flag should be set
        flag = cur.execute("SELECT value FROM metadata WHERE key = 'sek_prices_migrated'").fetchone()
        assert flag is not None and flag[0] == '1'

    def test_migration_is_idempotent(self, tmp_path):
        """Running create_tables twice should not re-apply the migration."""
        db_file = tmp_path / "test_idempotent.db"
        db = DatabaseHandler(str(db_file))
        db.connect()
        cur = db.get_cursor()

        cur.execute("INSERT INTO assets (asset) VALUES ('Asset B')")
        asset_id = cur.execute("SELECT asset_id FROM assets WHERE asset = 'Asset B'").fetchone()[0]

        cur.execute("""
            INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, processed)
            VALUES ('2023-03-01', '1111', 'Köp', 'Asset B', 10, 50, -500, 0, 'SEK', 'TESTB', 1)
        """)
        cur.execute("INSERT INTO asset_prices (asset_id, price_date, price, source) VALUES (?, '2023-03-01', 50.0, 'transaction')", (asset_id,))
        db.commit()
        cur.execute("DELETE FROM metadata WHERE key = 'sek_prices_migrated'")
        db.commit()

        # First run: migration applies
        db.create_tables()
        price1 = cur.execute("SELECT price FROM asset_prices WHERE asset_id = ?", (asset_id,)).fetchone()[0]

        # Manually corrupt the price to verify migration doesn't re-run
        cur.execute("UPDATE asset_prices SET price = 999.0 WHERE asset_id = ?", (asset_id,))
        db.commit()

        # Second run: migration should NOT apply (flag already set)
        db.create_tables()
        price2 = cur.execute("SELECT price FROM asset_prices WHERE asset_id = ?", (asset_id,)).fetchone()[0]

        assert price2 == 999.0  # Not overwritten by migration


# ---------------------------------------------------------------------------
# DataParser end-to-end: SEK prices written during transaction processing
# ---------------------------------------------------------------------------

class TestParserSekPrices:
    """Tests that DataParser writes SEK prices to asset_prices during processing."""

    def test_buy_writes_sek_price(self, tmp_path):
        """A buy with courtage should store the courtage-adjusted SEK price."""
        db_file = tmp_path / "test_parser_sek.db"
        csv_file = tmp_path / "test_data.csv"

        csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2023-01-01;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
2023-01-02;1111;Köp;Asset A;10;100;-1050;50;SEK;TESTA;-
"""
        csv_file.write_text(csv_content, encoding="utf-8")

        db = DatabaseHandler(str(db_file))
        parser = DataParser(db)
        parser.add_data(str(csv_file))
        parser.process_transactions()

        db.connect()
        cur = db.get_cursor()

        # SEK price = (abs(-1050) - 50) / 10 = 100.0
        ap = cur.execute("""
            SELECT price FROM asset_prices ap
            JOIN assets a ON ap.asset_id = a.asset_id
            WHERE a.asset = 'Asset A'
        """).fetchone()
        assert ap is not None
        assert abs(ap[0] - 100.0) < 0.01

        # latest_price should also be SEK
        lp = cur.execute("SELECT latest_price FROM assets WHERE asset = 'Asset A'").fetchone()
        assert abs(lp[0] - 100.0) < 0.01

    def test_non_sek_buy_derives_sek_from_total(self, tmp_path):
        """A non-SEK buy should derive the SEK price from the SEK total."""
        db_file = tmp_path / "test_nonsek.db"
        csv_file = tmp_path / "test_data.csv"

        # Buy 32 units at 8.40 EUR, courtage 0, total = -2982.1 SEK (FX ~11.08)
        # sek_price = 2982.1 / 32 = 93.19
        csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2023-06-01;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
2023-06-15;1111;Köp;EUR ETC;32;8,40;-2982,1;0;SEK;TESTE;-
"""
        csv_file.write_text(csv_content, encoding="utf-8")

        db = DatabaseHandler(str(db_file))
        parser = DataParser(db)
        parser.add_data(str(csv_file))
        parser.process_transactions()

        db.connect()
        cur = db.get_cursor()

        ap = cur.execute("""
            SELECT price FROM asset_prices ap
            JOIN assets a ON ap.asset_id = a.asset_id
            WHERE a.asset = 'EUR ETC'
        """).fetchone()
        assert ap is not None
        assert abs(ap[0] - 93.19) < 0.01
