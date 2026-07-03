# Elements Modular Merge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Merge `ELEMENT-SKILL.md` into `clink-integ-skills` as a Standard Integration Elements sub-capability with docs, routing, artifacts, review checks, README coverage, and tests.

**Architecture:** Add `references/elements-integration.md` as the canonical Elements module and route Elements prompts through Standard Integration. Extend runtime signal detection and artifact generation without creating a fifth top-level route. Preserve existing standard integration artifacts because Elements still depends on backend session creation, webhooks, and reconciliation.

**Tech Stack:** Node.js ESM runtime scripts, Markdown skill modules, custom test harness under `tests/`.

---

### Task 1: Runtime Red Tests

**Files:**
- Modify: `tests/run_skill_runtime_tests.mjs`

- [ ] **Step 1: Add failing tests for Elements prompts**

Add checks that `@clink-ai/clink-elements`, `loadClinkElements`, `promoCodeChange`, inline/drawer layouts, and Next.js client-only prompts route to Standard Integration and emit Elements artifacts.

- [ ] **Step 2: Run runtime tests to verify failure**

Run: `pnpm test:runtime`
Expected: FAIL because Elements artifacts are not emitted yet.

### Task 2: Structure Red Tests

**Files:**
- Modify: `tests/run_structure_tests.mjs`

- [ ] **Step 1: Add failing structure expectations**

Require `references/elements-integration.md` and check `SKILL.md`, README files, `references/standard-integration.md`, `references/output-artifacts.md`, and `references/review-checklist.md` mention the Elements module and key concepts.

- [ ] **Step 2: Run structure tests to verify failure**

Run: `pnpm test:structure`
Expected: FAIL because the module and mentions do not exist yet.

### Task 3: Elements Reference Module And Skill Docs

**Files:**
- Create: `references/elements-integration.md`
- Modify: `SKILL.md`
- Modify: `references/standard-integration.md`
- Modify: `references/output-artifacts.md`
- Modify: `references/review-checklist.md`
- Modify: `README.md`
- Modify: `README-zh.md`

- [ ] **Step 1: Create the Elements module**

Migrate durable content from `ELEMENT-SKILL.md` into `references/elements-integration.md` and reshape it around mental model, integration shape selection, server/client boundary, headless template strategy, lifecycle, host UI sync, loading strategy, layout guidance, and review constraints.

- [ ] **Step 2: Wire module references**

Update the main skill routing and module maps so Elements prompts are handled as Standard Integration plus the Elements module.

- [ ] **Step 3: Run structure tests**

Run: `pnpm test:structure`
Expected: PASS after docs are wired.

### Task 4: Runtime Implementation

**Files:**
- Modify: `lib/skill-runtime.mjs`

- [ ] **Step 1: Add Elements signal helpers**

Add detection for Elements SDK terms, promotion-code terms, layout terms, and client-only framework terms.

- [ ] **Step 2: Add Elements artifacts**

When the route is `merchant_standard_integration` and Elements signals are present, append `elements_frontend_checklist`, `elements_event_mapping`, `elements_error_handling_checklist`, `elements_host_ui_todo`, `elements_layout_recipe`, `elements_lifecycle_checklist`, and `elements_server_client_boundary`. Add `promotion_code_ui_contract` only when promotion-code signals are present.

- [ ] **Step 3: Add runtime note**

For Elements prompts, add a note that Elements is embedded, not hosted checkout, and webhook/server reconciliation remains authoritative.

- [ ] **Step 4: Run runtime tests**

Run: `pnpm test:runtime`
Expected: PASS after runtime changes.

### Task 5: Full Verification

**Files:**
- All touched files

- [ ] **Step 1: Run full test suite**

Run: `pnpm test`
Expected: PASS.

- [ ] **Step 2: Inspect git status**

Run: `git status --short`
Expected: only intentional tracked changes plus the pre-existing untracked `ELEMENT-SKILL.md` unless it is explicitly removed or ignored later.

- [ ] **Step 3: Commit implementation**

Commit the implementation after tests pass.
