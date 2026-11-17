## Description:

Converts AI-GEO structured brand assets into CSDN-ready technical tutorial drafts and assists with local browser draft filling for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljseeking](https://clawhub.ai/user/ljseeking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, B2B technical teams, and AI-GEO content operators use this skill to turn structured brand knowledge into CSDN tutorial and architecture article assets. The skill can then prefill a visible local CSDN draft so a human can review, revise, save, or publish manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser automation automatically clicks a publish-labeled control and hides automation indicators, which can exceed a conservative draft-filling boundary.

Mitigation: Remove the automation-suppression Chromium flag and require explicit user confirmation before any publish or settings button click; keep final save and publish actions manual.

Risk: Running a local Playwright browser while logged into CSDN can affect the user's platform account if the workflow is changed or misunderstood.

Mitigation: Use a visible browser session, do not store login state or credentials, stop on CAPTCHA or security checks, and review any automation edits against the bundled safety rules.

Risk: Generated articles, summaries, tags, or examples may contain inaccurate facts, exaggerated claims, or noncompliant marketing language.

Mitigation: Use the publish checklist to manually verify facts, examples, brand mentions, AI-GEO claims, and CSDN community fit before saving or publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ljseeking/skills/csdn-geo-draft-publisher)
- [Artifact README](artifact/README.md)
- [Automation safety rules](artifact/automation/safety_rules.md)
- [Playwright draft flow](artifact/automation/playwright_draft_flow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, checklist Markdown, CSDN metadata text, code examples, and optional local Playwright command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a CSDN article, markdown-ready copy, candidate titles, summary, tags, code examples, publish checklist, and draft status report.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
