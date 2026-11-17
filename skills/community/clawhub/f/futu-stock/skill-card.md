## Description:

Access Futu stock market data via MCP server - real-time quotes, K-lines, options, account info for HK/US/CN markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuizhengqi1](https://clawhub.ai/user/shuizhengqi1)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query Futu market data, screen securities, inspect options data, and retrieve account, funds, and positions information through a configured Futu OpenD and MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose local environment variables and sensitive financial account data to the third-party MCP server.

Mitigation: Run it in an isolated environment without unrelated secrets, and treat account, funds, and positions results as sensitive financial data.

Risk: The MCP server dependency may be installed as unpinned code.

Mitigation: Review and pin the MCP server dependency before deployment.

Risk: Trading features can allow AI-assisted trading if enabled.

Mitigation: Keep FUTU_ENABLE_TRADING disabled unless trading access is intentionally required and separately controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuizhengqi1/skills/futu-stock)
- [Futu OpenD command documentation](https://openapi.futunn.com/futu-api-doc/opend/opend-cmd.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return sensitive account, funds, and positions information when those tools are enabled.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
