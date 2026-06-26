## Description: <br>
Firm Delivery Export converts structured JSON output from a multi-agent workflow run into deliverables such as GitHub pull requests, Jira or Linear tickets, Markdown reports, project briefs, and structured documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and delivery teams use this skill after a firm-orchestration run to turn workflow results into reviewable team deliverables in GitHub, Jira, Linear, Slack, or Markdown-based documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real pull requests, tickets, messages, and files in team systems. <br>
Mitigation: Use only the token needed for the selected destination, prefer fine-grained repo or project-scoped credentials, and keep generated GitHub work in draft review flows with human approval. <br>
Risk: Exported workflow content may persist sensitive information in external tools, Slack webhooks, or local Markdown fallback files. <br>
Mitigation: Preview and redact content before publishing, restrict destination access, and avoid sending secrets or confidential workflow data to channels or files that are not approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/firm-delivery-export) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON schemas and destination-specific delivery instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create draft GitHub pull requests, Jira or Linear issues, Slack digests, or local Markdown documents depending on the selected delivery format.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
