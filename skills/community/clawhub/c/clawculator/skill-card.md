## Description: <br>
Analyze OpenClaw costs and detect billing issues with bundled source code, no runtime fetches, and only the node binary required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echoudhry](https://clawhub.ai/user/echoudhry) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to audit local configuration, session usage, workspace size, and cost exposure, then review deterministic findings and suggested remediation commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw configuration, session metadata, and transcript-derived usage files. <br>
Mitigation: Review the bundled files before installing and run it only in workspaces where local cost and session analysis is acceptable. <br>
Risk: Generated reports can summarize session and cost history. <br>
Mitigation: Review Markdown, JSON, terminal, and HTML outputs before sharing them outside the local environment. <br>
Risk: Generated HTML snapshots can contact Google Fonts. <br>
Mitigation: Avoid opening or sharing generated HTML in privacy-sensitive or offline contexts until the font import is removed. <br>
Risk: Suggested fix commands may change OpenClaw configuration if copied and executed. <br>
Mitigation: Treat suggested commands as manual advice and review each change before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/echoudhry/clawculator) <br>
- [Declared project homepage](https://github.com/echoudhry/clawculator) <br>
- [Live demo](https://echoudhry.github.io/clawculator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, html, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, Markdown, JSON, and local HTML reports with suggested fix commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Session keys are truncated in output; Markdown reports may be written to a default or user-provided path.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
