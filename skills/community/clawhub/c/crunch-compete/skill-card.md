## Description: <br>
Use when working with Crunch competitions - setting up workspaces, exploring quickstarters, testing solutions locally, or submitting entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[philippWassibauer](https://clawhub.ai/user/philippWassibauer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and data science practitioners use this skill to work through the CrunchDAO competition lifecycle: setting up isolated workspaces, exploring quickstarters, testing solutions locally, and submitting entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package installation can alter the user's Python environment or introduce dependency risk. <br>
Mitigation: Use a dedicated virtual environment for each competition and review package installs before approving them. <br>
Risk: CrunchDAO submission tokens may be stored in the project's .crunch directory. <br>
Mitigation: Keep the .crunch directory private and never write tokens into source files, scripts, notebooks, logs, or committed files. <br>
Risk: Submission commands can send competition entries to CrunchDAO. <br>
Mitigation: Run local tests first and confirm any crunch push before submitting. <br>


## Reference(s): <br>
- [Crunch Compete on ClawHub](https://clawhub.ai/philippWassibauer/crunch-compete) <br>
- [Crunch CLI Reference](references/cli-reference.md) <br>
- [Competition Setup Examples](references/competition-setup.md) <br>
- [crunch-cli on PyPI](https://pypi.org/project/crunch-cli/) <br>
- [CrunchDAO Hub](https://hub.crunchdao.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and code suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include virtual environment setup, PyPI package installation, Crunch CLI commands, local testing steps, and submission guidance.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
