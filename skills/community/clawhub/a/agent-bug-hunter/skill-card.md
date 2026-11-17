## Description:

Imported specialist agent skill for bug hunter. Use when requests match this domain or role.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nntrivi2001](https://clawhub.ai/user/nntrivi2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to guide proactive bug hunting, root-cause investigation, security and performance checks, and verification of bug fixes before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages an active bug-hunting posture with broad activation triggers.

Mitigation: Confirm the intended repository, scope, and allowed actions before running broad scans or applying fixes.

Risk: The artifact references local files and companion debugging skills that may not exist in the target environment.

Mitigation: Verify referenced resources before use and replace local path assumptions with available project documentation or explicit user-provided files.

Risk: Generated fix proposals or shell commands could change project behavior if applied without review.

Mitigation: Review proposed changes, run relevant tests, and verify the original issue is reproduced and resolved before declaring a fix complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nntrivi2001/skills/agent-bug-hunter)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Code, Shell commands, Markdown]

**Output Format:** [Markdown text with code, shell command, and verification guidance as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose code changes, diagnostic commands, test runs, and review checklists; users should review actions before applying them.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
