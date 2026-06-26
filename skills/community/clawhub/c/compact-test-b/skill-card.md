## Description: <br>
Smart context compaction for OpenClaw agents that scans tool outputs, extracts important details into memory files, and produces a pre-compact checklist before /compact. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavmson](https://clawhub.ai/user/wavmson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to preserve important task context before conversation compression. It is intended to scan large tool outputs, record selected facts or decisions, and ask for confirmation before compacting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist sensitive conversation or tool-output details too broadly. <br>
Mitigation: Require explicit confirmation before memory writes and exclude secrets, tokens, credentials, cookies, private keys, personal data, and sensitive configuration values. <br>
Risk: Important context could still be lost if compression happens before unresolved warning items are handled. <br>
Mitigation: Review the pre-compact checklist, resolve warning items, and compact only after user confirmation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wavmson/compact-test-b) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown checklist with concise status notes and optional memory-file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append selected details to memory/YYYY-MM-DD.md when the agent has user approval and suitable memory tooling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
