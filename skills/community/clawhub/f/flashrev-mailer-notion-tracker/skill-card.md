## Description: <br>
Logs FlashRev mailer send and dry-run records to a configured Notion database for tracking, auditing, and campaign history lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sawera557](https://clawhub.ai/user/sawera557) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators running FlashRev outreach use this skill after send or dry-run batches to sync campaign send history into Notion and query prior sends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FlashRev outreach metadata and email body previews can be sent to the configured Notion database. <br>
Mitigation: Install only when that data handling is acceptable, restrict the Notion integration to the intended database, and use query-only mode when inspection is sufficient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sawera557/flashrev-mailer-notion-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js plus NOTION_TOKEN and NOTION_DATABASE_ID; can write records to Notion or query existing campaign records.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
