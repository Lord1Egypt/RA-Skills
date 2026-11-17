## Description:

Use when an agent needs to call the FlowUs API through the FlowUs CLI, authenticate FlowUs, upload a file, create or update a page, query a database, search content, edit Markdown page content, or any task involving the `flowus` command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flowus](https://clawhub.ai/user/flowus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to work with authorized FlowUs content through the FlowUs CLI, including pages, blocks, databases, search, Markdown content, and files. It guides preflight checks, authentication, command discovery, and write confirmation before remote FlowUs changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward authenticated FlowUs API calls that access or change workspace content.

Mitigation: Approve installer, login, upload, and write actions only when the FlowUs identity, target page or database, and intended content are recognized.

Risk: Bearer tokens or saved credentials could be exposed if handled through chat, command arguments, logs, or files.

Mitigation: Use preconfigured credentials or an approved secret channel, redact credential output, and avoid passing tokens directly in commands.

Risk: An unverified installer or update could run code without official integrity assurance.

Mitigation: Use the official FlowUs CDN only after explicit approval, compare the installer with official checksum or signature data when available, and prefer manual installation if integrity data is unavailable.

Risk: Remote writes could update the wrong page, database, block, or file target.

Mitigation: Confirm the target, operation, expected impact, and content before writes; read current content first when feasible.

## Reference(s):

- [FlowUs CLI Skill Page](https://clawhub.ai/flowus/skills/flowus-skills)
- [FlowUs Publisher Profile](https://clawhub.ai/user/flowus)
- [FlowUs CLI Installer](https://cdn2.flowus.cn/flowus-cli/install)
- [FlowUs API Base URL](https://api.flowus.cn)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JSON CLI output for stable command results when FlowUs commands are run.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
