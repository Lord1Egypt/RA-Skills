## Description:

Scan AI agent skills, MCP servers, and plugins for security vulnerabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elliotllliu](https://clawhub.ai/user/elliotllliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to audit AI agent skills, MCP servers, plugins, and plugin archives before installation, publication, or CI/CD promotion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells users to run an unpinned remote npm package against local files.

Mitigation: Prefer an exact pinned package version and review the npm package and publisher before use.

Risk: Running the scanner with broad local access could expose files or environment secrets outside the intended scan target.

Mitigation: Run it in an isolated environment with read-only access to the intended target and no unnecessary credentials or environment secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elliotllliu/skills/agentshield-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON scan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scanner scores, findings, thresholds, and review guidance.]

## Skill Version(s):

0.5.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
