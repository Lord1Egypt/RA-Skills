## Description:

A Chinese-language Excel formula assistant that turns natural-language requests into Excel formulas, explains formulas, lists common formula templates, and diagnoses common formula errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

External users and spreadsheet practitioners use this skill to generate, understand, browse, and troubleshoot Excel formulas from Chinese natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional AI mode may send the user's formula description to OpenAI.

Mitigation: Avoid using --ai for confidential workbook data, employee information, customer data, or sensitive business context.

Risk: Generated formulas and troubleshooting guidance may be incorrect or incomplete for a specific workbook.

Mitigation: Review and test formulas against representative workbook data before using them in business workflows.

Risk: The release evidence notes an unused or unpinned openpyxl dependency.

Mitigation: Pin or remove unused dependencies before deployment according to the organization's dependency management policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-excel-formula)
- [AISoBrand website](https://aisobrand.com)
- [AISoBrand free diagnosis](https://aisobrand.com/free-diagnosis.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown and plain text with Excel formulas and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language responses; optional AI generation can use OPENAI_API_KEY, while default formula generation uses local template matching.]

## Skill Version(s):

1.2.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
