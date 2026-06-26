## Description: <br>
Guides agents in using the Anthropic Claude API for chat, tool use, vision, document analysis, coding, cost control, and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to plan and execute Claude API workflows through the Anthropic MCP server while choosing appropriate models, setting required parameters, controlling token cost, and handling errors safely. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Anthropic API credentials when used with runtime tools. <br>
Mitigation: Store the API key in environment variables, never paste it into prompts, and avoid printing or logging the key or API headers. <br>
Risk: Prompts, images, documents, or chat history may contain sensitive data sent to a third-party model provider. <br>
Mitigation: Review and redact PII, PHI, financial data, screenshots, documents, and internal business information before sending requests. <br>
Risk: Unbounded or poorly chosen Claude calls can create unnecessary cost. <br>
Mitigation: Choose the cheapest viable model, set tight max_tokens values, estimate tokens for large jobs, use caching for repeated context, and batch bulk work when appropriate. <br>
Risk: Model output and tool-use arguments may be untrusted or affected by prompt injection. <br>
Mitigation: Validate tool-use inputs against strict schemas before execution and review model outputs before using them in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/simonpierreboucher02/anthropic-api-al) <br>
- [Anthropic API documentation](https://docs.anthropic.com/en/api) <br>
- [Anthropic model documentation](https://docs.anthropic.com/en/docs/about-claude/models) <br>
- [Anthropic Messages API](https://docs.anthropic.com/en/api/messages) <br>
- [Anthropic API errors](https://docs.anthropic.com/en/api/errors) <br>
- [Anthropic vision documentation](https://docs.anthropic.com/en/docs/build-with-claude/vision) <br>
- [Model reference](reference/models.md) <br>
- [Endpoint reference](reference/endpoints.md) <br>
- [Parameter reference](reference/parameters.md) <br>
- [Common errors](reference/common-errors.md) <br>
- [Best practices](reference/best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with JSON examples, checklists, and API request patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; it requires an Anthropic API key when paired with runtime tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
