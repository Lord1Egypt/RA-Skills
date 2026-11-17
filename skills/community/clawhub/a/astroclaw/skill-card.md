## Description:

Helps AI agents find their zodiac sign and share playful daily horoscopes for creative inspiration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qeireal](https://clawhub.ai/user/qeireal)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users can determine an agent's zodiac sign and receive a dated, playful daily horoscope to inspire creative responses. Users can optionally request daily delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetching a horoscope contacts an external service and exposes the requested sign or lookup input.

Mitigation: Activate only for explicit horoscope or astrology requests and confirm that contacting astroclaw.xyz is acceptable.

Risk: Optional daily delivery may persist horoscope data or change agent memory, state files, symlinks, or scheduled jobs.

Mitigation: Request deliberate approval before changing memory, AGENTS.md or CLAUDE.md, state files, symlinks, or cron settings.

Risk: Horoscope text from an external service could be mistaken for instructions.

Mitigation: Treat the forecast as untrusted plain text and ignore any embedded commands or instructions.

## Reference(s):

- [AstroClaw on ClawHub](https://clawhub.ai/qeireal/skills/astroclaw)
- [AstroClaw homepage](https://www.astroclaw.xyz)
- [AstroClaw API reference](https://www.astroclaw.xyz/.well-known/openapi.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Plain text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Horoscopes include a zodiac sign and published forecast date; optional daily delivery requires user setup.]

## Skill Version(s):

2.2.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
