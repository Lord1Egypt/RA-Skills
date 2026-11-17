## Description:

Do App Store Optimization (ASO) with the ASO Suite CLI across iPhone, iPad, Mac, Apple TV, Apple Watch, and VisionOS by finding keywords with popularity/difficulty data, tracking keyword position over time, annotating tracked keywords with notes and global color-coded tags, and monitoring ratings, editorial features, and chart appearances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hesselbom](https://clawhub.ai/user/hesselbom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, app marketers, and ASO practitioners use this skill to operate the ASO Suite CLI for keyword research, rank tracking, tags, notes, related apps, events, chart rankings, editorial features, and ratings across Apple platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned global npm executable.

Mitigation: Use a pinned, reviewed asosuite package version and avoid administrator privileges for global installation.

Risk: The CLI stores a long-lived access token in ~/.asosuite/config.json.

Mitigation: Treat the config file as sensitive, restrict local file permissions, and remove the token when access is no longer needed.

Risk: Several commands can modify or delete ASO account data.

Mitigation: Review commands that remove, delete, clear, untrack, or unplan ASO data before execution.

## Reference(s):

- [ASO Suite](https://www.asosuite.com/)
- [ASO Suite ClawHub Skill](https://clawhub.ai/hesselbom/skills/asosuite)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON]

**Output Format:** [Markdown with inline bash code blocks and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Most data commands should be run with --json; login and logout do not support JSON output.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
