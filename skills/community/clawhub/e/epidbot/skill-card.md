## Description:

Interact with EpidBot - AI-powered assistant for Brazilian public health data (DATASUS/SINAN).

This skill is ready for commercial/non-commercial use.

## Publisher:

[fccoelho](https://clawhub.ai/user/fccoelho)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query the EpidBot REST API for public-health data analysis, report retrieval, file upload workflows, and dataset or knowledge-base operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests, uploaded files, query content, and results are transmitted to the external EpidBot service.

Mitigation: Confirm the user trusts the EpidBot service, has authority to share the data, and has minimized or de-identified sensitive public-health information before use.

Risk: Publishing a dataset can make private data visible to all EpidBot users.

Mitigation: Require explicit confirmation before publishing and verify the dataset contains no sensitive, identifiable, or regulated data.

Risk: Authentication material could be exposed if credentials or tokens are included in datasets or request bodies.

Mitigation: Keep credentials in environment variables and do not upload secrets, API keys, or tokens as data.

## Reference(s):

- [EpidBot homepage](https://kwar-ai.com.br/epidbot)
- [ClawHub skill page](https://clawhub.ai/fccoelho/skills/epidbot)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown, API calls]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses environment variables for API authentication and base URL configuration.]

## Skill Version(s):

2.4.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
