## Description:

Generate dark neon cyber-fantasy dashboards, glassmorphism surfaces, and gamified React and Tailwind UIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isdou](https://clawhub.ai/user/isdou)

### License/Terms of Use:

MIT

## Use Case:

Developers and frontend teams use this skill to design or restyle React, Tailwind, and CSS interfaces into dark cyber-fantasy dashboards, membership centers, event pages, profile screens, and gamified status panels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blindly copying the global CSS can disable page scrolling or text selection, and heavy blur or animation effects can harm performance.

Mitigation: Merge only the CSS variables and utilities needed for the target UI, avoid global overflow or selection changes unless intentional, and verify responsiveness, contrast, scroll behavior, and performance.

Risk: Reusing maintainer publishing commands without review can delete files through rsync --delete or run an unexpected ClawHub CLI version.

Mitigation: Check source and destination paths before running destructive sync commands, use an LTS Node runtime, and prefer a pinned ClawHub CLI version for release workflows.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/isdou/skills/cyber-fantasy-ui)
- [Publisher profile](https://clawhub.ai/user/isdou)
- [Project homepage from ClawHub metadata](https://github.com/isdou/aoleme-ui-skill)
- [Skill entrypoint](artifact/SKILL.md)
- [Tailwind design tokens](artifact/resources/tailwind.config.js)
- [CSS utility patterns](artifact/resources/global.css)
- [Static demo](artifact/demo/index.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with optional React, Tailwind, CSS, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selective Tailwind token merges, CSS utility adaptations, UI component patterns, and verification notes.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
