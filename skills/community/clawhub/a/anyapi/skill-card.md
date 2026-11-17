## Description:

AnyAPI lets agents retrieve live, normalized data from social, search, marketplace, and bot-blocked web sources through CLI, MCP, REST, or SDK interfaces with USD pay-per-request billing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kev1n](https://clawhub.ai/user/kev1n)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use AnyAPI when a task needs structured live data from third-party platforms, search results, profiles, posts, reviews, transcripts, ads, or pages that block direct fetching. It supports agent workflows through catalog search, API schema inspection, quoted and billed API calls, result shaping, SDK integration, and local result review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route prompts, targets, and retrieved data through an external hosted API provider.

Mitigation: Use it only for tasks where sending that data to AnyAPI is acceptable, and require approval before sensitive target research.

Risk: The workflow can trigger signup, login, paid calls, MCP registration, bug reports, or feedback submission.

Mitigation: Require explicit human approval before account actions, paid/external calls, MCP registration, or submissions back to the provider.

Risk: The artifact recommends installing and running `anyapi-cli@latest`, which can execute an unpinned package version.

Mitigation: Prefer a pinned and reviewed CLI version before installation or execution.

Risk: The CLI may persist credentials and full API results in local configuration and `.anyapi/` files.

Mitigation: Clean up stored result files and local credentials when the task is complete.

## Reference(s):

- [SDK and Direct HTTP Reference](references/sdks.md)
- [AnyAPI Documentation](https://getanyapi.com/docs)
- [AnyAPI Documentation Index](https://getanyapi.com/docs/llms.txt)
- [AnyAPI OpenAPI Document](https://api.getanyapi.com/openapi.json)
- [AnyAPI CLI Repository](https://github.com/getanyapi-com/cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, JSON API responses, and local JSON result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API calls may create .anyapi result files, use local credential configuration, and report USD cost fields such as costUsd.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
