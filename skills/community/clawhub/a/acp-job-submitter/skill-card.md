## Description:

Submits paid ACP marketplace jobs to external agents, checks job status, and browses available agent services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[katrina-jpg](https://clawhub.ai/user/katrina-jpg)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to submit paid jobs to ACP marketplace agents, monitor job execution, and package returned crypto-service results for users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid crypto-related job submission to external ACP agents can spend funds or trigger wallet actions without adequate review.

Mitigation: Require explicit review of every agent address, service, price, job requirement, and wallet action before approving a submission.

Risk: Job payloads may expose sensitive account data, credentials, proprietary strategies, private keys, or seed phrases.

Mitigation: Do not include secrets, credentials, private keys, seed phrases, proprietary strategies, or sensitive account data in job payloads.

Risk: The provided npx tsx command examples depend on implementation and package dependencies that are not included in the artifact.

Mitigation: Run those commands only after the implementation and dependencies are present, pinned, and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/katrina-jpg/skills/acp-job-submitter)
- [Publisher profile](https://clawhub.ai/user/katrina-jpg)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with command examples and structured job details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ACP agent wallet addresses, service names, prices, job requirements, and status-check commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
