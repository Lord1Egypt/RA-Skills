## Description:

AI Voiceover helps agents plan compliant AI narration for social video by choosing a voice and model, rewriting copy for spoken delivery, directing ElevenLabs generation, and routing human mix and review before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Social media teams, creators, and marketing operators use this skill to create AI voiceover briefs and scripts for Reels, Shorts, explainers, dubbing, and localized video while enforcing consent, disclosure, captions, and human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may involve third-party voice services and personal voice samples.

Mitigation: Confirm documented consent for any cloned voice and protect voice samples as personal data.

Risk: Synthetic voice can create impersonation or rights risk, especially for celebrity soundalikes or commercial cloning.

Mitigation: Use only the user's own voice, a documented-consent clone, licensed talent, a library voice, or a designed voice; refuse unconsented real-person imitation.

Risk: AI voice in ads, political content, or localized videos may be misleading without clear disclosure.

Mitigation: Plan visible or caption-level AI voice disclosure before publishing and review each localized output.

Risk: Generated narration can be mismatched, poorly mixed, or unsuitable for sound-off social viewing.

Mitigation: Keep human mix/review before publishing and pair voiceover with captions.

## Reference(s):

- [The VOICE framework](references/the-voice-framework.md)
- [ElevenLabs 2026 capabilities](references/elevenlabs-2026-capabilities.md)
- [Consent, disclosure + tools layer](references/consent-disclosure-and-tools.md)
- [Scripting for the ear + two worked VO scripts](references/script-for-the-ear-and-recipes.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with voice brief fields, script drafts, model and settings recommendations, and compliance notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes consent, disclosure, captioning, localization review, and human mix/review checkpoints.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and evals state 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
