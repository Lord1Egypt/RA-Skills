## Description:

Use when the user wants a webpage, article, markdown, or pasted text summarized in the current session and exported as a reusable bundle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiseqingyang](https://clawhub.ai/user/wiseqingyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract article text, create a structured summary with tags, and export the result as reusable JSON, Markdown, HTML, and PNG files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and URL/rendering paths have unsafe scope according to server security evidence.

Mitigation: Review helper scripts before installation, run the skill in a sandbox with restricted network access, and avoid custom installer destinations until containment is improved.

Risk: Summarizing sensitive local files or untrusted URLs can expose private content or process untrusted input.

Mitigation: Use non-sensitive inputs, validate article sources before extraction, and avoid passing confidential local files to the workflow.

Risk: Headless browser rendering currently depends on Chrome sandbox handling that the security guidance flags for improvement.

Mitigation: Run browser rendering only in a controlled sandboxed environment and review Chrome invocation behavior before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wiseqingyang/skills/article-summary-card)
- [Output Schema](references/output-schema.md)
- [Planning Prompt](references/prompts/plan-system.md)
- [Summary Prompt](references/prompts/summary-system.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured summary JSON rendered to Markdown, HTML, and PNG]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports include article title, source, one-sentence summary, sections, closing takeaway, and tags.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
