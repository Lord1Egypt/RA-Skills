## Description: <br>
Syncs AI coding assistant configuration files from a single canonical source into native formats for Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, Windsurf, Cline/Roo, Aider, Kiro, Amazon Q, Goose, Trae AI, Zed, Amp, OpenCode, and Warp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nadalpiantini](https://clawhub.ai/user/nadalpiantini) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to keep AI coding assistant instructions synchronized across tools from `.claude/rules/` or `CLAUDE.md` as the canonical source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A non-dry-run execution can write or replace assistant configuration files in the target repository. <br>
Mitigation: Run with `--dry-run` first, limit outputs with `--tools`, and review or back up existing assistant config files before writing. <br>
Risk: Incorrect or stale canonical rules can be propagated into multiple assistant tools. <br>
Mitigation: Review `.claude/rules/` or `CLAUDE.md` before generation and commit generated files together so changes are auditable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [configuration, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and plain-text configuration files with terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run previews, selected-tool generation, and initialization from an existing CLAUDE.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
