## Description:

Create a tldr page from documentation URLs and command examples, requiring both URL and command name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to turn authoritative command documentation into concise tldr-style Markdown pages with practical command examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated tldr examples can include commands that reset, delete, clean, or force changes.

Mitigation: Review generated examples before running them, especially destructive command patterns.

Risk: Help-like flags can cause the skill to summarize its own instructions instead of creating a command page.

Mitigation: Provide a normal command name and authoritative documentation URL when requesting a new tldr page.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jhauga/skills/create-tldr-page)
- [git tldr reference example](https://raw.githubusercontent.com/jhauga/tldr/refs/heads/main/pages/common/git.md)
- [distrobox-create tldr reference example](https://raw.githubusercontent.com/jhauga/tldr/refs/heads/main/pages/linux/distrobox-create.md)
- [nmcli tldr reference example](https://raw.githubusercontent.com/jhauga/tldr/refs/heads/main/pages/linux/nmcli.md)
- [Git documentation example](https://git-scm.com/docs/git)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown tldr page with inline shell command examples; concise text guidance when required inputs are missing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires both an authoritative documentation URL and a command name; generated examples should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
