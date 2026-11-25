## Description:

Run the post-training lifecycle on Crusoe Intelligence Foundry. Prepare and validate chat-format datasets, launch supervised fine-tuning (SFT) jobs, monitor training runs, pick and download LoRA adapter checkpoints, and deploy base models or fine-tuned adapters to dedicated self-serve inference endpoints — all through Crusoe's OpenAI-compatible APIs. Use when the user wants to fine-tune or train a model on their data, create a LoRA adapter, upload a training dataset to Crusoe, deploy a fine-tuned model, or stand up a dedicated inference deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crusoe](https://clawhub.ai/user/crusoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare and validate chat-format training data, fine-tune models with LoRA on Crusoe Intelligence Foundry, monitor jobs and select checkpoints, and deploy base models or adapters as inference endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Training datasets may contain sensitive information that is sent to Crusoe for processing.

Mitigation: Review the dataset for sensitive information and confirm you are comfortable sending it to Crusoe before uploading it.

## Reference(s):

- [Crusoe Managed AI documentation](https://docs.crusoe.ai/managed-ai/overview/)
- [Fine-tuning API specification](https://api.intelligence.crusoecloud.com/v1/swagger.json)
- [Self-Serve Deployments API specification](https://api.crusoecloud.com/v1/openapi.json)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with Python, shell, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workflow steps, API request examples, and dataset validation guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
