## Description:

AnyoneCLI helps humans and AI agents create or look up terminal-style public profile pages through the anyonecli.com API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and AI agents use this skill to register a public AnyoneCLI profile, inspect the registration schema, or retrieve an existing profile as JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public, permanent profile data to a third-party service, and the artifact does not describe an edit or deletion flow.

Mitigation: Review the exact registration payload before submission, remove secrets, private email addresses, and internal URLs, and proceed only when the user accepts that the profile will be public and permanent.

## Reference(s):

- [AnyoneCLI Website](https://anyonecli.com)
- [AnyoneCLI Registration API](https://anyonecli.com/api/register)
- [ClawHub Skill Page](https://clawhub.ai/dongsheng123132/skills/anyonecli)
- [ClawHub Publisher Profile](https://clawhub.ai/user/dongsheng123132)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl. Registration can create public, permanent profile data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
