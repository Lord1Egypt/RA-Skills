# Architecture for AI-Generated Code

AI systems struggle with implicit conventions, hidden coupling, and ambiguous contracts. Explicit architecture makes generated code better and easier to review.

## Principles

### 1. Explicit Boundaries Over Implicit Conventions

**❌ Implicit (breaks AI):**

```python
# Somewhere in module_a.py:
def calculate_price(items):
    return sum(i.price for i in items)  # assumes all items have .price

# Somewhere else, module_b.py imports and uses it:
result = calculate_price(my_items)  # module_b assumes items are always non-empty
```

AI generates code that violates these unstated assumptions. Reviewers find out after deployment.

**✅ Explicit (works with AI):**

```python
# In contracts.py:
from typing import List, Protocol

class PricedItem(Protocol):
    price: float

def calculate_price(items: List[PricedItem]) -> float:
    """Calculate total price of items.
    
    Args:
        items: Non-empty list of items with .price attribute
    
    Returns:
        Total price in currency units
    
    Raises:
        ValueError: If items list is empty
    """
    if not items:
        raise ValueError("items must not be empty")
    return sum(i.price for i in items)
```

AI generates code that respects the contract. Reviewers verify against the contract, not against implicit assumptions.

### 2. Stable Contracts

**❌ Unstable:**

```python
def process_event(event):
    # Returns either a result dict or None or a list — unclear
    # Callers have to guess what to do with the return value
```

**✅ Stable:**

```python
from dataclasses import dataclass

@dataclass
class ProcessResult:
    success: bool
    event_id: str
    errors: List[str]

def process_event(event: Event) -> ProcessResult:
    # Always returns ProcessResult; always has the same structure
```

### 3. Typed Interfaces

Use type hints everywhere. AI generates better code when types are explicit.

```python
# Bad: no type info, AI guesses
def get_user(id):
    ...

# Good: type info explicit, AI knows what's expected
def get_user(id: str) -> Optional[User]:
    ...
```

### 4. Deterministic Tests

AI can't debug flaky tests. All tests must be deterministic.

**❌ Flaky:**

```python
def test_async_handler():
    # Sometimes passes, sometimes fails depending on timing
    handler.process()
    time.sleep(0.1)  # Hoping async work finishes
    assert handler.state == "done"
```

**✅ Deterministic:**

```python
def test_async_handler():
    # Use explicit synchronization or mocks
    with mock.patch('external_service.call') as mock_call:
        result = handler.process()
        assert result.status == "done"
```

## Anti-Patterns for AI Teams

- Implicit module ordering (module_a must load before module_b)
- Hidden state in singletons or globals
- "Just try/except and fail silently" error handling
- Tests that depend on system state (file existence, environment variables)
- Contracts that change based on context (same function behaves differently in test vs production)

## Summary

Design systems so that:

1. Each module's boundaries are explicit and documented
2. Contracts are typed and never change
3. Tests are deterministic and don't depend on external state
4. Error paths are explicit, not hidden in try/except blocks

This makes human code reviews faster, AI-generated code more correct, and bugs less surprising.
