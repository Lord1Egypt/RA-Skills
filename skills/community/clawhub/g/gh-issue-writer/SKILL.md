---
name: gh-issue-writer
description: Draft well-structured GitHub issues from a description, error, or idea. Supports bug reports, feature requests, enhancements, and tasks. Optionally submits directly via the GitHub CLI or API. Use when someone says "write a GitHub issue", "open an issue for", "file a bug", "create a feature request", or describes a problem that needs to be tracked.
metadata: {"clawdbot":{"emoji":"🐛","requires":{"bins":["gh","git","curl"]},"primaryEnv":"GH_TOKEN","os":["linux","darwin","win32"]}}
---

# gh-issue-writer

Draft clear, actionable GitHub issues from a brief description, error message, or idea. Covers bug reports, feature requests, enhancements, and tasks.

---

## Step 1 — Understand the Input

Ask (or infer from context):

1. **What type of issue?** Bug | Feature Request | Enhancement | Task | Question
2. **What repo?** (detect from `git remote get-url origin` if in a git dir, otherwise ask)
3. **What happened / what's wanted?** (the raw description, error, or idea)
4. **Optional:** Labels, assignee, milestone, environment details

If the user gives you enough context, proceed without asking — draft and show for confirmation.

---

## Step 2 — Draft the Issue

Use the appropriate template below. Fill every field; omit sections only if genuinely not applicable.

### Bug Report

```markdown
## Description
<!-- Clear, one-paragraph summary of the problem. -->

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
<!-- What should have happened? -->

## Actual Behavior
<!-- What actually happened? Include error messages verbatim. -->

## Environment
- OS:
- Browser / Runtime / Version:
- Relevant config or dependencies:

## Logs / Screenshots
<!-- Paste relevant logs, stack traces, or attach screenshots. -->

## Additional Context
<!-- Anything else that might help: related issues, recent changes, workarounds tried. -->
```

### Feature Request

```markdown
## Problem / Motivation
<!-- What problem does this solve? Why does it matter? -->

## Proposed Solution
<!-- Describe the feature clearly. What would it look like? How would it work? -->

## Alternatives Considered
<!-- Other approaches you thought about and why you ruled them out. -->

## Acceptance Criteria
- [ ]
- [ ]

## Additional Context
<!-- Mockups, related issues, prior art, links. -->
```

### Enhancement (improvement to existing behavior)

```markdown
## Current Behavior
<!-- What does it do now? -->

## Desired Behavior
<!-- What should it do instead? -->

## Why This Matters
<!-- Impact: who benefits, how much, how often? -->

## Suggested Implementation
<!-- Optional: any technical ideas or constraints. -->
```

### Task / Chore

```markdown
## What needs to be done
<!-- Clear, specific description of the work. -->

## Why / Context
<!-- Why is this needed now? What does it unblock? -->

## Definition of Done
- [ ]
- [ ]
```

---

## Step 3 — Write a Strong Title

Title format by type:

| Type | Pattern | Example |
|------|---------|---------|
| Bug | `Bug: <what fails> on <where>` | `Bug: 500 on POST /login when payload missing field` |
| Feature | `Feature: <capability> for <who/where>` | `Feature: CSV export for admin reports` |
| Enhancement | `Enhance: <what> — <improvement>` | `Enhance: error messages — add field-level detail` |
| Task | `Task: <verb> <thing>` | `Task: upgrade Stripe SDK to v16` |

Rules:
- Under 72 characters
- No vague words ("fix thing", "update stuff")
- Specific: what + where, not just what

---

## Step 4 — Suggest Labels & Metadata

Recommend labels based on type and content:

| Signal | Suggested Labels |
|--------|-----------------|
| Bug | `bug`, `needs-repro` |
| Feature | `enhancement`, `feature-request` |
| High impact / blocking | `priority:high` |
| Needs more info | `needs-info` |
| Good for contributors | `good first issue` |
| Security | `security` |
| Performance | `performance` |
| Docs | `documentation` |

Also suggest:
- **Assignee:** who owns this area of the codebase?
- **Milestone:** which release or sprint does this target?

---

## Step 5 — Present for Review

Show the complete draft:

```
**Title:** <title>

**Type:** Bug / Feature / Enhancement / Task
**Suggested labels:** bug, priority:high
**Suggested assignee:** (if known)

---
<full issue body>
---
```

Ask: "Does this look right? I can adjust the title, add details, or submit it directly."

---

## Step 6 — Optional: Submit

> **Prerequisites for submission:**
> - `gh` CLI (authenticated via `gh auth login`) — preferred path
> - `GH_TOKEN` env var — required for the curl API fallback
> - `git` — used to detect the repo from `git remote get-url origin`
>
> Drafting (Steps 1–5) works without any of these.

If the user says "submit", "create it", "go ahead", or similar:

### Via GitHub CLI (preferred)
```bash
gh issue create \
  --repo owner/repo \
  --title "<title>" \
  --body "<body>" \
  --label "bug,priority:high" \
  --assignee "@me"
```

### Via GitHub API (fallback if `gh` isn't available)
```bash
curl -s -X POST \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/{owner}/{repo}/issues \
  -d '{
    "title": "<title>",
    "body": "<body>",
    "labels": ["bug"],
    "assignees": []
  }'
```

On success, output the issue URL. On error, show the response and offer to retry.

---

## Quality Checklist

Before presenting the draft, verify:

- [ ] Title is specific and under 72 chars
- [ ] For bugs: repro steps are numbered and minimal
- [ ] Expected vs actual behavior is clearly separated
- [ ] Environment section filled (OS, version, runtime)
- [ ] No vague language ("sometimes", "doesn't work", "weird behavior")
- [ ] Logs/errors quoted verbatim, not paraphrased
- [ ] Ends with a clear ask or next step

---

## Tips for Better Issues

**Do:**
- Quote error messages exactly — don't summarize them
- Include the minimal repro — what's the smallest thing that triggers the bug?
- Link related issues with `#<number>`
- Mention what you've already tried

**Don't:**
- "Works on my machine" without environment details
- Multiple unrelated problems in one issue
- Vague titles like "Login broken" or "Feature request"
- Screenshot of code instead of pasted text

---

## See Also

- GitHub's official issue template docs: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests
- Set up templates: create `.github/ISSUE_TEMPLATE/` in your repo
