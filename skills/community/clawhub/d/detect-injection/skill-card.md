## Description:

Checks agent input for prompt-injection attempts and optionally checks agent input or output for content-safety violations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zskyx](https://clawhub.ai/user/zskyx)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to screen untrusted user messages for prompt injection and to check sensitive input or output before it is used in public-facing or multi-user agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Moderation checks can be bypassed or weakened by unsafe configuration and mode handling.

Mitigation: Run the skill only in a constrained environment and do not treat it as an automated security gate until the shell script is fixed or sandboxed.

Risk: If environment variables or the direction argument are attacker-controlled, the script may allow unsafe behavior, including possible code execution.

Mitigation: Restrict who can set environment variables and invocation arguments, and use trusted wrapper code for automated deployments.

Risk: Moderated text may be sent to Hugging Face and OpenAI services.

Mitigation: Use the skill only when sending the moderated text to those services is allowed by the deployment's privacy and compliance requirements.

## Reference(s):

- [Hugging Face Inference model endpoint](https://router.huggingface.co/hf-inference/models/$MODEL)
- [OpenAI Moderations API endpoint](https://api.openai.com/v1/moderations)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON verdicts with optional action guidance; Markdown usage instructions with bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Input checks can include prompt-injection scoring; content checks run only when an OpenAI API key is configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
