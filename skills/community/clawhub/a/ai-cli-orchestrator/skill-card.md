## Description: <br>
Orchestrates multiple AI CLI tools by detecting available providers, prioritizing them, and switching among them for automation workflows with fallback on errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnatom](https://clawhub.ai/user/cnatom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to coordinate installed AI command-line tools, choose a preferred provider, and fall back to another provider when limits, auth failures, timeouts, or validation issues interrupt a task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository context or credential-related configuration may be routed through multiple external AI CLI providers. <br>
Mitigation: Use the skill first on low-sensitivity projects, avoid secret-bearing prompts or diffs, and confirm which providers are enabled before running task automation. <br>
Risk: Automatic fallback can broaden which AI providers receive task context after an error or limit condition. <br>
Mitigation: Review or disable fallback behavior for sensitive work, and set provider priority explicitly before use. <br>
Risk: The scan script writes AI CLI availability configuration in the user's home directory. <br>
Mitigation: Inspect the generated configuration before relying on it and remove providers that should not receive project context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnatom/ai-cli-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and YAML/JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local AI CLI availability configuration for agent workflows.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
