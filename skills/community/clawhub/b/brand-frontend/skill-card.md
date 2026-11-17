## Description:

Brand Frontend guides an agent through a brand discovery interview, Google Stitch-based landing page generation, iterative design review, and delivery of deployment-ready HTML assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidbergman121](https://clawhub.ai/user/davidbergman121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and makers use this skill when they need a standalone landing or marketing page but have not yet defined brand identity, visual direction, or launch-ready page assets. The skill helps an agent interview the user, translate brand choices into a design system, generate and refine pages with Google Stitch, and package final HTML for deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install a changing external Google Stitch SDK, including global installation by default.

Mitigation: Prefer a project-local pinned SDK install and confirm package-manager commands before installation.

Risk: The skill may open generated HTML previews automatically.

Mitigation: Ask whether the user wants browser previews or file paths before opening generated files.

Risk: The workflow depends on STITCH_API_KEY for Google Stitch access.

Mitigation: Use a scoped key, keep it in the local environment, and never echo or transcribe it.

Risk: User-provided screenshots or logos may be saved into the delivered bundle.

Mitigation: Avoid sensitive assets and confirm which saved assets should be included before delivery.

## Reference(s):

- [Brand Frontend ClawHub skill page](https://clawhub.ai/davidbergman121/skills/brand-frontend)
- [Interview Framework](artifact/references/interview-framework.md)
- [Stitch Architecture Reference](artifact/references/stitch-architecture.md)
- [State Management, Pitfalls & Templates](artifact/references/state-and-pitfalls.md)
- [Google Stitch SDK documentation](https://google-stitch.com/docs/sdk/ai-sdk)
- [Google Stitch DESIGN.md documentation](https://google-stitch.com/docs/design-md/overview)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Conversational guidance with Markdown and code snippets, plus generated local HTML bundle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local .stitch state, design documentation, optional user asset copies, and a deployment bundle when the workflow completes.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
