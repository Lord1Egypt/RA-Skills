## Description:

Generates API documentation from Python source code through a multi-step pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dapan0902](https://clawhub.ai/user/dapan0902)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn Python modules into structured API reference documentation, including public symbol inventories, Google-style docstrings, examples, and a quality check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled documentation template and checklist are Chinese-language by default.

Mitigation: Users needing English or multilingual API documentation should adjust the skill materials or explicitly request the desired language before generation.

Risk: Generated API documentation can omit or misdescribe public symbols if the initial inventory is incomplete.

Mitigation: Review and confirm the public API inventory before docstring generation and run the included quality checklist before accepting the final document.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dapan0902/skills/doc-pipeline)
- [API documentation template](artifact/assets/api-doc-template.md)
- [Docstring style guide](artifact/references/docstring-style.md)
- [API documentation quality checklist](artifact/references/quality-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown API reference content with Python docstring examples and checklist results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces staged review output before the final documentation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
