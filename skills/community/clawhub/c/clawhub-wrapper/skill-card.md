## Description:

Download and install skills from ClawHub (https://clawhub.ai). Use when user wants to browse, search, or download skills from the ClawHub skill registry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[douglarek](https://clawhub.ai/user/douglarek)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search the ClawHub registry and install selected skills by slug or ClawHub URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs remote ClawHub packages into an active local skills directory without enough validation or containment.

Mitigation: Use only trusted ClawHub packages, review package contents before enabling them, avoid untrusted slugs or URLs, and prefer versions that validate slugs, verify package integrity, stage downloads for review, and ask before overwriting installed skills.

## Reference(s):

- [ClawHub](https://clawhub.ai)
- [ClawHub skill page](https://clawhub.ai/douglarek/skills/clawhub-wrapper)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Text]

**Output Format:** [Markdown guidance with shell command invocations and terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download remote zip packages, install files under the user's local agent skills directory, and display registry metadata.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
