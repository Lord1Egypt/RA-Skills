## Description: <br>
Builds a redacted, dry-run outside-help plan for blocked agent work when progress stalls, version drift may matter, or the user asks for official or community guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gongyu0918-debug](https://clawhub.ai/user/gongyu0918-debug) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to decide when a stuck active thread should seek official or community guidance and to produce a redacted advisory plan without browsing by itself. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Host integrations that write suggestion files, schedule background delivery, or enable heartbeat delivery can make outside-help plans appear without enough operator control. <br>
Mitigation: Keep those integrations explicit, scoped, rate-limited, and user-controlled, with quiet-window and no-pending-approval checks before automatic delivery. <br>
Risk: Community or external advice may be mistaken for instructions or command targets. <br>
Mitigation: Treat outside pages as untrusted advisory data, require user authorization before executing commands or changing code/configuration, and check available platform safety status before applying repo, package, skill, plugin, or registry suggestions. <br>
Risk: Thread context used for query planning may contain secrets, internal paths, customer data, or credential fragments. <br>
Mitigation: Redact sensitive values before planning, keep public-only search as the default, and require explicit user opt-in before using private connectors, private repositories, or internal documentation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gongyu0918-debug/skills/find-community-help) <br>
- [Source Homepage](https://github.com/gongyu0918-debug/find-community-help) <br>
- [Trigger Policy](references/trigger-policy.md) <br>
- [Search Playbook](references/search-playbook.md) <br>
- [Suggestion Contract](references/suggestion-contract.md) <br>
- [Threat Model](references/threat-model.md) <br>
- [Host Adapters](references/host-adapters.md) <br>
- [Community Workflows](references/community-workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown advisory plan with optional structured suggestion block and dry-run query-plan fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run only; advisory output is scoped to the active thread and does not browse, run external commands, or write durable memory by itself.] <br>

## Skill Version(s): <br>
0.3.6 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
