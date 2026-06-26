## Description: <br>
Use Augment Code (Auggie CLI) to analyze, generate, and modify code through Edith smart glasses or OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samdickson22](https://clawhub.ai/user/samdickson22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to call Augment Code's Auggie CLI from Edith smart glasses or OpenClaw for code generation, project analysis, debugging, prototyping, and code guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A coding-agent CLI may access repository contents, including secrets or sensitive proprietary code. <br>
Mitigation: Run the skill only in scoped repositories under version control and avoid projects containing secrets or sensitive proprietary code unless that exposure is acceptable. <br>
Risk: Generated code, debugging advice, or project analysis may be incorrect or unsuitable for the target codebase. <br>
Mitigation: Review generated changes and recommendations before applying or deploying them. <br>
Risk: Installing Auggie from an untrusted source could introduce supply-chain risk. <br>
Mitigation: Install Auggie only from the official Augment Code source. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/samdickson22/edith-augment-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and concise natural-language summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should summarize generated code, analysis findings, debugging causes and fixes, or setup errors for voice-friendly delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and shipables.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
