-- Mortgage calculation parameters per listing.
-- Defaults (20 % down, 5 % annual rate, 25-year amortisation) are applied by
-- the backend at save/refresh time; users can override them via the edit UI.
ALTER TABLE listings ADD COLUMN down_payment_pct       REAL;
ALTER TABLE listings ADD COLUMN mortgage_interest_rate REAL;
ALTER TABLE listings ADD COLUMN amortization_years     INTEGER;
