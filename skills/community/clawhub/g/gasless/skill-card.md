## Description:

Gasless is presented as a gasless blockchain analysis skill, but the release evidence shows it ships a local record-management shell tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers can use this skill to inspect or run a simple local command-line record manager while treating its blockchain-analysis claims as unverified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised gasless blockchain analysis purpose does not match the shipped local record-manager behavior.

Mitigation: Validate the behavior against the intended use case before deployment and do not rely on it for protocol or on-chain security analysis.

Risk: Commands can mutate local files by adding, removing, exporting, and changing configuration data.

Mitigation: Run only after review, avoid sensitive entries, use a controlled GASLESS_DIR, and do not execute with elevated privileges.

Risk: Exports are written to the current working directory.

Mitigation: Run from a trusted directory and review generated export files before sharing or committing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/gasless)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, remove, search, and export local journal/config files under GASLESS_DIR or ~/.gasless.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
