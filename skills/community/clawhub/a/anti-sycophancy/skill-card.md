## Description: <br>
Three-layer sycophancy defense for AI coding assistants that rewrites confirmatory prompts, activates critical response behavior, and installs persistent rules for Claude Code and OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcjl](https://clawhub.ai/user/0xcjl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using Claude Code or OpenClaw use this skill to reduce sycophantic assistant behavior by transforming confirmatory prompts, activating critical response patterns, and installing persistent anti-sycophancy rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes local prompt handling and persistent assistant rules, which can make responses more critical or disruptive than intended. <br>
Mitigation: Review the changes to ~/.claude/settings.json, ~/.claude/CLAUDE.md, and SOUL.md; use the documented status and uninstall commands if the behavior is not desired. <br>
Risk: Layer 1 rewrites confirmatory prompts with pattern matching, so it can alter user intent or miss semantic cases. <br>
Mitigation: Use the documented verify command to inspect transformations, and rely on the skill and persistent rules where text rewriting is not appropriate. <br>
Risk: Layer 1 is Claude Code-specific and is not available through the OpenClaw shell-script path. <br>
Mitigation: For OpenClaw, use the Layer 3 persistent rules and do not expect shell-hook prompt rewriting unless a compatible Plugin SDK hook is added. <br>


## Reference(s): <br>
- [ArXiv 2602.23971: Ask Don't Tell](https://arxiv.org/abs/2602.23971) <br>
- [Design Notes](docs/DESIGN.md) <br>
- [Installation Guide](docs/INSTALL.md) <br>
- [openclaw-playbook sycophancy prompt research](https://github.com/0xcjl/openclaw-playbook/blob/main/docs/003-sycophancy-prompt-research.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration edits, and plain-text prompt transformations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local Claude Code and OpenClaw prompt-handling and persistent instruction files when installation commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
