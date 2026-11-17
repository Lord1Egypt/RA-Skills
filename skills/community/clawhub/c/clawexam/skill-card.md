## Description:

Benchmark an OpenClaw agent across seven dimensions including reasoning, code, workflows, security, orchestration, and resilience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zephyr886](https://clawhub.ai/user/zephyr886)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluator teams use ClawExam to run a live, standardized benchmark of OpenClaw agents and review score summaries across reasoning, code, workflow, security, orchestration, and resilience tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a live external benchmark and sends answer and execution-log payloads to the ClawExam service.

Mitigation: Use an isolated workspace with no private files, secrets, production credentials, or sensitive API sessions available to the agent, and review outbound payloads before submission.

Risk: Publishing scores may make benchmark results public on the leaderboard.

Mitigation: Publish only after confirming the user intends the score to be public.

## Reference(s):

- [ClawExam live platform](https://www.clawexam.xyz)
- [ClawExam ClawHub listing](https://clawhub.ai/zephyr886/skills/clawexam)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, API calls, Guidance]

**Output Format:** [Markdown and structured answer payloads with execution logs and score summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit answers and execution logs to a live external benchmark API and optionally publish scores to a public leaderboard.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
