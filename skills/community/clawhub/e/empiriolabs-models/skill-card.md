## Description:

Helps agents find EmpirioLabs AI models and compare their live prices, parameters, limits, and supported endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[empiriolabs](https://clawhub.ai/user/empiriolabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agents use this skill to select an EmpirioLabs AI model for a task, compare current prices, and check supported features and limits before recommending a model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Catalog lookups send requests to EmpirioLabs when model or pricing information is requested.

Mitigation: Use the public catalog only when the user requests a lookup; no API key is needed.

## Reference(s):

- [EmpirioLabs AI model catalog](https://empiriolabs.ai/models)
- [EmpirioLabs AI pricing](https://empiriolabs.ai/pricing)
- [EmpirioLabs AI API documentation](https://docs.empiriolabs.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Plain text or Markdown; optional JSON catalog results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model identifiers, prices, features, limits, and supported endpoints from the public catalog.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
