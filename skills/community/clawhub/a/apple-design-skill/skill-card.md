## Description:

Guides AI assistants to generate Apple-style frontend UI code using design tokens, multilingual typography, layout patterns, copywriting rules, and image curation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaos-xxl](https://clawhub.ai/user/chaos-xxl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to have an AI coding assistant produce Apple-style product pages, feature showcases, pricing pages, and related frontend UI. It supplies visual tokens, typography rules, copywriting patterns, image guidance, and layout templates for code generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated UI may include third-party font links or image-source recommendations.

Mitigation: Review font and image choices for project policy, licensing, privacy, and network behavior before shipping generated pages.

Risk: The artifact includes dev/test dependencies and example outputs that may become stale.

Mitigation: Update dependencies and re-run local tests before exposing any development or test server.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/chaos-xxl/skills/apple-design-skill)
- [Artifact README](artifact/README.md)
- [Core prompt](artifact/prompts/main.md)

## Skill Output:

**Output Type(s):** [code, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML/CSS code blocks and optional Tailwind configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest Google Fonts links, image search keywords, and CSS fallback styles; security evidence reports no hidden execution, persistence, data theft, or privilege escalation.]

## Skill Version(s):

1.0.0 (source: server release metadata, manifest.json, package.json, changelog released 2025-01-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
