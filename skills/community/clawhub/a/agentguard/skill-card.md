## Description:

AgentGuard monitors agent file access, API calls, and communications to detect suspicious behavior, log events, and generate security reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manas-io-ai](https://clawhub.ai/user/manas-io-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use AgentGuard to monitor AI agent activity, review security alerts, and generate reports about file access, API destinations, communications, and anomalous behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently records sensitive file and communication metadata.

Mitigation: Narrow watched directories, keep retention short, restrict permissions on ~/.agentguard, and review generated logs before sharing them.

Risk: Privacy protections are advertised but may need hardening before relying on them for sensitive environments.

Mitigation: Avoid logging full URLs or sensitive paths, verify hashing behavior against expected data, and do not rely on advertised encryption without an implementation review.

Risk: Monitoring or alerting may be disabled or altered if it runs with the same permissions as a compromised agent.

Mitigation: Run the monitor separately with limited write access, as suggested by the artifact notes.

## Reference(s):

- [AgentGuard ClawHub Skill Page](https://clawhub.ai/manas-io-ai/skills/agentguard)
- [AgentGuard Documentation](https://docs.clawdhub.com/skills/agentguard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text, JSON status output, JSONL logs, YAML configuration, and Markdown security reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local logs, alerts, baselines, and reports under ~/.agentguard by default.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact README, and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
