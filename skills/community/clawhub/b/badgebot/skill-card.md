## Description:

Monitor a Slack channel for images or text of leads, extract contact details from badges and business cards, enrich them with Apollo.io, sync them to HubSpot, and handle Slack DM replies that update HubSpot fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mchensf](https://clawhub.ai/user/mchensf)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and operations teams use this skill to turn Slack-posted badge or business-card leads into enriched HubSpot contacts. Developers or workspace admins can use it to configure a polling workflow across Slack, Apollo, and HubSpot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow processes personal lead data from badges, business cards, Apollo, and HubSpot.

Mitigation: Confirm authorization for collecting, enriching, storing, and syncing this data before deployment.

Risk: The workflow relies on Slack, Apollo, and HubSpot credentials and CRM write access.

Mitigation: Use dedicated least-privilege credentials and keep tokens out of logs, prompts, and shared state files.

Risk: The artifact includes example shell-style API calls that could be unsafe if implemented with literal string substitution.

Mitigation: Implement HTTP calls with safe JSON serialization, input validation, and safe temporary-file handling.

Risk: Apollo personal email and phone reveal behavior may expose more contact data than needed.

Mitigation: Disable personal email or phone reveal unless the business workflow specifically requires it.

Risk: The workflow sends lead summaries to a hard-coded Slack user in the artifact.

Mitigation: Make the DM recipient configurable and verify the recipient before sending lead data.

## Reference(s):

- [Apollo People Enrichment API](artifact/references/apollo.md)
- [Apollo People Enrichment Documentation](https://docs.apollo.io/reference/people-enrichment)
- [ClawHub Skill Listing](https://clawhub.ai/mchensf/skills/badgebot)
- [Publisher Profile](https://clawhub.ai/user/mchensf)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands, JSON examples, API request patterns, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and workflow instructions for Slack, Apollo, and HubSpot integrations; it does not itself execute the integrations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
