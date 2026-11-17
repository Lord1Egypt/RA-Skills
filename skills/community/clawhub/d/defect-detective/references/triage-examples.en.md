# Triage Examples

Three full cases covering the main path and both skip branches. For everyday triage the rules in SKILL.en.md are enough; read this when a branch call is unclear or when you need an output-format reference.

> Ticket IDs, paths, payloads, and data in the examples are fictional or redacted for demonstration; they do not represent any real system or real ticket.

## Case A: Backend API error — dedup hit (main path)

**Input signal:**

```text
Order service checkout API throws:
java.lang.NullPointerException
  at com.mystar.order.service.OrderService.submit(OrderService.java:142)
  at com.mystar.order.controller.OrderController.post(OrderController.java:88)
  at org.springframework.web.filter.OncePerRequestFilter.doFilter(...)
2026-11-12T14:32:11.204+08:00, requestId=req_8f3a2b, thread=http-nio-8080-exec-12
```

**Step 1 — fingerprint:** `NullPointerException · OrderService.submit / order · checkout API`. Timestamp, requestId, and thread name stripped; the Spring frame is a framework frame and stays out of the fingerprint.

**Step 2 — relaxation ladder (cross-stack, no component filter):**

- Level 1: `NullPointerException + OrderService + checkout` → no results
- Level 2: `NullPointerException + order service` → hits TICKET-8842 "Intermittent NPE on checkout" (open, similarity: high — all fingerprint-present core items [exception type, module/endpoint, message traits] match; the fingerprint has no error code, which does not participate). With no error code in the fingerprint, L2 runs as "exception type + module/endpoint" per the workflow rule
- Level 3: not executed (ladder stops descending once a level hits)

**Step 3 — layer known** (service name + server-side stack): `git blame` near OrderService.java shows PR-3021 refactored the coupon calculation three days ago.

**Step 4 — ownership:** Order Service team — basis: TICKET-8842 historical assignment + PR-3021 author's team.

**Report (excerpt):**

```text
Defect: NPE on order checkout API
Fingerprint: NullPointerException · OrderService.submit / order

Known issue?  likely
  - TICKET-8842  Intermittent NPE on checkout  (open, high) — all fingerprint-present core items match; "intermittent" vs this report's "every time" needs engineer review

Likely owner: Order Service team — TICKET-8842 history + PR-3021 author

Recent suspect changes:
  - PR-3021  OrderService coupon-calc refactor — touched the failing area three days ago

Evidence:
  - Search keywords: L1 "NullPointerException+OrderService+checkout" (none); L2 "NullPointerException+order service" (hit)
  - Search scope: cross-stack
  - Code correlation: order repo main branch blame

Related: two other closed NPE tickets in the same area within the last 30 days, neither touching the checkout path

Recommendation: link to existing ticket (TICKET-8842)
Status: complete
```

Note: similarity is "high" yet "Known issue?" stays "likely" — the repro discrepancy (intermittent vs always) is left for the engineer to reconcile; do not merge on your own.

## Case B: Frontend display issue — skip step 3 (frontend branch)

**Input signal:** "The coupon list on the checkout page misaligns on Safari — the button overlaps the input box. Chrome is fine."

**Step 1 — fingerprint:** `style misalignment · checkout coupon list · Safari`. Pure UI description, no exception or error code; the fingerprint is area + symptom.

**Step 2 — ladder:** Level 1 `Safari style misalignment + coupon list` → hits TICKET-9013 (open, similarity: medium — per the FAQ baseline, the fingerprint-present core items module/area and symptom match, but the message traits differ: this report is Safari-only while the ticket covers all Chromium browsers). Listed as candidate.

**Step 3 — skipped:** frontend rendering/style issue with no backend clue → note "frontend display issue, no backend code to correlate".

**Step 4 — ownership:** Web frontend team — basis: TICKET-9013 carries the checkout-web component tag.

**Report (excerpt):**

```text
Defect: Safari checkout coupon list misaligned
Fingerprint: style misalignment · checkout coupon list · Safari

Known issue?  likely (medium-similarity candidates only)
  - TICKET-9013  Chromium-wide checkout coupon list misaligned  (open, medium) — module/area and symptom hit; message traits differ (this report is Safari-only)

Likely owner: Web frontend team — TICKET-9013 component tag checkout-web

Recent suspect changes: N/A — frontend display issue, no backend code to correlate
Related: none

Recommendation: needs more info — the engineer confirms whether same root cause; do not link on your own (medium similarity does not support linking per the FAQ rules)
Status: complete
```

## Case C: Environment/config issue — skip step 3 + no-match ticket suggestion (real smoke-test case)

**Input signal:**

```text
Environment: macOS + zsh, AI agent running in a sandboxed execution environment
Symptom: agent fails to write skill files:
  [Errno 13] Permission denied: '~/.trae-cn/skills/fast-commit/SKILL.md'
  os.makedirs('~/.trae-cn/skills/fast-commit') also Permission denied
The same process writes to the project directory without issue; only ~/.trae-cn/skills/ is denied. Reproduces every time.
```

**Step 1 — fingerprint:** `Errno13/EPERM · ~/.trae-cn/skills/ · sandbox write (selective denial)`. Username and skill name stripped. Key trait: selective denial (same process writes fine to the project dir) → points at sandbox write policy, not filesystem corruption.

**Step 2 — ladder (cross-stack):** all three levels executed, no results — the reachable tracker does not cover this product domain. Per the FAQ rule, state it honestly: no match ≠ definitely new.

**Step 3 — skipped:** environment/config issue (sandbox policy, file permissions) → note "no code repository to correlate".

**Step 4 — ownership:** platform sandbox-policy team — basis: path is platform config territory + selective denial controlled by the sandbox write policy (component-based inference, no ticket-history corroboration; labeled as inferred).

**Report (excerpt):**

```text
Defect: EPERM writing to ~/.trae-cn/skills/ in sandbox; project-dir writes fine
Fingerprint: Errno13/EPERM · ~/.trae-cn/skills/ · sandbox write

Known issue?  no (no match in the reachable tracker)

Likely owner: platform sandbox-policy team — path in platform config area + selective denial from sandbox write policy

Recent suspect changes: N/A — environment/config issue, no code repository to correlate

Evidence:
  - Search keywords: L1 "EPERM+skills+Permission denied"; L2 "EPERM"; L3 "skill write" (all no results)
  - Search scope: cross-stack; the reachable tracker does not cover this domain
  - Code correlation: skipped

Related: none

Recommendation: file new ticket (reachable tracker does not cover this domain; cannot fully rule out a known issue)
Status: complete

Ticket suggestion:
  Title: EPERM writing to ~/.trae-cn/skills/ in sandbox (project-dir writes work)
  Description: Errno13/EPERM · ~/.trae-cn/skills/; reproduces every time; same process writes project dir fine, only the user-home config area is denied
  Suggested owner: platform sandbox-policy team
```

Note the Evidence field honestly states "the reachable tracker does not cover this domain" — that transparency is part of the report's credibility; hiding search limits is what would mislead the filing decision.
