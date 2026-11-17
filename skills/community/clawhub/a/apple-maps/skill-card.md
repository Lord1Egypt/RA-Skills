## Description:

Search places, open routes, and run Apple Maps workflows on macOS using local CLI commands and shortcut automation with explicit safety checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Mac users and agents use this skill to search Apple Maps for places, nearby categories, addresses, routes, and reusable map links while applying confirmation gates for sharing, routing, and bulk opens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided map queries could be interpolated unsafely into shell commands.

Mitigation: Percent-encode query values and pass the generated Apple Maps URL as a separate process argument to `open -a Maps`.

Risk: Map queries, route origins, destinations, or generated share links may disclose location intent.

Mitigation: Use minimal query strings, preview generated URLs, and require explicit approval before opening sensitive searches, sharing links, or launching multiple map links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/apple-maps)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Apple Maps endpoint](https://maps.apple.com)
- [Skill homepage](https://clawic.com/skills/apple-maps)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Apple Maps URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended for macOS and should preview generated Apple Maps URLs before launch.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
