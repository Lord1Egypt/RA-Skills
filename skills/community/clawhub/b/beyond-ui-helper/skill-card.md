## Description:

Install, configure, and troubleshoot the @beyondcorp/beyond-ui React/Tailwind component library. Use when an agent needs to add the package, wire the generated CSS, align Tailwind themes, run Storybook/tests/build, or reference Beyond-UI components, hooks, and known caveats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[machineke](https://clawhub.ai/user/machineke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Beyond-UI to React applications, import its generated CSS, align Tailwind theme tokens, use component and hook examples, and run local verification commands before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install npm packages and peer dependencies in a host project.

Mitigation: Run installation in a controlled development environment, review package changes, and rely on a lockfile or pinned versions where possible.

Risk: The artifact includes known audit and dependency upgrade watch items for the Beyond-UI stack.

Mitigation: Review the known-issues advisory notes and run lint, tests, and builds before publishing or upgrading.

Risk: The server security guidance notes a shell syntax error in install-beyond-ui.sh that affects reliability.

Mitigation: Review and correct the install script before relying on it for automated setup.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/machineke/skills/beyond-ui-helper)
- [Beyond-UI Setup Reference](references/setup.md)
- [Beyond-UI Component Catalogue](references/components.md)
- [Hooks & Utilities Reference](references/hooks.md)
- [Theming Beyond-UI](references/theming.md)
- [Contributor Workflow Reference](references/workflow.md)
- [Known Issues & DX Watchlist](references/known-issues.md)
- [Beyond-UI Storybook](https://storybook.ui.beyondsoftwares.com)
- [Beyond-UI Library Landing Page](https://ui.beyondsoftwares.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, and file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose package installation, CSS import edits, Tailwind configuration changes, and verification commands for the host project.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
