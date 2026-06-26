## Description: <br>
Onboards coding agents to Bright Data by routing them to the right setup path for live web work, product integration, MCP usage, authentication, or direct REST access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meirk-brd](https://clawhub.ai/user/meirk-brd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill when first setting up Bright Data access, choosing between CLI tools, product integration, MCP, authentication-only setup, or direct REST calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run a remote installer. <br>
Mitigation: Prefer the npm or npx install path when practical, or download and inspect the installer before executing it. <br>
Risk: The skill handles Bright Data API credentials and local configuration. <br>
Mitigation: Use a scoped API key, protect local config and .env files, and avoid exposing tokens in URLs, logs, or screenshots. <br>
Risk: The skill can install additional Bright Data skills through the CLI. <br>
Mitigation: Review additional skills before installing or using them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/meirk-brd/brightdata-agent-onboarding) <br>
- [Bright Data product documentation](https://docs.brightdata.com) <br>
- [Bright Data LLM-friendly docs index](https://docs.brightdata.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell, dotenv, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to narrower Bright Data skills after onboarding.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
