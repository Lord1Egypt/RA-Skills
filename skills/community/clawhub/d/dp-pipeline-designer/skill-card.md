## Description:

Designs, generates, submits, and monitors DP Data Processing Platform pipelines from natural-language requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hxp365](https://clawhub.ai/user/hxp365)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to translate pipeline requirements into DP Platform and Apache Flink job designs, StreamJob XML configuration, REST API submissions, and job status guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles DP_API_KEY and includes a documented HTTP server example.

Mitigation: Configure DP_SERVER_URL with HTTPS, use only trusted DP Platform endpoints, and avoid sending real API keys to unencrypted HTTP URLs.

Risk: The skill can submit and start DP Platform jobs.

Mitigation: Review generated pipeline designs before execution and confirm submitted jobs cannot affect production data unless that is intended.

Risk: API keys could be exposed in logs or user-visible output.

Mitigation: Do not print or store any part of DP_API_KEY in logs, generated files, or troubleshooting output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hxp365/skills/dp-pipeline-designer)
- [Publisher Profile](https://clawhub.ai/user/hxp365)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with StreamJob XML, curl commands, status summaries, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit and start DP Platform jobs through REST API calls when the required server URL and API key are configured.]

## Skill Version(s):

2.0.1 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
