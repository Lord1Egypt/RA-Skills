## Description:

Agent Q Skills provides guidance for Moon Dev's AI trading agents, including multi-exchange setup, agent workflows, LLM provider switching, and crypto backtesting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prblmsolvrx](https://clawhub.ai/user/prblmsolvrx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to understand, configure, run, debug, and extend a multi-agent crypto trading system. It helps agents produce setup guidance, commands, configuration patterns, backtesting code, and risk-management advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward live crypto trading and forced position closing.

Mitigation: Use paper-trading or sandbox exchange accounts until configuration, risk limits, and kill-switch behavior are verified.

Risk: Trading examples and orchestrator commands could place live orders when connected to funded accounts.

Mitigation: Do not run trading commands with funded accounts unless live order placement is intentional and supervised.

Risk: RBI workflows can generate executable backtesting code from videos, PDFs, or text.

Mitigation: Treat generated code and external source material as untrusted; review and sandbox execution before use.

Risk: Use of cloud LLM providers can expose account positions, strategy details, or other sensitive trading context.

Mitigation: Avoid sending raw account positions, private strategy details, secrets, or private keys to cloud LLM providers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prblmsolvrx/skills/agentqskills)
- [Publisher profile](https://clawhub.ai/user/prblmsolvrx)
- [SKILL.md](artifact/SKILL.md)
- [AGENTS.md](artifact/AGENTS.md)
- [WORKFLOWS.md](artifact/WORKFLOWS.md)
- [ARCHITECTURE.md](artifact/ARCHITECTURE.md)
- [CLAUDE.md](artifact/CLAUDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include trading workflow guidance, exchange configuration snippets, backtesting code, and command examples.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
