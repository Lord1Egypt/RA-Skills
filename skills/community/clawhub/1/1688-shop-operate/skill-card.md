## Description: <br>
1688 Shop Operate helps agents run authenticated 1688 shop health diagnostics for core metrics, traffic structure, industry transaction ranking, and customer profile analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External 1688 shop operators and supporting agents use this skill to retrieve store operation data and produce concise Markdown health reports. It supports peer comparison, traffic analysis, transaction ranking, customer profile analysis, and follow-up improvement guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a 1688 AK credential and stores it locally. <br>
Mitigation: Use the browser AK flow when possible, avoid placing the AK in chat, screenshots, logs, or shared directories, and clear the AK with `configure --clear` when finished. <br>
Risk: Diagnostic commands may expose sensitive store performance data in command output or logs. <br>
Mitigation: Run the skill only in trusted workspaces, avoid logging `configure --status`, and limit report sharing to intended recipients. <br>
Risk: Automatic usage reporting and the local callback server introduce review-sensitive behavior in shared or managed environments. <br>
Mitigation: Review these behaviors before deployment and use the skill only where local callback handling and usage reporting are acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/1688-shop-operate) <br>
- [AK Configuration Guide](references/capabilities/configure.md) <br>
- [Core Metrics Guide](references/capabilities/get_core_metrics.md) <br>
- [Traffic Structure Guide](references/capabilities/get_traffic_structure.md) <br>
- [Transaction Ranking Guide](references/capabilities/get_transaction_ranking.md) <br>
- [Customer Profile Guide](references/capabilities/get_customer_profile.md) <br>
- [Common Error Handling](references/common/error-handling.md) <br>
- [1688 AK Portal](https://clawhub.1688.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command results with Markdown report content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return success status, markdown, and structured data; reports must be grounded in returned data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
