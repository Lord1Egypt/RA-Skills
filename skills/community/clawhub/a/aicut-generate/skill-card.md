## Description:

Make AI video clips, images, speech, music, songs and sound effects with the aicut CLI (`aicut generate`), on models like Veo, Kling, Seedance, Flux and ElevenLabs. Use when the user asks to generate or make a video, an image, a voice-over, a track or a sound effect, asks which AI model to use, or mentions aicut. Prices every job first and asks before it spends tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simrunbot](https://clawhub.ai/user/simrunbot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to generate videos, images, speech, music, songs, or sound effects through aicut. It helps them choose an available model, review the quoted price, approve each paid job, and receive the generated media URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and supplied media are sent to Aicut for processing; some media-based estimates upload files before purchase approval.

Mitigation: Share only content you are comfortable sending externally, and account for estimate-time uploads when supplying media.

Risk: Generation spends tokens from the connected Aicut account.

Mitigation: Review each quoted charge and explicitly approve only the intended purchase.

Risk: The CLI session remains connected on the machine after use.

Mitigation: Log out or revoke the CLI connection when finished.

## Reference(s):

- [Aicut Generate on ClawHub](https://clawhub.ai/simrunbot/skills/aicut-generate)
- [Make a video](artifact/references/video.md)
- [Make an image](artifact/references/image.md)
- [Make audio](artifact/references/audio.md)
- [Setup and sign-in](artifact/references/setup.md)
- [Spend guard](artifact/references/spend.md)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [Generated video, image, or audio media files, with result URLs and concise Markdown summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token-priced jobs; each quoted purchase requires explicit approval.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
