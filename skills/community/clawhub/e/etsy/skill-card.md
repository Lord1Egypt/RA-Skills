## Description:

Improve Etsy listings with buyer-intent keywords, margin-safe pricing checks, and structured experiments that raise qualified traffic and conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External Etsy shop operators and their agents use this skill to audit listing quality, improve search relevance, protect unit economics, and plan measurable listing experiments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store durable Etsy shop context, including product types, margin constraints, active experiments, and compliance sensitivities, under ~/etsy/.

Mitigation: Create or update local shop memory only after user consent, and avoid storing raw chat transcripts or unnecessary sensitive details.

Risk: Listing, pricing, or campaign advice can harm margins or mislead buyers if applied without review.

Mitigation: Review recommendations before making Etsy changes, verify fees and shipping assumptions, and avoid trademarked terms, unverifiable claims, and misleading delivery promises.

Risk: Marketplace credentials and payment details would be sensitive if shared during advisory workflows.

Mitigation: Do not provide Etsy passwords, payment credentials, API secrets, or other secrets to the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/etsy)
- [Skill Homepage](https://clawic.com/skills/etsy)
- [Setup - Etsy](artifact/setup.md)
- [Listing Audit Playbook - Etsy](artifact/listing-audit-playbook.md)
- [Memory Template - Etsy](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured action lists, audit notes, experiment plans, and local context templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local shop memory files under ~/etsy/ only after user consent; does not publish marketplace changes automatically.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
