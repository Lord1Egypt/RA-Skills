## Description: <br>
Contract Check guides users through company-specific contract review settings, then reviews business contracts for veto-level risks, warnings, required clauses, and improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chartgen-ai](https://clawhub.ai/user/chartgen-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users and legal or commercial teams use this skill to initialize company contract review thresholds and assess PDF, Word, or text contracts against those thresholds. It produces a structured review report with veto items, warnings, required-clause checks, and suggested revisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved contract-review settings may contain sensitive business thresholds or negotiation preferences. <br>
Mitigation: Use the skill only in a trusted workspace, avoid storing confidential thresholds unless needed, and remove the local configuration when it should no longer be reused. <br>


## Reference(s): <br>
- [Contract Check ClawHub release page](https://clawhub.ai/chartgen-ai/contract-check) <br>
- [Configuration questions reference](references/config-questions.md) <br>
- [Contract redlines reference](references/redlines.md) <br>
- [Contract keyword reference](references/keywords.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, shell commands] <br>
**Output Format:** [Markdown-style contract review report with JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-only behavior; may write a reusable contract-review configuration file in the user's workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
