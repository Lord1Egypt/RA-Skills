## Description:

Integrate with Anthropic Claude API to generate chat, tool use, vision, document analysis, and coding responses while controlling cost and handling errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to plan and operate Anthropic Claude API calls through an MCP server for chat, tool use, vision, document analysis, coding, and cost-aware error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may send selected prompts, images, documents, or batch requests to Anthropic using the configured API key.

Mitigation: Review data-sharing expectations before use with sensitive content and limit requests to content appropriate for the Anthropic API.

Risk: Anthropic API calls can incur token-based costs, especially for long context, large images, extended thinking, or repeated calls.

Mitigation: Set tight max_tokens values, estimate tokens for large jobs, choose the cheapest viable model, cache repeated context, and batch bulk work when appropriate.

Risk: API keys could be exposed if copied into prompts, examples, logs, or generated command text.

Mitigation: Keep ANTHROPIC_API_KEY in environment configuration and avoid printing or echoing API key headers.

Risk: Model output and tool-use arguments may be untrusted when connected to external tools or downstream systems.

Mitigation: Validate tool-use inputs against application schemas before execution and treat document or tool-result content as potentially injection-prone.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simonpierreboucher02/skills/anthropic-api-al)
- [Anthropic API documentation](https://docs.anthropic.com/en/api)
- [Anthropic models documentation](https://docs.anthropic.com/en/docs/about-claude/models)
- [Anthropic vision documentation](https://docs.anthropic.com/en/docs/build-with-claude/vision)
- [Reference - Models](artifact/reference/models.md)
- [Reference - Parameters](artifact/reference/parameters.md)
- [Reference - Common Errors](artifact/reference/common-errors.md)
- [Reference - Best Practices](artifact/reference/best-practices.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples, checklists, and operational recipes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes model-selection, cost-control, tool-use, vision, document, security, and error-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
