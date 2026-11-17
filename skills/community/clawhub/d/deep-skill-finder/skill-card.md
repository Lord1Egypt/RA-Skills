## Description:

Finds and recommends community skills for a task, and supports installing selected skills or evaluating skills the agent has used.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lintong123](https://clawhub.ai/user/lintong123)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to find and compare community skills that fit a task, then install a skill after the user selects it. Users can also use it to review skills from recent agent work and prepare feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill's privacy promises conflict with data sharing.

Mitigation: Keep weekly personalization disabled unless sharing work-derived keywords is explicitly approved, and use generalized search queries.

Risk: The security review reports flaws that can upload files prematurely or overwrite other skills on Windows.

Mitigation: Defer installation until archive containment and upload validation order are fixed.

Risk: Redaction does not protect screenshot or video contents, and remote package handling, retention, and deletion behavior were not verified.

Mitigation: Inspect complete feedback and media before submission, review downloaded skills separately, and do not rely on redaction to protect media contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lintong123/skills/deep-skill-finder)
- [Skill evaluation guide](references/skill-evaluation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Ranked skill recommendations and concise evaluation guidance in Markdown; feedback drafts may be structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are limited to five results.]

## Skill Version(s):

1.3.6 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
