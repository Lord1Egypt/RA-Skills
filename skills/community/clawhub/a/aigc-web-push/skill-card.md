## Description:

Creates AI-assisted articles, image posts, and videos, then sends them to WeChat Official Accounts or cloud computers for publication on other sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lihengdao](https://clawhub.ai/user/lihengdao)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and communications teams use this skill to create written, graphic, and video content, then prepare drafts or publish to WeChat and supported sites through a cloud computer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates the release suspicious with medium confidence, and inspection was incomplete (8 of 12 components fully inspected).

Mitigation: Review the partially inspected components and publishing workflow before enabling the skill in an agent environment.

Risk: Publishing and draft cleanup can affect external accounts and their content.

Mitigation: Confirm the destination account and draft or publish mode before sending; review the target account before using draft cleanup.

Risk: The security guidance calls out broad activation, dependency installation, and reliance on an external publishing service.

Mitigation: Limit activation to the intended content workflow, review optional dependency sources before installation, and use the publishing service only when trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lihengdao/skills/aigc-web-push)

## Skill Output:

**Output Type(s):** [Text, HTML, Images, Video, Configuration instructions, Shell commands]

**Output Format:** [HTML, Markdown, image and video files, configuration guidance, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content can be prepared as a draft or sent for publication to a selected channel and destination.]

## Skill Version(s):

3.6.11 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
