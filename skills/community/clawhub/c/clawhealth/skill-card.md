## Description: <br>
Performs a two-phase OpenClaw audit with a fast structural scan and a detailed quality review for security, cron jobs, configuration, and skill health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[merlinrabens](https://clawhub.ai/user/merlinrabens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw installations, identify security and operational hygiene issues, and prioritize remediation for configuration, cron, and skill quality problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw configuration, cron, skill, and workspace files and may encounter sensitive values. <br>
Mitigation: Mask secret values and report only file paths, key names, and secret types unless the user explicitly approves more detail. <br>
Risk: Audit findings and remediation guidance can affect operational configuration decisions. <br>
Mitigation: Review findings before applying changes, and treat the skill output as recommendations rather than automatic configuration edits. <br>


## Reference(s): <br>
- [Remediation Guide](references/remediation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Markdown report with JSON scan results and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with python3 and reports findings, scores, and recommended actions.] <br>

## Skill Version(s): <br>
0.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
