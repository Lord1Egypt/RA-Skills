## Description:

Multi-source deep research agent. Searches the web, synthesizes findings, and delivers cited reports. No API keys required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raidan-ai](https://clawhub.ai/user/raidan-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run multi-source web research, compare sources, and produce concise or full cited research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can fetch arbitrary URLs while researching.

Mitigation: Review URLs before fetching, use safer URL-fetching controls, and avoid substituting untrusted URLs into shell commands.

Risk: The workflow can save research reports locally.

Mitigation: Confirm the destination path before writing reports, especially in shared storage or environments with sensitive local files.

Risk: The security verdict is suspicious for environments with access to private networks, cloud metadata, sensitive local files, or shared storage.

Mitigation: Review before installing in those environments and restrict network and filesystem access where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raidan-ai/skills/deep-research-pro-1-0-2)
- [Project homepage listed in skill metadata](https://github.com/paragshah/deep-research-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown reports with inline citations and optional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save longer research reports as local Markdown files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
