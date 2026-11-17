## Description:

Collect structured Glassdoor company information from one or more known company URLs. Do not use for job-search results or Indeed company URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect structured company information from known Glassdoor company URLs through Dataify Builder and receive completed results or a resumable task ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented behavior and bundled scripts cover more Dataify/Glassdoor workflows than a narrow known-company-URL collector.

Mitigation: Use the skill only for Glassdoor tasks you intend to submit, and verify the selected scraper tool and task ID before execution or follow-up monitoring.

Risk: Generated curl previews can contain user-supplied or otherwise untrusted parameter values.

Mitigation: Inspect generated commands before running them and avoid executing previews that include unexpected URLs, parameters, or shell-sensitive content.

Risk: Dataify API token handling can expose credentials if tokens are pasted into chat, committed, or written into long-lived shell files unnecessarily.

Mitigation: Prefer session-scoped token setup, keep tokens out of chat and version control, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-glassdoor-company-by-url)
- [Tool Parameter Catalog](artifact/references/tool-params.json)
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill)
- [Dataify Builder Endpoint](https://scraperapi.dataify.com/builder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a completed Dataify task result, a task ID, or a resume command when collection is interrupted or times out.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
