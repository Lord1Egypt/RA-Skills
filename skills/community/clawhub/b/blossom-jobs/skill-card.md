## Description:

Set up Blossom Hire, create local work opportunities, and help employers and jobseekers move through Blossom work flows in plain language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbiwu](https://clawhub.ai/user/robbiwu)

### License/Terms of Use:

MIT-0

## Use Case:

External employers and jobseekers use this skill to set up Blossom Hire accounts, post or manage local work opportunities, search and apply for jobs, review candidates, and schedule PopIns through confirmed Blossom marketplace requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A permanent unscoped Blossom account API key grants durable account access if exposed.

Mitigation: Persist the key only in secure credential storage, never paste or log it, and contact Blossom support to rotate or revoke access if exposure is suspected.

Risk: Marketplace actions can create, update, delete, post, apply for, or schedule work-related records.

Mitigation: Summarize the exact action and target, obtain clear user confirmation, and claim completion only from the structured successful action returned by Blossom.

Risk: Unrelated personal data, credentials, or conversation history could be sent to Blossom unnecessarily.

Mitigation: Send only the minimum current Blossom-related instruction and avoid forwarding unrelated prompts, documents, credentials, cookies, tokens, notes, or hidden reasoning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robbiwu/skills/blossom-jobs)
- [Blossom homepage](https://blossomai.org)
- [Blossom protocol API](https://hello.blossomai.org/api/v1/blossom/protocol)

## Skill Output:

**Output Type(s):** [Guidance, Text, API calls, Configuration]

**Output Format:** [Markdown and JSON/HTTP request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes concise user-facing responses and Blossom API requests based on confirmed marketplace actions.]

## Skill Version(s):

2.0.2 (source: server release metadata; artifact frontmatter reports 4.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
