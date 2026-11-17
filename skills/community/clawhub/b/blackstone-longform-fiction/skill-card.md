## Description:

黑石写作助手·中长篇小说版 helps fiction writers turn ideas, outlines, characters, and existing chapters into long-form story plans, draft prose, revisions, and continuity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jony4](https://clawhub.ai/user/jony4)

### License/Terms of Use:

MIT-0

## Use Case:

External fiction authors use this agent to develop medium-form, long-form, web-serial, and serialized fiction from early ideas through outlines, character work, chapter drafting, revision, polishing, and continuity review. It can work locally with author-provided files and can optionally use the Blackstone cloud story memory when the author opts in.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store a long-lived Blackstone cloud access token in local WorkBuddy configuration.

Mitigation: Install only when the Blackstone service is trusted, avoid exposing local configuration, do not display full tokens, and revoke affected devices from the Blackstone connect page.

Risk: The skill includes an update flow that can replace its own files after user approval.

Mitigation: Review update prompts carefully, accept updates only from blackstone.wansu.tech, require checksum verification, and do not update unless the author explicitly agrees.

Risk: Cloud story memory can upload author content and incur per-call charges when used.

Mitigation: Keep cloud mode on ask by default, explain each upload or paid cloud-memory action before it runs, and enable automatic sync only after an explicit user choice.

Risk: The skill may read, create, or modify manuscript files during writing workflows.

Mitigation: Read only user-specified files needed for the task and confirm target files and edit ranges before creating or modifying local manuscript content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jony4/skills/blackstone-longform-fiction)
- [Publisher Profile](https://clawhub.ai/user/jony4)
- [Blackstone Website](https://blackstone.wansu.tech)
- [Blackstone Longform Edition](https://blackstone.wansu.tech/longform)
- [Quickstart](references/quickstart.md)
- [Security Boundaries](references/security.md)
- [Cloud Story Memory](references/mcp.md)
- [Account and Device Authorization](references/account.md)
- [Local File Management](references/local-files.md)
- [Pricing](references/pricing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with optional code blocks, shell commands, configuration snippets, and local file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or edit author-approved local manuscript files and may initiate user-approved Blackstone cloud memory, account, billing, feedback, or update flows.]

## Skill Version(s):

1.3.3 (source: frontmatter, VERSION.md, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
