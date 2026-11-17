## Description:

Organize Chrome bookmarks through OpenClaw with preview, explicit confirmation, apply, undo, and a local Chrome executor bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoshidefeng](https://clawhub.ai/user/xiaoshidefeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan conservative Chrome bookmark cleanup, preview proposed folder and bookmark changes, and execute approved changes through a local Chrome bridge with undo support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants an unpacked Chrome extension access to browser bookmarks and uses a localhost bridge to read, validate, apply, and undo bookmark changes.

Mitigation: Use a low-risk Chrome profile or export a bookmark backup before use, review every preview carefully, and apply changes only after explicit confirmation.

Risk: The local bridge and extension messaging paths are under-protected, so another local process or extension may be able to interact with exposed control paths.

Mitigation: Run the bridge only while actively using the skill, stop it afterward, and prefer future versions that add authentication and sender validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoshidefeng/skills/bookmark-organize)
- [Chrome Executor Extension README](artifact/apps/chrome-executor-extension/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured bookmark action plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans require preview and explicit confirmation before bookmark mutation; apply and undo results should be reported only after local bridge verification.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter and package.json report 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
