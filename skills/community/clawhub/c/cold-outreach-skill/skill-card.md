## Description:

Meta-skill for orchestrating Apollo API, LinkedIn API, YC Cold Outreach, and MachFive Cold Email into a complete B2B cold outreach pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4gen](https://clawhub.ai/user/h4gen)

### License/Terms of Use:


## Use Case:

External teams and developers use this skill to define an outreach job, source and enrich B2B leads, generate personalized multi-step email sequences, and prepare campaign handoff assets without directly sending messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation instructions use mutable latest ClawHub installer code and include a bulk update command for all local skills.

Mitigation: Review or pin the ClawHub installer and required skill versions before installation, and avoid bulk updates unless that behavior is intended.

Risk: The workflow requires outreach API credentials that could be exposed to unrelated local tools if the environment is overprivileged.

Mitigation: Run the skill in a least-privileged environment and provide only MATON_API_KEY and MACHFIVE_API_KEY when the outreach workflow needs them.

Risk: Personalized outreach can become misleading if lead-specific facts, posts, quotes, or proof points are fabricated.

Mitigation: Keep unavailable enrichment fields explicit, require verifiable personalization context, and flag generated sequences for revision when factuality or CTA checks fail.

## Reference(s):

- [Cold Outreach Skill on ClawHub](https://clawhub.ai/h4gen/skills/cold-outreach-skill)
- [Publisher profile](https://clawhub.ai/user/h4gen)
- [Inspected upstream skills](references/inspected-skills.md)
- [ClawHub](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs LeadSummary, EnrichmentSummary, SequencePackage, and ExecutionPlan sections; sequence generation depends on required API keys and upstream skills.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
