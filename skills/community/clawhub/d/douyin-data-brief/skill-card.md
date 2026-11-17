## Description:

Turn a Douyin link or a keyword into a one-page Douyin brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and analysts can use this skill to turn a Douyin post, keyword, or already-copied source material into a concise, attributed brief about engagement, the opening hook, an audience comment, and whether to follow the account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting requests broader account permissions, including unrelated media-creation and voice-change permissions.

Mitigation: Use pasted material without connecting when possible; otherwise review the requested permissions and prefer Douyin-only authorization if available.

Risk: Lookups are paid, and credentials may remain available to other Beatra skills after this package is removed.

Mitigation: Approve each paid lookup individually and review shared credentials before disconnecting or uninstalling.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/beatra-ai/skills/douyin-data-brief)
- [Looking up Douyin](artifact/references/douyin-lookup.md)
- [Writing the brief](artifact/references/brief.md)
- [Douyin brief workflow](artifact/references/workflow.md)
- [Updates and security](artifact/references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [One-page attributed Markdown brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Distinguishes user-supplied material from looked-up figures and includes lookup timing when available.]

## Skill Version(s):

0.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
