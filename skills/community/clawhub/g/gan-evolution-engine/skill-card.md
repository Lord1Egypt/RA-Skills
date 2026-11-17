## Description:

Generative Adversarial Evolution for AI Agent Skills uses a GAN-like loop to create, evaluate, and select skill variants for iterative capability improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sudabg](https://clawhub.ai/user/sudabg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent engineers use this skill to generate and benchmark variants of an existing agent skill, then select higher-fitness outputs for review, promotion, or publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs and writes untrusted generated variant code without reliable isolation.

Mitigation: Test only in a disposable container or virtual machine with network access disabled and no valuable workspace files.

Risk: Credential handling is flagged as unsafe by the server security evidence.

Mitigation: Remove inherited API keys, rotate the exposed EvoMap secret, and redact credential logging before installation or execution.

Risk: Bundled evolved skill outputs and hooks may introduce behavior outside the core GAN evolution workflow.

Mitigation: Remove or isolate bundled evolved outputs and hooks, then review the remaining files before use.

Risk: Dependency and path handling require review before normal workspace use.

Mitigation: Pin dependencies and validate generated paths before executing the skill on any non-disposable target.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sudabg/skills/gan-evolution-engine)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands, generated skill files, JSON evolution history, and optional publishing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces evolved skill variants under an output directory and records fitness history for review.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
