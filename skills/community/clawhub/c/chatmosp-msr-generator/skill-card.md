## Description:

Generates ChatMOSP MSR metal cluster structures, validates expected outputs, creates PNG and GIF visualizations, and sends results through Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanyangye](https://clawhub.ai/user/sanyangye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers using the ChatMOSP skill set use this skill after parameter preparation and user confirmation to run MSR/Wulff cluster generation for metal nanoparticle tasks. It helps validate generated structure files and produce visualization assets for user delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow runs an external mosp-for-chatMOSP Python engine that the server security evidence describes as unverified.

Mitigation: Verify the engine source and commit before use, and run it in a limited workspace without unrelated secrets.

Risk: Task names and output paths may be unsafe if accepted without restriction.

Mitigation: Restrict task names to simple safe characters and keep generated outputs inside an isolated task directory.

Risk: Generated files are sent through Feishu, which may be inappropriate for some data or environments.

Mitigation: Confirm Feishu upload is acceptable before sending results, or use a local-only workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanyangye/skills/chatmosp-msr-generator)
- [Publisher profile](https://clawhub.ai/user/sanyangye)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON action snippets, and generated structure file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and validates MSR structure files, static PNG images, GIF animations, and Feishu delivery guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
