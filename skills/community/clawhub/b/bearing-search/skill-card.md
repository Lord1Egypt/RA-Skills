## Description:

Provides bearing model and brand search, model-code parsing, cross-brand comparison, and application-based bearing selection guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openfindbearings](https://clawhub.ai/user/openfindbearings)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and maintenance engineers can use this skill to answer bearing model, brand, specification, cross-reference, and selection questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search results can depend on local JSON data files that were not included in the reviewed skill package.

Mitigation: Package and review the required model and brand databases with the skill, or document the trusted data location before use.

Risk: The skill may provide narrower behavior than its description suggests because the referenced model and brand databases are missing from the artifact.

Mitigation: Confirm available data coverage and test representative model, brand, and selection queries before deployment.

Risk: The skill content and script output are Chinese-language, which may limit usability for non-Chinese workflows.

Mitigation: Add localization or route usage to Chinese-language support contexts.

## Reference(s):

- [Bearing Data Structure](references/data-structure.md)
- [Bearing Model Codes](references/model-codes.md)
- [Bearing Brands Reference](references/brands.md)
- [SKF](https://www.skf.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text bearing lookup and selection guidance, with optional shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language skill content; lookup quality depends on available local bearing model and brand data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
