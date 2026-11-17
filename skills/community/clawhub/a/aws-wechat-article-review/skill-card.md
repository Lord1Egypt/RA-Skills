## Description:

Reviews WeChat public-account articles before publication for sensitive terms, typos, political and platform compliance, article quality, and finalization readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiworkskills](https://clawhub.ai/user/aiworkskills)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, and compliance reviewers use this skill to run local pre-publication checks on WeChat article drafts and receive a concrete remediation checklist before formatting or publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify article files during review and finalization.

Mitigation: Review proposed changes and keep a draft backup before allowing it to write review records, draft-stripped.md, or article.md.

Risk: Configured end-of-article embed placeholders may be added to finalized articles unless explicitly opted out.

Mitigation: Inspect the local embed configuration and document any intentional opt-out before finalization.

Risk: Finalization depends on a sibling Python script from the related writing skill.

Mitigation: Install the related skill suite together and review the sibling write.py script before using the citation-stripping finalization step.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aiworkskills/skills/aws-wechat-article-review)
- [Review Checklist](artifact/references/checklist.md)
- [Review Output Template](artifact/references/output-format.md)
- [AI Flavor Diagnostic Methodology](artifact/references/ai-flavor-check.md)
- [AI Flavor Calibration Samples](artifact/references/ai-flavor-check-samples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown review checklist with severity labels, suggested fixes, and finalized article files when the review passes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce review records, draft-stripped.md, and article.md after required checks and user confirmation.]

## Skill Version(s):

1.0.25 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
