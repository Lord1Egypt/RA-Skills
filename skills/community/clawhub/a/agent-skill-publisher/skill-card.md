## Description:

End-to-end workflow for publishing agent skills to GitHub, ClawdHub, and skills.sh, including repo creation, topic tagging, ClawdHub publishing, skills.sh index requests, and installation verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bryant24hao](https://clawhub.ai/user/bryant24hao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to publish agent skills across GitHub, ClawdHub, and skills.sh, with pre-flight checks, registry submission, and installation verification in one workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through public account-changing actions such as creating repositories, publishing releases, and opening index request issues.

Mitigation: Use minimal credentials, verify the target skill directory, and require explicit confirmation before each public publish or write step.

Risk: The workflow may run unpinned npx CLIs and describes patching local executable CLI code for a ClawdHub publish workaround.

Mitigation: Inspect CLI versions and exact file changes before execution, and avoid the patch workaround unless the user approves the specific change.

Risk: Publishing the wrong directory or files could expose secrets, user-specific paths, or unintended content.

Mitigation: Run the documented pre-flight checks and secret/path scans on a clean skill directory before any commit or publish operation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bryant24hao/skills/agent-skill-publisher)
- [Project Homepage](https://github.com/bryant24hao/skill-publisher)
- [GitHub CLI](https://cli.github.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify repository files, public GitHub repositories, ClawdHub releases, skills.sh index issues, and local npm cache files when the user approves those workflow steps.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
