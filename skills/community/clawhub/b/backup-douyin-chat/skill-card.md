## Description:

Safely operate a local Douyin chat backup workflow to log in by QR code, list conversations, create full or incremental backups, export JSON, JSONL, or HTML, verify completeness, and optionally download encrypted image media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hilper](https://clawhub.ai/user/hilper)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a local Douyin chat backup workflow for conversations visible to their own account, export readable or machine-readable archives, verify completeness, and handle media while preserving privacy boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles private chat history, media, account state, local databases, and exports.

Mitigation: Keep generated data local, protect files with owner-only permissions, avoid printing or sharing message bodies and credentials, and upload exports only after a separate explicit user request.

Risk: QR login and an undocumented Douyin endpoint may fail, change behavior, or trigger platform risk controls.

Mitigation: Use only conversations visible to the user's own account, require explicit risk-acceptance flags, and report exact blockers instead of attempting unsupported workarounds.

Risk: The inspected artifact references helper scripts that are not included in the artifact.

Mitigation: Run the read-only doctor check, review the actual local tool scripts before use, and stop if the expected installation is missing.

Risk: Media backfill may download from Douyin or CDN endpoints and signed media URLs can expire.

Mitigation: Run a dry run before media downloads, require the media-download risk flag, verify local media files before reporting success, and never print signed URLs or decryption keys.

## Reference(s):

- [Server-resolved GitHub provenance: hilper/douyin-chat-exporter](https://github.com/hilper/douyin-chat-exporter/tree/main/skills/backup-douyin-chat)
- [ClawHub skill page: Backup Douyin Chat](https://clawhub.ai/hilper/skills/backup-douyin-chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local file path reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exact blockers, aggregate message and media counts, completeness status, and clickable local export paths; should not include message bodies, cookies, signed URLs, or decryption keys.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
