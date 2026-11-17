## Description:

Automates publishing Markdown articles to CSDN by opening the editor, checking login state, filling the title and content, submitting the post, and returning the article link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echome123](https://clawhub.ai/user/echome123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to publish technical articles to CSDN from an agent workflow after they have logged in to their CSDN browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish posts under the user's logged-in CSDN account without a built-in final confirmation checkpoint.

Mitigation: Ask the agent to show the final title and full article content and wait for explicit user confirmation before clicking publish.

Risk: Publishing may expose unintended or unreviewed content publicly or submit it for CSDN review.

Mitigation: Review the final article content, title length, target account, and article link before treating the publication as complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/echome123/skills/csdn-publish)
- [CSDN Blog Editor](https://mp.csdn.net/mp_blog/creation/editor?spm=1010.2135.3001.4503)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls]

**Output Format:** [Markdown guidance with browser automation commands and returned article links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated CSDN browser session and user-provided article title and content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
