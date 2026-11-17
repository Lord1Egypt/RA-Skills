## Description:

Generates paid, API-backed job descriptions and role analyses for HR users from job and company inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g620710](https://clawhub.ai/user/g620710)

### License/Terms of Use:

MIT

## Use Case:

HR teams, recruiters, hiring managers, and founders use this skill to generate job descriptions, platform-specific variants, and role analysis from provided hiring details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and hiring details are sent to an undisclosed plaintext HTTP backend.

Mitigation: Use only after the publisher switches to HTTPS and discloses the backend operator and transmitted fields; avoid sending sensitive hiring data until this is resolved.

Risk: The security guidance reports material documentation and runtime mismatches.

Mitigation: Require the publisher to fix command examples, declare dependencies, and repair script syntax before installation or use.

Risk: The skill depends on a paid API key for usage.

Mitigation: Use a scoped JD_API_USER_KEY, monitor credits and usage, and rotate the key if it is exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g620710/skills/ai-jd-generator)
- [Publisher profile](https://clawhub.ai/user/g620710)
- [Skill documentation](artifact/SKILL.md)
- [License file](artifact/LICENSE.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text job-description content with command-line status and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JD_API_USER_KEY; calls a paid external API.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
