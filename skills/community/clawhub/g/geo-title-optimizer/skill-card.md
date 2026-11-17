## Description:

Plan and evaluate factual Chinese titles for articles and product content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External content creators and agents use this skill to draft and compare factual Chinese titles, connect each title's promise to supplied evidence and article text, and prepare platform-specific versions when current limits are provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags conflicting guidance about whether drafts may be saved online and content may be published.

Mitigation: Use local title preparation by default. Before any aimeGeo handoff, confirm authorization covers the project, draft upload, destination account, and publishing targets; keep confidential drafts local unless sharing is intended.

## Reference(s):

- [Title output schema](references/title-output-schema.md)
- [aimeGeo Getting Started](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md)
- [aimeGeo AI Assistant Guide](https://github.com/aiispower/aimegeo/blob/main/docs/ai-assistant.md)
- [aimeGeo main repository](https://github.com/aiispower/aimegeo)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Markdown title briefs and platform versions; JSON title candidates and QA results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evidence and scoring rationale; platform limits are marked budget_unknown when no current source is supplied.]

## Skill Version(s):

0.1.2 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
