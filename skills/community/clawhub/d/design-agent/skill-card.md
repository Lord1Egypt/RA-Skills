## Description:

Design consultation skill for AI agents that provides structured design prompts, DESIGN.md files, color systems, typography rules, spacing conventions, and component patterns for visual outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[defineagain](https://clawhub.ai/user/defineagain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when generating or improving HTML, React, newsletters, PDFs, or other visual outputs that need consistent design tokens, typography, spacing, component patterns, and review guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill suggests running an unpinned third-party npx command.

Mitigation: Pin the package version and execute the command only in a trusted or restricted environment.

Risk: The skill encourages broad invocation across visual workflows.

Mitigation: Require agent or user confirmation before applying this skill automatically to unrelated visual tasks.

Risk: The skill may create DESIGN.md files that affect downstream design decisions.

Mitigation: Ask before writing DESIGN.md files and review the generated design guidance before other agents consume it.

## Reference(s):

- [Design Tokens - Base System](references/design-tokens.md)
- [Integration Guide - How Other Skills Call design-agent](references/integration-guide.md)
- [Design Prompt Template](assets/design-prompt-template.md)
- [Vercel-Inspired Minimal Design Standards](assets/example-design-standards/vercel-minimal.md)
- [design-extractor.com](https://www.design-extractor.com)
- [typeui.sh](https://www.typeui.sh)
- [Design prompts collection](https://lnkd.in/gy8z4XRF)
- [awesome-design-md](https://lnkd.in/ghx8RddV)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with design tokens, checklists, CSS snippets, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose creating a DESIGN.md file and may recommend visual review iterations before final output.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
