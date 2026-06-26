## Description: <br>
Prepare and publish an OpenClaw skill to ClawHub with checks for sensitive content, generalization steps, directory scaffolding, git setup, and a confirmed ClawHub publish command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cdmichaelb](https://clawhub.ai/user/cdmichaelb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to prepare new or updated OpenClaw skills for ClawHub publication. It guides them through auditing, creating a publishable copy, generalizing configuration, verifying the clean state, and publishing only after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing can make skill contents public. <br>
Mitigation: Review generated files and approve the final `npx clawhub@latest publish` command only after confirming no sensitive content remains. <br>
Risk: The skill asks an agent to inspect skill directories for secrets, PII, hardcoded paths, and other sensitive content. <br>
Mitigation: Use it only on skill directories the user intends to prepare for publication and review the audit findings before creating a publishable copy. <br>


## Reference(s): <br>
- [ClawdHub Publish Helper on ClawHub](https://clawhub.ai/cdmichaelb/clawhub-publish-helper) <br>
- [ClawHub](https://clawhub.ai) <br>
- [Audit Checklist](references/checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and checklist-style guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user review and confirmation before any publish command is run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
