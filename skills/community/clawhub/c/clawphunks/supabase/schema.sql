-- ClawPhunks Database Schema

-- ============================================================================
-- ITEMS: All 10k phunks with their pre-built data URIs
-- ============================================================================

CREATE TABLE IF NOT EXISTS items (
  token_id INTEGER PRIMARY KEY,
  data_uri TEXT NOT NULL,
  minted BOOLEAN DEFAULT FALSE,
  minted_to TEXT,
  tx_hash TEXT,
  minted_at TIMESTAMPTZ,
  traits JSONB,

  CONSTRAINT valid_token_id CHECK (token_id >= 0 AND token_id < 10000)
);

CREATE INDEX idx_items_unminted ON items(token_id) WHERE minted = FALSE;
CREATE INDEX idx_items_minted_to ON items(minted_to) WHERE minted = TRUE;

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Get a random unminted item and lock it
CREATE OR REPLACE FUNCTION claim_random_item(recipient TEXT)
RETURNS TABLE(token_id INTEGER, data_uri TEXT) AS $$
DECLARE
  item RECORD;
BEGIN
  SELECT i.token_id, i.data_uri INTO item
  FROM items i
  WHERE i.minted = FALSE
  ORDER BY RANDOM()
  LIMIT 1
  FOR UPDATE SKIP LOCKED;

  IF item IS NULL THEN
    RAISE EXCEPTION 'No items available';
  END IF;

  UPDATE items SET minted = TRUE, minted_to = recipient, minted_at = NOW()
  WHERE items.token_id = item.token_id;

  RETURN QUERY SELECT item.token_id, item.data_uri;
END;
$$ LANGUAGE plpgsql;

-- Mark item as minted with tx hash
CREATE OR REPLACE FUNCTION finalize_mint(p_token_id INTEGER, p_tx_hash TEXT)
RETURNS VOID AS $$
BEGIN
  UPDATE items SET tx_hash = p_tx_hash WHERE token_id = p_token_id;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- RLS
-- ============================================================================

ALTER TABLE items ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read items" ON items FOR SELECT USING (true);
CREATE POLICY "Service write items" ON items FOR ALL USING (true) WITH CHECK (true);
