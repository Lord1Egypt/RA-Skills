## Description:

Guides a Chinese-language workflow for generating acrylonitrile synthesis section CAD drawings through the JixieTools guest production-sheet API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liv09370](https://clawhub.ai/user/liv09370)

### License/Terms of Use:

MIT-0

## Use Case:

External users and engineering agents use this skill to collect CAD design parameters, call JixieTools calculation and guest production-sheet endpoints, and present generated drawing status and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Engineering design parameters are sent to unauthenticated guest endpoints on jixietools.com.

Mitigation: Use the skill only for parameters acceptable to share with that service, and review values before submission.

Risk: Returned filenames, guest codes, and production-sheet URLs may function as private access links.

Mitigation: Treat returned identifiers and links as sensitive, and avoid sharing them in public logs or messages.

Risk: The release security summary notes a mismatch between the acrylonitrile purpose and gear-product examples or category IDs.

Mitigation: Verify the product and category mapping before relying on the generated CAD output for acrylonitrile work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liv09370/skills/acrylonitrile)
- [JixieTools API base](https://jixietools.com/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API calls]

**Output Format:** [Chinese conversational guidance with Markdown tables, JSON examples, and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns calculation values, generated filenames, guest codes, production-sheet URLs, status updates, and generated file links when the external service succeeds.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
