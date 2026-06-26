## Description: <br>
Zero Trust security hardening for OpenClaw deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanistolberg](https://clawhub.ai/user/stanistolberg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit and harden OpenClaw AI agent deployments by applying egress controls, plugin allowlisting, tool scoping, and runtime configuration checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change firewall policy and OpenClaw runtime authority. <br>
Mitigation: Run audit and dry-run modes first, keep firewall and OpenClaw configuration backups available, and review hardening.json before applying changes. <br>
Risk: Provider allowlists and whitelist.sh can permit outbound destinations. <br>
Mitigation: Remove provider domains that are not needed and use whitelist.sh only after reviewing the destination domain and port. <br>
Risk: tools.exec and tools.elevated settings can broaden local execution authority. <br>
Mitigation: Review tools.exec, tools.elevated, and Telegram allowFrom entries, then restrict authorized identities before applying the hardening configuration. <br>


## Reference(s): <br>
- [Zero Trust Principles for AI Agents](artifact/references/zero-trust-principles.md) <br>
- [Known Audit False Positives](artifact/references/false-positives.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/stanistolberg/clawd-zero-trust) <br>
- [Project Homepage](https://github.com/stanistolberg/clawd-zero-trust) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run, audit, verification, and mutating commands; mutating operations can require root privileges.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence, README, CHANGELOG, hardening.json; SKILL.md frontmatter lists 1.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
