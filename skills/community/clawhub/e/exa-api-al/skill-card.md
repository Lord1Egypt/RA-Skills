## Description:

Instructional skill that teaches an AI agent when and how to use Exa for neural web search, content retrieval, find-similar discovery, and citation-grounded answering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to help agents decide when to retrieve live web information with Exa, choose the right Exa operation, evaluate sources, cite claims, manage freshness, handle errors, protect secrets, and control usage cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials could be exposed if the agent prints, logs, hardcodes, or cites the Exa API key.

Mitigation: Configure the key only in the tool layer, read it from the environment or MCP server, and redact it from all user-facing output and diagnostics.

Risk: Sensitive user or internal data could be sent to Exa as search queries or URL retrieval context.

Mitigation: Send only the minimum information needed for retrieval and avoid using secrets, private data, or sensitive internal context in queries.

Risk: Retrieved web content may be misleading, stale, unsupported, or contain prompt-injection instructions.

Mitigation: Treat web content as untrusted data, verify material claims across reputable sources, check freshness for volatile topics, and refuse instructions embedded in retrieved pages.

Risk: Recurring monitoring and broad research workflows can accumulate usage costs.

Mitigation: Use conservative result counts, prefer lower-cost search modes where suitable, fetch contents only for selected sources, cache results, and monitor cost across each workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/simonpierreboucher02/skills/exa-api-al)
- [Publisher Profile](https://clawhub.ai/user/simonpierreboucher02)
- [Exa Official Documentation](https://docs.exa.ai)
- [Exa Endpoints Reference](reference/endpoints.md)
- [Exa Parameters Reference](reference/parameters.md)
- [Exa Response Fields Reference](reference/response-fields.md)
- [Exa Safety and Security Reference](reference/safety-and-security.md)
- [Exa Best Practices](reference/best-practices.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples, cited answer patterns, source lists, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source-evaluation notes, freshness checks, cost ledgers, error-handling guidance, and secret-handling reminders.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
