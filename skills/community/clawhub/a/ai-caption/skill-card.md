## Description:

Scenario-focused Sparki skill for caption-heavy edits while using the official Sparki setup, API-key, and upload workflow guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to route caption-first video editing requests to Sparki, including subtitles, readable captions, and short-form edits that work without sound.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private videos and API keys may be exposed through remote processing or local configuration.

Mitigation: Review before installing for sensitive workflows, prefer SPARKI_API_KEY over saved plaintext credentials, and avoid submitting private videos unless Sparki handling is acceptable.

Risk: Endpoint overrides can redirect uploads and API-key validation away from the official Sparki service.

Mitigation: Use the official agent-api.sparki.io endpoint and avoid setup commands with a custom --base-url unless the endpoint is fully trusted.

Risk: Downloaded video outputs can be written outside the expected workspace if paths are chosen carelessly.

Mitigation: Choose explicit output paths in a controlled directory and review configured default output locations before running downloads.

## Reference(s):

- [Sparki homepage](https://sparki.io)
- [ClawHub AI Caption skill page](https://clawhub.ai/fischerlam/skills/ai-caption)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands; Sparki CLI commands return JSON and may download MP4 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SPARKI_API_KEY for authenticated Sparki API use and writes results to an explicit or configured local output path.]

## Skill Version(s):

1.0.12 (source: SKILL.md frontmatter, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
