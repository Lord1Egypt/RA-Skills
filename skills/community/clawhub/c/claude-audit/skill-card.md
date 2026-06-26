## Description: <br>
Full project audit - launches 5 parallel AI agents (security, bugs, dead code, architecture, performance) to scan your codebase read-only, then compiles a unified report with health grade (A+ to F) and offers surgical fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atobones](https://clawhub.ai/user/atobones) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill in Claude Code to run a language-agnostic project audit across security, bugs, dead code, architecture, and performance, then receive a prioritized Markdown report and optional fix proposals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The one-line installer downloads and executes a remote shell script. <br>
Mitigation: Install manually or inspect the installer before using the one-line command. <br>
Risk: Auto-fix mode can modify repository files without a confirmation step. <br>
Mitigation: Run /audit without --fix first, and only use --fix on a clean version-controlled branch where changes can be reviewed and reverted. <br>
Risk: A full audit may expose sensitive repository context to the active agent environment. <br>
Mitigation: Scope sensitive repositories with a path, --changed, --focus, and .auditignore. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/atobones/claude-audit) <br>
- [Publisher profile](https://clawhub.ai/user/atobones) <br>
- [Project homepage](https://github.com/atobones/claude-audit) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with structured findings, severity grades, action plans, and optional code or command suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose targeted code changes when the user chooses a fix mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
