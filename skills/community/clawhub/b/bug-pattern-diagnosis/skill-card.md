## Description:

Helps developers match reported intermittent, environment-specific, or unusual bug symptoms against a curated case library, then produce verification-first diagnostic guidance and optional new case notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site reliability engineers use this Chinese-language skill to structure bug symptoms, compare them with prior diagnostic cases, and choose quick checks before changing code or infrastructure. It is especially suited to intermittent failures, multi-instance behavior differences, strange logs, Kubernetes and EMQX incidents, and cases that may need to be captured for future reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A similar prior case could be overmatched and lead to incorrect debugging advice or unnecessary code changes.

Mitigation: Require the agent to restate uncertainty, run current-environment checks first, and treat case files as diagnostic evidence rather than final answers.

Risk: Suggested Kubernetes, EMQX, curl, or cluster leave/join commands could affect live services if copied without review.

Mitigation: Review commands before execution, confirm namespace, node, broker, credentials, and maintenance window, and verify the faulty target before applying remediation.

Risk: Artifact examples include environment-specific paths, service names, ports, and logs that may not match the user's system.

Mitigation: Adapt all paths, hostnames, ports, topics, and code references to the active project before running checks or proposing fixes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/skills/bug-pattern-diagnosis)
- [Skill definition](artifact/SKILL.md)
- [BUG01 multi-replica identity context case](artifact/experience/BUG01.md)
- [BUG02 Netty event loop and heap case](artifact/experience/BUG02.md)
- [BUG03 EMQX route table synchronization case](artifact/experience/BUG03.md)
- [BUG04 MQTT ClientID takeover case](artifact/experience/BUG04.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown diagnostic guidance with structured checks and optional inline code or shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should frame prior cases as evidence and require independent verification before applying fixes.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence, released 2026-04-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
