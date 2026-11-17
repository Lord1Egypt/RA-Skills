## Description:

Cohere Translator helps agents translate text and files across 23 languages using Cohere's Command A Translate model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lykeion-dev](https://clawhub.ai/user/lykeion-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to translate short text, files, or stdin/stdout streams while keeping large file contents outside the agent context window. It is suited to multilingual documentation, operational text, markdown, and code-adjacent translation workflows that can use the Cohere API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Translated text and file contents are sent to Cohere.

Mitigation: Do not use the skill for secrets, regulated data, or confidential files unless that external processing is approved.

Risk: The Cohere API key can be exposed to local process inspection when passed through the curl command invocation.

Mitigation: Prefer COHERE_API_KEY over --api-key and run the skill only in trusted local environments.

## Reference(s):

- [Cohere API Keys](https://dashboard.cohere.com/api-keys)
- [Cohere Labs Non-Commercial License](https://cohere.com/cohere-labs-cc-by-nc-license)
- [ClawHub Skill Page](https://clawhub.ai/lykeion-dev/skills/cohere-translator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, translated files, or JSON metadata with token counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports file, stdin, stdout, and JSON modes; large file inputs are automatically chunked with rate-limit pacing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
