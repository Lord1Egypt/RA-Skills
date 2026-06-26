## Description: <br>
Creates standardized directory structures for AI model projects, covering data, tokenization, model training, experiments, provenance tracking, quality records, health checks, trace generation, run comparison, checkpoint management, and strict documentation rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billwanttobetop](https://clawhub.ai/user/billwanttobetop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI engineers use this skill to scaffold and maintain organized AI model project workspaces for data preparation, tokenization, training, post-training, reinforcement learning, evaluation, and documentation hygiene. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project scaffolding and upgrade commands can create or update files in the selected project directory. <br>
Mitigation: Run commands from the intended workspace, review generated files before committing them, and keep project work under version control. <br>
Risk: The documentation linter can edit documents in place when run with --fix. <br>
Mitigation: Run the linter without --fix first, inspect reported issues, and apply fixes only after confirming the affected files. <br>
Risk: Checkpoint cleanup can delete checkpoint files when run without --dry-run. <br>
Mitigation: Use checkpoint_mgmt clean with --dry-run first and archive important checkpoints before executing deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/billwanttobetop/ai-project-scaffold) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python utility scripts, shell command examples, generated project files, and configuration templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates files in the target project directory when initialization, upgrade, component-addition, doc-fix, checkpoint-cleanup, or archival commands are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
