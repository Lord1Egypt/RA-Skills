-- Backfill mortgage defaults: 20% down, 4% annual rate, 25-year amortization.
-- mortgage_monthly is recomputed separately via sqlite3 CLI (exp/ln not
-- available through sqlx's SQLite connection).
UPDATE listings
SET
    down_payment_pct       = 0.20,
    mortgage_interest_rate = 0.04,
    amortization_years     = COALESCE(amortization_years, 25);
