## Description:

Install, repair, or manually configure the GrowthCircle.id gc-provider for OpenClaw and Hermes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramaaditya49](https://clawhub.ai/user/ramaaditya49)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install or repair the GrowthCircle provider in OpenClaw, configure GrowthCircle manually in Hermes, migrate Hermes configuration to OpenClaw, and verify model access with the same key used for inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or replace executable provider code and change local OpenClaw or Hermes configuration.

Mitigation: Use it only when provider installation or repair is intended, review the publisher and provider source first, and back up configuration before migration or repair.

Risk: Unpinned or forced plugin installation can replace reviewed code with a newer or unexpected package.

Mitigation: Prefer a pinned, reviewed plugin version or digest, and reserve `--force` for repairing a known problem.

Risk: GrowthCircle API keys could be exposed through chat, logs, repositories, screenshots, or frontend code.

Mitigation: Keep `GROWTHCIRCLE_API_KEY` in a private credential store or environment variable and redact secret values in examples and troubleshooting output.

Risk: Using a model ID not returned for the active key can route requests incorrectly or fail for Free, Paid, or Team access.

Mitigation: Discover models with `/v1/models` using the same key that will make requests, then use returned model IDs exactly.

## Reference(s):

- [GC Provider Install Guide](references/install-guide.md)
- [GrowthCircle AI Console Docs](https://d.growc.id/llms/ai-console.md)
- [GrowthCircle Member AI Console](https://growthcircle.id/app/ai)
- [GrowthCircle OpenAI-Compatible Endpoint](https://ai.growthcircle.id/v1)
- [gc-provider Plugin Source](https://github.com/Growth-Circle/gc-provider)
- [ClawHub Skill Page](https://clawhub.ai/ramaaditya49/skills/gc-provider-install)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Redacts secret values in examples and includes verification steps for OpenClaw and Hermes paths.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
