## Description:

Retrieves authoritative, up-to-date technical documentation, API references, configuration details, and code examples for any developer technology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kritsanan1](https://clawhub.ai/user/kritsanan1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to look up current documentation, API references, code examples, setup instructions, and version-specific behavior for external developer technologies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install or run a mutable third-party CLI for many technical tasks.

Mitigation: Review before installing, prefer a pinned ctx7 version in an isolated environment, and avoid global installation.

Risk: Documentation queries may expose credentials, personal data, proprietary code, or sensitive internal details.

Mitigation: Keep Context7 queries limited to non-sensitive technical intent and remove secrets or confidential material before lookup.

Risk: Fallback answers may rely on training knowledge when Context7 quota is exhausted or the user cannot authenticate.

Mitigation: Tell the user why Context7 was not used and clearly note that fallback information may be outdated.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits Context7 lookups to three attempts per question and directs agents to avoid sensitive query content.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
