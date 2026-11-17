# Expected output skeleton — Fixture 16

## This is a CI regression test, not a user-facing fixture

The expected output is the result of running the dead-ref guard:

```text
Files scanned: <N>
✅ No dead references to specs/<Vendor>/<Part>.yaml found in user-facing files.
```

(Exit code 0)

## Pre-fix state (for context)

Before commit `4c59552`, the dead-ref guard reported:
- ❌ 6 file(s) have dead refs — see above
- Specifically the 6 files listed in fixture 16's table

## Required structural elements

- [ ] `check_no_specs_dead_refs.sh` exits 0
- [ ] Output reports 0 dead refs (was 6 before commit)
- [ ] All 6 specific lines still contain the disclaimer phrase

## How to verify

```bash
bash scripts/check_no_specs_dead_refs.sh
echo "Exit code: $?"  # should be 0
```

## Acceptance criteria

- [ ] Exit code 0
- [ ] "✅ No dead references" message printed
- [ ] No "❌" lines for the 6 known files
