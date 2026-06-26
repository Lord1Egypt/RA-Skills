## Description: <br>
Persistent identity and memory context layer for AI agents across platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernardtai](https://clawhub.ai/user/bernardtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to Digaide for persistent user identity, long-term memory enrichment, persona consistency, and progress-aware workflows across sessions and platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send memory and identity context to Digaide's service. <br>
Mitigation: Install only if you trust Digaide with that context, review Digaide's privacy and retention terms, and avoid sending sensitive data unless necessary. <br>
Risk: The skill requires a sensitive DIGAIDE_API_KEY credential. <br>
Mitigation: Use a scoped or dedicated API key when available and protect it in the agent runtime environment. <br>
Risk: A custom DIGAIDE_API_BASE endpoint can redirect agent traffic. <br>
Mitigation: Set DIGAIDE_API_BASE only to an endpoint you trust and verify before use. <br>


## Reference(s): <br>
- [Digaide Homepage](https://digaide.com) <br>
- [Digaide API](https://api.digaide.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/bernardtai/digaide-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API Calls] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DIGAIDE_API_KEY and curl; may use DIGAIDE_API_BASE for a custom endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
