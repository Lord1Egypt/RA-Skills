## Description: <br>
Analyze OpenClaw agent configuration and API usage patterns to identify cost-saving opportunities, diagnose inefficient heartbeat settings, estimate API spend, and generate recommendations to reduce LLM API costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kryzl19](https://clawhub.ai/user/kryzl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to review OpenClaw configuration, estimate daily, weekly, and monthly API costs, diagnose heartbeat waste, and prioritize practical cost-saving changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts inspect local OpenClaw configuration and installed skill files to estimate API costs. <br>
Mitigation: Run the scripts only in environments where local configuration inspection is acceptable, and review generated reports before sharing them. <br>
Risk: Cost reports are estimates and may differ from actual provider billing. <br>
Mitigation: Compare recommendations against provider cost logs before making billing or operational decisions. <br>
Risk: The security guidance notes required tools such as python3 and bc, and flags that analyze.sh may need a small fix for an undefined tool-overhead variable. <br>
Mitigation: Confirm required local tools are installed and test analyze.sh before relying on its full report output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kryzl19/api-cost-optimizer-kryzl19) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports and terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cost estimates are based on local configuration analysis and user-supplied parameters, not live provider billing data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
