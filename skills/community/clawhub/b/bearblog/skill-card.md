## Description:

Create and manage blog posts on Bear Blog (bearblog.dev). Supports extended Markdown, custom attributes, and browser-based publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azade-c](https://clawhub.ai/user/azade-c)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to draft, edit, publish, unpublish, and manage Bear Blog posts through an authenticated browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated browser automation can publish or unpublish Bear Blog content without enough user review.

Mitigation: Review the target post, slug, content, scheduled date, and visibility before any publish or unpublish action.

Risk: The artifact includes a deletion workflow that bypasses the browser confirmation dialog.

Mitigation: Require a separate explicit deletion confirmation and keep a backup before using any delete flow.

Risk: Persistent cookies allow later browser actions to operate on the logged-in Bear Blog account.

Mitigation: Use the skill only with the intended account and clear or isolate the browser session when finished.

## Reference(s):

- [Bear Blog](https://bearblog.dev)
- [Mistune](https://github.com/lepture/mistune)
- [ClawHub Bearblog Skill](https://clawhub.ai/azade-c/skills/bearblog)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with browser action command examples and Bear Blog header/body templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires browser.enabled and an authenticated Bear Blog session.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
