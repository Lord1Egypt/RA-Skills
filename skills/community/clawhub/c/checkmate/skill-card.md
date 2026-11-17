## Description:

Enforces task completion by turning a goal into pass/fail criteria, running a worker, judging the output, feeding back gaps, and looping until every criterion passes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[insipidpoint](https://clawhub.ai/user/insipidpoint)

### License/Terms of Use:


## Use Case:

Developers and operators use Checkmate when a task needs quality gates, such as code, documentation, reports, or research that should be iterated until judged complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spawned agents can inherit broad shell, web, installed-skill, connected-account, messaging, and background execution authority.

Mitigation: Install only where the skill can safely have the same practical reach as the host OpenClaw agent, and prefer a private workspace directory.

Risk: Non-interactive batch mode removes human review gates for criteria approval and checkpoints.

Mitigation: Use interactive mode for sensitive tasks and avoid --no-interactive unless the task and environment are fully trusted.

Risk: Checkpoint replies are written verbatim to disk and can steer the orchestrated work.

Mitigation: Do not paste secrets or untrusted third-party text into checkpoint replies.

## Reference(s):

- [Checkmate ClawHub skill page](https://clawhub.ai/insipidpoint/skills/checkmate)
- [ClawHub](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files and direct user notifications; final content depends on the requested task.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists iterative workspace artifacts and writes the best passing or best available result to final-output.md.]

## Skill Version(s):

2.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
