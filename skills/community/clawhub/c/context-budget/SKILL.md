---
name: "context-budget"
description: "Measure and safely reduce always-loaded agent instruction context in characters and tokens."
---

# Context budget

Always-loaded files such as `AGENTS.md`, `MEMORY.md`, `SOUL.md`, `USER.md`,
`IDENTITY.md`, and `SECURITY.md` are injected into an agent's prompt. Their
cost recurs on every turn. Measure that cost before changing instructions, then
reduce it without weakening authority, safety, or meaning.

Use this skill when runtime logs report bootstrap truncation, per-turn context
cost is high, policies appear in several files, or a persistent rule is being
added.

## The two units differ

Runtime truncation limits are expressed in **characters**; model cost is paid
in **tokens**. Optimising one does not guarantee improvement in the other.

Do not abbreviate words as a token-saving technique. In the measured nine-pair
sample in `references/method.md`, no abbreviation saved a token and three cost
more. Remove duplication and unnecessary text instead.

## Workflow

1. **Measure before editing.** Character-only estimation is the safe default:

   ```bash
   scripts/context-budget.py --workspace <path> --sections
   ```

   For exact token counts, explicitly select a trusted loopback tokenizer for
   that run:

   ```bash
   scripts/context-budget.py --workspace <path> --sections \
     --tokenizer-url http://127.0.0.1:<port>/tokenize \
     --tokenizer-model <model>
   ```

   Tokenization sends complete selected-file contents to that local process.
   The script rejects non-loopback endpoints, inherited endpoint settings,
   path traversal, and symlinked inputs. Confirm that the tokenizer does not
   retain requests. Without a working endpoint the report marks token counts
   as estimates.

2. **Map authority before moving text.** Classify every rule by identity,
   safety, privacy, secrets, tool authority, approval, delivery, and task
   specificity. Keep always-on authority and safety rules in their required
   precedence layer. Move only task-specific material whose on-demand loader
   and trigger are verified. Relocation changes delivery context and can change
   behaviour even when wording is unchanged.

3. **Deduplicate across files.** Keep each rule in its canonical home and leave
   a pointer only where the pointer is guaranteed to load the rule before it is
   needed. Preserve every unique condition and exception.

4. **Give each file one job.** Separate operating rules, temperament, identity,
   audience preferences, memory, and security policy. Resolve conflicts before
   editing.

5. **Compress remaining prose.** Merge sections that answer the same question,
   turn repeated-prefix lists into tables, and remove connective text while
   preserving conditions.

6. **Verify syntax and semantics.** Use distinctive markers only as a missing-
   text check. Also review every moved or rewritten rule for meaning,
   precedence, and availability. Run regressions for direct injection,
   quoted/forwarded injection, secret exfiltration, unauthorized external
   delivery, destructive requests, and a legitimate authorized operation.

7. **Re-measure and report both units.** Treat estimates as estimates and
   record the tokenizer model when exact counts are used.

## Safety boundaries

- Measurement is local and read-only unless an explicitly selected loopback
  tokenizer is used; then full selected-file contents enter that local service.
- Editing always-loaded instructions is a production behaviour change. Require
  explicit operator intent for the edit scope and preserve higher-precedence
  rules.
- Never compress or move a security policy merely to save tokens.
- Preserve machine-managed blocks byte for byte, including their markers.
- Prefer protected repository history for rollback. If separate backups are
  required, store them only in a local access-restricted directory, exclude
  them from sync and version control, use restrictive file permissions, and
  delete them after a fresh session passes; verify deletion.
- Hold any required writer lease for the full edit and release it after
  validation.
- Re-baseline instruction-file integrity checks after the approved change.
- Know exactly what a default report does and does not hide. It **redacts** the
  absolute workspace path and the text of duplicated instruction lines. It
  **shows** file names, section headings and path prefixes, deliberately: an
  operator cannot act on a budget that will not say which file or section costs
  the most. Treat a default report as naming your instruction files.
- `--show-content` additionally reveals the workspace path and the duplicated
  line text. Use it only with explicit intent, keep the output local, and redact
  before sharing.

## Verification gate

A pass is complete only when all hold:

1. each file and the full set are within their character limits;
2. the marker checklist reports zero missing rules;
3. semantic and precedence review finds no weakened or unavailable rule;
4. all six assurance regressions pass;
5. before/after characters and tokens are recorded, with estimates labelled;
6. one fresh session runs without truncation or behaviour regressions;
7. temporary backups are securely removed after the clean-session gate.
