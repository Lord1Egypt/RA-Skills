## Description:

Analyze cex operations. Use when you need to understand cex mechanisms, evaluate protocol security, or reference on-chain concepts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can invoke the skill for CEX-oriented reference workflows, but the inspected artifact primarily provides shell commands for maintaining local entries, searching them, exporting them, and viewing simple statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found a scope mismatch: the skill is presented as CEX or blockchain analysis, while the artifacts implement a persistent local data manager.

Mitigation: Review the commands and expected behavior before installation, and do not rely on the artifact as substantive CEX security analysis without independent validation.

Risk: The security review states that the artifact can write, delete, and export local entries and has unsafe shell handling in the config update path.

Mitigation: Run it only in a contained environment with non-sensitive test data until the publisher fixes the scope mismatch and shell-handling issues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/cex)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell command examples and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, modify, delete, or export local JSONL and CSV files under the configured CEX data directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
