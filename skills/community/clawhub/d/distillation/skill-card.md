## Description:

Distillation helps users collect distillation-tower CAD parameters, calculate them through jixietools.com, and create a guest production sheet for generated drawing results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liv09370](https://clawhub.ai/user/liv09370)

### License/Terms of Use:

MIT-0

## Use Case:

External users and engineers use this skill to generate distillation-tower CAD drawing workflows by selecting a product, entering parameters one at a time, reviewing calculated values, and creating a guest production sheet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CAD and design parameters are sent to the external service jixietools.com.

Mitigation: Disclose this data sharing before use and avoid submitting sensitive or proprietary design details unless the user has approved that service.

Risk: Generated results are returned through unauthenticated guest links.

Mitigation: Warn users that generated links may expose result details and should be shared only with intended recipients.

Risk: The security summary reports inconsistent product-category instructions that could send design details into the wrong workflow.

Mitigation: Verify the selected product and category before submitting parameters; the publisher should align the category instructions before release.

Risk: Shell interpolation examples can mishandle user-provided values.

Mitigation: Prefer structured HTTP requests with JSON serialization and review command inputs before execution.

## Reference(s):

- [ClawHub Distillation skill page](https://clawhub.ai/liv09370/skills/distillation)
- [Jixietools API base endpoint](https://jixietools.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown with parameter tables, curl command examples, JSON response summaries, status updates, and generated service links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include guest production-sheet links and output-file lists returned by jixietools.com after user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
