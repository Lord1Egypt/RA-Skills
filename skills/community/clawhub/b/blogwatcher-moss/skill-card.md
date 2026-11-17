## Description:

Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memoryf](https://clawhub.ai/user/memoryf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content-monitoring users can use this skill to install and operate the blogwatcher CLI for tracking RSS/Atom feeds, scanning for new posts, and managing local article state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command uses an unpinned third-party Go module, so future upstream changes can alter the executable installed by the skill.

Mitigation: Use a pinned, reviewed module version when possible and review the upstream project before installing or updating the CLI.

Risk: Scanning feeds contacts user-provided blog or RSS/Atom URLs and stores local tracking state through the blogwatcher CLI.

Mitigation: Verify feed URLs before adding them and use the CLI only in environments where outbound network access and local tracking data are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/memoryf/skills/blogwatcher-moss)
- [Blogwatcher CLI Homepage](https://github.com/Hyaxia/blogwatcher)
- [Publisher Profile](https://clawhub.ai/user/memoryf)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of the external blogwatcher CLI and may result in local tracking data managed by that CLI.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
