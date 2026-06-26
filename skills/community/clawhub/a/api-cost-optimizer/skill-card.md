## Description: <br>
Analyze OpenClaw agent configuration and API usage patterns to estimate API spend, diagnose heartbeat waste, and recommend cost-saving changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kryzl19](https://clawhub.ai/user/kryzl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to estimate OpenClaw API spend, diagnose heartbeat-related waste, and prioritize configuration changes before costs grow unexpectedly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated optimization guidance may be applied to agent or heartbeat configuration without review. <br>
Mitigation: Review generated AGENTS.md and HEARTBEAT.md changes before replacing existing files, keep a backup, and be cautious with optional provider or API-key configuration patches. <br>
Risk: Cost estimates may differ from actual provider billing because the scripts use configuration analysis and default pricing rather than live metering. <br>
Mitigation: Compare estimates with provider cost logs before making budget or production configuration decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kryzl19/api-cost-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown-style cost reports and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Estimates are based on configuration analysis and default provider pricing, not live API metering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
