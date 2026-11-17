## Description:

GetSkill helps OpenClaw agents search, install, update, list, and configure skills from the getskill.work service by using CLI commands, Git repositories, and local OpenClaw skills directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlei9](https://clawhub.ai/user/zlei9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to discover remote skills, install or update them into an OpenClaw environment, inspect local skill paths, manage cached repositories, and configure the API endpoint used for skill lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update remote skills into the active OpenClaw environment with limited provenance.

Mitigation: Use it only with trusted package sources, trusted API endpoints, and reviewed repositories; inspect fetched skill contents before enabling them.

Risk: Install and update workflows can copy remote repository contents into local skills directories.

Mitigation: Require explicit confirmation before overwriting existing skills, and prefer pinned versions or reviewed commits for remote content.

Risk: The setup guidance may involve global npm or pnpm installation of the getskill CLI.

Mitigation: Avoid elevated global installs where possible and verify the npm package before installation.

## Reference(s):

- [ClawHub getskill Skill Page](https://clawhub.ai/zlei9/skills/getskill)
- [Publisher Profile](https://clawhub.ai/user/zlei9)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline bash commands and command-output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in local OpenClaw skill files being installed, updated, listed, or left unchanged depending on the selected CLI operation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
