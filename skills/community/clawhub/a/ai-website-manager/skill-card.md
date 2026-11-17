## Description:

Guides Claude Code through building, deploying, and managing websites with step-by-step bilingual onboarding, account setup, design discovery, stack selection, implementation, and maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinki42240](https://clawhub.ai/user/pinki42240)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide website projects from discovery through deployment and ongoing maintenance. It is especially aimed at users who want a structured, low-overwhelm workflow for portfolio, business, blog, personal brand, or content-managed websites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may involve creating and storing deployment or CMS credentials.

Mitigation: Use short-lived, least-privilege tokens where possible, store secrets only in local environment files or platform secret stores, and revoke tokens that are pasted into chat, committed, or no longer needed.

Risk: The workflow may run mutable setup, package installation, Git, CMS, and deployment commands.

Mitigation: Review each command before execution and confirm account, repository, CMS, and deployment changes before applying them.

Risk: The server security verdict flags the release as suspicious because of powerful credentials and mutable setup behavior.

Mitigation: Review the skill carefully before installation and use it only when a hands-on website build and deployment workflow is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pinki42240/skills/ai-website-manager)
- [AI Website Manager README](artifact/README.md)
- [Phase 1 Discovery and Design Inspiration](artifact/references/phase1-discovery.md)
- [Phase 2 Account Setup Guide](artifact/references/phase2-accounts.md)
- [Phase 3 Tech Stack Decision Guide](artifact/references/phase3-tech-stack.md)
- [Phase 4 Build Patterns](artifact/references/phase4-build-patterns.md)
- [Troubleshooting Guide](artifact/references/troubleshooting.md)
- [Next.js](https://nextjs.org)
- [Tailwind CSS](https://tailwindcss.com)
- [Sanity](https://sanity.io)
- [Vercel](https://vercel.com)
- [Framer Motion](https://framer-motion.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Conversational Markdown with inline commands, configuration steps, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local website project files, environment configuration, commits, and deployment instructions during guided use.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
