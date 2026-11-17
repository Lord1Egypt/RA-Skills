## Description:

Uses browser automation to publish prepared videos to the Bilibili creator platform with title, description, category, tags, cover, and submission checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnyxu820](https://clawhub.ai/user/johnnyxu820)

### License/Terms of Use:


## Use Case:

External creators and agents use this skill to publish video files to B站 through a logged-in Bilibili creator account. It guides upload, metadata entry, category and tag selection, cover setup, submission, and post-submission verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public content through the user's logged-in Bilibili account, and the security evidence flags an unwanted insulting phrase appended to video descriptions.

Mitigation: Remove the phrase and require a final preview of title, description, tags, category, cover, and account before clicking publish.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/johnnyxu820/skills/bilibili-video-publish)
- [Bilibili Creator Upload Page](https://member.bilibili.com/platform/upload/video/frame?page_from=creative_home_top_upload)

## Skill Output:

**Output Type(s):** [Guidance, Browser automation actions]

**Output Format:** [Markdown instructions with checklist-style steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in Bilibili account and browser extension session; publication should stop after one successful submission.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
