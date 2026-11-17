## Description:

Reviews AI-generated product images before listing or advertising, producing a risk rating, eight item-by-item checks, and prompt fixes that can guide a rerun.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators and image-production teams use the skill to review AI-generated product images before listing or advertising. It returns a structured eight-point report, a recommendation, and prompt corrections; a person should still review the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags external image processing and privacy concerns.

Mitigation: Avoid sending sensitive images until the provider’s data handling and the skill’s behavior have been reviewed.

Risk: The security guidance flags the possibility of reports being overwritten.

Mitigation: Save reports to a dedicated output path and preserve existing reports before running the skill.

Risk: The security assessment has partial analysis coverage.

Mitigation: Treat the scan as incomplete and review the skill and provider data handling before use with sensitive images.

## Reference(s):

- [Skill release page](https://clawhub.ai/dlazyai/skills/detect-task)
- [Provider CLI reference](references/provider-cli.md)
- [Model flags reference](references/model-flags.md)
- [Platform image specifications](references/platform-specs.md)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with a risk rating, an eight-item review table, a recommendation, and prompt correction sentences.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may guide a rerun; model assessments can be inaccurate and require human review.]

## Skill Version(s):

1.0.34 (source: frontmatter; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
