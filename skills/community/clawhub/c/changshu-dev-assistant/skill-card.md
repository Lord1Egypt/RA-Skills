## Description: <br>
Changshu Dev Assistant helps developers migrate SQL Server SQL to Dameng, scan code for security and quality issues, search local knowledge bases, and manage prompt and model-usage workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fish1981bimmer](https://clawhub.ai/user/fish1981bimmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for Dameng database migration work, SQL analysis and formatting, code security and quality review, local knowledge-base lookup, and LLM-backed development assistance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad local developer-assistant access and can read or process local project and knowledge-base files. <br>
Mitigation: Review the code before installation and restrict WIKI_PATH or other search targets to non-sensitive folders. <br>
Risk: External LLM settings can transmit prompts or code to configured model providers. <br>
Mitigation: Enable external LLM configuration only for projects where sending prompts to that provider is intended and approved. <br>
Risk: Command-line arguments and configuration can expose secrets if API keys or passwords are passed directly. <br>
Mitigation: Use environment variables for LLM credentials and avoid passing secrets on the command line. <br>
Risk: Run and conversion features may execute or import code from other local Hermes skill locations. <br>
Mitigation: Use run and convert commands only with trusted local skill directories and review imported tools before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fish1981bimmer/changshu-dev-assistant) <br>
- [Quickstart Guide](templates/QUICKSTART.md) <br>
- [Dameng Database Guide](references/dameng_database_guide.md) <br>
- [Script Audit Report](references/audit-2026-06-06.md) <br>
- [Hardcoding Audit and Fix](references/hardcoding-audit-2026-06-20.md) <br>
- [Optimization Suggestions](references/optimization-suggestions.md) <br>
- [Test Automation Guide](references/test_automation_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, terminal text, generated code snippets, JSON reports, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include SQL conversion results, scan findings, knowledge-base matches, prompt templates, model statistics, and setup guidance.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
