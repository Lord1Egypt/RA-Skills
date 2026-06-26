## Description: <br>
Cursor Agent CLI integration - AI-powered coding agent for terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kailian](https://clawhub.ai/user/kailian) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to invoke Cursor Agent CLI for terminal-based coding sessions, planning, code review, test generation, documentation, and automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cursor Agent CLI modes can modify local code, run unattended, or use credentials when the user enables those options. <br>
Mitigation: Prefer plan or ask mode first, keep sandbox protections enabled, avoid force or trust modes in untrusted repositories, and review generated changes before merging or deploying. <br>
Risk: Installation and authentication flows may expose users to pipe-to-shell installer risk or leaked API keys. <br>
Mitigation: Verify Cursor's installer source before running it and keep API keys out of shell history, logs, and committed files. <br>


## Reference(s): <br>
- [Cursor CLI Documentation](https://cursor.com/docs/cli/overview) <br>
- [Cursor Cloud Agents](https://cursor.com/agents) <br>
- [ClawHub Skill Page](https://clawhub.ai/kailian/cursor-agent-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cursor Agent may produce file changes or JSON output depending on the selected mode and flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
