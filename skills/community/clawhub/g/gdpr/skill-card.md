## Description:

Audit GDPR compliance, generate privacy policies, and document data flows. Use when auditing practices, drafting policies, or checking consent flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, privacy teams, and compliance operators use this skill to record GDPR compliance activities, audit findings, consent changes, retention events, and policy updates in local command-line logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compliance notes may be retained in local plaintext logs and exports.

Mitigation: Use the skill only for non-secret audit notes and protect the local data directory and exported files according to internal retention and access-control requirements.

Risk: Users may enter passwords, tokens, private keys, full personal identifiers, or regulated records into stored command entries.

Mitigation: Do not enter secrets or regulated personal data unless the environment has appropriate privacy controls and plaintext storage is acceptable.

Risk: The security verdict is suspicious because the GDPR-branded logger lacks stronger privacy controls for sensitive compliance text.

Mitigation: Review the skill before installing and confirm that its local logging behavior fits the intended compliance workflow.

## Reference(s):

- [Gdpr Skill on ClawHub](https://clawhub.ai/bytesagain3/skills/gdpr)
- [bytesagain3 Publisher Profile](https://clawhub.ai/user/bytesagain3)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Files, Configuration]

**Output Format:** [Command-line text plus local plaintext logs and optional JSON, CSV, or TXT exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores command entries under ~/.local/share/gdpr/ and can export accumulated records.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
