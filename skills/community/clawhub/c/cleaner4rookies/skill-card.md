## Description:

OpenClaw temporary file cleanup tool that scans ~/.openclaw/workspace/ and previews, archives, or deletes matching files according to configurable rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beforesun](https://clawhub.ai/user/beforesun)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to manage temporary workspace files with a dry-run preview, archival rules, deletion rules, and optional scheduled cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cleanup behavior can delete or move workspace files when --force or scheduled execution is used.

Mitigation: Review cleaner.yaml before use, keep dry_run enabled, and run a manual preview before using --force or cron.

Risk: The documented whitelist should not be relied on until fixed.

Mitigation: Avoid force execution for important workspaces and confirm protected files are outside the matching cleanup rules.

Risk: Archived files may still be needed later.

Mitigation: Inspect cleaner-archive before deleting it or changing archive retention practices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beforesun/skills/cleaner4rookies)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default dry-run preview with optional --force execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
