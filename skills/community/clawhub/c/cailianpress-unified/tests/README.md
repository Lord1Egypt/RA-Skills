# Tests

This folder contains lightweight validation for the V1 unified CLS skill.

## Current coverage

- schema helpers
- red/highlight filter behavior
- heat filter behavior

## Run

```bash
cd skills/cailianpress-unified
PYTHONPATH=. python3 -m pytest tests -q
```

## Note

The current runtime environment used during implementation did not have `pytest` installed, so the test files were created but not executed here.
