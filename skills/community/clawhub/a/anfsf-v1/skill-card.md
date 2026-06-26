## Description: <br>
Asf V4 helps OpenClaw users apply governance gates, ownership proofs, economics scoring, rework-risk analysis, and safe optimization to agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alshowse-tech](https://clawhub.ai/user/alshowse-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to evaluate OpenClaw changes against veto rules, ownership constraints, role-assignment costs, contract coupling, and runtime optimization safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optimizer settings can change governance or workflow behavior when enabled in an OpenClaw environment. <br>
Mitigation: Review optimizer settings before installation and enable them only where those governance changes are acceptable. <br>
Risk: Configuration edits can disrupt an existing OpenClaw setup. <br>
Mitigation: Back up and validate the OpenClaw configuration before editing it. <br>
Risk: Publishing or installation workflows may involve a ClawHub API token. <br>
Mitigation: Protect any ClawHub API token used for publishing or related workflows. <br>
Risk: The bundled security-audit script is a developer helper, not a hardened security boundary. <br>
Mitigation: Treat scripts/security-audit.sh as supplemental review support and rely on normal deployment security controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alshowse-tech/anfsf-v1) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Artifact configuration](artifact/config/asf-v4.config.yaml) <br>
- [OpenClaw project reference](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses and Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool outputs include governance decisions, ownership proofs, scoring results, risk estimates, role-count recommendations, conflict resolutions, and optimizer status.] <br>

## Skill Version(s): <br>
1.5.2 (source: ClawHub release evidence; artifact package metadata reports 0.9.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
