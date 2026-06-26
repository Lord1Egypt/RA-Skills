## Description: <br>
Figma-to-frontend visual QA workflow for building pages from Figma designs and tightening existing implementations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[valerii-baidak](https://clawhub.ai/user/valerii-baidak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build, compare, and tighten web UI implementations against a Figma frame. It exports Figma references, captures rendered pages, runs visual and layout comparisons, and guides code fixes for spacing, typography, color, and structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Figma token and makes authenticated requests to the official Figma API. <br>
Mitigation: Use a read-scoped Figma token, keep it in the environment as FIGMA_TOKEN, and avoid persisting it in logs or artifacts. <br>
Risk: The workflow can guide frontend code edits after visual comparison. <br>
Mitigation: Review generated code diffs before committing or deploying changes. <br>
Risk: Rendered screenshots, exported Figma images, and diff reports may contain sensitive product or design content. <br>
Mitigation: Store run artifacts locally, limit access to figma-pixel-runs, and clean those folders when the comparison work is complete. <br>
Risk: External font or CDN links added during implementation can change network behavior. <br>
Mitigation: Review any new external asset links and approve only sources required for the target design. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/valerii-baidak/figma-pixel) <br>
- [Setup](references/setup.md) <br>
- [Workflow checklist](references/workflow.md) <br>
- [Figma input layer](references/figma.md) <br>
- [Artifact handling](references/artifacts.md) <br>
- [Script reference](references/scripts.md) <br>
- [OpenCV analysis](references/opencv.md) <br>
- [Figma personal access tokens](https://help.figma.com/hc/en-us/articles/8085703771159-Manage-personal-access-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, code edits, JSON reports, screenshots, and visual diff artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local run folders for Figma metadata, reference images, rendered screenshots, pixel comparison reports, and layout analysis artifacts.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
