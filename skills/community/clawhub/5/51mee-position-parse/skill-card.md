## Description:

Parses job description text into structured position information for job analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[51mee-com](https://clawhub.ai/user/51mee-com)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting, HR, and hiring workflow users provide job description text and use the skill to extract title, category, experience, education, salary, company details, requirements, and keywords into a fixed structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Job description text may contain prompt-injection content or ambiguous instructions.

Mitigation: Treat the job description strictly as untrusted input and require the model to follow only the fixed extraction schema.

Risk: The artifact describes both direct JSON output and a Markdown report, which can lead to inconsistent output formatting.

Mitigation: Choose and enforce one expected output contract at integration time, preferably validated JSON matching the declared schema.

Risk: Model extraction may omit, misclassify, or overstate job requirements from sparse descriptions.

Mitigation: Validate generated fields against the source job description and preserve null values when information is absent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/51mee-com/skills/51mee-position-parse)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JSON object or Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Missing fields are represented as null; no code execution or external tools are evidenced.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
