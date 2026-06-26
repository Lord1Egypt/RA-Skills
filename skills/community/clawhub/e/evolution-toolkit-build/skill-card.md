## Description: <br>
Evolution Toolkit provides portable agent self-improvement tooling to capture session handoffs, analyze reasoning style, scan guidance for contradictions, log predictions, optimize playbooks, run Socratic questioning, and analyze cross-session coherence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ergopitrez](https://clawhub.ai/user/ergopitrez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve session continuity, analyze reasoning and guidance drift, run prediction and calibration workflows, and improve agent playbooks across workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The toolkit can retain private workspace-derived profiles, session imprints, prediction logs, and coherence reports. <br>
Mitigation: Use a dedicated workspace, avoid storing secrets or sensitive customer/internal content in memory logs, and review files written under memory/. <br>
Risk: Configured playbook optimization can send playbook or test-case data to Gemini or Google services. <br>
Mitigation: Use a limited API key and run the optimizer only after confirming the configured inputs are safe to send externally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ergopitrez/evolution-toolkit-build) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Session Continuity Protocol](artifact/protocols/session-continuity.md) <br>
- [Thinking Partner Protocol](artifact/protocols/thinking-partner.md) <br>
- [Example configuration](artifact/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, Markdown reports, optional JSON output, shell command examples, and configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some tools write local memory or report files under the configured workspace; the playbook optimizer can use Gemini or Google API keys when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
