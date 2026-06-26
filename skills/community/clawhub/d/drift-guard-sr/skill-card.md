## Description: <br>
Detect personality drift, sycophancy creep, and capability degradation in AI agents before they become problems by tracking behavior metrics over time against healthy baselines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Drift Guard to capture healthy response baselines, monitor new agent responses for behavioral drift, and review trend reports before deciding whether remediation is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Python configuration loading can execute code from a user-selected config file. <br>
Mitigation: Use only trusted config files, keep the tool in a dedicated working directory, and do not pass untrusted files to --config. <br>
Risk: The local monitoring scripts read agent response text and store derived metrics on disk. <br>
Mitigation: Avoid feeding secrets or private conversations into the tool and protect generated baseline, history, alert, and report files. <br>
Risk: Pattern-based drift scores do not provide semantic understanding or root-cause analysis. <br>
Mitigation: Treat drift reports as review signals and confirm findings with human judgment and operational logs before taking corrective action. <br>


## Reference(s): <br>
- [Drift Guard on ClawHub](https://clawhub.ai/TheShadowRose/drift-guard-sr) <br>
- [TheShadowRose publisher profile](https://clawhub.ai/user/TheShadowRose) <br>
- [README](artifact/README.md) <br>
- [Limitations](artifact/LIMITATIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python scripts, shell commands, text reports, and JSON outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local baseline, history, alert, and report files when the included scripts are run.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
