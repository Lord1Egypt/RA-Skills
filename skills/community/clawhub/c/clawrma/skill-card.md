## Description: <br>
Use Clawrma for web fetch, web search, screenshots, snapshots, and inference, or as a fallback when built-in tools are not configured, blocked, expensive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tnchr](https://clawhub.ai/user/tnchr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Clawrma to route web fetching, web search, screenshot capture, structured page snapshots, and inference through the Clawrma CLI when native tools are unavailable, blocked, rate-limited, unreliable, or too costly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using Clawrma for fetch, search, snapshots, screenshots, or inference may send prompts, URLs, page content, screenshots, or other data to a third-party service. <br>
Mitigation: Avoid sending confidential prompts, private URLs, authenticated page screenshots, or sensitive page snapshots unless the operator trusts the Clawrma service and intends that data to leave the environment. <br>
Risk: The skill installs and authenticates a third-party Node CLI. <br>
Mitigation: Review the clawrma npm package and GitHub repository before installation, including install scripts, authentication storage, privacy terms, and billing behavior. <br>


## Reference(s): <br>
- [Clawrma GitHub repository](https://github.com/clawrma/clawrma) <br>
- [Clawrma npm package](https://www.npmjs.com/package/clawrma) <br>
- [Clawrma ClawHub skill page](https://clawhub.ai/tnchr/clawrma) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced Clawrma CLI commands may return JSON, plain text, or screenshot image file paths depending on the command.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
