## Description:

Creates Dianxiaobao Amazon pending-product drafts from 1688 product offers by checking credentials, selecting stores, mapping categories and attributes, processing images, assembling listing payloads, and saving drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and e-commerce operators use this skill to turn a 1688 offer into a Dianxiaobao Amazon pending draft for later review and publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Store credentials can be exposed through unnecessary command-line paths.

Mitigation: Prefer the documented session-based commands, avoid direct encryptedCode command-line usage, and rotate credentials if they may have appeared in shell history or logs.

Risk: Product images and listing data are sent to Dianxiaobao, AlphaShop, and 1688 image-gateway services.

Mitigation: Install and run the skill only when that data sharing is acceptable for the products and stores involved.

Risk: Local .env and /tmp session files may contain sensitive operational data.

Mitigation: Protect local environment files and session directories, and remove or restrict them after the listing workflow is complete.

## Reference(s):

- [Amazon Listing Chain Reference](references/amazon-listing-chain.md)
- [Amazon Listing Troubleshooting](references/troubleshooting.md)
- [ClawHub skill listing](https://clawhub.ai/1688aiinfra/skills/1688-distribution-amazon)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local session files under /tmp and draft payload artifacts during execution.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact metadata reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
