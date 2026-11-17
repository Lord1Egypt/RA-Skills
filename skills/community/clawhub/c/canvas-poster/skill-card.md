## Description:

Canvas Poster generates server-side PNG posters and dashboards from a declarative section-based JSON DSL powered by @napi-rs/canvas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoweismydd-cloud](https://clawhub.ai/user/zhaoweismydd-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create long-form data posters, dashboards, analytical reports, comparison charts, and infographic-style PNGs from structured configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caller-controlled output paths can overwrite local files.

Mitigation: Keep output paths inside a dedicated directory, confirm before overwriting files, and reject absolute or traversal paths from untrusted configuration.

Risk: Large canvas sizes or high record counts can exhaust local resources during rendering.

Mitigation: Set limits on canvas width, height, section count, and record count before using the skill in automated workflows.

Risk: Untrusted poster configuration can drive file writes and expensive rendering work.

Mitigation: Install and run the skill only with trusted configuration inputs or behind validation safeguards.

## Reference(s):

- [Canvas Poster ClawHub Skill Page](https://clawhub.ai/zhaoweismydd-cloud/skills/canvas-poster)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [@napi-rs/canvas](https://github.com/nicknisi/napi-rs-canvas)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PNG image files with Markdown guidance, JavaScript snippets, and JSON-style configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return canvas dimensions, image buffer metadata, and output path when used through the JavaScript API.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
