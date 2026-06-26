## Description: <br>
Cross-client analytics for Greek accounting firms. Surfaces trends, anomalies, and risks across financial data. Read-only, outputs to /data/reports/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Accounting teams use this skill to review local Greek accounting data across clients, surface portfolio trends and anomalies, and produce confidence-rated advisory findings for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes sensitive cross-client accounting and financial data. <br>
Mitigation: Limit OPENCLAW_DATA_DIR to the intended local accounting dataset and install it only where broad cross-client analysis is authorized. <br>
Risk: Generated analytics reports may reveal sensitive client information. <br>
Mitigation: Protect /data/reports/analytics/ with appropriate access controls and retention policies. <br>
Risk: Scheduled overnight runs could operate outside the intended review process. <br>
Mitigation: Review any external scheduler configuration before enabling recurring analytics jobs. <br>
Risk: The required jq binary could introduce supply-chain risk if installed from an untrusted source. <br>
Mitigation: Install jq only from trusted operating system repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/analytics-and-advisory-intelligence) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/satoshistackalotto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain-English advisory reports, Markdown-style responses, JSON analytics files, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local accounting data from OPENCLAW_DATA_DIR and writes analytics outputs under /data/reports/analytics/.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
