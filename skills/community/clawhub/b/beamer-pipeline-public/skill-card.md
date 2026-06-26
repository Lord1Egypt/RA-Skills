## Description: <br>
Convert academic papers or notes into Chinese academic Beamer slides using a seven-phase local pipeline with pluggable agent execution and LaTeX compilation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccmxigua](https://clawhub.ai/user/ccmxigua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to convert academic papers or structured notes into Chinese Beamer slide packages with phase prompts, local validation gates, and optional agent or LaTeX execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown image URLs can trigger outbound downloads during asset preparation. <br>
Mitigation: Use --skip-assets for untrusted documents or when outbound network requests are not acceptable, and review asset_manifest.json before using localized figures. <br>
Risk: Configured agent and LaTeX commands can execute local tools in the output workspace. <br>
Mitigation: Use --no-agent for prompt-only runs, review --agent-cmd and --latex-cmd before execution, and run the pipeline in a controlled workspace. <br>
Risk: Generated decks may include source paper text or figures with redistribution limits. <br>
Mitigation: Publish generated decks only when the user has rights to redistribute the source content and figures. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ccmxigua/beamer-pipeline-public) <br>
- [Beamer Pipeline Public skill documentation](artifact/SKILL.md) <br>
- [Beamer Pipeline Public architecture notes](artifact/references/beamer-pipeline-code-explanation.md) <br>
- [Upstream design notes](artifact/references/UPSTREAM_DESIGN_NOTES.md) <br>
- [Beamer generation contract](artifact/templates/beamer_contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown prompts, JSON state files, LaTeX source, PDF output when compilation succeeds, logs, and generated workspace files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local output workspace; may invoke configured local agents or LaTeX tools; can download Markdown image URLs unless --skip-assets is used.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
