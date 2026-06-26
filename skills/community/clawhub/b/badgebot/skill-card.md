## Description: <br>
Monitors a Slack channel for lead images or text, extracts contact details, enriches them through Apollo, syncs to HubSpot, and replies in Slack with summaries and contact links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mchensf](https://clawhub.ai/user/mchensf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and operations teams use this skill to turn Slack-posted badge or business-card leads into enriched CRM contacts. It supports Slack polling, Apollo enrichment, HubSpot contact lookup or updates, and in-thread follow-up workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can move personal contact data across Slack, Apollo, and HubSpot. <br>
Mitigation: Use least-privilege tokens, confirm that the Slack channel, HubSpot portal, and DM recipient are authorized, and document retention and cleanup for state files and logs. <br>
Risk: The workflow can update HubSpot CRM records based on Slack replies. <br>
Mitigation: Require review before HubSpot writes and constrain accepted update instructions to approved CRM fields. <br>
Risk: Apollo enrichment can reveal personal emails or phone numbers. <br>
Mitigation: Disable personal email and phone reveal unless approved for the deployment. <br>


## Reference(s): <br>
- [Apollo People Enrichment API](references/apollo.md) <br>
- [Apollo People Enrichment documentation](https://docs.apollo.io/reference/people-enrichment) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes workflow steps for Slack polling, Apollo enrichment, HubSpot updates, state tracking, and operational error handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
