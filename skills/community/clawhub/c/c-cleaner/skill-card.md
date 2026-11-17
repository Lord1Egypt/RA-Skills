## Description:

c-cleaner helps an agent analyze Windows C-drive storage, identify temporary files, caches, large files, and migration candidates, and guide or execute cleanup workflows with user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjflydudu](https://clawhub.ai/user/jjflydudu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support staff, and Windows power users can use this skill to inspect C-drive disk usage, find large or cleanable files, generate cleanup recommendations, and run cautious cleanup steps after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup actions can permanently delete files, including cache contents and Recycle Bin contents in aggressive mode.

Mitigation: Use scan or dry-run mode first, inspect the exact paths and item list, and avoid --yes or aggressive mode unless the user explicitly accepts the deletion impact.

Risk: The security summary notes that promised preview, backup, and confirmation safeguards are not fully enforced by the cleanup script.

Mitigation: Require a preview-before-clean workflow, remove or restrict confirmation bypass, and add an exact deletion manifest before relying on automated cleanup.

Risk: Reports can expose local filesystem paths and storage details that may be sensitive.

Mitigation: Review generated reports before sharing them and redact user names, project names, and sensitive paths.

## Reference(s):

- [C-drive cleanup guide](references/cleanup-guide.md)
- [ClawHub skill page](https://clawhub.ai/jjflydudu/skills/c-cleaner)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline PowerShell or Python commands and optional JSON reports from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include filesystem paths, estimated cleanable space, cleanup summaries, and follow-up optimization recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
