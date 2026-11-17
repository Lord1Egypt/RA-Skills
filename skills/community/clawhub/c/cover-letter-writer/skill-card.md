## Description:

CareerMax AI generates tailored cover letters from resume text and job descriptions for cover letters, application letters, role-specific pitches, and customized job application messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rahulphenomenon](https://clawhub.ai/user/rahulphenomenon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate tailored cover letters by matching a candidate resume with a specific job description. It supports CareerMax API-backed cover letter generation with preview and credit-cost confirmation before creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup invokes a mutable @careermax/agent-toolkit package while using the user's CareerMax API key.

Mitigation: Pin and review the @careermax/agent-toolkit version before installation or execution.

Risk: The skill requires a CareerMax API key for operation.

Mitigation: Use a narrowly scoped CareerMax API key if available and rotate the key if package or account compromise is suspected.

Risk: Cover letter generation can consume CareerMax credits.

Mitigation: Review the preview summary and credit-cost confirmation before approving generation.

## Reference(s):

- [CareerMax AI Agent](https://careermax.ai/ai-agent)
- [CareerMax](https://careermax.ai)
- [ClawHub Skill Page](https://clawhub.ai/rahulphenomenon/skills/cover-letter-writer)
- [ClawHub Publisher Profile](https://clawhub.ai/user/rahulphenomenon)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAREERMAX_API_KEY and npx; cover letter generation uses preview and credit-cost confirmation before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
