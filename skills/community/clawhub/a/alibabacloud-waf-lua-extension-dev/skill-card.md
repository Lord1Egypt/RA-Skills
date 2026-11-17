## Description:

Use when creating, editing, or reviewing WAF 3.0 custom Lua extension plugins, plugin parameters, or request validation logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create, edit, or review Alibaba Cloud WAF 3.0 custom Lua extension plugins and request validation logic. It helps produce plugin code, parameter and test configuration, and review guidance for configuring plugins in the WAF console.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because several referenced files were missing, so its benign verdict has medium confidence.

Mitigation: Review the missing referenced files and assess whether you trust the publisher before relying on the skill.

Risk: A missing plugin parameter can make a request check match unexpectedly and block traffic.

Mitigation: Validate required parameters before using them, then check both matching and passing cases with the console debug workflow.

Risk: A Lua execution timeout can skip the protection logic, allowing the request through.

Mitigation: Keep plugin work within the documented execution limit and verify behavior in the console debug workflow.

## Reference(s):

- [Alibaba Cloud WAF 3.0 Extension Plugins documentation](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/extensions)
- [Examples and project templates](artifact/references/examples.md)
- [Extension plugin console lifecycle](artifact/references/console-lifecycle.md)
- [Lua API reference](artifact/references/lua-api-reference.md)

## Skill Output:

**Output Type(s):** [Code, Configuration, Guidance, Test cases]

**Output Format:** [Markdown with Lua code and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include plugin metadata, parameter definitions, simulated traffic cases, and console setup guidance.]

## Skill Version(s):

0.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
