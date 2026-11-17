## Description:

Maps citation networks to trace research evolution, identify influential papers, and discover hidden connections in scientific literature for systematic reviews, bibliometric analysis, and research planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and research operations teams use this skill to build and analyze citation networks from seed papers, DOIs, titles, PMIDs, or offline graph files. It supports literature review planning, influential-paper discovery, and citation relationship mapping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries and paper identifiers may be sent to Semantic Scholar.

Mitigation: Use non-sensitive seed data, or use offline network files when query confidentiality matters.

Risk: The skill can write citation-network output files locally.

Mitigation: Choose output paths deliberately and review generated JSON before sharing or importing it into other tools.

Risk: Some documentation examples do not match the shipped script.

Mitigation: Check the available CLI options and test with demo or offline mode before relying on documented examples.

## Reference(s):

- [Semantic Scholar Graph API](https://api.semanticscholar.org/graph/v1)
- [Citation Chasing Mapping on ClawHub](https://clawhub.ai/aipoch-ai/skills/citation-chasing-mapping)
- [AIpoch Publisher Profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; the shipped script can also produce local JSON citation-network files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the Semantic Scholar API and may write citation-network output files locally.]

## Skill Version(s):

0.1.0 (source: server release metadata and tile.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
