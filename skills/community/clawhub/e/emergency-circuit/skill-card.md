## Description:

Monitors AI agents in real time to detect anomalies, enforce safety policies, and trigger emergency shutdowns to reduce damage and cost overruns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor autonomous agents, enforce resource and safety policies, review incidents, and stop agents when policy violations or anomalous behavior are detected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable external code from npm or GitHub.

Mitigation: Install only from trusted sources and verify the exact package or repository version before use.

Risk: Emergency kill commands and automatic shutdown behavior can interrupt agent work.

Mitigation: Test policies in sandbox or staging first, confirm agent IDs before kill commands, and plan recovery for interrupted work.

Risk: Policy configuration errors can cause unwanted stops or insufficient protection.

Mitigation: Validate policies before deployment and review logs and incidents after policy changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/emergency-circuit)
- [GitHub Repository](https://github.com/ZhenRobotics/openclaw-emergency-circuit)
- [npm Package](https://www.npmjs.com/package/openclaw-emergency-circuit)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with bash, JSON, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes monitoring commands, policy examples, incident review guidance, and integration snippets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
