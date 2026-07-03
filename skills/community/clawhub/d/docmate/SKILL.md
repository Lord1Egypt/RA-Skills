---
name: docmate
description: "Documentation QA and repair skill for agent platforms: answer from project docs, verify stale implementation-sensitive claims against code, report documentation gaps, and optionally open GitHub PRs or GitLab MRs. This ClawHub package is an install notice; use the native curl installer for the runtime skill."
---

# DocMate

DocMate is a skill-first documentation QA and documentation repair assistant for agent platforms. It helps an agent answer from project documentation, verify docs against code when runtime behavior matters, report missing or stale documentation, and optionally repair confirmed documentation gaps through GitHub pull requests or GitLab merge requests.

DocMate is useful when you want an agent to:

- route documentation questions to configured repositories through `docmate.catalog.json`;
- distinguish docs-only answers from questions that must verify implementation details in code;
- produce concise gap reports with document evidence, code evidence, affected docs, and confidence;
- use `ask`, `auto`, or `off` modes for controlled documentation repair;
- repair docs in temporary git worktrees without dirtying the user's main checkout.

## Install

If you installed DocMate through ClawHub, this package is only a ClawHub page and install notice. It is not the DocMate runtime skill body.

Use the native installer from the README:

```bash
curl -fsSL https://raw.githubusercontent.com/wufei-png/DocMate/main/scripts/install.sh | bash
```

The native installer is required because DocMate is configured at install time. It installs the selected English or Chinese runtime skill, creates `references/docmate.catalog.json`, records the documentation repositories you want DocMate to use, and links the skill into the selected agent hosts.

Do not use this ClawHub package as the active DocMate skill. After running the curl installer, use the installed DocMate skill and edit the generated catalog path printed by the installer.
