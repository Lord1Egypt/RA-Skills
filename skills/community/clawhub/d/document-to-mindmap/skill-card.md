## Description:

Converts documents, long text, webpages, images, meeting notes, reports, and study materials into structured, editable ProcessOn mind maps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leilizhang](https://clawhub.ai/user/leilizhang)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to condense documents, webpages, images, meeting notes, reports, and study materials into markdown mind-map content and ProcessOn view/image links for review and editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send full document content to ProcessOn.

Mitigation: Use it only with documents approved for submission to ProcessOn; avoid confidential, regulated, or customer-sensitive content unless organizational policy allows that service.

Risk: The skill describes remote version checks and an automatic forced update flow.

Mitigation: Independently verify the source, version, and changelog before accepting or running any update command.

Risk: The client may store a persistent local partner identifier.

Mitigation: Review local storage behavior and remove or manage the identifier according to user or organization privacy policy.

Risk: The client may delete Markdown inputs placed under temp or `.agents/cache` paths.

Mitigation: Keep source copies outside cleanup paths and pass disposable copies when using file-based input.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leilizhang/skills/document-to-mindmap)
- [Publisher Profile](https://clawhub.ai/user/leilizhang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown mind-map outline plus ProcessOn image and online view URLs; the client script returns JSON from the ProcessOn API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports ProcessOn theme and structure options; defaults to mind_free when the requested structure is not recognized.]

## Skill Version(s):

1.1.10 (source: server release metadata, SKILL.md frontmatter, coze-version.json, github-version.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
