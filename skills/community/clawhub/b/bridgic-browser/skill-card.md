## Description: <br>
Browser Automation helps agents drive real browser sessions for dynamic pages, authenticated workflows, web UI interaction, scraping, form filling, end-to-end checks, and CLI-to-SDK browser automation code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tielei](https://clawhub.ai/user/tielei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to browse JavaScript-rendered pages, operate web interfaces, preserve or isolate login state, connect to existing Chrome sessions, and generate browser automation commands or Python SDK code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse authenticated browser sessions and persistent profile data. <br>
Mitigation: Use a dedicated or ephemeral browser profile unless the task explicitly requires access to an existing logged-in session. <br>
Risk: CDP mode can attach automation to an existing Chrome instance. <br>
Mitigation: Prefer a separate Chrome profile or explicit CDP target, and confirm that the intended browser session is being automated before running sensitive tasks. <br>
Risk: Storage-state files, downloads, network captures, screenshots, videos, and logs can contain sensitive data. <br>
Mitigation: Treat generated browser artifacts as secrets and delete or store them according to the user's data handling requirements. <br>
Risk: The install script modifies project dependency files and installs browser automation dependencies. <br>
Mitigation: Review the install script and dependency configuration before execution, then validate the environment after installation. <br>
Risk: Stealth and scraping capabilities can be misused or violate site terms. <br>
Mitigation: Use the skill only for authorized browsing and automation, and follow applicable website terms, rate limits, and legal requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tielei/bridgic-browser) <br>
- [CLI Guide](references/cli-guide.md) <br>
- [SDK Guide](references/sdk-guide.md) <br>
- [CLI and SDK API Mapping Guide](references/cli-sdk-api-mapping.md) <br>
- [CDP Mode](references/cdp-mode.md) <br>
- [Environment Variables and Login State](references/env-vars.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python code, configuration snippets, and browser automation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser workflow steps, CLI-to-SDK mappings, environment settings, and validation commands.] <br>

## Skill Version(s): <br>
0.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
