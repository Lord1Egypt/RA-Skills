## Description:

Consensus is a third-party CLI-oriented skill presented for consensus analysis, while server security evidence reports that its bundled script behaves as a local record manager.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users may use this skill as a CLI helper for recording, listing, searching, exporting, and configuring local consensus-related notes. It should not be relied on as a protocol-security or on-chain consensus analysis tool without review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is presented as blockchain consensus analysis, but server security evidence says the script manages local records instead.

Mitigation: Review the skill before installation and do not use its output as consensus, protocol-security, or on-chain analysis without independent validation.

Risk: The script writes, removes, and exports local data and can create export files in shared or sensitive directories.

Mitigation: Run it only in an intended working directory, set CONSENSUS_DIR to a non-sensitive location, and review files before sharing exports.

Risk: Server security guidance identifies the config command as unsafe with untrusted keys or values and notes stored/exported data may be malformed unless fixed.

Mitigation: Use trusted config keys and values only, avoid passing unsanitized input, and validate stored or exported records before downstream use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/consensus)
- [Publisher profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration]

**Output Format:** [Plain text CLI output with JSONL, JSON, or CSV files for stored and exported records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local data under CONSENSUS_DIR or ~/.consensus and may export files into the current working directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
