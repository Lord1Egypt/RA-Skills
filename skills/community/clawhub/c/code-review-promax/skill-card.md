## Description:

Reviews user-provided code changes for correctness, regression risk, compatibility, and related issues, then returns structured, actionable findings to support merge decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-zihan](https://clawhub.ai/user/z-zihan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review diffs, files, commits, GitHub pull requests, and GitLab merge requests, identify actionable risks, and make informed merge decisions. Its bundled fix workflow can apply user-approved review fixes one at a time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fixed Chinese heading may not suit teams whose review reports need to be readable in another language.

Mitigation: Confirm the heading is acceptable for the intended users and review any localization needs before adopting the report format.

Risk: A local path-like reference could not be resolved, so its supporting material may be unavailable.

Mitigation: Check that the referenced material is present and accessible in the installed skill package before relying on it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/z-zihan/skills/code-review-promax)
- [Project homepage](https://github.com/z-Zihan/awesome-skills)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown code review report with actionable findings; optional user-approved code fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report language follows the user's language; the fix workflow previews each change for approval.]

## Skill Version(s):

2.2.0 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
