## Description:

Use `apix` to search, browse, and execute API endpoints from local markdown vaults. Use this skill to discover REST API endpoints, inspect request/response schemas, and make HTTP calls directly from the terminal without leaving your environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dngpng](https://clawhub.ai/user/dngpng)

### License/Terms of Use:


## Use Case:

Developers, engineers, and agent operators use this skill to discover REST API endpoints, inspect request and response schemas, import OpenAPI specs, and make terminal-based HTTP calls from local API documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The curl-to-shell installer can execute remote code before the user has independently verified the release.

Mitigation: Prefer the Homebrew installation path or a verified release, and review the installer source before running it.

Risk: `apix call` can trigger state-changing API requests.

Mitigation: Before running state-changing calls, check the endpoint, method, authentication, payload, and expected side effects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dngpng/skills/apix)
- [apix installer](https://apix.sh/install)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents toward concise endpoint inspection before executing API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
