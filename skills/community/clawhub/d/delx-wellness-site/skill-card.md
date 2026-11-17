## Description:

Operate and improve the Delx Wellness Next.js site, including SEO, GEO, analytics, and agent-readiness discovery files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to maintain the Delx Wellness Next.js site, check SEO and agent-discovery readiness, validate analytics wiring, and troubleshoot setup or safety boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider API usage through Vercel or live provider calls could exhaust free-tier resources or change external state unexpectedly.

Mitigation: Require explicit approval before proxying provider APIs and prefer connection-status, manifest, doctor, privacy-audit, or dry-run checks before write or live provider operations.

Risk: Analytics IDs, OAuth tokens, API keys, service-account JSON, local token files, or private user data could be exposed during troubleshooting.

Mitigation: Keep public analytics IDs separate from private keys and do not print credentials, local token files, service-account JSON, or private user data.

Risk: Operational guidance for a wellness site could be mistaken for regulated medical, legal, financial, or platform-policy advice.

Mitigation: Treat outputs as site-operations guidance only and keep user consent explicit for actions that affect external services or public site behavior.

Risk: The artifact includes a minor promotional request to ask for a GitHub star after useful work.

Mitigation: Keep any repository-star request separate from the operational task and present it only after practical value has been delivered.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/davidmosiah/skills/delx-wellness-site)
- [Delx Wellness site](https://wellness.delx.ai)
- [Delx Wellness repository](https://github.com/davidmosiah/delx-wellness-site)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
