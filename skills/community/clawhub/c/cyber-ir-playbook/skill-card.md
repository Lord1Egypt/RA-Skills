## Description: <br>
Build incident response timelines and report packs from event logs for detection-to-recovery reporting, phase tracking, and stakeholder-ready incident summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x-Professor](https://clawhub.ai/user/0x-Professor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security operations and incident-response teams use this skill to convert incident event logs into ordered timelines, phase summaries, and internal or executive report artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incident logs and generated reports may contain sensitive internal response details. <br>
Mitigation: Run the skill only on files intended for analysis, choose an appropriate output location, and review reports before sharing them outside the incident-response team. <br>
Risk: Generated timelines or phase summaries may be incomplete or misleading if source events are missing, malformed, or out of scope. <br>
Mitigation: Validate event inputs and review the generated report before using it for operational or stakeholder decisions. <br>


## Reference(s): <br>
- [IR Phase Guide](references/ir-phase-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated JSON, Markdown, or CSV report artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report generation reads JSON incident input up to 1 MiB and writes the selected output artifact.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
