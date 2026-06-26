## Description: <br>
Voluntary Freedom Preserving Protocol for self-governing AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ovrsr](https://clawhub.ai/user/ovrsr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to let an agent voluntarily adopt a five-law governance framework, verify signed constitution files, and maintain reversible local adoption and audit records with user consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or append persistent local governance records after adoption. <br>
Mitigation: Require explicit user consent and review the exact SOUL.md, MEMORY.md, and .openclaw audit-file changes before approving adoption. <br>
Risk: The root skill is prompt-layer governance and cannot mechanically veto tool calls. <br>
Mitigation: Use the companion dispatcher-layer plugin only when stronger tool-call enforcement is desired, and review that plugin separately before installation. <br>
Risk: The five-question pre-action check depends on model reasoning quality. <br>
Mitigation: For uncertain or high-impact actions, ask for consent, stage changes reversibly, and record the rationale for audit. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ovrsr/freedom-preserving-protocol) <br>
- [Publisher Profile](https://clawhub.ai/user/ovrsr) <br>
- [Compatibility](docs/COMPATIBILITY.md) <br>
- [Revocation](docs/REVOCATION.md) <br>
- [Troubleshooting](docs/TROUBLESHOOTING.md) <br>
- [Companion Enforcement Plugin Source](https://github.com/ovrsr/freedom-preserving-protocol/tree/main/plugin) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON audit or verification outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file changes for SOUL.md, MEMORY.md, and .openclaw audit files after explicit user consent.] <br>

## Skill Version(s): <br>
1.3.2 (source: SKILL.md frontmatter, package.json, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
