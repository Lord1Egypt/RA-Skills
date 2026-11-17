## Description:

Make one transparent animated sticker package from one static reference image and one natural-language motion prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufei-png](https://clawhub.ai/user/wufei-png)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users and developers use this skill to turn a single reference image plus a motion prompt into a validated transparent animated sticker package, with optional platform-specific exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that a packaging script can overwrite or recursively delete caller-selected local paths without an enforced output boundary.

Mitigation: Install and run the skill only in a contained project workspace, keep output paths under a disposable or dedicated output directory, and avoid pointing outputs at existing folders.

Risk: Generated sticker packages and platform exports can be misleading or unsuitable if technical checks pass but visual identity, meaning, loop, alpha, or small-size readability are not inspected.

Mitigation: Require the documented visual validation step after every package or export change, and deliver only artifacts whose validation reports mark both technical and visual validation as passing.

## Reference(s):

- [Agent Skills Specification](https://agentskills.io/specification)
- [Motion plan](references/motion-plan.md)
- [Platform exports](references/platform-exports.md)
- [Transparency branch](references/transparency.md)
- [Validation](references/validation.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Transparent animated WebP sticker package with JSON validation reports, PNG source frames, optional GIF exports, and Markdown or shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one sticker per invocation; default packages include source frames, motion metadata, reference metadata, a contact sheet, validation reports, and optional platform exports.]

## Skill Version(s):

0.8.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
