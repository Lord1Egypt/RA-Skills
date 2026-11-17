## Description:

Use this skill for Feishu/Lark OpenAPI integration work, including OpenClaw Feishu bot setup, credential configuration outside the skill, Docx document reads and writes, user-owned document creation, block editing, and Sheets, Base, Wiki, Drive, or IM API operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luz404](https://clawhub.ai/user/luz404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect agents to Feishu/Lark through OpenAPI-based document, sheet, base, wiki, drive, IM, OAuth token, and OpenClaw routing workflows. It helps configure credentials outside the skill, perform read/write operations, and preserve user-owned cloud resource behavior when tokens are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured Feishu endpoint variables could send credentials to an unverified host.

Mitigation: Use the default Feishu endpoints unless the exact custom host has been verified, keep .env and FEISHU_ENV_FILE under workspace control, and grant only the scopes needed for the requested operation.

Risk: The package changes DNS behavior for Feishu OpenAPI fallback resolution.

Mitigation: Review or remove the DNS fallback before using production credentials, and fix network or DNS issues outside the shared skill when possible.

Risk: Write operations can modify Feishu cloud resources using tenant, app, or user credentials.

Mitigation: Perform a read-only check before writing, use the smallest write needed, prefer user tokens for user-owned resources, and verify the result after the operation.

Risk: Unpinned runtime dependencies may change behavior over time.

Mitigation: Pin and review dependencies before deployment in production or credentialed environments.

## Reference(s):

- [Setup](references/setup.md)
- [Audited Interfaces](references/interfaces.md)
- [Operations](references/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and compact JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Feishu document metadata, block IDs, resource IDs, URLs, changed records, and verification status; credentials and tokens should not be printed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
