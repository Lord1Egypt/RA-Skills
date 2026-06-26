## Description: <br>
Install, authenticate, and use Claude Code CLI as a native coding tool for any OpenClaw agent system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Asif2BD](https://clawhub.ai/user/Asif2BD) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent operators use this skill to install Claude Code CLI, authenticate with a Claude Max OAuth token, and configure it as a coding backend or direct CLI tool for implementation, refactoring, bug fixes, reviews, and project scaffolding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Claude Code OAuth tokens are credential-sensitive and can grant access to paid Claude Code usage. <br>
Mitigation: Protect the token like a paid-account credential, store it in environment variables or a secrets manager, keep config.patch and shell files private, and never commit tokens to version control. <br>
Risk: The skill enables agents to invoke a powerful coding CLI that may propose or apply code changes. <br>
Mitigation: Review diffs, run builds or tests, and use branches or approval workflows before committing or pushing changes. <br>
Risk: The installer fetches the Claude Code CLI from npm and depends on the installed package version. <br>
Mitigation: Verify the npm package and version in controlled environments before relying on it for production workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Asif2BD/claude-code-cli-openclaw) <br>
- [ProSkills Listing](https://proskills.md/skills/claude-code-cli) <br>
- [GitHub Repository](https://github.com/ProSkillsMD/skill-claude-code-cli) <br>
- [MissionDeck.ai](https://missiondeck.ai) <br>
- [Claude Code Official Docs](https://docs.anthropic.com/en/docs/claude-code) <br>
- [Claude Code CLI on npm](https://www.npmjs.com/package/@anthropic-ai/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, authentication, OpenClaw configuration, workflow, troubleshooting, and security guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter, changelog, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
