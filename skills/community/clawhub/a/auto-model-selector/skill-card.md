## Description:

Auto Model Selector routes user prompts to local or cloud AI models based on request complexity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mymrxu](https://clawhub.ai/user/mymrxu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to classify prompt complexity, recommend a local or cloud model, and manage cost-aware model routing configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may be sent over plaintext HTTP to a hard-coded private-network Ollama service.

Mitigation: Use the skill only with a trusted Ollama endpoint, preferably localhost or an explicitly configured secured service, before routing sensitive prompts.

Risk: Automatic model detection can rewrite the model configuration during imports, routing, or update flows.

Mitigation: Review and back up models.json before use, and confirm that automatic detection and configuration updates are acceptable for the deployment.

## Reference(s):

- [Artifact README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/mymrxu/skills/auto-model-selector)
- [Publisher profile](https://clawhub.ai/user/mymrxu)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration, Guidance]

**Output Format:** [JSON routing results and command-line text for model management actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend model identifiers, report routing reasons, and update model configuration during detection or update flows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
