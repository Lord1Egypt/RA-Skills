## Description: <br>
Search prospects, accounts, contacts, and outreach data in Apollo.io via the Apollo API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, revenue operations, and go-to-market users use this skill to search and enrich Apollo prospects, accounts, contacts, outreach emails, tasks, calls, deals, and CRM records from chat. It can also guide confirmed account, contact, sequence, task, call, and deal updates through the connected Apollo account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a connected Apollo account through ClawLink and can reach sensitive sales, contact, account, and outreach data. <br>
Mitigation: Install only if the publisher and ClawLink connection are trusted, review the Apollo permissions before use, and revoke the connection when it is no longer needed. <br>
Risk: Write, destructive, bulk, sequence, and enrichment operations can modify CRM data or consume Apollo credits. <br>
Mitigation: Preview and confirm the target resource and intended effect before writes or destructive actions, and confirm large searches, bulk operations, or enrichment before execution. <br>
Risk: Apollo tool availability, parameter schemas, IDs, labels, and custom fields can vary by live account and catalog state. <br>
Mitigation: List and describe the live Apollo tools before unfamiliar actions, retrieve required IDs and field definitions from Apollo reference endpoints, and avoid inferring sequence, campaign, label, or custom field identifiers from names. <br>


## Reference(s): <br>
- [ClawHub Apollo Skill Page](https://clawhub.ai/hith3sh/apollo-sales) <br>
- [Apollo API Documentation](https://apolloio.github.io/apollo-api-docs/) <br>
- [Apollo Contact Search API](https://apolloio.github.io/apollo-api-docs/#search-contacts) <br>
- [Apollo Organization Enrichment](https://apolloio.github.io/apollo-api-docs/#organization-enrichment) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON parameters for ClawLink Apollo tool calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool calls use the user's connected Apollo account through ClawLink. The skill emphasizes live tool discovery, preview before writes, explicit confirmation for write or destructive actions, and caution for credit-consuming searches or enrichment.] <br>

## Skill Version(s): <br>
1.0.6 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
