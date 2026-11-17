## Description:

Ai C Plan reads AI-C project plan files in MD or CSV format and autonomously implements steps in dependency order, including code changes, tests, reporting, environment examples, migrations, progress tracking, and commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sercanmetalore](https://clawhub.ai/user/sercanmetalore)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to execute AI-C repository project plans end to end from plan files, while producing implementation changes, validation output, progress records, and commits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a highly autonomous implementation workflow with broad authority over repository changes, migrations, progress files, and git history.

Mitigation: Use it only for the intended AI-C repository layout and require explicit review before migrations, git initialization, git add ., or commits.

Risk: The skill text references hardcoded /home/adige/AI-C paths and treats repository architecture documents as execution guidance.

Mitigation: Change hardcoded paths to workspace-local paths before use and review project documents as untrusted input before allowing them to steer implementation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sercanmetalore/skills/ai-c-plan)
- [ClawHub Publisher Profile](https://clawhub.ai/user/sercanmetalore)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown progress reports with code, file changes, shell commands, and configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify repository files, environment example files, migration files, progress records, and git commits when allowed by the workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
