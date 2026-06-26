## Description: <br>
Guided creation of multiple OpenClaw agents and their workspace templates, including scoped questions, draft review, confirmed file writes, optional CLI setup, and summary reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcxGGmu](https://clawhub.ai/user/zcxGGmu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create one or more OpenClaw agent workspaces with structured agent identity, operating rules, user-profile, bootstrap, and style files. It helps gather requirements, draft files, confirm writes, optionally run OpenClaw CLI setup, and summarize created agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent workspace changes, including overwriting files when forced. <br>
Mitigation: Confirm each target workspace path, review every generated file before writing, and use --force only when an overwrite is intended. <br>
Risk: Profile and preference files such as USER.md can accidentally capture sensitive personal or operational information. <br>
Mitigation: Keep secrets and sensitive credentials out of generated profile files and review drafts before committing them to disk. <br>
Risk: CLI setup commands may change OpenClaw agent configuration. <br>
Mitigation: Run CLI setup only after confirming the agent id, workspace path, and whether the user wants docs-only output. <br>


## Reference(s): <br>
- [Create Agents Wizard on ClawHub](https://clawhub.ai/zcxGGmu/create-agents-wizard) <br>
- [Question Bank](references/question-bank.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown drafts, workspace files, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update OpenClaw workspace files after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
