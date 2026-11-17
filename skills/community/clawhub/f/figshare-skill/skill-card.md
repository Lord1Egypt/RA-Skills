## Description:

Helps agents search Figshare, download public article files, manage account articles, and create or upload Figshare research outputs through the Figshare v2 REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and research-support teams use this skill to discover public Figshare content, download article files, and manage authenticated article, collection, project, upload, and publishing workflows from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated helper scripts can create, update, upload, or publish Figshare account content and may expose a Figshare token if run in an unsafe environment.

Mitigation: Use the least-privileged Figshare token possible, keep the token out of logs and shared shells, and require explicit user confirmation before account-changing operations.

Risk: The download helper may overwrite local files when saving article files into an existing workspace.

Mitigation: Download into a new or reviewed output directory and sanitize or inspect target filenames before using the helper on valuable workspaces.

Risk: The new-version helper publishes after uploading, which can make the new Figshare version public when that is not intended.

Mitigation: Avoid the new-version helper unless publication is explicitly intended, and review the article ID and file path before execution.

## Reference(s):

- [Skill homepage](https://github.com/Agents365-ai/figshare-skill)
- [ClawHub skill listing](https://clawhub.ai/agents365-ai/skills/figshare-skill)
- [Figshare API documentation](https://docs.figshare.com/)
- [Figshare token management](https://figshare.com/account/applications)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON/curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call bundled shell helpers for Figshare download, upload, and new-version workflows when the user confirms account-changing actions.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
