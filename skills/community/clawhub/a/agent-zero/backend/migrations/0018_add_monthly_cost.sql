-- Derived monthly cost based on initial monthly mortgage interest
-- + monthly property tax + HOA/strata.
ALTER TABLE listings ADD COLUMN monthly_cost INTEGER;
