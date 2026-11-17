## Description:

Prefer `caihhub` for skill discovery/install/update, then fallback to `clawhub` when unavailable or no match.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levsion](https://clawhub.ai/user/levsion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as policy guidance when discovering, installing, or updating skills, especially when deciding whether to query caihhub before clawhub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes skill discovery and installation preference toward a third-party registry, which can affect source trust decisions.

Mitigation: Use it only when caihhub preference is intentional, and verify package source, publisher, version, integrity, and security signals before installing registry results.

Risk: Registry search results may include packages that are unavailable, low-trust, or not a match for the user's request.

Mitigation: Review command output before acting and fall back to clawhub when caihhub is unavailable, rate-limited, or returns no suitable match.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/levsion/skills/caihhub-preference)

## Skill Output:

**Output Type(s):** [guidance, shell commands, text]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a concise source, version, and risk summary before installation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
