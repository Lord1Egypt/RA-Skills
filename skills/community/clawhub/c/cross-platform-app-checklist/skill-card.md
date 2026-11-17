## Description:

Review multi-platform app changes and release readiness for UI, lifecycle, permissions, media and distribution risks. Produces platform-specific findings, evidence gaps and test plans for iOS/iPadOS, Android and desktop apps. Use for compatibility or app-release reviews, not standalone API explanations or prose edits without app-behavior or distribution impact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentx-icu](https://clawhub.ai/user/agentx-icu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release reviewers use this checklist to assess cross-platform app changes or release candidates, identify evidence gaps and prioritize follow-up checks across the app’s actual targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: State-changing tests, privileged diagnostics, builds, signing or publishing can alter project or release state.

Mitigation: Keep reviews read-only and obtain separate authorization before performing those actions.

Risk: Secrets included in evidence reports could be exposed.

Mitigation: Keep secrets out of evidence reports; record material names and purpose without secret values.

## Reference(s):

- [Complete checklist catalog](references/checklist.md)
- [Layout and screens](references/layout.md)
- [Permissions, privacy and data](references/permissions.md)
- [Desktop specifics](references/desktop.md)
- [Testing and release integration](references/testing.md)
- [Store distribution guide](references/stores.md)
- [Flutter notes](references/flutter.md)
- [ClawHub release page](https://clawhub.ai/agentx-icu/skills/cross-platform-app-checklist)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review with prioritized findings, evidence gaps, next actions and device test plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scoped to the app’s stated targets and review mode; includes stable checklist IDs and distinguishes verified evidence from outstanding checks.]

## Skill Version(s):

0.1.1 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
