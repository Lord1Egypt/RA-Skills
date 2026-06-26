## Description: <br>
clinstagram is a hybrid Instagram CLI for AI agents that supports posting, DMs, stories, analytics, followers, hashtags, likes, and comments through Meta Graph API and optional private API modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[199-bio](https://clawhub.ai/user/199-bio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use this skill to operate Instagram workflows from a structured CLI, choosing official Graph API paths when available and private API paths when the configured policy allows them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live authority to post content, send DMs, publish stories, delete comments, and perform engagement actions on Instagram accounts. <br>
Mitigation: Use official-only or hybrid-safe mode by default, run dry-run previews before action, and require explicit user approval before DMs, publishing, comment deletion, or growth actions. <br>
Risk: Private API login can involve private-account credentials and may increase account or platform enforcement risk. <br>
Mitigation: Avoid private API login unless necessary, prefer official Graph API backends, use a trusted proxy only, and store sessions through the configured secret store. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/199-bio/clinstagram) <br>
- [Project homepage](https://github.com/199-biotechnologies/clinstagram) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses machine-readable exit codes, backend_used metadata, remediation fields, dry-run previews, and policy blocks for restricted actions.] <br>

## Skill Version(s): <br>
0.2.0 (source: pyproject.toml and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
