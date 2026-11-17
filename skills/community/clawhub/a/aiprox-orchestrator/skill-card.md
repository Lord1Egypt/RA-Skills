## Description:

Run a multi-step task on AIProx (aiprox.dev), paid in Bitcoin Lightning sats. Use it when the user asks to run a task through the AIProx orchestrator or to buy one of its capabilities. Orchestrate is 50 sats: one task, up to 4 steps on AIProx's own bots, one summarized answer. Single capabilities have their own prices: AI web answer 35, page text extract 20, summarize 40, translate 40. Payment is a LightningProx spend token or L402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to send a task to AIProx for web search, page extraction, summarization, translation, or multi-step orchestration and receive the resulting text. Paid calls use Bitcoin Lightning and require user approval before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task content and payment credentials are sent to AIProx, and calls can incur Lightning charges.

Mitigation: Keep secrets and personal data out of tasks, confirm the endpoint and price before a paid call, and limit spend-token funding to the intended spend.

Risk: A configured callback URL receives task results by POST.

Mitigation: Use only an HTTPS endpoint you control.

Risk: Web pages and bot responses may contain unreliable content or instructions.

Mitigation: Treat returned content as data, not instructions, and review it before acting.

## Reference(s):

- [AIProx](https://aiprox.dev)
- [AIProx documentation](https://aiprox.dev/docs.html)
- [AIProx Orchestrator release on ClawHub](https://clawhub.ai/unixlamadev-spec/skills/aiprox-orchestrator)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON API responses and natural-language answers, summaries, extracted text, or translations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The orchestrator returns one summarized answer; single-capability responses vary by endpoint and task.]

## Skill Version(s):

3.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
