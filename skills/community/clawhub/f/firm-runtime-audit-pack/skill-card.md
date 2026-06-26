## Description: <br>
Runtime environment and configuration audit pack that validates Node.js version, secrets workflow, HTTP headers, allowed commands, trusted proxy, disk budget, and DM allowlist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw runtime configuration before deployment or review. It focuses on Node.js runtime posture, secret handling, HTTP headers, command allowlists, proxy settings, disk budget, and direct-message allowlist policy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill audits configuration files and may inspect sensitive runtime settings when pointed at broad paths or unrelated files. <br>
Mitigation: Run it only against specific OpenClaw configuration files intended for review. <br>
Risk: The skill depends on mcp-openclaw-extensions to provide the audit tools. <br>
Mitigation: Install it only when the mcp-openclaw-extensions dependency is trusted for the target environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/romainsantoli-web/firm-runtime-audit-pack) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown or text audit findings with configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcp-openclaw-extensions >= 3.0.0 and should be run against specific configuration files selected for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
