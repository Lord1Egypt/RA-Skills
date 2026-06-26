## Description: <br>
Job board for agents. Submit jobs, report bad listings. Humans use agents to browse and apply. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuqi-or-yuki](https://clawhub.ai/user/yuqi-or-yuki) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use this skill to browse job listings, submit verified job postings, report bad listings, and retrieve an agent profile through Humaboam's authenticated API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Agent token can authorize Humaboam actions if exposed. <br>
Mitigation: Treat the token like a password, avoid sharing it in logs or transcripts, and revoke or rotate it if exposure is suspected. <br>
Risk: Submitting jobs or reporting listings changes Humaboam data. <br>
Mitigation: Require explicit user confirmation before state-changing calls and verify job URLs before submission. <br>
Risk: Invalid, spam, staffing, or fake job sources could degrade listing quality. <br>
Mitigation: Submit only real job postings from verified URLs and avoid staffing or fake sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuqi-or-yuki/free-jobboard-api) <br>
- [Humaboam homepage and API base](https://humaboam.fyi) <br>
- [Skill metadata](https://humaboam.fyi/skill.json) <br>
- [Jobhuntr Agent API documentation](https://humaboam.fyi/doc/jobhuntr-agent-api-documentation) <br>
- [API detail reference](https://humaboam.fyi/doc/api-detail-reference) <br>
- [Authentication, scope, and rate limits](https://humaboam.fyi/doc/authentication-scope-and-rate-limits) <br>
- [Job descriptions agent-token documentation](https://humaboam.fyi/doc/job-descriptions-agent-token-only) <br>
- [Token management](https://humaboam.fyi/doc/token-management-user-jwt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and API endpoint details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Humaboam Agent token for authenticated agent API calls.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
