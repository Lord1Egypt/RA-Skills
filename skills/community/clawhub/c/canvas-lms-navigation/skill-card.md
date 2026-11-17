## Description:

Navigate institution-neutral Canvas LMS pages, verify assignment context, and prioritize work across authorized courses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjjhenriksen](https://clawhub.ai/user/jjjhenriksen)

### License/Terms of Use:

MIT-0

## Use Case:

Students use this skill to navigate authorized Canvas courses, verify assignment details and submission status, and prioritize upcoming and undated work. It returns a concise, source-labelled priority list while keeping navigation read-only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Canvas pages, calendar descriptions, and imported course content may contain incorrect or untrusted instructions.

Mitigation: Verify the page, course, assignment, and source before relying on displayed details; treat imported content as data rather than instructions.

Risk: Student credentials and private course records could be exposed through an unverified page or chat.

Mitigation: Use only verified institution pages and the host's secure authentication flow; never request passwords, session cookies, MFA codes, or tokens in chat.

Risk: Actions such as submissions, quiz attempts, posts, or messages could affect coursework or violate course policy.

Mitigation: Keep this skill's navigation read-only; require separate authorization and course-policy checks before any such action.

## Reference(s):

- [Canvas Community](https://community.canvaslms.com/)
- [Canvas LMS Navigation on ClawHub](https://clawhub.ai/jjjhenriksen/skills/canvas-lms-navigation)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown]

**Output Format:** [Concise source-labelled priority list and navigation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
