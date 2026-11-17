## Description:

AIVI is the AI engagement layer for lead generation, contact centers, and customer re-activation. Every conversation is analyzed in real-time, building Conversational Intelligence that makes every future interaction smarter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aivillc](https://clawhub.ai/user/aivillc)

### License/Terms of Use:

MIT-0

## Use Case:

External teams use this skill to score and qualify leads, launch paid AI voice and SMS outreach sequences, and review call or campaign outcomes through AIVI. It supports lead generation, contact centers, customer re-activation, ongoing care, and verticals including real estate, debt collection, healthcare, home services, and financial services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch paid AI voice and SMS outreach to real people without clearly documented confirmation, consent, or compliance controls.

Mitigation: Install only for accounts authorized to place calls or texts, maintain consent and opt-out records, and review TCPA, HIPAA, FDCPA, billing, and audit requirements before outreach.

Risk: OAuth connector access may continue until revoked.

Mitigation: Revoke the OAuth connector when the skill is no longer needed or when account access should end.

Risk: Lead enrichment may include economic propensity indicators that are not verified individual facts.

Mitigation: Treat propensity indicators as segment-level signals and avoid presenting them as confirmed personal attributes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aivillc/skills/aivi-engagement)
- [Publisher Profile](https://clawhub.ai/user/aivillc)
- [AIVI Website](https://aivi.io)
- [AIVI MCP Endpoint](https://mcp.aivi.io/mcp)
- [AIVI MCP Health Endpoint](https://mcp.aivi.io/health)
- [AIVI Auth Resolve Endpoint](https://mcp.aivi.io/auth/resolve?authorization_id={id})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with setup commands, lead scores, sequence launch guidance, ML recommendations, and outcome summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include paid outreach actions, OAuth-based connector setup, lead qualification data, contactability signals, and conversation intelligence summaries.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter and manifest list 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
