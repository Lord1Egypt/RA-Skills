## Description:

Prepare and submit an observed physical or digital problem to CleanApp, choose publication and notice permissions, or track recorded review decisions and actions. Use for a user's hazard, access barrier, waste, infrastructure, software bug, scam or service failure report. Excludes ordinary advice, emergency dispatch and autonomous bulk collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[borisolver](https://clawhub.ai/user/borisolver)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to prepare a factual report about an observed hazard, access barrier, waste, infrastructure issue, software bug, scam, or service failure. It can preview the report, submit it with the user's chosen publication and notice permissions, and explain the recorded receipt status and next action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitting a report can permit publication or notices when those permissions are explicitly approved and the report passes server checks.

Mitigation: Review the exact report and both handling permissions before submission; request private publication and no notices when that is preferred.

Risk: The private receipt contains a bearer tracking token that authorizes status checks for that receipt.

Mitigation: Keep the receipt file private and out of shared logs, posts, and commits.

## Reference(s):

- [CleanApp agent onboarding](https://www.cleanapp.io/agents)
- [CleanApp agent intake API reference](references/API_REFERENCE.md)
- [ClawHub release page](https://clawhub.ai/borisolver/skills/cleanapp)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Guidance]

**Output Format:** [JSON report payloads and concise text summaries of private receipts and status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submissions require approval for the exact report and its publication and notice permissions. Receipts contain a private tracking token; publication, notice delivery, and issue resolution are not guaranteed.]

## Skill Version(s):

0.3.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
