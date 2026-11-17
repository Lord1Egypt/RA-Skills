## Description:

Review Business Requirements Documents in `.docx` format by reading the existing BRD, extracting paragraph-level context, drafting clarification questions for unclear statements, and producing a final Word document that combines comments and tracked changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chipmunkrpa](https://clawhub.ai/user/chipmunkrpa)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts, product owners, and implementation teams use this skill to review BRD Word documents for ambiguity, missing acceptance criteria, undefined actors, dependencies, and unclear business rules. The skill supports a Word-native review workflow that produces reviewer comments, tracked replacement wording, and a structured paragraph review JSON file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input BRDs, review JSON, and reviewed DOCX files may contain confidential business content and proposed edits.

Mitigation: Run the skill only on BRDs intended for local processing and review generated .review.json and .reviewed.docx files before sharing.

Risk: Dependency behavior can vary across Python environments when versions are not pinned.

Mitigation: Install dependencies in an isolated virtual environment and pin versions for repeatable deployments.

Risk: Documents with heavy tables or special layout may require visual confirmation after comments and tracked revisions are applied.

Mitigation: Inspect the reviewed DOCX in Word or a document-rendering workflow before delivery when layout fidelity matters.

## Reference(s):

- [Review JSON Schema](references/review-json-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/chipmunkrpa/skills/brd-reviewer)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, structured review JSON, and reviewed DOCX file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces <name>.review.json and <name>.reviewed.docx beside the source BRD unless another output path is requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
