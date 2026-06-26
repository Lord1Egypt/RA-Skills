## Description: <br>
Use this skill when you need portable agent self-improvement tooling: capture session handoffs, measure reasoning style, scan guidance for contradictions, log predictions, optimize playbooks, run Socratic questioning, or analyze cross-session coherence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ergopitrez](https://clawhub.ai/user/ergopitrez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Evolution Toolkit to preserve session continuity, audit reasoning patterns, scan guidance for contradictions, log prediction calibration, and improve playbooks across agent workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The toolkit persists self-audit and session-memory files in the configured workspace. <br>
Mitigation: Set EVOLUTION_TOOLKIT_WORKSPACE to a narrow intended directory and periodically delete old imprints, reports, fingerprints, and history. <br>
Risk: Workspace notes, logs, test cases, or playbooks may contain sensitive information that is later stored or processed by the toolkit. <br>
Mitigation: Keep secrets out of CURRENT.md, daily memory logs, test cases, and playbooks before running toolkit scripts. <br>
Risk: skill-optimizer can send configured playbook content to Gemini when run. <br>
Mitigation: Run skill-optimizer only with content approved for Gemini API sharing, and do not treat --dry-run as offline mode. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ergopitrez/evolution-toolkit) <br>
- [Publisher Profile](https://clawhub.ai/user/ergopitrez) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, terminal output, JSON reports, generated files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some scripts write local memory, imprint, report, fingerprint, prediction, or playbook files under the configured workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
