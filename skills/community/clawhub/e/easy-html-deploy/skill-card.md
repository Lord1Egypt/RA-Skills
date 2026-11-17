## Description:

Deploy a single self-contained HTML page to htmlcode.fun for instant sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[520xiaomumu](https://clawhub.ai/user/520xiaomumu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish, inspect, and manage single-file HTML pages on htmlcode.fun when fast sharing is more important than full project hosting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML files are uploaded to and published on htmlcode.fun.

Mitigation: Deploy only HTML that is appropriate to send to and publish on that service, and do not include secrets or private data.

Risk: Version-management actions can overwrite, unpublish, delete, or switch public versions.

Mitigation: Inspect the target code and version first; append a new version instead of changing liked or uncertain versions.

Risk: htmlcode.fun is not a full static hosting platform for complex applications.

Mitigation: Use it for single-file HTML pages, and choose a dedicated app host when a project needs build steps, backend services, custom domains, or asset pipelines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/520xiaomumu/skills/easy-html-deploy)
- [htmlcode.fun guide](https://www.htmlcode.fun/s/htmlcode-fun-guide)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and returned deployment URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return code, url, detailUrl, versionUrl, versionNumber, qrCode, and preserveHint fields from htmlcode.fun responses.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
