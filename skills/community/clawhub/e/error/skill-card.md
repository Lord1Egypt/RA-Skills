## Description:

Error handling reference — error types, exception patterns, HTTP status codes, retry strategies, and observability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a quick reference for designing error handling, selecting HTTP status codes, implementing retry and circuit-breaker strategies, logging failures, and debugging production issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an ERROR_DIR configuration note even though the inspected artifact does not use that directory.

Mitigation: Review the configuration note during publication and either document the intended behavior or remove the unused setting to avoid misleading installers.

Risk: The skill provides static implementation guidance that may not match every production system or regulatory requirement.

Mitigation: Treat the output as reference material and have engineers review recommendations before applying them to production systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/error)
- [Publisher profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reference material and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static guidance printed by a local bash helper; evidence.security reports no file, credential, or network access.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
