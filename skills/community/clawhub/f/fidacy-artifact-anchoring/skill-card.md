## Description:

Prove a document existed and was never altered, without uploading it anywhere. Use when your agent produces or receives contracts, invoices, claim documents, prescriptions, reports or images whose integrity may be questioned later. Hashes the file locally, anchors only the 64-hex digest through Fidacy onto a Bitcoin-checkpointed audit chain, and returns a signed receipt anyone can verify publicly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fidacy](https://clawhub.ai/user/fidacy)

### License/Terms of Use:

Apache License

## Use Case:

Developers, legal operations teams, finance teams, insurance teams, and other external users can use this skill to anchor final documents or media by local SHA-256 hash and later verify whether the artifact still matches the anchored digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned third-party MCP package locally against files they choose.

Mitigation: Use a pinned and reviewed package version, limit filesystem access to intended artifacts, and run it only for files appropriate for Fidacy processing.

Risk: The workflow requires a Fidacy engine API key for anchoring.

Mitigation: Use a narrowly scoped, revocable API key and rotate or revoke it if exposure is suspected.

## Reference(s):

- [Fidacy Artifact Anchoring on ClawHub](https://clawhub.ai/fidacy/skills/fidacy-artifact-anchoring)
- [Fidacy Web Verifier](https://fidacy.com/verify)
- [Fidacy Artifact Verification API](https://api.fidacy.com/v1/verify/artifact?sha256=<hex>)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tool names, command snippets, verification URLs, receipt details, and status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Anchoring returns a signed receipt and status; verification returns match or mismatch status for a file path or SHA-256 digest.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
