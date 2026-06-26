## Description: <br>
Bootstrap skill for DiagForge that helps an agent find the repository, understand the project structure, run the canonical cold-start smoke test, and begin the Visio-based drawing workflow safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qweadzchn](https://clawhub.ai/user/qweadzchn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to onboard into the DiagForge Visio workflow, validate a local environment, and start producing editable Visio diagram assets from reference figures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run setup and smoke-test commands from an external DiagForge repository. <br>
Mitigation: Review the repository and Python scripts before execution, then run them only in an environment intended for the DiagForge Visio workflow. <br>
Risk: VISIO_BRIDGE_TOKEN is used for a local Visio bridge and could be exposed if printed or logged. <br>
Mitigation: Set VISIO_BRIDGE_TOKEN only for the user's own local bridge and avoid printing, logging, or sharing the token. <br>


## Reference(s): <br>
- [DiagForge GitHub repository](https://github.com/qweadzchn/DiagForge) <br>
- [Agent Visio Use on ClawHub](https://clawhub.ai/qweadzchn/diagforge-agent-visio-use) <br>
- [qweadzchn publisher profile](https://clawhub.ai/user/qweadzchn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and PowerShell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only onboarding guidance; no executable code is bundled in the package.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
