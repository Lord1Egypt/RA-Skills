## Description:

AI-powered video highlight extraction that identifies the most engaging moments and generates viral-ready video clips from online URLs or local files, with export options for aspect ratios, caption styles, AI reframing, and AI-generated hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wayinvideo](https://clawhub.ai/user/wayinvideo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, marketers, and developers use this skill to submit videos to WayinVideo for highlight extraction and exported short-form clips. It is suited for social media clips, highlight reels, and long-to-short video repurposing where third-party media processing is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected videos, supported video URLs, and related task metadata to the third-party WayinVideo service.

Mitigation: Use only with media and URLs approved for third-party processing, and avoid confidential recordings, private/internal URLs, or sensitive project names unless organizational review permits it.

Risk: The security summary flags an under-scoped upload path that users should review before installation.

Mitigation: Review local upload handling and destination validation before using the skill with sensitive media or high-trust environments.

Risk: Polling can trigger host system event notifications when event polling is enabled.

Mitigation: Enable system-event polling only when host notifications are desired and appropriate for the environment.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/wayinvideo/skills/ai-clipping)
- [WayinVideo AI Clipping API Documentation](https://wayin.ai/api-docs/ai-clipping/)
- [WayinVideo API Dashboard](https://wayin.ai/wayinvideo/api-dashboard)
- [Supported Languages](artifact/assets/supported_languages.md)
- [Platform Duration Guidance](artifact/assets/platform_duration.md)
- [Platform Ratio Guidance](artifact/assets/platform_ratio.md)
- [Caption Style Templates](artifact/assets/caption_style.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and WAYIN_API_KEY; outputs project IDs, saved JSON result paths, and downloadable clip links when export is enabled.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
