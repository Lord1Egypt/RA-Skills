## Description: <br>
Browser Use Agent is a knowledge skill that helps agents reason about Browser-Use-style web automation workflows and related implementation constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to guide agent-assisted browser automation tasks such as web interaction planning, form handling, data collection, and implementation review. Security evidence should be reviewed before use because the release mixes browser-automation claims with authoritative finance/ZVT guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release scope is unclear because security evidence reports a mismatch between browser-automation claims and authoritative finance/ZVT instructions. <br>
Mitigation: Require publisher clarification of the skill's purpose and triggers before installation or operational use. <br>
Risk: The skill advertises high-impact browser actions such as checkout, login, uploads, and persistent browser profiles. <br>
Mitigation: Do not grant credentials, payment access, persistent profiles, form submission, uploads, purchases, or account-change permissions without explicit domain limits and final human approval gates. <br>
Risk: Generated logs or skill files could retain sensitive workflow details. <br>
Mitigation: Define retention rules for logs and generated files before using the skill with sensitive browsing or finance workflows. <br>


## Reference(s): <br>
- [Authoritative seed.yaml](references/seed.yaml) <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/browser-use-agent) <br>
- [Doramagic crystal page](https://doramagic.ai/zh/crystal/browser-use-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text guidance with code and shell-command snippets when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Host agents consume references/seed.yaml directly; no installation is required.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
