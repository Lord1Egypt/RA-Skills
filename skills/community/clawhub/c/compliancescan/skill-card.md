## Description: <br>
Run a GDPR/DSGVO website compliance scan via the compliancescan.eu API; report the 0-100 score and findings, check credits, and list past scans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2g4y1](https://clawhub.ai/user/2g4y1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run compliancescan.eu GDPR/DSGVO website scans, review compliance scores and findings, check available credits, and retrieve prior scan details from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive compliancescan.eu API key. <br>
Mitigation: Require COMPLIANCESCAN_API_KEY from the environment and do not ask for, print, or log the key or Authorization header. <br>
Risk: Starting a full compliance scan can consume account credits or plan allowance. <br>
Mitigation: Start exactly one scan per invocation, avoid automatic retries after most failures, and check in-flight or latest scans after timeouts. <br>
Risk: Operational steps may affect accounts, billing, or production scan history. <br>
Mitigation: Review commands before approving account-impacting actions and use the documented read-only account and scan-list endpoints when a write is not needed. <br>
Risk: API responses can omit or expose unreliable fields for tracker, issue, or security-header results. <br>
Mitigation: Report only fields present in the API response, use the stored scan detail endpoint for authoritative tracker lists, and state unavailable fields instead of inventing values. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/2g4y1/compliancescan) <br>
- [Publisher Profile](https://clawhub.ai/user/2g4y1) <br>
- [compliancescan.eu](https://compliancescan.eu) <br>
- [compliancescan.eu dashboard](https://compliancescan.eu/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Concise Markdown with compliance scores, findings, account status, scan history, and guarded curl/jq command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses COMPLIANCESCAN_API_KEY, curl, and jq; starting a full scan is a write action that can consume one scan credit.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
