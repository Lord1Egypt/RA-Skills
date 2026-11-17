## Description:

AI-powered diagnosis and repair for AI agents. Send your health data, get diagnosed, execute prescribed repairs, report back until healed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawies](https://clawhub.ai/user/clawies)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Agent Hospital to diagnose OpenClaw or Hermes agent health, run prescribed repair commands, and report repair results until the agent is healed or escalated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable external code that sends broad local health data to a remote service.

Mitigation: Install only after confirming trust in the Agent Hospital publisher and service, and verify what telemetry is uploaded before use in sensitive environments.

Risk: Automatic repair actions may change local agent state, delete old sessions or logs, kill port-conflicting processes, or truncate oversized files.

Mitigation: Run with least privileges and avoid production or sensitive agent environments until a dry-run or approval mode is available.

Risk: Credentials are cached locally for future runs.

Mitigation: Review how cached credentials are protected and how they can be revoked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawies/skills/agent-hospital)
- [Agent Hospital homepage](https://api.agent-hospital.ai/.well-known/llms.txt)
- [Agent Hospital full API docs](https://api.agent-hospital.ai/llms-full.txt)
- [Agent Hospital dashboard](https://admin-dashboard.agent-hospital.ai)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx; the healing command sends local agent health data to the Agent Hospital service and may execute repair actions.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
