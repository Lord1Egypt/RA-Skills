# agent-command-guard-hardening

An AgentSkill for changing a command interception layer **without pretending it is a security boundary**.

Guards around `rm`, `sudo`, `chmod`, `launchctl` and friends are easy to add and easy to fool. This skill makes the change auditable: baseline first, a matrix with negative controls, classification tested without execution, and the bypass surface written next to the guarantee.

It is a small engineering idea, published in case it is useful. No product, no service. Developed through agent operation and corrected against real failures, not hand-authored as a prompt template.

## The three ideas

1. **Baseline before change.** Wrapper bytes, hashes, and the effective `PATH` for every controlled command. Without it, “it still works” is an opinion.
2. **Three-case matrix.** Should-block, negative control, known bypass. A matrix without negative controls only measures enthusiasm; a matrix without bypass cases overstates the guarantee.
3. **Classify, do not execute.** The guard exposes `classify(argv) -> allow|deny`. Test that. Never run the destructive command to see what happens.

## Quickstart

```
python3 scripts/matrix_run.py --classifier examples/classifier-demo.sh --matrix examples/matrix.json
python3 scripts/bypass_scan.py examples/scripts-sample.sh
```

`matrix_run.py` executes only the classifier, compares each decision with the expected value, and exits non-zero on any mismatch. It reports pass counts by class, so a regression in negative controls is visible immediately.

`bypass_scan.py` scans files for absolute-path invocation, nested shells, interpreter one-liners, pipe-to-shell, and `eval`. A hit is a review item, not proof of exploitability.

## What it does not do

- It is not a security boundary. A `PATH` wrapper cannot stop absolute paths, nested interpreters, or direct syscalls.
- It does not execute the test commands, so it cannot prove behaviour — only classification.
- It does not replace OS permissions, sandboxing, or least privilege.
- A guard that silently breaks routine commands is a regression, not a hardening.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Baseline, matrix, classifier contract, syntax gate, logging, rollback, discipline. |
| `references/bypass-surfaces.md` | What a wrapper cannot stop, and how to state it honestly. |
| `scripts/matrix_run.py` | Runs the matrix against a classifier; never executes the case. |
| `scripts/bypass_scan.py` | Finds risky invocation forms in files. |
| `examples/` | Toy classifier, 8-case matrix (3 block / 3 negative / 2 bypass), sample script. |

## License

MIT. Use it, fork it, rewrite it.
