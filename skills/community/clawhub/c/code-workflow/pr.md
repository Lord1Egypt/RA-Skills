# PR Workflow (with Visual Evidence)

Extends the standard code-workflow with **capture and attachment** steps for PRs that benefit from visual evidence.

## When to Use

- UI/frontend changes that are easier to review with screenshots
- Before/after comparisons (layout, styling, behavior)
- User explicitly asks "PR with screenshots", "capture and PR", "create PR"

## Workflow

The standard 4-stage workflow is extended with two additional steps:

```text
1. Research       (standard code-workflow step 1)
2. Plan           (standard code-workflow step 2, with verification plan)
3. User Review    (standard code-workflow step 3)
4. Implement      (standard code-workflow step 4, TDD by default)
5. Capture        ← NEW: take visual evidence
6. PR             ← NEW: create PR with attachments
```

Steps 1-4 follow the standard code-workflow. Steps 5-6 are described below.

## Step 5: Capture

After implementation is complete and tests pass, capture visual evidence.

### Capture Methods

| Method | When to Use | Tool |
|--------|------------|------|
| Browser screenshot | Web UI changes | Playwright MCP `playwright.playwright_browser_take_screenshot` (see [`skills/web-browser`](../web-browser/SKILL.md)) |
| Terminal output | CLI/API changes | Copy relevant output |
| Before/after comparison | Visual regressions, layout fixes | Screenshot both states |

### Capture Procedure

1. **Start the dev server** if not already running
2. **Navigate to the changed page/component** via Playwright
3. **Take screenshots** of the relevant state:
   - Before state (from main/base branch if needed)
   - After state (current implementation)
4. **Save captures** to a temporary location

### Image Format Priority

| Format | Use Case |
|--------|----------|
| WebP | Static screenshots (smallest size, GitHub supported) |
| PNG | When WebP is not available or transparency needed |
| GIF | Short animations, hover effects, transitions |
| MP4/WebM | Complex interactions, multi-step flows |

### Capture Naming

```text
pr-assets/<issue-number>-<description>-before.webp
pr-assets/<issue-number>-<description>-after.webp
```

## Step 6: Create PR with Attachments

### PR Body Template

```markdown
## Summary
<1-3 bullet points>

## Visual Changes
<!-- For before/after -->
| Before | After |
|--------|-------|
| ![before](url) | ![after](url) |

<!-- For single screenshot -->
![description](url)

## Test plan
- [ ] ...
- [ ] (if there is a cross-repo dependency) infra-repo PR merged + deployment confirmed

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### Cross-repo Dependency Check (required when creating a PR)

If the code depends on env-var / infra changes in another repo:
1. State the dependency in the PR body: `Depends on: {org}/{repo}#{PR}`
2. Add "infra-repo PR merged + deployment confirmed" to the Test Plan
3. **Keep Draft until the infra PR is merged** — do not switch to Ready before that

```markdown
# Example — bottom of PR body
## Dependencies
- Depends on: example-org/infra-provisioning#26 (inventory variable additions)
```

### Attachment Methods

**Method 1: GitHub Issue/PR image upload (preferred)**
- Drag-and-drop or use `gh` CLI to upload
- Images are hosted on GitHub's CDN

**Method 2: Inline in PR body**
- Reference images committed to the repo (use `pr-assets/` directory)
- Clean up `pr-assets/` after PR is merged

### Commit Strategy

- **Do not commit screenshots to the repo** unless they serve as permanent documentation
- Use GitHub's image upload for PR-only visual evidence
- If screenshots must be committed (e.g., docs), use a dedicated `pr-assets/` directory and clean up after merge

## Opt-out

If the user says `--no-capture` or the change has no visual component, skip steps 5-6 and create a standard PR.
