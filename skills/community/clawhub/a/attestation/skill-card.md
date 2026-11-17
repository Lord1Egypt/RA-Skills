## Description:

Analyze attestation operations. Use when you need to understand attestation mechanisms, evaluate protocol security, or reference on-chain concepts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use this skill for command-oriented attestation note tracking, status checks, search, export, and configuration. Reviewers should treat it as a local datastore utility rather than relying on it for protocol analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill is mislabeled: it claims attestation analysis, while its behavior is a local record store that can persist, delete, export, and reconfigure data.

Mitigation: Use it only as a local note/config datastore and review the commands before relying on generated records or exported data.

Risk: The security guidance warns against storing sensitive attestation or protocol data until purpose, storage behavior, deletion/export controls, and input handling are fixed.

Mitigation: Avoid sensitive entries, set ATTESTATION_DIR deliberately, and inspect local data and exports before sharing or retaining them.

## Reference(s):

- [ClawHub Attestation skill page](https://clawhub.ai/bytesagain1/skills/attestation)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Plain text and command output, with optional JSONL or CSV export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists local records under ~/.attestation by default or ATTESTATION_DIR when configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
