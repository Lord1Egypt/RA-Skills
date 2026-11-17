## Description:

A method for building verified B2B contact bases from public registries and public pages with per-field proof, no guessed emails, retention controls, suppression filtering, and GDPR-oriented constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, sales and research teams, and developers use this skill to build or enrich B2B contact bases from public entity registries and public organisation pages while retaining per-field proof and respecting suppression, retention, and opt-out obligations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Collected contact data could be delivered without proof for each populated field.

Mitigation: Require a proof gate that rejects any populated value whose source URL companion is empty before delivery.

Risk: Suppressed contacts could be reached again if opt-out matching is incomplete.

Mitigation: Keep a persistent suppression list above per-run directories, normalise addresses on both sides, and check every email field before producing deliverable output.

Risk: Business contact records could be retained past the declared retention period.

Mitigation: Stamp delete_after during collection and run a retention purge across every run directory before each new run.

Risk: The method could be misused for private individuals, guessed emails, breach data, login-gated sources, or sources whose terms prohibit automated collection.

Mitigation: Limit use to public B2B sources, leave unproven fields empty, and drop any source or request that falls outside the declared scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexbloch-ia/skills/agentic-osint-contact-base)
- [Publisher homepage](https://blochagents.com)
- [Skill source artifact](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON schemas and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The intended agent output is a locally persisted B2B contact dataset plus a short method sheet after the operator implements proof, merge, suppression, and retention gates.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
