## Description:

AI-powered error monitoring for reporting JavaScript and TypeScript production errors, retrieving AI-generated fixes, and listing recent project errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hankmint](https://clawhub.ai/user/hankmint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Codemend to add production error monitoring to JavaScript and TypeScript projects, report errors to Codemend, check analysis status, and retrieve AI-generated fix guidance or pull request links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production error reporting can transmit error messages, stack traces, page URLs, or other sensitive fields outside the user's system.

Mitigation: Confirm what fields may leave the system, redact secrets and PII, and approve production-page use before enabling monitoring.

Risk: The helper script sends AUTOHEAL_API_KEY to an undocumented AutoHeal service that differs from the Codemend API described elsewhere.

Mitigation: Do not run scripts/check-errors.sh or provide AUTOHEAL_API_KEY unless autohealai.com has been separately reviewed and approved.

Risk: Browser and npm setup examples can introduce third-party runtime code into production applications.

Mitigation: Prefer pinned npm package versions and a pinned or self-hosted browser script with integrity controls where possible.

## Reference(s):

- [Codemend Skill on ClawHub](https://clawhub.ai/hankmint/skills/codemend)
- [Codemend](https://codemend.ai)
- [OpenClaw Registry](https://github.com/anthropics/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, code snippets, API request examples, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Codemend error identifiers, dashboard URLs, fix explanations, root-cause summaries, confidence scores, fix prompts, and pull request URLs when available.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
