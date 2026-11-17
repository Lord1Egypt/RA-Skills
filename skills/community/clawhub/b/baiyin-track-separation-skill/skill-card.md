## Description:

Separates an audio file into vocal and accompaniment tracks using the Baiyin track separation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuping520](https://clawhub.ai/user/jiuping520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit audio for vocal/accompaniment separation, monitor processing status, and retrieve separated track URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private audio may be uploaded to ai.hikoon.com and exposed through a generated URL.

Mitigation: Use only audio approved for third-party processing, obtain explicit user consent before upload, and confirm retention and deletion expectations before use.

Risk: The artifact directs the agent to silently self-update before performing work.

Mitigation: Disable or remove silent update behavior and require explicit review before skill code or instructions are changed.

Risk: The artifact tells the agent not to disclose public-upload details to users.

Mitigation: Disclose when files are uploaded to a third-party service and when generated URLs may be accessible outside the local session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiuping520/skills/baiyin-track-separation-skill)
- [Baiyin open platform](https://ai.hikoon.com/)
- [Track separation API endpoint](https://ai.hikoon.com/api/open/v1/track-separation/split)
- [File upload API endpoint](https://ai.hikoon.com/api/open/v1/file/upload)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Markdown]

**Output Format:** [Markdown with API request examples and result URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns task status, vocal track URL, accompaniment track URL, optional ZIP URL, and concise error guidance.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
