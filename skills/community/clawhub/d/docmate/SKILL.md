---
name: docmate
description: "Documentation QA and repair skill for agent platforms: answer from project docs, verify stale implementation-sensitive claims against code, report documentation gaps, and optionally open GitHub PRs or GitLab MRs. This ClawHub package is an install notice; follow the official repository documentation for the runtime skill."
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

This ClawHub package is an install notice, not the DocMate runtime skill body. DocMate is configured at installation time, so use the official repository's installation documentation and review the current source before making any local agent-host changes.

Official repository: https://github.com/wufei-png/DocMate

The native setup selects an English or Chinese runtime skill, creates `references/docmate.catalog.json`, records the documentation repositories you want DocMate to use, and links the skill into the selected agent hosts.

After installation, use the installed DocMate skill and edit the generated catalog path printed by the installer.
