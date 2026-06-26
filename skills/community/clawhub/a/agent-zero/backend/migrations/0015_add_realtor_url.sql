-- Rename `url` to `redfin_url` (making it nullable so realtor-only listings
-- can exist without a Redfin URL) and add `realtor_url`.
-- SQLite cannot ALTER a column's NOT NULL constraint, so we recreate the table.
--
-- Strategy: save child table data, drop children, recreate listings, restore children.

-- 1. Save child table rows to temp tables
CREATE TEMPORARY TABLE tmp_images AS SELECT * FROM images_cache;
CREATE TEMPORARY TABLE tmp_history AS SELECT * FROM listing_history;

-- 2. Drop children (removes FK references to listings)
DROP TABLE images_cache;
DROP TABLE listing_history;

-- 3. Recreate listings with new schema
CREATE TABLE listings_v2 (
    id                       INTEGER PRIMARY KEY AUTOINCREMENT,
    redfin_url               TEXT UNIQUE,
    realtor_url              TEXT,
    title                    TEXT NOT NULL DEFAULT '',
    description              TEXT NOT NULL DEFAULT '',
    price                    INTEGER,
    price_currency           TEXT,
    street_address           TEXT,
    city                     TEXT,
    region                   TEXT,
    postal_code              TEXT,
    country                  TEXT,
    bedrooms                 INTEGER,
    bathrooms                INTEGER,
    sqft                     INTEGER,
    year_built               INTEGER,
    lat                      REAL,
    lon                      REAL,
    created_at               TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at               TEXT,
    notes                    TEXT,
    parking_garage           INTEGER,
    parking_covered          INTEGER,
    parking_open             INTEGER,
    land_sqft                INTEGER,
    property_tax             INTEGER,
    skytrain_station         TEXT,
    skytrain_walk_min        INTEGER,
    radiant_floor_heating    INTEGER,
    ac                       INTEGER,
    hoa_monthly              INTEGER,
    monthly_total            INTEGER,
    has_rental_suite         INTEGER,
    rental_income            INTEGER,
    status                   TEXT,
    nickname                 TEXT,
    school_elementary        TEXT,
    school_elementary_rating REAL,
    school_middle            TEXT,
    school_middle_rating     REAL,
    school_secondary         TEXT,
    school_secondary_rating  REAL,
    down_payment_pct         REAL,
    mortgage_interest_rate   REAL,
    amortization_years       INTEGER,
    mortgage_monthly         INTEGER
);

INSERT INTO listings_v2 (
    id, redfin_url, realtor_url,
    title, description,
    price, price_currency,
    street_address, city, region, postal_code, country,
    bedrooms, bathrooms, sqft, year_built,
    lat, lon,
    created_at, updated_at, notes,
    parking_garage, parking_covered, parking_open, land_sqft, property_tax,
    skytrain_station, skytrain_walk_min, radiant_floor_heating, ac,
    hoa_monthly, monthly_total, has_rental_suite, rental_income,
    status, nickname,
    school_elementary, school_elementary_rating,
    school_middle, school_middle_rating,
    school_secondary, school_secondary_rating,
    down_payment_pct, mortgage_interest_rate, amortization_years, mortgage_monthly
)
SELECT
    id, url, NULL,
    title, description,
    price, price_currency,
    street_address, city, region, postal_code, country,
    bedrooms, bathrooms, sqft, year_built,
    lat, lon,
    created_at, updated_at, notes,
    parking_garage, parking_covered, parking_open, land_sqft, property_tax,
    skytrain_station, skytrain_walk_min, radiant_floor_heating, ac,
    hoa_monthly, monthly_total, has_rental_suite, rental_income,
    status, nickname,
    school_elementary, school_elementary_rating,
    school_middle, school_middle_rating,
    school_secondary, school_secondary_rating,
    down_payment_pct, mortgage_interest_rate, amortization_years, mortgage_monthly
FROM listings;

DROP TABLE listings;
ALTER TABLE listings_v2 RENAME TO listings;

-- Partial unique index so multiple NULL realtor_urls are allowed but
-- two rows cannot share the same non-NULL realtor.ca URL.
CREATE UNIQUE INDEX idx_listings_realtor_url
    ON listings(realtor_url) WHERE realtor_url IS NOT NULL;

-- 4. Recreate child tables
CREATE TABLE images_cache (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id    INTEGER NOT NULL REFERENCES listings(id),
    source_url    TEXT    NOT NULL,
    sha256        TEXT,
    phash         INTEGER,
    local_path    TEXT,
    position      INTEGER NOT NULL DEFAULT 0,
    created_at    TEXT,
    UNIQUE(listing_id, source_url)
);

CREATE TABLE listing_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id  INTEGER NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
    field_name  TEXT NOT NULL,
    old_value   TEXT,
    new_value   TEXT,
    changed_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_listing_history_listing_id ON listing_history(listing_id);

-- 5. Restore child table data
INSERT INTO images_cache SELECT * FROM tmp_images;
INSERT INTO listing_history SELECT * FROM tmp_history;

DROP TABLE tmp_images;
DROP TABLE tmp_history;
