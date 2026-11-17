## Description:

Upload and use your own LoRA or checkpoint on Runware, including importing custom safetensors weights through the Runware API and using the assigned AIR for generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to import existing LoRA, checkpoint, LyCORIS, VAE, or embedding weights into Runware, assign a durable AIR, and generate with the uploaded model after confirming readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private model-weight URLs can expose proprietary weights if they are permanently public or include durable shared credentials.

Mitigation: Prefer short-lived signed URLs, avoid embedding secrets in shareable URLs, expire or delete hosted files after import, and keep Runware's private setting enabled unless publication is intentional.

Risk: Incorrect category, architecture, or readiness assumptions can cause failed imports or unusable generated output.

Mitigation: Resolve the live Runware upload schema before submitting, match architecture to the model's training base, and confirm readiness through model availability or a small inference test.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runware/skills/bring-your-own-model)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with API parameters and command-oriented steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow guidance for validating Runware model import schemas, assigning AIR values, checking readiness, and running inference.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
