## Description:

Encodes, decodes, escapes, and converts text across Base64, URL encoding, HTML entities, JSON escaping, hexadecimal, binary, ROT13, and Unicode escape formats through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transform text for web, API, data transmission, debugging, and lightweight obfuscation workflows. It is suited for routine format conversion when the text can be sent to AgentPMT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send arbitrary text to AgentPMT for remote processing.

Mitigation: Do not use it with secrets, credentials, private keys, proprietary files, regulated data, or other sensitive payloads unless organizational approval covers AgentPMT processing.

Risk: Mutable remote setup or live schema content can affect invocation behavior.

Mitigation: Use the included schema for ordinary calls, verify live schema details before production integration, and pin or audit referenced setup skills before using installation paths.

Risk: The security verdict is suspicious because the skill is a remote text encoder with privacy and setup-chain considerations.

Mitigation: Prefer local encoding tools for routine transformations and install this skill only when remote AgentPMT processing and the listed credits are acceptable.

## Reference(s):

- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/data-format-encoder)
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/data-format-encoder)
- [Data Format Encoder Schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [text, JSON, API Calls, guidance]

**Output Format:** [JSON responses containing transformed text and call status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [All product actions take a required text parameter; each action is listed at 5 credits in the included schema.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
