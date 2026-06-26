## Description: <br>
Repair-first self-evolution for OpenClaw: audit logs, memory, and installed skills, then run measurable mutation cycles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IceMasterT](https://clawhub.ai/user/IceMasterT) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect OpenClaw session history, memory, and installed skills, then generate repair-first evolution directives. It is intended for local workflow improvement, with review and dry-run modes available before significant file changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local agent session logs, workspace memory, user profile files, and skill metadata into generated prompts. <br>
Mitigation: Run only in trusted workspaces, keep secrets out of logs and memory files, and avoid sending generated prompts to cloud model providers unless the contents are safe to disclose. <br>
Risk: The skill encourages self-evolution and file-changing mutation cycles, which can alter local workspace behavior. <br>
Mitigation: Prefer --dry-run or --review before applying changes, inspect generated directives, and keep changes scoped and reversible. <br>
Risk: Included OpenAI and OpenRouter agent templates may cause prompts containing local context to leave the machine when used with cloud-backed agents. <br>
Mitigation: Use local execution or dry-run mode for sensitive work, and confirm the agent/model stack before routing generated prompts to external providers. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/IceMasterT/funky-fund-flamingo) <br>
- [Publisher Profile](https://clawhub.ai/user/IceMasterT) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [Anti-Degeneration Lock](ADL.md) <br>
- [Value Function Mutation](VFM.md) <br>
- [Capability Tree](TREE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and local prompt artifacts with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local evolution state, persistent memory, and prompt artifacts; dry-run and review modes reduce mutation risk.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.0.35) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
