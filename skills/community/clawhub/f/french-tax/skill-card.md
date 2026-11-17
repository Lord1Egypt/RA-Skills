## Description:

一个提供法国个人所得税计算的MCP服务器，支持基于净应税收入和家庭构成的计算，并动态获取最新税档信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve French income-tax information, tax brackets, form details, deadlines, tax-law references, and to calculate French income tax from net taxable income and household composition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in plaintext in a local .env file.

Mitigation: Use a throwaway or restricted API key, keep the workspace private, and inspect or delete the generated .env file after use.

Risk: Tax-related inputs are sent to a remote XiaoBenYang service.

Mitigation: Use the skill only when the user trusts the service and is comfortable sharing the submitted tax parameters.

Risk: A configurable API endpoint can be overridden by untrusted environment variables or .env contents.

Mitigation: Review environment variables and .env contents before running the skill, and do not allow untrusted values to control the endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/french-tax)
- [XiaoBenYang service](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Markdown, JSON, Files]

**Output Format:** [Markdown summaries derived from JSON API responses, with optional Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value and sends user-supplied tax parameters to the XiaoBenYang service.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
