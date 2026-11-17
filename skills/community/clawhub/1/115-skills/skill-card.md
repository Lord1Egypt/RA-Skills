## Description:

Manages 115 cloud-drive workflows through QR login, file browsing, search, share transfer, offline download, smart organization, cleanup recommendations, and capacity queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sukris](https://clawhub.ai/user/sukris)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a 115 cloud-drive account from an agent, including login, browsing, search, transfers, offline downloads, organization, cleanup advice, and storage checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores reusable 115 account cookies and uses them to access account data.

Mitigation: Install only if account access is acceptable, keep the cookie file private, and clear saved cookies after use or before sharing the environment.

Risk: An alternate web authentication path disables TLS certificate validation.

Mitigation: Avoid that web-auth flow until TLS validation is fixed; prefer authentication paths that preserve certificate validation.

Risk: File organization and file-operation features can immediately change cloud files.

Mitigation: Require explicit user confirmation and manually review source files, destination folders, and any dry-run results before enabling write operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sukris/skills/115-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style chat responses with file lists, status summaries, progress messages, and optional QR-code image delivery during login.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform cloud-file actions through the connected 115 account after user-directed workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
