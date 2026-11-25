# claim-audit

Re-run every number a document claims, then tell you which ones do not match.

## What it verifies

| Claim | How it is checked |
|---|---|
| `9/9 PASS` | re-runs `tests/run_golden.py`, parses the last line |
| `12 个文件` / `files=12` | counts the real file tree |
| `100/100` | re-scores with `lgd-skill-review/scripts/review.py --run` |
| `` `references/x.md` `` | checks the path exists (list/table/link lines only) |

## Usage

```bash
python scripts/audit.py check D:\path\to\pkg            # audit
python scripts/audit.py list  D:\path\to\pkg            # list claims only
python scripts/audit.py check D:\path\to\pkg --json --strict
```

Exit codes: `0` all matched · `1` at least one mismatch (`--strict` also fails on unverifiable) · `2` bad arguments.

## Self-check

```bash
python tests/run_golden.py     # 9/9 PASS
python demo/run_demo.py        # end-to-end: a package that claims 9/9 but ran 1/2
```

## What it refuses to do

- It does not judge whether a sentence is *true* — only whether the number is *that number*.
- It never rewrites the document. A mismatch is a human decision.
- It does not treat "cannot verify" as "wrong"; that is `--strict` only.

Details: [references/rules.md](references/rules.md), [references/limits.md](references/limits.md),
[references/usage.md](references/usage.md), [references/selfcheck.md](references/selfcheck.md).
