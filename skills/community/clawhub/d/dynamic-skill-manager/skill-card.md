## Description:

Track and manage OpenClaw skill usage, find idle skills, and safely uninstall unused skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welkeyever](https://clawhub.ai/user/welkeyever)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to inspect installed skills, track skill usage, identify idle skills, and manage skill cleanup. It is intended for local skill lifecycle management in an OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The uninstall workflow can remove local OpenClaw skill directories without a direct confirmation step.

Mitigation: Verify the target skill directory manually before uninstalling and avoid running cleanup automatically.

Risk: The server security summary reports a verified symlink flaw that could remove the wrong or protected skill.

Mitigation: Fix the symlink handling issue before trusting the skill for routine removal, and use uninstall only after checking the resolved target directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/welkeyever/skills/dynamic-skill-manager)
- [OpenClaw Homepage](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and script-generated text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included Python script can update a local skill registry, append usage logs, archive metadata, and remove local skill directories when uninstall is run.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
