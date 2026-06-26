## Description: <br>
Manage Google Ads campaigns - diagnose, optimize, and create campaigns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuckerschreiber](https://clawhub.ai/user/tuckerschreiber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and operators use this skill to inspect Google Ads account health, list campaign and keyword performance, and trigger guarded optimization runs through the Fullrun CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delegate high-impact authority to an external CLI that may change live Google Ads campaigns, bids, keywords, or budgets. <br>
Mitigation: Run diagnostic commands first and require human approval before using fullrun run for campaign-changing actions. <br>
Risk: A leaked or overly broad Fullrun API key could expose Google Ads management capability. <br>
Mitigation: Use the least-privileged API key available, store it only in the FULLRUN_API_KEY environment variable or approved secret storage, and rotate it if exposure is suspected. <br>
Risk: Installing an unverified CLI package can introduce supply-chain risk. <br>
Mitigation: Review before installing and verify the npm package and publisher before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tuckerschreiber/fullrun-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; Fullrun CLI commands return structured JSON by default.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the fullrun binary and FULLRUN_API_KEY; fullrun run is rate-limited to one run per hour.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
