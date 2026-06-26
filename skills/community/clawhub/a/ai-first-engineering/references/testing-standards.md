# Testing Standards for AI-Generated Code

AI-generated code has different failure modes than human code. Testing standards must be higher.

## Why Higher Standards?

- **Human code:** Developer knows the whole system; usually avoids obvious edge cases
- **AI code:** Generated from specs; may miss corner cases not explicitly mentioned in spec
- **Result:** Same test coverage is not enough; need intentional edge-case testing

## Three-Tier Testing Standard

### Tier 1: Regression Coverage (Required)

Every domain touched by code changes must have regression test coverage.

#### Example: Adding a discount calculation feature

```python
def test_discount_calculation_with_no_discount():
    # Existing test — ensure we didn't break normal flow
    assert calculate_price(items=100, discount=None) == 100

def test_discount_calculation_with_percentage():
    # Existing test — ensure old behavior still works
    assert calculate_price(items=100, discount=Discount(type="percent", value=10)) == 90

def test_discount_calculation_with_flat():
    # NEW test — but regression category (covers touched domain)
    assert calculate_price(items=100, discount=Discount(type="flat", value=20)) == 80
```

**Not optional.** Every touched domain needs regression coverage before code ships.

### Tier 2: Explicit Edge-Case Assertions

Write tests that explicitly check corner cases.

```python
def test_discount_with_negative_value():
    # AI might ignore this case in naive implementation
    with pytest.raises(ValueError):
        Discount(type="percent", value=-10)

def test_discount_exceeding_price():
    # Flat discount larger than total price — should fail or cap?
    # Explicit test prevents surprise behavior
    result = calculate_price(items=50, discount=Discount(type="flat", value=100))
    assert result == 0  # or assert raises; but not undefined behavior

def test_discount_with_zero_items():
    # Empty list edge case
    with pytest.raises(ValueError):
        calculate_price(items=[], discount=None)

def test_discount_with_none_items():
    # Null input edge case
    with pytest.raises(TypeError):
        calculate_price(items=None, discount=None)
```

### Tier 3: Integration Checks for Boundaries

Test behavior across module boundaries.

```python
def test_discount_persists_across_database_roundtrip():
    # Edge case: Discount is calculated, saved to DB, retrieved — still correct?
    discount = Discount(type="percent", value=10)
    db.save(discount)
    retrieved = db.load(discount.id)
    assert retrieved.value == 10  # Not corrupted by serialization

def test_discount_with_concurrent_updates():
    # Edge case: Two requests updating discount at same time
    # Should not lose updates or corrupt state
    ...

def test_discount_calculation_with_invalid_currency_rates():
    # External dependency edge case: currency conversion fails
    with mock.patch('currency_service.get_rate', side_effect=Exception("API down")):
        with pytest.raises(CurrencyConversionError):
            calculate_price_in_other_currency(...)
```

## Checklist for AI-Generated Code

Before approving AI-generated code in review, verify:

- ✅ Regression tests written for all touched domains
- ✅ Edge cases explicitly tested (empty lists, nulls, invalid inputs)
- ✅ Boundary conditions tested (zero, max value, opposite extreme)
- ✅ Error paths tested (external calls fail, timeouts, bad data)
- ✅ Integration tests verify cross-module behavior
- ✅ Flaky tests? (If a test fails intermittently, AI can't fix it — fix test first)

## Anti-Pattern: "Code coverage is 90%, we're good"

High coverage does not mean high quality. A test that runs code without asserting anything is worthless.

```python
# This "covers" the discount logic but doesn't assert anything:
def test_discount():
    calculate_price(items=100, discount=Discount(type="percent", value=10))
    # No assertion — test passes even if function returns 999

# This actually tests the discount logic:
def test_discount():
    result = calculate_price(items=100, discount=Discount(type="percent", value=10))
    assert result == 90  # Explicit assertion
```

## What AI Struggles With (Mark for Extra Review)

- ❌ Database transactions and rollback safety
- ❌ Concurrent access and race conditions
- ❌ External API retry logic and timeouts
- ❌ Feature flag logic and canary deploys
- ❌ Data migration safety (backward compatibility)

If AI-generated code touches these areas, add extra regression tests and review carefully.
