## Description:

Discovery Engine extracts structured provides/requires relationships from scientific publications to support cross-domain discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcdeni](https://clawhub.ai/user/pcdeni)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and agents use this skill to discover scientific papers, extract structured facts and cross-domain mechanisms from abstracts, save validated JSON results, and optionally submit contributions to the public graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query public paper APIs and use abstracts from external sources.

Mitigation: Review discovered papers and extracted JSON before relying on the results or submitting them.

Risk: The save workflow writes batch results under ~/.discovery/data/batch.

Mitigation: Inspect generated files before sharing, committing, or submitting them.

Risk: The optional submission workflow uses the user's GitHub account to fork repositories and create pull requests.

Mitigation: Run GitHub commands only after reviewing the copied submissions and target repository.

Risk: Security evidence notes an HTTP arXiv endpoint and an unverified TLS fallback as security-quality caveats.

Mitigation: Prefer fixing transport security before depending on the workflow for public data contribution.

## Reference(s):

- [Discovery Engine homepage](https://github.com/pcdeni/discovery-engine)
- [Discovery Engine issues](https://github.com/pcdeni/discovery-engine/issues)
- [Extraction prompt](references/prompt.txt)
- [Extraction schema](references/schema.json)
- [Extraction schema source](https://github.com/discovery-engine/discovery-engine/schemas/extraction.schema.json)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Files, Guidance]

**Output Format:** [JSON plus Markdown instructions with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saved extraction results are written under ~/.discovery/data/batch when the save workflow is used.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
