## Description:

Collect structured GitHub repository information from one or more known repository URLs. Do not use for GitHub code search or arbitrary webpages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to collect structured data for known public GitHub repository URLs through Dataify, monitor the asynchronous task, and return the final JSON result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository targets and task results are sent through Dataify using the user's API token.

Mitigation: Install only when this data flow is acceptable; keep the token in the environment and do not paste it into chat or generated outputs.

Risk: The package contains broader business, search, and web unlocker workflows beyond the narrow GitHub repository collection purpose.

Mitigation: Review the installed artifact and prefer a narrowed release that removes unrelated workflows before using it in sensitive environments.

Risk: The security guidance flags scoping and credential-handling issues, including GitHub URL validation, import path behavior, curl quoting, and reusable tokens in URLs.

Mitigation: Validate target URLs as GitHub repository URLs and resolve the flagged implementation issues before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-github-repository-by-repo-url)
- [Publisher Profile](https://clawhub.ai/user/dataify-server)
- [Tool Parameter Catalog](references/tool-params.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON results from completed Dataify tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DATAIFY_API_TOKEN environment variable and a public GitHub repository URL; default behavior waits for completion and returns the final collected result.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
