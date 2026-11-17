## Description:

Send local files, uploaded attachments, or URLs for e-signature with Nota Sign while handling credential setup, PROD or UAT environment selection, file validation, signer collection, and envelope execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notasign](https://clawhub.ai/user/notasign)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send supported documents or URLs to one or more signers through Nota Sign. The workflow helps collect signer details, configure Nota Sign credentials, select PROD or UAT, validate files, and initiate the envelope.

### Deployment Geography for Use:

Global, subject to the supported Nota Sign server regions CN, AP1, AP2, and EU1.

## Known Risks and Mitigations:

Risk: The skill stores a long-lived Nota Sign private key in plaintext configuration.

Mitigation: Store credentials only in the home Nota Sign config with restrictive file permissions, avoid project-local config files, and do not echo private keys in responses.

Risk: The runtime fallback can fetch unpinned npm tooling during execution.

Mitigation: Prefer a pinned dependency workflow or a preinstalled Node.js 18+ and tsx environment; review before using live npx downloads.

Risk: The workflow handles documents, signer data, and remote document URLs sent to Nota Sign.

Mitigation: Use only documents and signer data authorized for Nota Sign, and avoid submitting arbitrary internal or private-network URLs as document inputs.

## Reference(s):

- [Nota Sign ClawHub skill page](https://clawhub.ai/notasign/skills/esign)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns an envelope ID and send summary on success; surfaces validation or API errors on failure.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
