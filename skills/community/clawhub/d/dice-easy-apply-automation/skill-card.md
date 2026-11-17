## Description:

Automate Dice.com Easy Apply searches and applications with Puppeteer/Chromium, resume and cover-letter uploads, remote-role filtering, and conservative application guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ralyodio](https://clawhub.ai/user/ralyodio)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and job-search operators use this skill to guide an agent through Dice.com remote Easy Apply searches, resume and cover-letter uploads, duplicate tracking, and conservative skip decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's default browser launch pattern disables Chromium sandboxing while using a persistent logged-in profile.

Mitigation: Run it in a dedicated low-privilege account or isolated environment, remove sandbox-disabling flags where possible, and use an isolated browser profile.

Risk: The workflow uploads resume and optional cover-letter PDFs to Dice applications.

Mitigation: Keep DRY_RUN enabled until behavior is verified and only point RESUME_PDF and COVER_PDF at documents intended for submission.

Risk: Automated job applications may encounter CAPTCHA, MFA, identity checks, unknown required questions, or stale profile resumes.

Mitigation: Stop for account-security prompts, skip unknown required questions, and verify expected filenames before submitting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ralyodio/skills/dice-easy-apply-automation)
- [Dice Remote Easy Apply Search URL Pattern](https://www.dice.com/jobs?filters.workplaceTypes=Remote&filters.easyApply=true&q=<QUERY>)
- [Dice Easy Apply Wizard URL Pattern](https://www.dice.com/job-applications/<job-id>/wizard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, JavaScript, JSON, and text snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides browser automation, state tracking, audit reporting, and conservative application skip rules.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
