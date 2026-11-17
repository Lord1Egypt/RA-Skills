## Description:

Figma-to-frontend visual QA workflow for building pages from Figma designs and tightening existing implementations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[valerii-baidak](https://clawhub.ai/user/valerii-baidak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to build pages from Figma frames, compare rendered pages against Figma references, and guide layout, typography, spacing, color, and structure fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs broad local browser and image comparison automation with weak containment.

Mitigation: Run it in an isolated workspace or container and use only trusted target page URLs.

Risk: Setup depends on mutable npm and browser dependencies.

Mitigation: Pin dependencies before setup and avoid running install commands as root.

Risk: The skill requires a Figma API token.

Mitigation: Use a read-only or minimum-scope Figma token and avoid persisting the token in logs, artifacts, or committed files.

Risk: Local run artifacts can contain screenshots or Figma data.

Mitigation: Review figma-pixel-runs artifacts before sharing or committing them.

## Reference(s):

- [README](README.md)
- [Setup](references/setup.md)
- [Workflow](references/workflow.md)
- [Figma Input Layer](references/figma.md)
- [Expected Artifacts](references/artifacts.md)
- [Script Contracts](references/scripts.md)
- [OpenCV Diff Analysis](references/opencv.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code and shell command blocks, plus local JSON, PNG, and Markdown report artifacts from the skill scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Figma API metadata, reference images, rendered screenshots, pixel diff images, and comparison reports under figma-pixel-runs when the user explicitly requests a pipeline run.]

## Skill Version(s):

1.0.14 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
