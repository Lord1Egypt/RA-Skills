## Description: <br>
Query Claude API usage and cost reports from the command line with secure macOS Keychain storage for an Admin API key and table or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberash-dev](https://clawhub.ai/user/cyberash-dev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineering teams, and operations users use this skill to install and run a CLI for reviewing Anthropic Claude Admin API usage and cost reports from macOS. It supports day-to-day spend tracking, token usage review, JSON export, and scripted reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs a global npm package that handles an Anthropic Admin API key. <br>
Mitigation: Confirm the package name and publisher, review the linked source repository when needed, and only provide an Admin API key appropriate for use with this CLI. <br>
Risk: Usage and cost reports may expose organization-level operational or billing information. <br>
Mitigation: Run the CLI in trusted environments and limit access to users who are authorized to view Anthropic usage and cost data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cyberash-dev/claude-cost-cli) <br>
- [Source repository](https://github.com/cyberash-dev/claude-cost-cli) <br>
- [Anthropic Admin API usage and cost documentation](https://platform.claude.com/docs/en/build-with-claude/usage-cost-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, JSON] <br>
**Output Format:** [Markdown with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI produces tabular stdout or JSON reports for usage and cost queries.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
