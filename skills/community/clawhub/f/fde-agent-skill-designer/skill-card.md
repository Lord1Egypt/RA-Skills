## Description:

Packages approved POC scenarios, PRDs, and deployment constraints into reusable, evaluable Agent Skills, and when explicitly requested builds mock-first runnable POC scaffolds with guardrails and smoke evaluations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xukun0821](https://clawhub.ai/user/xukun0821)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and field delivery engineers use this skill to convert approved PRD and deployment handoff packages into agent skill design packages with boundaries, guardrails, evaluations, platform adapters, and optional mock POC scaffolds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runnable POC scaffolds can turn untrusted names or scenarios into executable local JavaScript.

Mitigation: Use only trusted POC metadata until validation is added, run generated POCs in a constrained local environment, and keep them away from production credentials and real customer data.

Risk: A generated scaffold or offline example could be mistaken for representative production validation.

Mitigation: Treat runnable mode as mock-first evidence only and complete representative Stage 6 validation before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xukun0821/skills/fde-agent-skill-designer)
- [Agent skill design package template](references/agent-skill-pack.md)
- [Agent skill assessment design](references/evaluation-design.md)
- [General Agent Skills platform adaptation](references/platform-adapters.md)
- [Minimum runnable POC build mode](references/poc-build-mode.md)
- [Public method sources](references/public-sources.md)
- [OpenAI: Build skills](https://developers.openai.com/codex/skills/)
- [Anthropic: Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [OWASP Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown design packages with optional generated skill files, configuration, shell commands, JSON manifests, and smoke-evaluation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runnable POC mode is mock-first and requires a user-specified target directory and authorization scope.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
