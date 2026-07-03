## Description: <br>
Use when turning a coding goal or PRD into bounded build missions, running those missions with Codex or Droid, verifying outcomes separately, and preserving receipts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h-mascot](https://clawhub.ai/user/h-mascot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Geordi to break coding goals or PRDs into bounded agent missions, run those missions through Codex or Droid, and preserve verification logs and receipts. It is suited for feature work, refactors, test fixes, and review follow-up where separate acceptance checks are required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer creates a PATH command and relies on remote GitHub code. <br>
Mitigation: Review the installer and install from a pinned, inspected checkout before using the skill in important repositories. <br>
Risk: Mission prompts, receipts, and logs may include local project context or sensitive repository details. <br>
Mitigation: Do not run Geordi in repositories containing secrets or sensitive private data unless that context is approved for agent prompts and local receipts. <br>
Risk: The reviewed package is missing the CLI executable that the installer expects. <br>
Mitigation: Confirm the bundle contains the expected executable and run the documented version and doctor checks before relying on the installed command. <br>


## Reference(s): <br>
- [Geordi ClawHub release page](https://clawhub.ai/h-mascot/geordi) <br>
- [Geordi build loop](references/geordi-build-loop.md) <br>
- [Geordi agent identity](references/geordi-agent-identity.md) <br>
- [Geordi README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local mission, prompt, log, and state files when the tool is installed and run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces bounded mission definitions, agent prompts, command receipts, verification logs, and local .geordi state.] <br>

## Skill Version(s): <br>
1.0.603 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
