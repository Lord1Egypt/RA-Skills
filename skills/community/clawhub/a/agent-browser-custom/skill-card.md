## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexbingquanxu-cpu](https://clawhub.ai/user/alexbingquanxu-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to drive browser workflows through the external agent-browser CLI, using accessibility snapshots and ref-based element selection for deterministic navigation, interaction, extraction, and session handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved browser state, cookies, localStorage, and authentication files can expose account access. <br>
Mitigation: Treat saved state as credentials, avoid printing or sharing it, and do not commit saved state files. <br>
Risk: Browser automation can perform account-impacting actions such as purchases, public posts, settings changes, or production changes. <br>
Mitigation: Use test or least-privileged accounts and manually review sensitive actions before execution. <br>
Risk: The skill depends on an external agent-browser CLI. <br>
Mitigation: Install and use the CLI only when the publisher and package source are trusted. <br>


## Reference(s): <br>
- [agent-browser CLI](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance assumes the external agent-browser CLI is installed and may lead the agent to create browser state, screenshots, or PDF files when those commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
