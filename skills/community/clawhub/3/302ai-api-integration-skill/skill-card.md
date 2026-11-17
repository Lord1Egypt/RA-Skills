## Description:

Helps agents find 302.AI APIs, retrieve documentation, and generate integration code for the user's programming language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharkqwy](https://clawhub.ai/user/sharkqwy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose 302.AI APIs and generate starter integration code, shell commands, and configuration guidance for AI, media, document, search, RAG, and utility workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users for a live 302.AI API key and its examples place keys directly in generated code.

Mitigation: Use environment variables or a local secret manager, avoid pasting live keys into chat, and remove hardcoded credentials from generated examples before running or sharing code.

Risk: Broad activation rules can cause the skill to engage for unrelated API or AI requests.

Mitigation: Install it only when a 302.AI-focused helper is desired and confirm that generated endpoints and documentation links stay on expected 302.AI domains.

Risk: Generated integration code may be incomplete or unsuitable for a production service without review.

Mitigation: Review generated code before execution, add project-specific error handling and rate-limit controls, and test with non-sensitive data first.

## Reference(s):

- [API Category Index](artifact/references/api_categories.md)
- [Integration Code Templates](artifact/references/integration_examples.md)
- [Parse Script Usage](artifact/references/parse_script_usage.md)
- [302.AI API Documentation](https://doc.302.ai/)
- [302.AI API List](https://doc.302.ai/llms.txt)
- [ClawHub Skill Page](https://clawhub.ai/sharkqwy/skills/302ai-api-integration-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoint choices, generated request code, error-handling notes, and credential handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
