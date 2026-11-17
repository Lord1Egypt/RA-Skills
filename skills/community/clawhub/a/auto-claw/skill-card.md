## Description:

Autonomously monitors and optimizes WordPress sites with SEO fixes, performance audits, A/B testing, security checks, and competitor tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiongmao11132](https://clawhub.ai/user/xiongmao11132)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, WordPress operators, and agencies use Auto-Claw to audit and automate SEO, performance, content, conversion, and WordPress site operations through an agent-driven CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make high-impact WordPress and server changes.

Mitigation: Run it in a constrained environment with least-privilege WordPress or service accounts and HTTPS-only connections.

Risk: Unsafe command execution and weak approval safeguards could allow unintended site changes.

Mitigation: Remove shell=True command construction and --allow-root usage, pin SSH host keys, and replace demo approval stubs with a real fail-closed approval system.

Risk: Cron jobs and mu-plugin deployment can create persistent site behavior.

Mitigation: Require explicit approval, document rollback steps, and audit every persistent change before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/xiongmao11132/skills/auto-claw)
- [README.md](artifact/README.md)
- [QUICKREF.md](artifact/QUICKREF.md)
- [SEO deployment notes](artifact/docs/seo-deployment-20260324.md)
- [Performance deployment notes](artifact/docs/performance-deployment-20260324.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI-oriented text with generated WP-CLI commands, JSON or JSON-LD snippets, HTML snippets, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require WordPress URL, web root, credentials or vault configuration, and explicit approval before site-changing actions.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
