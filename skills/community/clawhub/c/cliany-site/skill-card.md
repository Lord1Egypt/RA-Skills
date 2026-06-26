## Description: <br>
Use when the user wants to automate web workflows into CLI commands via Chrome CDP and LLM. Supports exploring pages, generating adapters, and replaying actions through the cliany-site tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pearjelly](https://clawhub.ai/user/pearjelly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn browser workflows into repeatable CLI commands, including environment checks, website login, workflow exploration, adapter generation, and command replay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can automate websites through Chrome, including logged-in sessions. <br>
Mitigation: Use test or low-privilege accounts first and avoid sensitive pages unless the configured LLM provider is trusted with page structure and text. <br>
Risk: Generated adapters and commands may perform unintended website actions. <br>
Mitigation: Review generated adapters and commands before running them against important accounts or production workflows. <br>
Risk: Saved browser sessions can persist after automation is complete. <br>
Mitigation: Clear saved sessions when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pearjelly/cliany-site) <br>
- [Publisher profile](https://clawhub.ai/user/pearjelly) <br>
- [Project homepage](https://github.com/pearjelly/cliany.site) <br>
- [Project documentation](https://cliany.site) <br>
- [Support issues](https://github.com/pearjelly/cliany.site/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with CLI commands, JSON envelopes, and generated Python/Click adapter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or replay website-specific adapter commands after Chrome CDP and LLM credentials are configured.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
