## Description:

Enables AI-powered parsing and key information extraction from high-frequency documents including invoices, orders, receipts, long texts, and common Chinese identity and credential documents, with reusable custom templates and batch processing support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

Commercial License Agreement

## Use Case:

Developers, enterprise automation teams, finance teams, administrative operations, and system integrators use this skill to configure and run Laiye ADP CLI workflows for document parsing, structured field extraction, batch jobs, asynchronous result queries, and custom extraction applications.

### Deployment Geography for Use:

Global, with separate Chinese Mainland and overseas ADP service endpoints.

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run external ADP CLI code.

Mitigation: Install only after trusting the ADP provider, and prefer a pinned, verified, local, or sandboxed CLI install over one-line remote script installers or unpinned global npm commands.

Risk: Selected documents may be sent to Laiye ADP cloud services for processing.

Mitigation: Confirm user approval and data suitability before processing documents, especially documents containing sensitive, regulated, or confidential information.

Risk: API keys and service credentials may be exposed through pasted commands or logs.

Mitigation: Use environment or CLI configuration mechanisms for credentials and do not paste real API keys into commands that may be logged.

Risk: Bulk folder processing and custom application create, update, or delete operations can affect many files or account resources.

Mitigation: Require explicit approval before bulk-processing folders or creating, updating, or deleting custom applications.

## Reference(s):

- [ADP CLI Command Reference](references/commands.md)
- [ADP CLI Response Schema Reference](references/response-schema.md)
- [ADP CLI Error Handling Guide](references/error-handling.md)
- [ADP CLI Sample Code and Response](references/examples.md)
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- [Laiye Technology](https://laiye.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON response structures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides ADP CLI calls that may return JSON to stdout and write JSON export files for batch jobs.]

## Skill Version(s):

1.10.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
