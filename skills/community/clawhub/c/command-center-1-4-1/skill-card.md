## Description: <br>
Mission control dashboard for OpenClaw - real-time session monitoring, LLM usage tracking, cost intelligence, and system vitals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcdentoncore](https://clawhub.ai/user/jcdentoncore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a local OpenClaw dashboard for monitoring agent sessions, LLM usage, costs, scheduled jobs, and system health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard can expose sensitive agent sessions, workspace metadata, operator identities, and local dashboard/topic state. <br>
Mitigation: Run it only on a trusted machine, bind or firewall it to localhost, and enable strong authentication before any LAN, VPN, tunnel, or public exposure. <br>
Risk: The skill includes operational controls for OpenClaw jobs and helper scripts for setup, dependencies, tunnels, and Linear synchronization. <br>
Mitigation: Review commands and scripts before execution, use least-privilege credentials, and avoid unattended use until the operator has verified the configured actions. <br>
Risk: Server evidence flags sensitive credentials, OAuth token needs, and purchase-related capability tags. <br>
Mitigation: Install only in environments where those permissions are intended, keep credentials scoped and local, and avoid exposing secrets through dashboard configuration or logs. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/jcdentoncore/command-center-1-4-1) <br>
- [README](README.md) <br>
- [Architecture overview](docs/architecture/OVERVIEW.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML dashboard] <br>
**Output Format:** [Markdown guidance, shell commands, local web dashboard pages, and JSON/SSE API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a local Node.js dashboard server on port 3333 by default.] <br>

## Skill Version(s): <br>
1.4.1 (source: SKILL.md frontmatter and package.json; ClawHub release metadata version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
