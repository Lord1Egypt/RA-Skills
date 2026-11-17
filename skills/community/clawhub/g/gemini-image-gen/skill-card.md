## Description:

Generate and edit images via Google Gemini API, including Gemini native generation, Imagen 3, style presets, batch generation, and HTML gallery output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iisweetheartii](https://clawhub.ai/user/iisweetheartii)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to generate or edit visual assets through the Google Gemini API, with optional style presets, batch runs, and gallery output. It is suited for creative image generation workflows that can safely send prompts and source images to Google.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and edited source images are sent to Google services.

Mitigation: Use only prompts and images that are appropriate to share with Google and avoid including secrets or sensitive personal data.

Risk: Heartbeat guidance can lead agents toward public posting, avatar changes, or memory saving.

Mitigation: Require explicit approval before publishing generated images, changing avatars, or saving generated content to memory.

Risk: Generated galleries may include captions derived from untrusted prompts.

Mitigation: Avoid opening or publishing generated galleries from untrusted prompts until captions are reviewed or escaped.

Risk: Installing or updating from an unverified path can increase supply-chain risk.

Mitigation: Prefer a pinned or otherwise verified ClawHub install and update path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/iisweetheartii/skills/gemini-image-gen)
- [Google AI Studio API Key Setup](https://aistudio.google.com/apikey)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Generated PNG images, prompts JSON, HTML gallery, and Markdown CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and GEMINI_API_KEY; output directory may contain generated images, prompts.json, and index.html.]

## Skill Version(s):

1.3.1 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
