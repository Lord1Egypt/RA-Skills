## Description:

The AEIF-based long-term memory hub for AI Agents to prevent repeating bugs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[404-unknow](https://clawhub.ai/user/404-unknow)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to add long-term experience memory to AI agents, retrieve prior fixes for recurring failures, and store successful troubleshooting patterns as AEIF capsules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist session-derived memory, including content from recent conversations.

Mitigation: Avoid use in sessions containing secrets or private customer data unless commit behavior is gated and sensitive content is redacted.

Risk: Retrieved memories may be injected as system-level advice.

Mitigation: Review injected advice before following it and avoid treating stored memories as authoritative instructions.

Risk: A bundled seed recommends disabling global Git TLS verification.

Mitigation: Remove or replace the Git SSL seed and do not run the global sslVerify false command.

Risk: The package is invoked through npx.

Mitigation: Pin the package and version used for npx execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/404-unknow/skills/engram-evomap)
- [Engram project page](https://404-unknow.github.io/Engram/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown advice with command-oriented guidance and AEIF capsule summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may be injected as system observations and may include patch, configuration, or workaround steps.]

## Skill Version(s):

0.1.0 (source: server release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
