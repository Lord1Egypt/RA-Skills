## Description: <br>
Open-source B2B AI SDR template with a 7-layer context system, 10-stage sales pipeline, 4-layer anti-amnesia memory, automated cron jobs, WhatsApp IP isolation, and multi-channel WhatsApp, Telegram, and email workflows built on OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ipythoning](https://clawhub.ai/user/ipythoning) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales teams, operators, and developers use this template to configure an AI SDR for B2B export businesses. It supports lead capture, qualification, follow-up, quote generation, CRM updates, and multi-channel customer conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release weakens execution safeguards and can make root-level OpenClaw configuration changes during deployment. <br>
Mitigation: Review the deploy scripts before use, run dry-run or staging deployment first, keep execution approvals under operator control, and avoid running the installer on production hosts until the changes are accepted. <br>
Risk: The release stores customer conversations and sales history long term. <br>
Mitigation: Define retention, access, export, and deletion controls before using the agent with real customers, and treat CRM, memory, and conversation records as sensitive customer data. <br>
Risk: The release instructs the agent to hide that it is AI. <br>
Mitigation: Remove or change AI-identity concealment prompts and align customer-facing disclosure with company policy and applicable law. <br>
Risk: Dashboard and gateway defaults may expose services on the network. <br>
Mitigation: Bind dashboards and gateways to loopback or a protected reverse proxy, require authentication, enable TLS, and restrict inbound ports with firewall rules. <br>
Risk: Installer telemetry is sent silently. <br>
Mitigation: Inspect and disable telemetry calls before installation if silent usage reporting is not acceptable. <br>
Risk: Broad skill installation and open contact policies can expand the agent's action surface. <br>
Mitigation: Install only required skills, restrict admin operations to an explicit whitelist, review channel contact policies, and require human approval for quotes, purchases, or other irreversible actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ipythoning/b2b-sdr-agent-template) <br>
- [Publisher profile](https://clawhub.ai/user/ipythoning) <br>
- [OpenClaw](https://openclaw.dev) <br>
- [Project repository linked by artifact](https://github.com/iPythoning/b2b-sdr-agent-template) <br>
- [Jina AI](https://jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JSON configuration, and generated deployment files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create OpenClaw workspace files, memory configuration, delivery queues, product knowledge base files, and deployment scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
