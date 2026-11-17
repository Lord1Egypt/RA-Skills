## Description:

AetherViz Master helps an agent turn a teaching topic into an interactive, browser-viewable educational visualization page with 3D, SVG, formulas, and responsive controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liwu800729](https://clawhub.ai/user/liwu800729)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers, students, education content creators, and developers use this skill to generate interactive HTML teaching pages for topics in physics, chemistry, biology, mathematics, astronomy, and programming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated pages may load third-party CDN code despite the zero-dependency claim.

Mitigation: Review generated HTML before use and remove remote dependencies or pin them with integrity checks.

Risk: The README suggests using npx serve . without pinning a package version.

Mitigation: Use a pinned local server package version or a built-in server such as python -m http.server for local preview.

Risk: The skill imposes strict output and attribution requirements that may not fit every deployment context.

Mitigation: Review generated output requirements before deployment and adjust them when attribution or format constraints conflict with local policy.

## Reference(s):

- [AetherViz Master ClawHub Release](https://clawhub.ai/liwu800729/skills/aetherviz-master)
- [Three.js Documentation](https://threejs.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/)
- [KaTeX](https://katex.org/)
- [D3.js](https://d3js.org/)

## Skill Output:

**Output Type(s):** [code, text]

**Output Format:** [Complete single-file HTML document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated page is intended to be saved as HTML and viewed in a modern WebGL-capable browser; evidence notes that generated pages may load third-party CDN code.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
