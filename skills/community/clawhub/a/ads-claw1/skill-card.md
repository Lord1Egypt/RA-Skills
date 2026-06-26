## Description: <br>
Telegram-first ads operations assistant for reporting, budget pacing, proposals, and competitor notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Phap1106](https://clawhub.ai/user/Phap1106) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ad operators and business owners use this skill to review Telegram-first campaign status, budget pacing, alerts, draft proposals, and competitor notes before making account decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use broad external search, scraping, credentials, and an unrestricted REST API tool. <br>
Mitigation: Restrict connected tools and API keys to least privilege, preferably read-only access, before installation. <br>
Risk: POST or account-changing API calls could affect ad accounts or spend if used without review. <br>
Mitigation: Require explicit confirmation before any http_request, POST, or account-changing action. <br>
Risk: Competitor research prompts may expose confidential campaign, customer, or account data to external services. <br>
Mitigation: Avoid including confidential data in competitor research unless the user has approved sharing it with those services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Phap1106/ads-claw1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Concise Markdown or text updates with proposal-style recommendations and command-oriented guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should distinguish facts from inferences, note missing or stale data, and request approval before spend-affecting actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
