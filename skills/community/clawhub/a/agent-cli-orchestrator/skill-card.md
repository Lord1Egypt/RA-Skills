## Description: <br>
Orchestrates multiple AI CLI tools by auto-detecting, prioritizing, and switching between them for stable, fallback-enabled automated coding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnatom](https://clawhub.ai/user/cnatom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to detect available AI CLI tools, select an execution strategy, and route coding or research tasks across fallback-capable CLI providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive prompts, diffs, summaries, or task context can be sent to configured AI CLI providers. <br>
Mitigation: Use only in repositories where those providers may receive project context, avoid production secrets in .env files, and require explicit approval before routing sensitive project context. <br>
Risk: The scanner sources shell configuration and can change persistent AI CLI configuration. <br>
Mitigation: Inspect or back up ~/.ai-cli-config.json before running the scanner and review shell configuration before sourcing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnatom/agent-cli-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands, YAML examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask the agent to inspect local configuration and CLI availability before selecting a provider.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
