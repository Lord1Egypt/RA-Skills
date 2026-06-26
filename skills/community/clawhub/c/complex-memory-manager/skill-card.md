## Description: <br>
Privacy-aware structured memory management for AI agents using public, internal-obfuscated, and private-not-stored tiers with cleanup and generalization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bustes01](https://clawhub.ai/user/bustes01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to give agents structured local memory guidance for storing learned patterns, tracking skill usage, managing non-public memory, and running cleanup without storing private secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The internal memory tier uses XOR plus Base64, which is weak obfuscation rather than secure encryption. <br>
Mitigation: Do not store secrets, PII, account data, or sensitive personal details in skill memory; use environment variables or a secret manager for private data. <br>
Risk: Persistent local memory can retain information longer than intended. <br>
Mitigation: Periodically inspect or clear memory directories and follow the documented cleanup protocol for expiry, archival, and deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bustes01/complex-memory-manager) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with JSON, YAML, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces memory-tier rules, cleanup checklists, storage formats, and example encryption helpers for agent use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
