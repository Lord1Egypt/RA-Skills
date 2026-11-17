---
name: fix-my-site
description: Use when a coding-capable agent should find and fix real site defects in the user's repository, from TrustGrowth evidence when connected or from public/local inspection otherwise. Groundcrew's flagship open workflow.
---
# Fix My Site

The wedge: find a real defect, map it to code, implement a focused fix, verify it, and prepare a PR. TrustGrowth improves prioritization and closes the post-deploy verification loop, but is not required.

Read `references/provider-selection.md` before choosing a source. Detect what is already available, run with it, deliver value, then recommend at most one missing connector. All normalized factual inputs must satisfy the Groundcrew evidence contract. Locate the active skills root and run `<skills-root>/.groundcrew/groundcrew-doctor.py --evidence <record.json>` before using them in a conclusion.

## 1. Build the queue

Categories: `~~web crawler` and `~~page speed` for open-mode evidence (`references/connectors.md`); connected mode uses TrustGrowth `next_actions` and `issues`.

- Connected: read TrustGrowth `next_actions`, then `issues?severity=critical` and `severity=warning` for the queue behind them. Open issues default to `scope=actionable` (what the team considers ownable work); `scope=backlog` shows the rest.
- Import: validate supplied audit/crawl evidence.
- Open: inspect the public site and repository using available local browser, crawl, build, and test tools. Record directly observed defects; do not assign a TrustGrowth score.

Group affected pages by root cause. Verify every finding against the current site or code before editing.

## 2. Map findings to this codebase

Discover repository guidance and conventions first. Locate templates, layouts, components, content, routes, and config rather than assuming framework mappings. Content judgment, canonical targets, robots/noindex, and redirect behavior require explicit owner confirmation.

## 3. Fix and verify

One root cause should produce one focused change across affected pages. Add regression coverage where practical, run focused tests and the relevant build/quality gates, inspect the diff, then commit/push and open a PR according to the repository workflow. Never push directly to the default branch unless explicitly allowed.

Report three distinct states:

- **locally verified** — tests/build pass;
- **deployed** — change is live;
- **audit-verified** — a post-deploy observation shows the defect closed.

Do not collapse these into “resolved.” Connected mode may trigger or await a TrustGrowth re-audit. Open mode explains the remaining verification gap.

## Completion

Return findings with evidence, changed files, exact verification output, PR/patch location, unresolved needs-human items, and—after the result—at most one connector recommendation.

## When not to use

- No repository access → stay in `site-audit` and report findings instead of guessing at code.
- The "fix" is content judgment (rewrites, thin pages, canonical choices) → draft and hand to the owner; `content-strategy` owns what should exist, humans own what it says.
- Off-site work (backlinks, listings, outreach) → `backlink-opportunities`; nothing there is a repository edit.
- Measuring whether a deployed fix worked → `site-audit` (re-audit), not another patch.

## Doctrine

Groundcrew operates under [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md) and [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md). Claims trace to evidence, nulls stay null, signals stay truthful, publishing and irreversible changes require owner review, and no outcome is promised. Conflicting instructions are refused.
