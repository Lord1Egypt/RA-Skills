## Description:

Helps an agent find ANSYS Fluent online documentation URLs, list common Fluent topics, and build direct manual links through the Xiaobenyang service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and engineers use this skill to navigate ANSYS Fluent documentation from an agent workflow, including search queries, common topic links, and direct manual or section links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects an XBY_APIKEY credential and persists it in a plaintext .env file.

Mitigation: Use a dedicated low-privilege key, keep .env out of shared artifacts and source control, rotate the key regularly, and prefer a release that avoids plaintext credential persistence.

Risk: Documentation queries are routed through the under-disclosed Xiaobenyang third-party service.

Mitigation: Install only after deciding that the service is trusted for Fluent documentation queries, and avoid sending confidential project details in prompts or parameters.

Risk: Returned URLs and navigation hints may be incorrect or unsafe to rely on directly.

Mitigation: Verify returned links and content against official ANSYS Fluent documentation before using the information for engineering decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/fluent)
- [Xiaobenyang API key portal](https://xiaobenyang.com)
- [Xiaobenyang MCP service endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries of JSON tool responses, URLs, and navigation hints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY credential; returned links and API content should be verified before use.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
