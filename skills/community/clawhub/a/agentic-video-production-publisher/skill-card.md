## Description:

Review AI video production packages for creative consistency, asset provenance, platform metadata, disclosure wording, and publishing readiness. Use when a user asks whether a video package is ready for YouTube, TikTok, or short-form release without uploading or scheduling content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, editors, and release reviewers use this skill to check AI video packages for provenance, platform metadata, disclosure language, public wording, and release readiness before a human-controlled publish step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user could treat the review verdict as permission to publish automatically or operate platform accounts.

Mitigation: Keep publishing, scheduling, monetization, account access, and credential handling outside the skill; require a human-controlled publish step.

Risk: Client-facing copy could accidentally expose private production notes, local paths, private prompts, account names, or source-asset links.

Mitigation: Review public surfaces separately and remove private or unpublished details before release.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review with categorized findings and a release verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verdict is one of ready, ready_with_notes, blocked, or do_not_publish.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
