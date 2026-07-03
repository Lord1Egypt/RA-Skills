## Description: <br>
Initializes a multi-agent Claude Code project scaffold with lifecycle hooks, subagent definitions, slash commands, planning support, spec-flow directories, and project/global memory templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrh07819](https://clawhub.ai/user/lrh07819) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill when starting a Claude Code project and want an AI-assisted development workflow with project discipline, quality gates, subagent roles, task execution, and persistent memory scaffolding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent Claude Code hooks and memory can affect future project sessions after installation. <br>
Mitigation: Review the generated .claude/settings.json and any ~/.claude files before continuing work, and remove or disable hooks that are not needed. <br>
Risk: Session catchup or prompt-preview behavior may expose prior session text that contains secrets or proprietary content. <br>
Mitigation: Disable those features or redact sensitive session logs before using the scaffold in confidential projects. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lrh07819/skills/claude-code-team-scaffold) <br>
- [Claude Code Hooks Documentation](https://docs.claude.com/en/docs/claude-code/hooks) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions and generated project scaffold files, including JSON settings, hook scripts, agent definitions, slash commands, and memory templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or append project-local .claude files and global Claude memory files when executed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
