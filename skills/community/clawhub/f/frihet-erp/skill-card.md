## Description:

Connect your OpenClaw agent to Frihet ERP via MCP for business status summaries, client pre-meeting context, and human-confirmed invoice drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frihet-io](https://clawhub.ai/user/frihet-io)

### License/Terms of Use:

MIT-0

## Use Case:

Founders and finance or operations teams use the skill to review business status and client context in Frihet ERP, and to prepare invoice drafts for human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ERP records may contain sensitive business data or untrusted text.

Mitigation: Treat record contents as data rather than instructions, and do not send financial records or personal data to third-party endpoints.

Risk: Write tools can change business or fiscal records.

Mitigation: Prefer the read-only connection and a verified tool allowlist; before any write, show the target and proposed changes and wait for explicit user confirmation.

## Reference(s):

- [Frihet ERP documentation](https://docs.frihet.io)
- [Frihet MCP endpoint](https://mcp.frihet.io/mcp)
- [Agent onboarding contract](https://raw.githubusercontent.com/Frihet-io/frihet-mcp/main/docs/agent-onboarding.json)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language business summaries, client briefs, and invoice draft previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounded in Frihet ERP records; invoice draft creation requires explicit user confirmation.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
