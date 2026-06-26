#!/usr/bin/env python3
"""TRE Validation — Smoke test after install."""
import sys
from pathlib import Path

# Add installed dir to path
sys.path.insert(0, str(Path(__file__).parent))

def test_import():
    try:
        from tre import cache_answer, get_cached_answer, get_metrics, clear_cache
        print("✓ Import successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_cache_roundtrip():
    from tre import cache_answer, get_cached_answer, clear_cache

    clear_cache()

    # Cache a clean answer
    r1 = cache_answer("test query", "test answer")
    assert r1["cached"] == True, f"Should cache clean answer: {r1}"
    print("✓ Clean answer cached")

    # Retrieve it
    cached = get_cached_answer("test query")
    assert cached is not None, "Should retrieve cached answer"
    assert cached[0] == "test answer", f"Wrong answer: {cached[0]}"
    print("✓ Cache hit retrieves correct answer")

    # Flagged answer not cached
    r2 = cache_answer("uncertain query", "I think maybe possibly it is 4")
    assert r2["cached"] == False, f"Should NOT cache flagged: {r2}"
    assert r2["flagged"] == True, f"Should flag uncertain: {r2}"
    print("✓ Uncertain answer flagged (not cached)")

def test_metrics():
    from tre import get_metrics, clear_cache
    clear_cache()

    m = get_metrics()
    assert "cache_hits" in m
    assert "cache_hit_rate_percent" in m
    print(f"✓ Metrics: {m}")

def main():
    print("Token Reduction Engine — Validation\n")
    ok = test_import()
    if not ok:
        sys.exit(1)

    test_cache_roundtrip()
    test_metrics()

    print("\n✅ All validation passed")

if __name__ == "__main__":
    main()
