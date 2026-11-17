## Description:

Queries mainland China enterprise records through Bainiu, including registration, shareholders, executives, legal and administrative risk, operating data, intellectual property, internet assets, relationship graphs, and batch basic-information exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bainiu-tech](https://clawhub.ai/user/bainiu-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current mainland China company information from Bainiu, including single-company lookups and batch exports of basic enterprise records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local secret-file handling may read a broader .env file than intended.

Mitigation: Use a dedicated BAINIU_API_KEY and prefer a scoped environment variable instead of relying on a project-level .env file.

Risk: Batch company lists are uploaded to Bainiu's external API and returned Excel links may contain sensitive business data.

Mitigation: Upload only company lists approved for sharing with Bainiu, and handle returned Excel links as sensitive.

Risk: Fallback web searches can introduce unverified company information when Bainiu returns no result.

Mitigation: Confirm with the user before using general web search as a fallback.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bainiu-tech/skills/bainiu-enterprise-data-query)
- [Bainiu Commercial Query Service](https://skill.bainiudata.com/home)
- [Configuration Reference](references/config.md)
- [Tool Reference](references/tools-reference.md)
- [Batch Enterprise Query Reference](references/batch-enterprise-query.md)
- [Error Codes and Troubleshooting](references/error-codes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAINIU_API_KEY; batch exports may return Excel download links.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
