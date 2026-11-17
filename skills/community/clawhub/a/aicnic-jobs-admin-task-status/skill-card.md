## Description:

Queries task status from the AICNIC job management system by fetching job details for a supplied jobId and returning the jobState field.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bylikai](https://clawhub.ai/user/bylikai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check AICNIC task status from a known jobId and retrieve related job metadata such as job ID, name, start time, and end time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided job IDs to an external AICNIC endpoint over plain HTTP, so job IDs and returned job metadata may be visible or modifiable on the network.

Mitigation: Use only job IDs that are acceptable to disclose, prefer HTTPS if the service supports it, and review returned metadata before relying on it.

Risk: Broad activation on ambiguous job identifiers could send unintended identifiers to the external AICNIC service.

Mitigation: Ask for confirmation before sending ambiguous identifiers and limit use to explicit AICNIC task status checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bylikai/skills/aicnic-jobs-admin-task-status)
- [AICNIC jobs API endpoint](http://www.aicnic.cn/jobs/api/jobs/infos/hpcai28/{jobId})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls]

**Output Format:** [Markdown text with optional inline shell commands and parsed status fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns job status and selected job metadata from the AICNIC API response.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
