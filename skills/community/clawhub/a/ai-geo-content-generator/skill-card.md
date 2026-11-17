## Description:

Generates AI-search-oriented brand content assets from a supplied brand knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljseeking](https://clawhub.ai/user/ljseeking)

### License/Terms of Use:

MIT-0

## Use Case:

Brand and content teams use this skill to convert an existing brand knowledge base into structured draft assets for AI search, AI agents, and public content channels. It supports website FAQ, Zhihu-style answers, Toutiao-style articles, llms.txt drafts, and quote sentence libraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand knowledge bases may contain confidential strategy, customer data, unreleased product details, or regulated information.

Mitigation: Remove secrets and sensitive personal or business data before use, and confirm which model provider will process the supplied content.

Risk: Security evidence reports conflicting privacy disclosures about sending supplied brand materials to an AI service.

Mitigation: Review privacy expectations before installation and avoid submitting confidential material unless the processing path is acceptable.

Risk: Generated drafts may contain unsupported claims when the source knowledge base is incomplete or covers regulated domains.

Mitigation: Use the skill's placeholder and self-check workflow, then manually review all drafts before publishing; require professional review for medical, financial, legal, education, or similarly sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ljseeking/skills/ai-geo-content-generator)
- [Input contract](artifact/docs/input_contract.md)
- [README](artifact/README.md)
- [Security audit](artifact/SECURITY_AUDIT.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown drafts, llms.txt text, structured checklists, and human-review guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated content is draft material based on the supplied brand knowledge base and is expected to be reviewed before publication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
