## Description:

Adversarial pre-build architecture review agent that reviews proposed builds, features, or operational decisions before code is written and returns APPROVE, REVISE, or REJECT with itemized findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jfulmines-star](https://clawhub.ai/user/jfulmines-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to get an independent architecture review before starting features, endpoints, schema changes, payment or auth work, or other high-confidence technical decisions. It helps identify scope, integration, security, deployment, and cost risks before implementation begins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advisory review can be influenced by untrusted task or repository text and should not be treated as an enforceable security boundary.

Mitigation: Manually review any APPROVE result before sensitive payment, authentication, production, or protected-file changes proceed.

Risk: Running the skill sends the task brief and selected repository metadata to Anthropic through the user's configured account.

Mitigation: Install and run only when the user is comfortable sharing that project context with the configured LLM provider.

## Reference(s):

- [Architecture Critic ClawHub Page](https://clawhub.ai/jfulmines-star/skills/architecture-critic)
- [README](README.md)
- [Security and Privacy](SECURITY.md)
- [General Architecture Critic Checklist](references/checklist-general.md)
- [Web / API Architecture Critic Checklist](references/checklist-web.md)
- [Security Checklist](references/security.md)
- [Payment Flows Checklist](references/payment-flows.md)
- [AI/LLM Builds Checklist](references/ai-builds.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal verdict text and a local Markdown verdict file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verdicts are APPROVE, REVISE, REJECT, or ERROR; local verdict files are written under specialists/critic-verdicts.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata; artifact frontmatter and clawhub.yaml report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
