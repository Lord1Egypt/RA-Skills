#!/usr/bin/env python3
"""
DeckCraft v5.2 — Input Validation Tests

Tests that DeckEngine rejects invalid inputs with friendly error messages.

Run:
    python3 tests/test_validation.py
"""
import sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import DeckEngine  # noqa: E402


def expect_raises(callable_, exc_type, description):
    """Helper: verify a callable raises an expected exception type."""
    try:
        callable_()
    except exc_type as e:
        print(f"  ✓ {description}: {type(e).__name__}: {str(e)[:80]}")
        return True
    except Exception as e:
        print(f"  ✗ {description}: expected {exc_type.__name__}, got {type(e).__name__}: {e}")
        return False
    print(f"  ✗ {description}: expected {exc_type.__name__}, but NO exception was raised")
    return False


def main():
    passed = 0
    total = 0

    print("=" * 70)
    print("DeckCraft — Input Validation Tests")
    print("=" * 70)

    # ── __init__ validation ─────────────────────────────────────
    print("\n[__init__]")
    total += 1
    if expect_raises(lambda: DeckEngine(theme_name="nonexistent"), ValueError,
                     "Invalid theme name rejected"):
        passed += 1
    total += 1
    if expect_raises(lambda: DeckEngine(canvas="nonexistent"), ValueError,
                     "Invalid canvas name rejected"):
        passed += 1
    total += 1
    if expect_raises(lambda: DeckEngine(theme_name=""), ValueError,
                     "Empty theme name rejected"):
        passed += 1
    total += 1
    if expect_raises(lambda: DeckEngine(canvas=""), ValueError,
                     "Empty canvas name rejected"):
        passed += 1

    # ── cover() validation ───────────────────────────────────────
    print("\n[cover]")
    eng = DeckEngine()
    total += 1
    if expect_raises(lambda: eng.cover(title=""), ValueError,
                     "Empty title rejected"):
        passed += 1
    total += 1
    if expect_raises(lambda: eng.cover(title=None), ValueError,
                     "None title rejected"):
        passed += 1
    total += 1
    if expect_raises(lambda: eng.cover(title=123), TypeError,
                     "Non-str title rejected"):
        passed += 1
    total += 1
    if expect_raises(lambda: eng.cover(title="x" * 300), ValueError,
                     "Too-long title rejected"):
        passed += 1

    # ── content() validation ─────────────────────────────────────
    print("\n[content]")
    eng = DeckEngine()
    total += 1
    if expect_raises(lambda: eng.content(title="T", bullets=[]), ValueError,
                     "Empty bullets rejected"):
        passed += 1
    total += 1
    if expect_raises(lambda: eng.content(title="T", bullets=["a"] * 30), ValueError,
                     "Too many bullets rejected"):
        passed += 1
    total += 1
    if expect_raises(lambda: eng.content(title="T", bullets="not a list"), TypeError,
                     "Non-list bullets rejected"):
        passed += 1
    total += 1
    if expect_raises(lambda: eng.content(title="T", bullets=["a", 123]), TypeError,
                     "Non-str bullet item rejected"):
        passed += 1

    # ── summary() validation ─────────────────────────────────────
    print("\n[summary]")
    eng = DeckEngine()
    total += 1
    if expect_raises(lambda: eng.summary(title="T", key_points=[]), ValueError,
                     "Empty key_points rejected"):
        passed += 1
    total += 1
    if expect_raises(lambda: eng.summary(title="T", key_points=["a"] * 20), ValueError,
                     "Too many key_points rejected"):
        passed += 1

    # ── closing() validation ─────────────────────────────────────
    print("\n[closing]")
    eng = DeckEngine()
    total += 1
    if expect_raises(lambda: eng.closing(title=None), ValueError,
                     "None title (when explicitly None) rejected"):
        passed += 1

    # ── save() validation ────────────────────────────────────────
    print("\n[save]")
    eng = DeckEngine()
    eng.cover(title="T")
    total += 1
    if expect_raises(lambda: eng.save(123), TypeError,
                     "Non-str path rejected"):
        passed += 1
    total += 1
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        eng.save("/tmp/no_extension_test_file")
        if w and "should end with .pptx" in str(w[0].message):
            print(f"  ✓ Non-.pptx extension warned: {w[0].message}")
            passed += 1
        else:
            print(f"  ✗ Non-.pptx extension should warn, got: {[str(x.message) for x in w]}")
    os.remove("/tmp/no_extension_test_file") if os.path.exists("/tmp/no_extension_test_file") else None

    # ── image_path warning (not exception) ───────────────────────
    print("\n[image_path]")
    eng = DeckEngine()
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        eng.cover(title="T", image_path="/nonexistent/path/to/image.png")
        if w and "file not found" in str(w[0].message):
            print(f"  ✓ Missing image file warned: {str(w[0].message)[:80]}")
            passed += 1
        else:
            print(f"  ✗ Missing image file should warn, got: {[str(x.message) for x in w]}")
    total += 1

    # ── Normal usage works ───────────────────────────────────────
    print("\n[normal usage]")
    eng = DeckEngine(theme_name="tech", canvas="9:16")
    eng.cover(title="Hello", subtitle="World", author="Me")
    eng.content(title="Content", bullets=["a", "b"], key_point="k")
    eng.summary(title="Sum", key_points=["a"])
    eng.closing()
    eng.save("/tmp/validation_test.pptx")
    if eng.slide_count == 4:
        print(f"  ✓ Normal flow: {eng.slide_count} slides, no exceptions")
        passed += 1
    else:
        print(f"  ✗ Normal flow: expected 4 slides, got {eng.slide_count}")
    total += 1
    if os.path.exists("/tmp/validation_test.pptx"):
        size = os.path.getsize("/tmp/validation_test.pptx")
        if size > 1000:
            print(f"  ✓ PPTX file written: {size} bytes")
            passed += 1
        else:
            print(f"  ✗ PPTX file too small: {size} bytes")
    else:
        print(f"  ✗ PPTX file not created")
    total += 1
    os.remove("/tmp/validation_test.pptx") if os.path.exists("/tmp/validation_test.pptx") else None

    # ── Summary ──────────────────────────────────────────────────
    print()
    print("=" * 70)
    print(f"Passed: {passed} / {total}")
    if passed == total:
        print("✓ All validation tests passed.")
        return 0
    print(f"✗ {total - passed} test(s) failed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
