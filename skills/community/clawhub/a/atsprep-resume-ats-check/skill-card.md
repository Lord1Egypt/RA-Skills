## Description:

Score a resume for applicant tracking systems (ATS) with ATSPrep's free checker, explain each issue in plain words and fix them with the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devabubakar](https://clawhub.ai/user/devabubakar)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to check a resume or CV for ATS issues, understand findings by severity, and improve bullets while preserving the facts they provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume text is sent to ATSPrep, and selected rewrite tools also send relevant text to Cloudflare Workers AI.

Mitigation: Share only the resume and job-post details needed for the task, remove unnecessary personal information, and use AI rewrite tools only if you are comfortable with that processing.

Risk: A custom ATSPREP_MCP_URL could send resume text to an endpoint the user has not vetted.

Mitigation: Leave ATSPREP_MCP_URL unset unless you intentionally trust the configured endpoint.

Risk: Resume scores and suggested edits may be mistaken for a guarantee or may overstate the user's experience if accepted without review.

Mitigation: Treat scores as guidance, review proposed changes, and include only skills and facts the user confirms.

## Reference(s):

- [ATSPrep Resume ATS Checker](https://atsprep.com/tools/ats-resume-checker)
- [ATSPrep MCP endpoint](https://atsprep.com/mcp)
- [ATSPrep MCP tools](references/tools.md)
- [Privacy guidance](references/privacy.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown with scores, severity-grouped findings, and suggested edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include resume feedback, bullet suggestions, and links to ATSPrep Studio; generated edits should preserve user-provided facts.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
