## Description: <br>
Alibaba International Station weekly business report analysis skill. Retrieves store weekly report data via browser session, validates, and presents structured diagnostics with on-demand deep report access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simoncai519](https://clawhub.ai/user/simoncai519) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Alibaba International Station sellers and e-commerce operators use this skill to retrieve weekly store-report data through an authenticated browser session, validate the response, and receive structured diagnostics with on-demand follow-up analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads private Alibaba International Station business reports from the currently logged-in browser account. <br>
Mitigation: Use a limited browser profile or limited account, confirm each fetch explicitly, and avoid accounts containing data that should not be exposed to the agent session. <br>
Risk: Detailed report retrieval can expose broader account data than the initial summary. <br>
Mitigation: Fetch the full report only after summary validation succeeds and keep follow-up analysis limited to explicit user questions. <br>
Risk: Repeated or automated requests may trigger throttling, system-busy responses, or unreliable report access. <br>
Mitigation: Limit report API calls to at most once per minute per user and stop or retry gently when Alibaba returns unavailable responses. <br>


## Reference(s): <br>
- [Workflow details](references/workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/simoncai519/alibaba-store-analysis) <br>
- [Alibaba International Station dashboard](https://i.alibaba.com/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown with tables, bullet lists, report links, and concise follow-up answers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the current authenticated Alibaba browser session; retrieves summary data first and detailed report data only after validation succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
