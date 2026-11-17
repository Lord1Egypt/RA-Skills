## Description:

Genera capturas UI tipo tutorial con estilo F100K, incluyendo terminales, cards de paso, callouts, screenshots, atajos, links, comparisons y listas, renderizadas como PNG mediante HTML, CSS y Puppeteer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-production agents use this skill to create tutorial-style PNG assets for landings, artifacts, carousels, and video overlays. It supports single-image rendering and manifest-driven batch rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The renderer handles some user-supplied template fields as raw HTML inside an unsandboxed browser.

Mitigation: Avoid rendering untrusted manifests or third-party text, and review inputs before execution.

Risk: Installation uses local npm dependencies and Puppeteer rendering.

Mitigation: Install only when the publisher is trusted and prefer pinned dependencies with a lockfile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/capturas-tutorial-formula100k)
- [Publisher profile](https://clawhub.ai/user/formula100k)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PNG files plus Markdown, YAML-style manifest guidance, JSON data examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may use transparent or cream backgrounds and can be generated one at a time or from a manifest.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
