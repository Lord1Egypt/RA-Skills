---
name: chrome-extension-maintainer
description: Release-gate and maintenance workflow for Chrome extensions covering Chrome Web Store policy, MV3, privacy, permissions, SEO/GEO, analytics triage, browser E2E evidence, i18n, packaging, and green/yellow/red publish decisions. Use when Codex needs to review an extension repo, diagnose growth or analytics issues, align listing/landing/support/privacy pages, choose tests to run, review data flow, or decide whether an extension is ready to publish or promote.
---

# Chrome Extension Maintainer

## Goal

Operate on Chrome extensions as small regulated products: a browser runtime, a permissions contract, a privacy promise, a public listing, a support surface, and a release history.

This skill is an operating workflow and review rubric. It does not bundle a Playwright harness, Chrome Web Store uploader, analytics connector, or package builder. Use repo-local scripts and installed tools when they exist, and report any missing tool as a release-evidence gap rather than inventing proof.

## When To Use

- A Chrome extension needs release readiness review, packaging, or a publish/no-publish decision.
- Store analytics, Search Console, GA, reviews, or support messages suggest weak growth or high uninstall risk.
- Manifest permissions, MV3 service-worker behavior, content scripts, host access, CSP, or privacy claims need review.
- Public surfaces need alignment: Chrome Web Store listing, landing page, support page, privacy page, screenshots, sitemap, or `llms.txt`.
- A Codex or ClawHub skill companion for Chrome extension maintenance needs validation before publication.

## Operating Order

1. Identify the target extension, release channel, and irreversible action.
   - Separate local Codex install, ClawHub registry publish, GitHub release, Chrome Web Store upload, submit, unpublish, rollback, and public promotion.
   - Do not perform any external upload, submit, registry publish, unpublish, rollback, deletion, or broad public promotion without explicit user approval.
2. Read the extension manifest, package scripts, listing copy, privacy/support pages, landing pages, and previous review artifacts.
3. If policy, Chrome versions, competitor claims, store requirements, or search behavior matter, verify current sources before deciding.
4. Document data flow:
   - browser-visible input
   - local extension storage
   - background/service-worker behavior
   - backend calls
   - third-party APIs or models
   - retention and deletion path
5. Check permissions:
   - prefer `activeTab` plus click-triggered `scripting`
   - justify every API and host permission
   - flag new warning surfaces before publish
6. Run the local gates that exist in the repo:
   - manifest/package validation
   - unit tests
   - Playwright/Puppeteer E2E with the unpacked extension
   - service-worker termination/restart tests when relevant
   - localization key/placeholder checks
   - accessibility and responsive layout checks
   - leak/secret scans when publishing public code or skills
7. Use real-user reviewer personas for at least the primary flow:
   - first-time user
   - privacy reviewer
   - Chrome Web Store reviewer
   - power user
   - localization reviewer
   - portfolio reviewer
8. Align public surfaces:
   - CWS title, summary, description, screenshots, privacy declarations, support URL, and reviewer notes
   - landing page, support page, privacy page, sitemap, robots, and `llms.txt` if present
   - Codex/ClawHub skill metadata when shipping a skill companion
9. Package and inspect the exact artifact intended for release.
10. Produce a green/yellow/red ship recommendation.

## Required Reference

Read `references/chrome-extension-maintenance-playbook.md` when the task involves release readiness, growth diagnosis, public listing/landing work, privacy claims, permissions, MV3 service workers, i18n, packaging, browser E2E evidence, or portfolio decisions.

## Validation Commands

Use the project’s own commands first. If the repo has no equivalent command, say that the evidence is missing.

For Chrome extension repos, typical gates are:

```bash
npm run check
npm test
npm run check:cws
npm run check:extension-locales
npm run e2e
npm run package
```

For Codex/ClawHub skill packages, use commands like:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>
clawhub whoami --no-input
clawhub inspect <slug> --no-input
find <skill-dir> -maxdepth 3 -type f -print | sort
```

Before publishing a skill package, confirm:

- `SKILL.md` is valid and has concrete workflow, rules, and validation guidance.
- `agents/openai.yaml` matches the skill’s actual scope.
- `.clawhubignore` excludes generated local state such as `.clawpatch/`, `.git/`, `.codex-run/`, `node_modules/`, `dist/`, logs, and cache files.
- no generated review state, local absolute paths, secrets, or private artifacts are in the package.
- ClawPatch or an equivalent review has either zero findings or documented non-applicability.

## Green/Yellow/Red

Green:
- primary browser flow works in real E2E evidence
- privacy and permission story matches code and public copy
- package/version identity is clear
- no untriaged P0/P1 findings remain

Yellow:
- usable for quiet test, beta, or local publication
- evidence or copy still has gaps
- do not broadly promote

Red:
- primary flow broken
- promise mismatch
- privacy ambiguity
- missing real browser evidence
- unresolved release blocker

## Review Output

Lead with critical findings. Then report:

- tests and commands run
- user flows verified
- files changed
- release artifacts created
- remaining blockers
- rollback or recovery path
- final green/yellow/red decision

## Rules

- Prefer fixes that reduce permission, privacy, and support risk.
- Treat installs as weak evidence; prioritize retained weekly users, uninstall ratio, conversion, support themes, and actual repeated use.
- Do not let listing or landing copy claim official affiliation, background crawling, unlimited use, hidden safety, or broad privacy promises unless the implementation proves it.
- For i18n, require `default_locale`, complete locale keys, placeholder parity, and RTL smoke coverage when `/_locales` exists.
- For MV3, assume service workers can terminate and require durable state for long work.
- For public skill publication, validate `SKILL.md`, `agents/openai.yaml`, references/scripts, leak risk, and registry auth before publishing.
