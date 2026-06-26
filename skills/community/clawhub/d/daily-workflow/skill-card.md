## Description: <br>
Bilingual EN/ZH project memory workflow for start work, checkpoint, wrap-up, and handoff. Maintains project-local Docs/ notes with target, metadata, status, compressed context, completed work, pending work, next actions, archives, and legacy migration from older Daily Workflow file names. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[englandtong](https://clawhub.ai/user/englandtong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to keep project-local workflow memory current at start work, checkpoints, wrap-up, and handoff. It records concise project metadata, status, completed work, pending work, next actions, archives, and AI handoff notes under Docs/ so work can resume with clear context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill maintains project-local Docs/ workflow files and may record sensitive project notes if the workspace contains private context. <br>
Mitigation: Review changes to Docs/ before sharing or committing them, and keep secrets, credentials, private customer data, full confidential documents, and large logs out of workflow notes. <br>
Risk: Broad trigger phrases may start the workflow when the user intended a casual note rather than a file update. <br>
Mitigation: Narrow custom trigger phrases in Docs/CONFIG.md or ask the agent to confirm before writing workflow files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/englandtong/daily-workflow) <br>
- [Security Guide](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown files and concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains project-local Docs/ workflow files; no global user state is written by default.] <br>

## Skill Version(s): <br>
3.0.0 (source: release evidence, SKILL.md, SECURITY.md, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
