## Description:

AnnData MCP retrieves AnnData object information through MCP for biomedical data analysis workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and biomedical data analysts use this skill to inspect AnnData files, summarize AnnData objects, and request descriptive statistics over selected attributes, genes, columns, or filtered observations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the Xiaobenyang API key in a plaintext .env file.

Mitigation: Use a dedicated workspace with non-production credentials, restrict workspace sharing, and rotate the key if the workspace is shared or archived.

Risk: AnnData file paths, URLs, and query parameters are sent to the Xiaobenyang service.

Mitigation: Use the skill only when the user trusts that service and is comfortable sending the selected dataset locations and query details.

Risk: Security evidence reports mismatched gaokao/Xiaobenyang configuration details.

Mitigation: Review the configuration and endpoint expectations before installing or using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/anndata)
- [Xiaobenyang API key site](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown summaries of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value before calling the external service.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
