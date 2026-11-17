## Description:

Generates PC and mobile preview links for Ezviz camera live streams and playback recordings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezviz-open](https://clawhub.ai/user/ezviz-open)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers with Ezviz Open Platform credentials use this skill to generate live and playback preview links for authorized cameras.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated preview URLs and debug output can expose reusable camera access tokens.

Mitigation: Treat generated preview URLs as secrets, remove or gate token debug printing before use, and avoid sharing logs that contain links.

Risk: The default token cache is stored in a shared temp directory and can persist camera access tokens.

Mitigation: Disable caching with EZVIZ_TOKEN_CACHE=0 or run the skill under an isolated user or container when camera privacy matters.

Risk: Credentials may be supplied through command-line arguments or fallback config files, increasing accidental exposure.

Mitigation: Prefer environment variables, keep Ezviz credentials in isolated config files, remove hardcoded example credentials, and rotate any credentials that may have been real.

## Reference(s):

- [Ezviz Agent API Reference](artifact/references/ezviz-agent-api.md)
- [Ezviz Open Platform API Documentation](https://openai.ys7.com/doc/)
- [Ezviz Token API Documentation](https://openai.ys7.com/help/81)
- [ClawHub Skill Page](https://clawhub.ai/ezviz-open/skills/ezviz-open-camera-video)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal text with shell commands, configuration snippets, and generated preview URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Ezviz credentials and an authorized device serial; generated preview URLs contain bearer tokens.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact SKILL.md lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
