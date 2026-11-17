## Description:

Find Bearings Skill helps agents answer bearing model, brand, specification, code parsing, cross-reference, and selection questions using packaged reference material and a local lookup script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openfindbearings](https://clawhub.ai/user/openfindbearings)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and maintenance teams can use this skill to look up bearing models, parse common bearing codes, compare brand equivalents, and draft bearing selection guidance for application scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The lookup script reads bearing data from an ancestor-level data/models path outside the packaged skill.

Mitigation: Review or fix the data path so it reads only packaged skill data, and avoid using it where unrelated or sensitive JSON files may exist in that ancestor path.

Risk: The package may overstate implemented capabilities relative to the current local lookup behavior.

Mitigation: Confirm the implemented search, parsing, brand lookup, and selection behavior before relying on outputs in operational decisions.

## Reference(s):

- [Bearing Data Structure](artifact/references/data-structure.md)
- [Bearing Model Codes](artifact/references/model-codes.md)
- [Bearing Brands Reference](artifact/references/brands.md)
- [SKF](https://www.skf.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional shell command snippets and tabular bearing details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include bearing dimensions, type explanations, suffix parsing, brand cross-references, and selection guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
