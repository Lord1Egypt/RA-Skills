## Description:

Felo AI Search helps agents run Felo API searches that synthesize multiple sources into structured summaries for research, trend scanning, and cross-source analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iml885203](https://clawhub.ai/user/iml885203)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and agents use this skill to query Felo for AI-summarized web research, community trend scanning, market news synthesis, and cross-source analysis. It is best suited to multi-source topic synthesis rather than single-site lookup or time-critical monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Felo and may expose sensitive, private, customer, or internal information.

Mitigation: Avoid including confidential content in queries and use the skill only when sending the query to Felo is acceptable.

Risk: The skill uses a Felo API key, so exposed credentials could allow unauthorized API use.

Mitigation: Prefer FELO_API_KEY from the environment or a secret manager, keep file-based keys permissioned with chmod 600, and rotate keys if exposed.

Risk: Felo results do not include guaranteed timestamps and may not satisfy time-critical lookup needs.

Mitigation: Use a timestamp-aware search tool for time-sensitive monitoring, exact dates, or single-source lookups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iml885203/skills/felo)
- [Felo AI](https://felo.ai)
- [Felo API endpoint](https://openapi.felo.ai/v2/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses FELO_API_KEY and returns AI-generated summaries with source links from the Felo API.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
