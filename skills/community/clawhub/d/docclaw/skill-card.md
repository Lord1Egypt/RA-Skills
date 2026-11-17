## Description:

DocClaw is a documentation skill for OpenClaw that combines live docs search, direct markdown fetch, and offline local-doc fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vibecodooor](https://clawhub.ai/user/vibecodooor)

### License/Terms of Use:


## Use Case:

Developers and engineers use DocClaw to answer OpenClaw documentation questions, find canonical docs links, fetch exact markdown pages, and fall back to local docs when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to docs.openclaw.ai and writes a local docs index or cache.

Mitigation: Install only where that network access and local caching are acceptable, and keep docs fetches restricted to docs.openclaw.ai.

Risk: Redirect handling could allow an off-domain request if every redirect target is not verified.

Mitigation: Require redirect targets to be verified before any off-domain request; this release also validates index-derived URLs and applies a trusted-host guard before fetches.

Risk: Fetched documentation can be stale or differ from installed OpenClaw runtime behavior.

Mitigation: Validate behavior-sensitive guidance with openclaw command help before acting on exact flags, keys, or paths.

## Reference(s):

- [DocClaw on ClawHub](https://clawhub.ai/vibecodooor/skills/docclaw)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include docs links, one-line relevance notes, fetched markdown paths, and local-doc search guidance.]

## Skill Version(s):

1.0.3 (source: SKILL.md version, CHANGELOG, server release evidence; released 2026-02-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
