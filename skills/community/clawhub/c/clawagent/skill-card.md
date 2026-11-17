## Description:

ClawAgent helps agents generate marketing images and videos, analyze or remix media, and publish video or image posts to connected social media accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiadouai](https://clawhub.ai/user/jiadouai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, ecommerce, and social media operators use this skill to create product visuals, short-form videos, lip-sync or singing media, campaign posters, Xiaohongshu-style image notes, and social posts from agent-guided workflows. Agents also use it to configure ClawAgent access, upload selected local media for processing, poll asynchronous jobs, and report unsupported feature requests with user consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles tokens, connected social accounts, media files, and ClawAgent service access.

Mitigation: Install only when the publisher and service are trusted; use a least-privilege temporary token and avoid shared machines.

Risk: Local media can be uploaded to remote cloud storage for processing.

Mitigation: Upload only intentionally selected files and avoid sensitive, private, identity, or restricted media.

Risk: Setup, upload, and update flows can install tooling, save credentials, or apply remote update instructions.

Mitigation: Do not run setup or upload with sudo, and approve updates only after reviewing the exact commands and changed files.

Risk: Publishing workflows can post content to authorized social media accounts.

Mitigation: Confirm the target account, content, and publishing time before issuing publish calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiadouai/skills/clawagent)
- [Publisher Profile](https://clawhub.ai/user/jiadouai)
- [Authentication and Authorization](references/auth.md)
- [Common Interfaces and Workflows](references/workflows.md)
- [Model Try-On](references/model_try_clothes.md)
- [Shoe Try-On](references/shoes_dressing.md)
- [Model Generation](references/model_produce.md)
- [Product Scene Image](references/business_product_scene.md)
- [Product Poster Generation](references/business_poster.md)
- [Xiaohongshu Note Images](references/ice_design_image_xhs.md)
- [Video Publishing](references/video_publish.md)
- [Image Publishing](references/image_publish.md)
- [Lip-Sync Video](references/ice_voice_video.md)
- [Singing Photo Video](references/image_song.md)
- [Video Remix](references/ai_mixed_script.md)
- [Video Clone](references/ai_clone_video.md)
- [Douyin Link Parsing](references/get_raw_url.md)
- [Video Analysis](references/analyze_video.md)
- [Unsupported Feature Reporting](references/unsupported_feature_reporting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown guidance with inline JSON and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May surface generated media URLs, uploaded file URLs, job identifiers, account identifiers, and social publishing status from ClawAgent tools.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
