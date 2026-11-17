## Description:

Build production-ready GPU liquid-glass surfaces with liquid-gl for React, Vite, or DOM interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woodfishhhh](https://clawhub.ai/user/woodfishhhh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add polished WebGL liquid-glass panels, cards, and UI surfaces while preserving readable DOM content and fallback behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adding the liquid-gl dependency can introduce normal frontend supply-chain and package-change risk.

Mitigation: Confirm the dependency is appropriate for the project, pin or lock its version, and review package changes before deployment.

Risk: WebGL liquid-glass effects can fail or become costly on some browsers, mobile devices, or complex pages.

Mitigation: Keep the CSS backdrop-filter fallback usable, profile GPU use, test Chromium desktop and a mobile viewport, and reduce resolution or expensive effects before broad rollout.

Risk: Incorrect layering or snapshot selection can produce blurred text, duplicate text, stale refraction, or blank lenses.

Mitigation: Keep content in a DOM overlay above an empty lens target, point snapshotSelector at the visual background, register dynamic backgrounds, and check console output during verification.

## Reference(s):

- [WebGL Tuning](references/tuning.md)
- [liquidGL](https://github.com/naughtyduk/liquidGL)
- [Build WebGL Liquid Glass on ClawHub](https://clawhub.ai/woodfishhhh/skills/build-webgl-liquid-glass)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with code snippets and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include React, CSS, TypeScript declarations, package installation commands, tuning values, fallback guidance, and verification steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
