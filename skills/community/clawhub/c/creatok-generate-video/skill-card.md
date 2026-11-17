## Description:

Use when generating, resuming, or checking TikTok videos, ads, or selling videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newt0n](https://clawhub.ai/user/newt0n)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate, resume, or check TikTok videos, ads, and selling videos through CreatOK. It supports confirmation before generation, runtime model capability checks, reference-image upload, task polling, and recovery by task ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact path can escape the documented output folder when run_id contains path separators.

Mitigation: Use only simple run IDs without slashes, backslashes, dots, or path separators until the path issue is patched; do not expose run_id to untrusted input.

Risk: CreatOK receives prompts, reference images, generated-video metadata, and the configured API key for this workflow.

Mitigation: Use the skill only when you trust CreatOK for those inputs, and avoid sending sensitive prompts, images, or secrets beyond the required CREATOK_API_KEY.

Risk: Video generation may consume credits or incur cost if started unintentionally.

Mitigation: Keep the confirmation gate in place, review model settings and estimated credits before submission, and use automatic confirmation only after explicit user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/newt0n/skills/creatok-generate-video)
- [Common Rules](references/common-rules.md)
- [CreatOK API keys](https://www.creatok.ai/app/workspace/api-keys)
- [CreatOK agent skills](https://www.creatok.ai/agent-skills)
- [CreatOK](https://www.creatok.ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [User-facing text plus result.json and result.md artifacts containing task status, task ID, and video URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREATOK_API_KEY and network access; writes run artifacts under generate-video/.artifacts/<run_id>/.]

## Skill Version(s):

0.1.6 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
