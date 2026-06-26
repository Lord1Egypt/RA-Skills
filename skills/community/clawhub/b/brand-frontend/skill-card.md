## Description: <br>
Brand Frontend interviews developers about brand identity, then uses Google Stitch to generate, refine, and package a polished standalone landing page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidbergman121](https://clawhub.ai/user/davidbergman121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external builders use this skill to turn a product, side project, or service into a brand-informed landing page through a short interview, Stitch generation, review, and delivery workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may install or update the Stitch SDK and use a sensitive Stitch API key before the user has clearly approved the setup. <br>
Mitigation: Require explicit approval before installing software, prefer a project-local pinned SDK install, and have the user set STITCH_API_KEY in their environment instead of pasting it into chat. <br>
Risk: Generated local state, copied user assets, and deployment bundles may contain sensitive project details or files that should not be shared unchanged. <br>
Mitigation: Review .stitch/metadata.json, .stitch/user-assets, generated HTML, and the final zip contents before sharing or deploying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidbergman121/brand-frontend) <br>
- [Google Stitch SDK documentation](https://google-stitch.com/docs/sdk/ai-sdk) <br>
- [Google Stitch DESIGN.md documentation](https://google-stitch.com/docs/design-md/overview) <br>
- [Brand Discovery Interview Framework](references/interview-framework.md) <br>
- [Stitch Architecture Reference](references/stitch-architecture.md) <br>
- [State Management, Pitfalls & Templates](references/state-and-pitfalls.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational guidance with generated HTML files, Markdown documentation, JSON metadata, shell commands, and a deployment bundle.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Stitch API key and may create local .stitch state, design files, user asset copies, and a final zip bundle.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
