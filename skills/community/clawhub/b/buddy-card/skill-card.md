## Description:

Generates a personalized Claude Buddy trading card by deriving Buddy attributes from the user's Claude Code account UUID and creating a holographic image with Gemini.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyz2102](https://clawhub.ai/user/dyz2102)

### License/Terms of Use:

MIT-0

## Use Case:

Claude Code users use this skill to generate a shareable image card showing their assigned Buddy species, rarity, accessories, stats, and card number. The workflow is intended for users who are comfortable letting an agent access local Claude Code credentials and call external image-generation services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Claude Code credentials from macOS Keychain and uses an OAuth token to request the user's profile UUID.

Mitigation: Install only after reviewing this behavior, keep Claude Code credentials local, and stop if the credential lookup or profile request is unexpected.

Risk: The generated image prompt is sent to Google or Gemini using the user's API key.

Mitigation: Use a restricted throwaway Google API key and avoid including personal data in prompts.

Risk: Custom Google base URLs, proxy settings, or the npx Bun fallback can route sensitive requests through untrusted infrastructure or runtime downloads.

Mitigation: Avoid custom GOOGLE_BASE_URL and untrusted proxy settings, and prefer an already installed trusted Bun or Node runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dyz2102/skills/buddy-card)
- [ClawHub publisher profile](https://clawhub.ai/user/dyz2102)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Google AI Studio API key setup](https://aistudio.google.com/apikey)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown-style instructions, shell commands, JSON buddy data, and a generated JPEG image file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the final card image to a user-selected path, defaulting to ~/Downloads/claude-buddy-card.jpg.]

## Skill Version(s):

1.1.0 (source: server release metadata, released 2026-03-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
