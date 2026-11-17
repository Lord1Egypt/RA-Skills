## Description:

Read and query retreat participant data from the Ceremonia Airtable base for participant counts, retreat attendance, contact segments, recipient lists, phone numbers, emails, and donation status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[austinmao](https://clawhub.ai/user/austinmao)

### License/Terms of Use:


## Use Case:

External operators and agents use this skill to retrieve Airtable participant records, build consent-aware email and SMS recipient lists, and answer retreat participation questions. Record changes are outside the default posture and require explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive participant contact and donation data.

Mitigation: Install and use it only in workspaces authorized to access the Airtable participant data, and keep contact details out of shared channels and logs unless there is a clear need.

Risk: The skill's record-change logging guidance can persist names, emails, phone numbers, and old or new sensitive values outside Airtable.

Mitigation: For record changes, log record IDs, field names, approval timestamps, and retention details instead of raw PII or sensitive values.

Risk: AIRTABLE_API_KEY may expose participant data if copied into shared memory, transcripts, or logs.

Mitigation: Keep AIRTABLE_API_KEY in an access-controlled environment and avoid echoing it in commands, logs, or agent-visible summaries.

Risk: Recipient lists could be used for outreach without valid consent or unsubscribe handling.

Mitigation: Use recipient lists only for consented outreach and always exclude unsubscribed records before sending email or SMS.

## Reference(s):

- [Airtable Web API Introduction](https://airtable.com/developers/web/api/introduction)
- [ClawHub Skill Page](https://clawhub.ai/austinmao/skills/airtable-participants)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and summarized Airtable query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AIRTABLE_API_KEY and local availability of curl and jq; Airtable pagination must be handled before reporting totals or recipient lists.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
