## Description:

Uses AnyToCopy to extract captions, scripts, titles, and optional media links from Douyin, Xiaohongshu, and other supported social media or video URLs through a browser workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darker314159](https://clawhub.ai/user/darker314159)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill when a user provides a Douyin, Xiaohongshu, or similar platform link and asks for the video's copy, title, script, or related media links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided social-media links are opened and processed by AnyToCopy, which may expose private, sensitive, account-limited, or confidential URLs to a third-party service.

Mitigation: Use the skill only with links that are appropriate to share with AnyToCopy, and avoid private or confidential content.

Risk: The workflow depends on the AnyToCopy website and its visible controls, so site changes can cause extraction failures or incomplete results.

Mitigation: Review extracted text before relying on it and update the browser workflow if the AnyToCopy interface changes.

## Reference(s):

- [AnyToCopy](https://www.anytocopy.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text containing extracted title, body/script text, and optional media links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser-based extraction; no local code execution or persistence is reported by the security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
