## Description:

Batch generates complete AI video drama episodes from multi-chapter novels, including voiceover, subtitles, covers, titles, tags, and short-form publishing outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghwyever](https://clawhub.ai/user/ghwyever)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and operators use this skill to convert multi-chapter novel text into serialized AI video drama episode packages for Douyin, Kuaishou, Fanqie, or TikTok-style publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Novel text and generated narration may be sent to external services.

Mitigation: Avoid confidential, unpublished, regulated, or client-owned text unless those data flows are approved.

Risk: The skill downloads media from service-returned URLs and composes media locally.

Mitigation: Run it in a sandboxed environment with reviewed network access and local file permissions.

Risk: The server security verdict is suspicious due to under-disclosed data sharing and unsafe execution patterns.

Mitigation: Review the skill carefully before installation and deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ghwyever/skills/fanqie-ai-video-drama)
- [ClawHub publisher profile](https://clawhub.ai/user/ghwyever)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, files]

**Output Format:** [Episode folders containing final_video.mp4, cover.jpg, info.json, and script.md, plus a JSON-like success or error response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local episode directories, downloads generated media, and composes final videos locally.]

## Skill Version(s):

5.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
