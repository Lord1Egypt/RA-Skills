## Description:

FactoriaGo helps agents support academic paper revision and resubmission by onboarding users, managing FactoriaGo projects and files, analyzing reviewer feedback, and drafting reviewer response letters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyh2556406](https://clawhub.ai/user/gyh2556406)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, PhD students, postdocs, and academic authors use this skill to revise LaTeX manuscripts after peer review, organize reviewer concerns, manage FactoriaGo revision projects, compile manuscripts, and draft point-by-point response letters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access FactoriaGo account data, manuscripts, reviewer comments, and project files.

Mitigation: Install only when this access is acceptable, use the minimum necessary account context, and review project/file actions before allowing them.

Risk: Passwords, session cookies, and provider API keys may be exposed if pasted into chat or stored in shell history.

Mitigation: Prefer FactoriaGo web settings for API-key setup, keep session cookies in environment variables only for the active session, and rotate any credentials that were exposed.

Risk: Automated edits or reviewer-response drafts could introduce incorrect manuscript changes or misleading responses.

Mitigation: Preview proposed edits, keep backups or version history, compile after LaTeX changes, and have the author review all response-letter content before submission.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/gyh2556406/skills/factoriago)
- [FactoriaGo Product Website](https://factoriago.com)
- [FactoriaGo API Reference](references/api.md)
- [FactoriaGo Revision Workflow](references/revision-workflow.md)
- [Reviewer Response Letter Templates](references/reviewer-response.md)
- [FactoriaGo Skill Guide](FactoriaGo-Skill-Guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and text or JSON results from FactoriaGo operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a FactoriaGo account, session cookie, project identifiers, manuscript files, reviewer comments, and a configured AI provider API key for AI-assisted features.]

## Skill Version(s):

2.9.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
