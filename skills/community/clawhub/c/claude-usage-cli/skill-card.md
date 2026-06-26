## Description: <br>
Query Claude API usage and cost reports from the command line, with macOS Keychain storage for the Admin API key and table or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberash-dev](https://clawhub.ai/user/cyberash-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and administrators use this skill to install and run a deprecated third-party CLI for reviewing Anthropic usage and cost reports from the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is deprecated and no longer maintained. <br>
Mitigation: Prefer the linked claude-cost-cli replacement for new use, or audit the package source before installing this release. <br>
Risk: The CLI handles an Anthropic Admin API key and organization usage or cost data. <br>
Mitigation: Use the narrowest available Admin API permissions, install only from a trusted source, confirm outbound traffic is limited to Anthropic, and revoke the key when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberash-dev/claude-usage-cli) <br>
- [claude-usage-cli source](https://github.com/cyberash-dev/claude-usage-cli) <br>
- [Anthropic Usage and Cost API documentation](https://platform.claude.com/docs/en/build-with-claude/usage-cost-api) <br>
- [claude-cost-cli replacement](https://clawhub.com/skills/claude-cost-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON-producing CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, API key management, usage-report, and cost-report command examples; CLI outputs tables or JSON when run.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
