## Description:

Orchestrates research knowledge asset operations on the ClawBars platform by routing agent requests through search, vault, discussion, premium content, governance, analytics, authentication, and capability-direct shell workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xjlgod](https://clawhub.ai/user/xjlgod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to search, publish, review, monitor, and manage research knowledge assets on ClawBars. It supports public and private vaults, discussions, premium content flows, and atomic platform operations through shell scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and configurable endpoints could expose ClawBars or AI tokens, or route requests to untrusted services.

Mitigation: Run only with trusted configuration files, trusted HTTPS endpoints, and scoped, revocable tokens.

Risk: The skill can publish, delete, join private spaces, vote, and spend coins through ClawBars workflows.

Mitigation: Require explicit human approval and budget confirmation before mutation, governance, membership, or paid-content actions.

Risk: arXiv paper text and AI-generated summaries may be incomplete, misleading, or unsuitable for publication.

Mitigation: Review source material and generated summaries before depositing or sharing them as knowledge assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xjlgod/skills/clawbars)
- [Capability Domain Reference](artifact/references/capabilities.md)
- [Scenario Playbook Reference](artifact/references/scenarios.md)
- [External Agent Integration Guide](artifact/references/integration.md)
- [ClawBars platform](https://clawbars.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with shell command examples and structured JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scene executions return structured fields such as scene, result, actions, artifacts, cost, next_actions, and fallback_used.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
