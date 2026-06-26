## Description: <br>
Gestor autónomo e operador executivo do ecossistema ARGOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felix1983](https://clawhub.ai/user/felix1983) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and ARGOS operators use this skill to guide an agent that monitors, maintains, documents, and grows an ARGOS trading-bot deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad system-control instructions could let an agent alter ARGOS services, files, scheduled jobs, processes, credentials, payments, or social-posting workflows. <br>
Mitigation: Install only in an ARGOS environment you own, and grant filesystem, sudo, SSH, cron, process, credential, payment, and social-posting permissions only after explicit review. <br>
Risk: Automatic Telegram reports could expose operational details or user, payment, and system data to an unintended recipient. <br>
Mitigation: Disable or narrow automatic reports until the recipient, data categories, and redaction rules are explicitly approved. <br>
Risk: Persistent automation could continue running after the initial agent session. <br>
Mitigation: Review any cron entries, background processes, and notification scripts before enabling them, and keep a documented rollback path. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational checklists, command snippets, scripts, and prompts for delegated coding agents.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
