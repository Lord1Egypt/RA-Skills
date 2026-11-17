## Description:

autoecom helps an agent create daily Instagram and TikTok product carousels for an ecommerce store by extracting brand signals, selecting a bestseller, generating branded slide images, requesting approval, and publishing through Upload-Post.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mutonby](https://clawhub.ai/user/mutonby)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and their agent operators use this skill to run a daily human-approved carousel workflow for Instagram and TikTok. It supports brand-kit extraction, product selection, slide planning, image generation, visual QA, publishing, and weekly learning from engagement metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish ecommerce content to connected social accounts through Upload-Post.

Mitigation: Use a dedicated Upload-Post profile, run a dry-run first, keep TikTok in draft mode, and require explicit approval before each real publish.

Risk: The workflow needs API keys for Gemini and Upload-Post and may receive keys through an agent conversation.

Mitigation: Store keys only in the local environment file, avoid echoing them, rotate any key pasted into chat, and restrict file access where the harness supports it.

Risk: Scheduled routines and broad fetching can continue operating after initial setup.

Mitigation: Review the daily and weekly schedules, limit network and filesystem permissions where possible, and disable routines when the campaign is paused.

Risk: Generated product imagery can drift from the real product in stylized scenes.

Mitigation: Perform visual QA on every slide and reject or regenerate slides that misrepresent the product before presenting them for approval.

Risk: The weekly learning loop can reinforce weak or misleading content patterns from noisy engagement data.

Mitigation: Review the weekly digest and audit files before relying on updated hook or imagery priors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mutonby/skills/autoecom)
- [Source repository](https://github.com/mutonby/skill-autoecom)
- [Google AI Studio API keys](https://aistudio.google.com/apikey)
- [Upload-Post](https://upload-post.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, JSON plans, generated image files, captions, hashtags, and publishing summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STORE_URL, GEMINI_API_KEY, UPLOAD_POST_API_KEY, and UPLOAD_POST_PROFILE; normal operation includes explicit user approval before live publishing.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
