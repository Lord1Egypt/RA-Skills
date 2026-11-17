## Description:

Deploy HTML pages, static directories, custom edge functions, and Edge KV workflows to Alibaba Cloud ESA edge nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy static sites, HTML pages, edge functions, and Edge KV data workflows to Alibaba Cloud ESA using SDK guidance and provided scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Alibaba Cloud authority can allow unintended production deployments or KV writes.

Mitigation: Use a narrowly scoped Alibaba Cloud RAM role instead of FullAccess where possible, and treat deployments and KV writes as real cloud changes.

Risk: Static-directory deployment can package unsafe or unintended local build output.

Mitigation: Review build artifacts before deployment and avoid running static-directory deployment on untrusted directories or directories containing symlinks.

Risk: Tokenized access URLs can expose deployed ESA routines if shared publicly.

Mitigation: Do not paste tokenized access URLs into public logs, tickets, or chats.

## Reference(s):

- [ESA Functions & Pages Deployment Reference](references/pages-api.md)
- [Edge KV Edge Key-Value Storage Reference](references/kv-api.md)
- [Alibaba Cloud SDK Default Credential Chain](https://www.alibabacloud.com/help/en/sdk/developer-reference/v2-manage-access-credentials)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide real Alibaba Cloud ESA deployments and Edge KV operations when used with valid cloud credentials.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
