## Description:

Scenario-focused Sparki skill for commentary-style edits while using the latest official Sparki setup, API-key, and upload workflow guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent users use this skill to turn existing footage into commentary-style, narrated, explainer, reaction, or recap edits with clearer spoken framing and structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos and prompts are sent to Sparki cloud services for processing.

Mitigation: Use the skill only with videos and prompts that are appropriate to share with Sparki, and avoid sensitive or confidential footage unless approved.

Risk: API keys can be saved in local plaintext configuration.

Mitigation: Prefer the SPARKI_API_KEY environment variable where possible and review permissions on ~/.openclaw/config/sparki.json if credentials are saved.

Risk: The CLI allows overriding the Sparki API base URL.

Mitigation: Use --base-url only for endpoints you control and trust.

Risk: Downloaded result URLs may be followed before stronger host and size validation is added.

Mitigation: Review result sources and output file paths before opening or sharing downloaded videos.

## Reference(s):

- [AI Commentary ClawHub Skill Page](https://clawhub.ai/fischerlam/skills/ai-commentary)
- [Sparki Homepage](https://sparki.io)
- [Sparki Telegram Upload](https://t.me/Sparki_AI_bot/upload)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of Sparki CLI workflows that upload video files, create edit projects, poll status, and download video outputs.]

## Skill Version(s):

1.0.12 (source: SKILL.md frontmatter, artifact/_meta.json, evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
