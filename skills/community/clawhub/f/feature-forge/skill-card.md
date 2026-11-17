## Description:

Generates complete features from natural language, including components, API routes, migrations, types, and tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guifav](https://clawhub.ai/user/guifav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement full-stack features in Next.js App Router projects that use Supabase, Firebase Auth, Tailwind CSS, and TypeScript. It guides an agent through planning, schema changes, data access, API routes, UI, tests, verification, and a final commit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad file-changing and commit authority.

Mitigation: Require a visible implementation plan, review diffs before acceptance, and run project tests and linting before merging generated changes.

Risk: Generated schema changes, API routes, or UI code may be incorrect or inconsistent with the existing application.

Mitigation: Review proposed database migrations, auth checks, generated types, and tests against the target project before deployment.

Risk: The workflow may run local tooling such as npx commands.

Mitigation: Prefer project-pinned package-manager scripts and review any new dependency or command before execution.

## Reference(s):

- [Feature Forge ClawHub Skill Page](https://clawhub.ai/guifav/skills/feature-forge)
- [Publisher Profile](https://clawhub.ai/user/guifav)
- [OpenClaw Skills Homepage](https://github.com/guifav/openclaw-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks, shell commands, file change summaries, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify project source files, database migrations, tests, and git commits when used by an agent with filesystem and command execution access.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
