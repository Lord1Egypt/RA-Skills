## Description:

Ask an EmpirioLabs AI text model a question and get its answer. Use when the user asks for a second opinion from another model on code, a plan, or a draft, wants a specific EmpirioLabs AI model to answer, wants several models to answer the same prompt side by side, or needs a model that reads images to describe a picture. Runs a bundled Python script that picks a text model from the live catalog (or the ones you name), can attach text files and images to the prompt, and prints the answer or saves it to the path you choose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[empiriolabs](https://clawhub.ai/user/empiriolabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to get one or more EmpirioLabs AI model responses to questions, code, plans, and drafts, or to ask a vision-capable model about an image. They can select models, include agreed text or image inputs, and save the response when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports a high-confidence possibility that an API key could be sent to another host after a redirect; the scan is partial.

Mitigation: Review redirect behavior before use, and use a narrowly scoped API key that can be rotated if needed.

Risk: Text files and images attached to a prompt are sent to the selected model service.

Mitigation: Attach only content the user has agreed to share with EmpirioLabs AI.

## Reference(s):

- [EmpirioLabs AI](https://empiriolabs.ai)
- [EmpirioLabs AI API Reference](https://docs.empiriolabs.ai)
- [EmpirioLabs AI MCP Setup](https://docs.empiriolabs.ai/mcp)
- [Manage EmpirioLabs AI API Keys](https://platform.empiriolabs.ai/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain text or JSON model responses, optionally saved to a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return one or several model responses; requests can set a maximum token count. Each selected model is billed for its request.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
