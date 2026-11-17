---
name: fec-security-review
description: Use when reviewing frontend security risks such as XSS, CSRF, sensitive data exposure, unsafe DOM APIs, untrusted user input, authentication/token handling, payment flows, file upload, CSP, dependency risk, or third-party scripts; Chinese triggers include security review, security check.
---

# Front-end security review

## Review modes and coverage

User-specified scope takes precedence over the default. Use the following three review modes:

- **Change review**: only when recent changes, current edits, staged changes, a PR or a commit are explicitly requested or clearly established by the active task, review those changes and necessary context. For local changes, inspect staged and unstaged diffs and relevant untracked project files within the requested scope; a staged-only request reviews only staged changes. If there are no changes, report that there is nothing to review; do not switch to recent commits or expand scope automatically.
- **Targeted review**: when files or directories are specified, inventory and review existing code in that scope, including unchanged code; no Git diff is required.
- **Project review (default)**: when no scope or change context is specified, or when the entire project is requested, inventory project-owned frontend code, related tests, configuration and dependency declarations, then review in module batches, including unchanged code; no Git diff is required.

Select scope before collecting diffs. A file/directory alone means full review of that scope; a path combined with an explicit change request restricts incremental review to that path. An unqualified invocation defaults to project review even if Git changes exist. At review start, state the selected mode and target scope. When automatically delegating review after edits, pass the current change scope explicitly; do not trigger project review merely because the reviewer was called.

Exclude dependency directories, build outputs, caches, generated files and third-party code by default, and record exclusions. Keep the frontend responsibility boundary; this is not a backend audit. A nonexistent target or a scope with no relevant files must be reported explicitly, not replaced with another scope.

Merge findings with the same root cause across batches. Report **review mode, target scope, reviewed files/modules, exclusions, unreviewed files/modules, completion status and verification commands/results**. If context or execution limits prevent completion, mark the review partial and list remaining modules; never claim complete project coverage. Reading callers for context or running project-wide lint/typecheck does not count as manual review of those files.

Change reviews retain merge recommendations. Targeted and project reviews use a risk assessment (Low / Medium / High, with blocking findings), not a claim of merge readiness. Preserve severity levels, evidence requirements and report filenames. Output reports only unless repairs are explicitly requested.

## Purpose

Identify client-side security risks in front-end code and recommend actionable fixes.

## Procedure

1. First confirm the review areas: user input, dynamic HTML, URL jump, authentication status, RBAC, file upload, payment/deletion and other sensitive operations, third-party scripts and dependencies.
2. Search for high-risk patterns: `dangerouslySetInnerHTML`, `v-html`, `innerHTML`, `document.write`, dynamic script, unverified redirect, and plain text token.
3. Review by risk type: XSS, CSP, sensitive data, CSRF, dependencies, input validation, file upload, open redirection, authentication authorization and third-party scripts.
4. Use the boundary model to determine responsibility: The client can only improve the experience and reduce misuse. Authentication, authorization, upload trust and sensitive operations must be finalized by the server.
5. High-risk issues are marked as blocking merges; front-end verification can only improve the experience and cannot be used as the only security boundary.
6. Output a hierarchical security report; see [references/report-template.md](references/report-template.md) for the report format.

## Detailed reference

- Load [references/security-checklist.md](references/security-checklist.md) when XSS, CSP, sensitive data, CSRF, dependencies and input validation details are required.
- When writing a security review report, load [references/report-template.md](references/report-template.md).

## Constraints

- Don't bypass security mechanisms to facilitate development.
- Don't rely on front-end validation as your only line of security.
- Do not trust any data coming from the client.
- High-risk issues must be marked as blocking merges when found.
- Separated from general code quality review: This skill focuses on threats, attack surfaces, and data breaches.
- Do not mechanically equate dependence on audit results with exploitable vulnerabilities; judgments need to be made based on the running path, exposure surface and repair cost.
- Do not treat hidden buttons, front-end route guards, or local role fields as authorization boundaries; APIs, SSR loaders, server actions, and sensitive operations must have server-side arbitration.

## Expected Output

Output a CRITICAL/HIGH/MEDIUM/LOW graded security review report. Each issue is associated with a specific file and line number, and repair suggestions are given; the report is saved as `reports/security-review-YYYY-MM-DD-HHmmss.md`.
