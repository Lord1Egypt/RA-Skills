## Description: <br>
Display GitHub Copilot premium request usage, quota, billing stats, and per-model multipliers for the authenticated user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitman86r](https://clawhub.ai/user/hitman86r) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and GitHub Copilot users use this skill to inspect premium request usage, remaining quota, overage costs, per-model usage, and alert thresholds from their authenticated GitHub account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires GitHub CLI authentication with billing-related Copilot scope to read usage data. <br>
Mitigation: Install only if you are comfortable granting the GitHub CLI the required scopes, and review the requested scopes before use. <br>
Risk: The displayed remaining quota depends on a locally configured plan because the GitHub API does not expose plan quota. <br>
Mitigation: Configure the correct Copilot plan and update it when the account plan changes. <br>


## Reference(s): <br>
- [GitHub Billing Usage REST API](https://docs.github.com/en/rest/billing/usage) <br>
- [GitHub Copilot Request Multipliers](https://docs.github.com/en/copilot/concepts/billing/copilot-requests#model-multipliers) <br>
- [API Reference](references/api.md) <br>
- [Model Multipliers](references/multipliers.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text dashboard, optional JSON, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local plan setting to ~/.config/copilot-usage/config.json when configured by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
