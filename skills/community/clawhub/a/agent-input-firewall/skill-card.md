## Description:

Prompt-injection and jailbreak firewall for AI agents that scans untrusted inbound text before an agent acts on it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lorcan84](https://clawhub.ai/user/lorcan84)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check untrusted posts, comments, direct messages, tool results, or scraped web content for prompt-injection or jailbreak attempts before the text is included in planning or decision prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or private agent input may be sent to the external cheetahsecurity endpoint.

Mitigation: Use only content approved for submission to that endpoint, and avoid secrets, private messages, authenticated tool output, source code, or personal data unless explicit approval is in place.

Risk: The skill describes a paid x402 pay-per-call flow after launch.

Mitigation: Set clear cost, authorization, and client controls before enabling any paid x402 workflow.

Risk: A clean scan result could be treated as permission to follow untrusted instructions.

Mitigation: Keep untrusted content as data and apply normal agent safety controls even when the scan response marks text as safe.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/lorcan84/skills/agent-input-firewall)
- [Cheetahsecurity Homepage](https://x402.cheetahsecurity.de)
- [Cheetahsecurity Scan Endpoint](https://x402.cheetahsecurity.de/scan)

## Skill Output:

**Output Type(s):** [guidance, shell commands, JSON]

**Output Format:** [Markdown instructions with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced scan API response includes safe, verdict, and risk_score fields.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
