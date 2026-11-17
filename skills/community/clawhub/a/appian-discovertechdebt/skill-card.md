## Description:

Scans an Appian application export for objects whose SAIL definitions reference outdated versioned functions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solarspiker](https://clawhub.ai/user/solarspiker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Appian application maintainers use this skill before releases or during periodic audits to find deprecated SAIL function references that should be updated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Appian API key with permission to export applications.

Mitigation: Use the least-privileged Appian API key that can perform the intended export and install only where that access is acceptable.

Risk: Exported Appian application ZIPs are saved locally after the scan.

Mitigation: Store exports only in approved locations and delete retained ZIPs when they are no longer needed.

Risk: The downloaded package ZIP and filename come from the Appian export response.

Mitigation: Prefer a hardened version that validates the download origin and sanitizes or ignores remote filenames before writing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/solarspiker/skills/appian-discovertechdebt)

## Skill Output:

**Output Type(s):** [text, shell commands, analysis]

**Output Format:** [Plain text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Appian application UUID and Appian API environment variables; may write exported application ZIPs locally.]

## Skill Version(s):

1.7.0 (source: server release metadata and scripts/index.js header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
