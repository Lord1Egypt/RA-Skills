## Description:

Create presentations, documents, social posts, and web pages via the Gamma.app API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autosolutionsai-didac](https://clawhub.ai/user/autosolutionsai-didac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create Gamma presentations, documents, social posts, and web pages from prompts or templates, then check generation status and retrieve live or exported results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that crafted presentation text can become local Python code execution before the API request is sent.

Mitigation: Do not use the skill with untrusted or confidential prompt text until the script passes values to Python as data rather than interpolating them into executable Python source.

Risk: The skill sends the Gamma API key and inputText content to Gamma's servers.

Mitigation: Use a dedicated Gamma API key, restrict usage to approved content, and rotate or revoke the key if exposure is suspected.

## Reference(s):

- [Gamma Homepage](https://gamma.app)
- [Gamma API Getting Started](https://developers.gamma.app/docs/getting-started)
- [Gamma API Reference](references/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/autosolutionsai-didac/skills/gamma-app-api)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Files, Guidance]

**Output Format:** [Markdown with bash commands, JSON API responses, and generated Gamma or export links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GAMMA_API_KEY, curl, and python3; input content is sent to Gamma's public API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
