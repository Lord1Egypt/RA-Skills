## Description: <br>
Coding Lead guides implementation-focused agents through task classification, direct execution, Claude ACP or acpx fallback, context-file continuity, and optional qmd and smart-agent-memory use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beyound87](https://clawhub.ai/user/beyound87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and implementation-focused agents use this skill to classify coding tasks, choose direct execution or Claude ACP execution paths, preserve context across medium and complex work, and verify implementation results before completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents that can modify code and run local commands. <br>
Mitigation: Install it only for agents intended to perform coding work, use it in version-controlled project directories, and review diffs and commands before accepting changes. <br>
Risk: Context files and memory entries may accidentally retain secrets or customer data. <br>
Mitigation: Keep .openclaw context files and memory entries free of secrets and sensitive data, and clean up temporary context files after task completion. <br>
Risk: Optional helper tools such as acpx, qmd, and smart-agent-memory affect execution behavior. <br>
Mitigation: Verify helper tools come from trusted sources, detect availability per session, and fall back to direct execution when tools are unavailable or fail. <br>
Risk: Running coding agents from configuration directories can damage local agent setup. <br>
Mitigation: Confirm the intended project working directory before spawning agents or writing files, and avoid spawning coding agents in ~/.openclaw/. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/beyound87/coding-lead) <br>
- [README](README.md) <br>
- [Prompt Templates & Examples](references/prompt-templates.md) <br>
- [Complex Tasks - Roles, QA Isolation, Parallel Strategies](references/complex-tasks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, file paths, context-file templates, and implementation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are task-dependent and may include code edits, command recommendations, context files, verification notes, and fallback guidance.] <br>

## Skill Version(s): <br>
3.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
