## Description:

Research stocks, markets, and the economy with FN2's grounded AI, and create, schedule, and manage research agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fn2](https://clawhub.ai/user/fn2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask grounded questions about stocks, markets, earnings, macroeconomic conditions, and company comparisons. They can also create, schedule, run, pause, resume, and delete FN2 research agents for recurring market research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent scheduled research agents.

Mitigation: Confirm the requested prompt and schedule before creating recurring agents, then report the created agent id and schedule back to the user.

Risk: The skill can delete an agent and its run history.

Mitigation: Confirm destructive delete requests explicitly and prefer pausing agents when the user may need the run history later.

Risk: FN2_API_BASE can direct authenticated requests, including the API key, to a non-default endpoint.

Mitigation: Keep FN2_API_BASE unset unless the user intentionally configured a trusted FN2-compatible endpoint.

Risk: API keys may have broader access than needed for the user's task.

Mitigation: Use least-privilege FN2 API key scopes such as chat for research, agents for agent management, and models for model listing.

## Reference(s):

- [FN2 CLI & API reference](references/api.md)
- [FN2 homepage](https://fn2.ai)
- [ClawHub skill page](https://clawhub.ai/fn2/skills/fn2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown and plain text, with optional JSON output from CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research calls may take 30-120 seconds and scheduled agent runs are asynchronous.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
