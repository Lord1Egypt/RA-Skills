## Description:

Normalises recognised characters or words from ancient manuscripts and excavated texts by mapping them to standardised forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aricgamma](https://clawhub.ai/user/aricgamma)

### License/Terms of Use:

MIT

## Use Case:

Researchers, developers, and humanities teams use this skill after OCR or character recognition to expand ancient terms into normalized aliases for search and retrieval workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on PyYAML and the release evidence notes a minor dependency-management caveat.

Mitigation: Install in a virtual environment and pin or hash-lock PyYAML before production use.

## Reference(s):

- [Skill page](https://clawhub.ai/aricgamma/skills/ancient-term-normalization)
- [Reference Documentation](references/REFERENCE.md)
- [Workflow](references/WORKFLOW.md)
- [Recognized Characters Schema](assets/schemas/recognized_chars.schema.json)
- [Normalized Terms Schema](assets/schemas/normalized_terms.schema.json)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [JSON file written to term_normalisation/normalized_terms.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source confidence values when provided and assigns unknown terms to a self-normalized form.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
