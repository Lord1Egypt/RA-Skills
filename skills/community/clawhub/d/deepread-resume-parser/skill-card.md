## Description:

Parse resumes and CVs into structured JSON - contact info, work history, education, skills, and total years of experience, with support for PDF, Word-exported PDF, and scanned resumes in varied layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uday390](https://clawhub.ai/user/uday390)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, recruiting teams, ATS builders, and talent operations teams use this skill to convert candidate resumes into structured data for ingestion, sourcing, skills matching, and review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume contents can include personal contact details and work-history data that are sent to DeepRead's API.

Mitigation: Review DeepRead's privacy and retention terms before processing real candidate data, and avoid sending resumes unless that external processing is acceptable.

Risk: The skill requires a DeepRead API key and may use BYOK-related account configuration.

Mitigation: Confirm API-key handling and BYOK routing in DeepRead's dashboard before production use.

Risk: Optional related DeepRead skills may add separate behavior beyond this parser.

Mitigation: Inspect and scan optional related skills before installing or using them.

## Reference(s):

- [DeepRead homepage](https://www.deepread.tech)
- [ClawHub skill page](https://clawhub.ai/uday390/skills/deepread-resume-parser)
- [DeepRead support issues](https://github.com/deepread-tech/deep-read-service/issues)

## Skill Output:

**Output Type(s):** [JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON responses with Markdown, Python, and cURL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPREAD_API_KEY and sends selected resume files to DeepRead's API for processing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
