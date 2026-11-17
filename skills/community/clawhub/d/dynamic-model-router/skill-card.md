## Description:

Routes AI tasks to a suitable model by weighing task complexity, cost, latency, quality, reliability, and historical feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skynet-jawol](https://clawhub.ai/user/skynet-jawol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to select an AI model and provider for a task and receive a confidence-scored routing decision with estimated cost, latency, and quality. It can be integrated with OpenClaw skill or plugin flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports shell command execution paths and prompt data written to shared temporary files.

Mitigation: Install only from trusted publishers and avoid sensitive prompts or API keys until execution uses argument-based spawning and prompt temporary files are protected or removed.

Risk: The security review reports OpenClaw provider integration code that can probe arbitrary provider URLs.

Mitigation: Use strict provider URL allowlists and review provider configuration before enabling OpenClaw integration.

Risk: The security review reports local configuration and log persistence.

Mitigation: Review storage locations, log contents, retention, and privacy documentation before using the skill with confidential workloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skynet-jawol/skills/dynamic-model-router)
- [Artifact README](artifact/README.md)
- [Artifact changelog](artifact/CHANGELOG.md)
- [OpenClaw](https://openclaw.ai)
- [OpenClaw Docs](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON routing decision with model, provider, confidence, reasoning, and performance metrics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local configuration, logs, temporary request files, and decision history depending on runtime settings.]

## Skill Version(s):

0.1.0 (source: server release metadata, package.json, skill.json, CHANGELOG released 2026-03-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
