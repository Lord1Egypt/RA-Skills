## Description:

Write and run safe AppleScript automation on macOS with dictionary discovery, robust quoting, and deterministic read-first workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and automation users use this skill to design, run, and troubleshoot macOS AppleScript workflows for app control, data extraction, and scripted UI actions while applying read-before-write and confirmation safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local AppleScript can control named macOS applications and may change app data if the user authorizes write actions.

Mitigation: Keep confirmation gates enabled, classify scope before execution, run a pre-read to confirm target identity, and verify state after writes.

Risk: The documented process-list probe is broader than many automation tasks require.

Mitigation: Prefer target-specific permission checks or app-specific read-only probes before running broader System Events process queries.

Risk: Unescaped user text in generated AppleScript can cause syntax errors or affect unintended command targets.

Mitigation: Use deterministic quoting patterns for dynamic values and reject input when command boundaries are unclear.

## Reference(s):

- [AppleScript Skill Page](https://clawhub.ai/ivangdavila/skills/applescript)
- [AppleScript Homepage](https://clawic.com/skills/applescript)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with AppleScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for local macOS automation with explicit confirmation gates for writes, deletes, and bulk changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
