"""Tests for the product cache."""

from inventory import store


def test_cached_lookup_reads_catalog_once(monkeypatch):
    """A repeated lookup is served from the cache."""
    reads = []

    def fake_read(sku):
        """Record each slow-path read and return a fixed product."""
        reads.append(sku)
        return {"name": "Lamp", "price_cents": 1999}

    monkeypatch.setattr(store, "_read_catalog_entry", fake_read)
    store._cache.clear()
    first = store.load_product("A1", 100.0)
    second = store.load_product("A1", 100.0)
    assert first == second
    assert reads == ["A1"]
