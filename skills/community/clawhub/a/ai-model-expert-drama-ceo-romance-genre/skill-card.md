## Description:

Helps short-drama and comic-production teams turn ideas, scripts, character images, or reference videos into AI-HIVE project blueprints, image/video generation commands, task tracking, and downloadable media outputs for CEO romance and related short-drama genres.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, studios, marketers, and developers use this skill to plan short-drama projects, create reusable production briefs, generate AI-HIVE image or video jobs, upload reference media, poll task status, and download generated results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured non-default endpoint could receive the user's AI-HIVE bearer API key.

Mitigation: Keep the default HTTPS AI-HIVE endpoint and do not set AI_HIVE_BASE_URL or --base-url to an untrusted host.

Risk: API keys may be exposed in shared environments or copied into public artifacts.

Mitigation: Store keys only in a private local environment or config file, restrict file permissions, and rotate keys if exposure is suspected.

Risk: Unreviewed dependency installation can introduce supply-chain exposure.

Mitigation: Install dependencies in an isolated environment with reviewed pinned versions before running the scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-ceo-romance-genre)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON files, shell commands, and downloaded image or video media]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files, AI-HIVE config files, uploaded media IDs, task IDs, pricing snapshots, and generated media files.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
