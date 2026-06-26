## Description: <br>
App Maker automates a six-phase full-stack application workflow from requirements analysis through UI design, database design, code generation, visual debugging, and deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chall2015](https://clawhub.ai/user/chall2015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to turn natural language requirements or PRD inputs into application plans, project scaffolds, generated frontend and backend code, configuration files, preview setup, and deployment guidance. It is most suitable for rapid prototyping and MVP development where generated outputs can be reviewed before installation, execution, or deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated application code and dependency manifests may introduce unsafe logic, vulnerable packages, or unexpected behavior. <br>
Mitigation: Review generated files before running npm install, starting a development server, or executing generated backend code. <br>
Risk: Model API keys and other secrets may be handled in local configuration files or screenshots. <br>
Mitigation: Use environment variables or a secret manager where possible, keep real keys out of examples and screenshots, and rotate any key that may have been exposed. <br>
Risk: Deployment steps can expose services publicly or create billing and access-control impact. <br>
Mitigation: Deploy only after checking secrets, authentication, authorization, cloud permissions, billing settings, and public network exposure. <br>
Risk: Prompts and project details may be sent to third-party model providers when API keys are configured. <br>
Mitigation: Review prompt contents and provider policies before sending confidential requirements, customer data, or proprietary design details. <br>
Risk: The tool writes generated files under the selected output directory. <br>
Mitigation: Run it in a dedicated workspace, inspect the output path before generation, and avoid pointing it at directories containing important existing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chall2015/app-maker) <br>
- [Publisher profile](https://clawhub.ai/user/chall2015) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Quick start guide](artifact/QUICKSTART.md) <br>
- [Configuration example](artifact/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON configuration, generated source files, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local project files and deployment guidance; generated code, dependency installation, secrets, billing exposure, and public deployment settings should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; packaged artifact metadata lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
