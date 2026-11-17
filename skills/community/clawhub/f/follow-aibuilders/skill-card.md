## Description:

Follow-aibuilders helps an agent collect public AI builder updates from X/Twitter, YouTube podcasts, and blogs, then turn them into concise English, Chinese, or bilingual digests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[champagne315](https://clawhub.ai/user/champagne315)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and AI practitioners use this skill to monitor selected AI builders, podcasts, and company blogs and receive curated digest-style summaries with source links. It also guides users through local setup and source, language, lookback-window, and prompt customization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use yt-dlp browser-cookie access when YT_DLP_COOKIES is set to a browser profile.

Mitigation: Run in a low-privilege environment and enable browser-cookie access only when the user accepts local session-cookie exposure.

Risk: User-added blog URLs may fetch arbitrary or private-network locations.

Mitigation: Do not add localhost or private-network blog URLs; review custom sources before running digest collection.

Risk: Prompt files and configuration can be changed locally and may alter summary behavior.

Mitigation: Review prompt and configuration changes before use, especially when another user or automation modified the artifact.

Risk: Command-line secrets can be exposed through shell history or process listings.

Mitigation: Avoid passing API keys on the command line; prefer a protected local environment file or omit optional user authentication.

Risk: The bundled npm lockfile may need dependency review before installation.

Mitigation: Regenerate or audit the npm lockfile before running npm install in the scripts directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/champagne315/skills/follow-aibuilders)
- [Artifact README](artifact/README.md)
- [yt-dlp releases](https://github.com/yt-dlp/yt-dlp/releases)
- [X Auth Helper extension](https://chromewebstore.google.com/detail/x-auth-helper/miflinhihdjikdpjjigaiafeoobkhikk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown digest with source links, plus setup and configuration guidance with inline shell commands when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English, Chinese, or bilingual summaries according to local user configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
