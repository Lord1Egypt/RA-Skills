## Description: <br>
Agentplace lets OpenClaw users browse, search, preview, and install free or paid community agent skills from the Agentplace marketplace when the user explicitly requests it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HimanshuNextbase](https://clawhub.ai/user/HimanshuNextbase) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use Agentplace to discover marketplace agents, inspect their metadata and package contents, and install selected agents locally after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The download-and-install workflow gives remote skill packages broad local write authority with limited validation. <br>
Mitigation: Install only from trusted publishers, inspect the full archive contents and skill documentation before final confirmation, and remove unrecognized installed skills from ~/.openclaw/workspace/skills. <br>
Risk: Paid-agent downloads require API key handling. <br>
Mitigation: Avoid pasting paid API keys into visible chat or shell history when possible, and use keys only for download authorization. <br>


## Reference(s): <br>
- [Agentplace ClawHub listing](https://clawhub.ai/HimanshuNextbase/agentplace) <br>
- [Agentplace marketplace API](https://api.agentplace.sh/marketplace/agents) <br>
- [Agentplace dashboard](https://www.agentplace.sh/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with command snippets, package metadata, and installation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include marketplace URLs, package-preview summaries, and confirmation prompts before download or installation.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
