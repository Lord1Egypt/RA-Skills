## Description:

Monitors OpenClaw JSON logs for ERROR-level entries, records deduplicated findings, and suggests system-level fixes for gateway, port, and session issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amd5](https://clawhub.ai/user/amd5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor OpenClaw runtime errors, keep a deduplicated error record, and receive suggested checks or manual recovery steps for common gateway, port, and session failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw error logs may contain sensitive data and are copied into persistent workspace files.

Mitigation: Add redaction before writing error records and review retained workspace files for sensitive content.

Risk: Log-derived text is appended to Markdown files and may affect how reports render.

Mitigation: Escape Markdown table content and other user-controlled log fields before appending them.

Risk: The release declares an install hook for a script that is not present in the artifact.

Mitigation: Provide and document the install script or remove the postinstall hook before deployment.

Risk: Fixed diagnostic commands inspect local services and OpenClaw sessions.

Mitigation: Document the commands and run the skill with least necessary workspace and system access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/amd5/skills/error-monitor-fix)
- [Publisher Profile](https://clawhub.ai/user/amd5)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Console text or JSON, with Markdown error records appended to workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains deduplication and fix-log JSON files in the OpenClaw workspace.]

## Skill Version(s):

3.0.0 (source: server evidence, skill.json, _meta.json, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
