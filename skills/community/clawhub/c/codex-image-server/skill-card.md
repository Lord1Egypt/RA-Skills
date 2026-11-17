## Description:

Use when a user wants to turn local Codex image_generation capability into a local HTTP image server for apps such as Photoshop plugins, design tools, or internal image workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catrefuse](https://clawhub.ai/user/catrefuse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to expose local Codex image generation through a local HTTP API for design tools, Photoshop plugins, and internal image workflows. It helps add health, capability, generation, image-file, cancellation, size-validation, and smoke-test behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server template can fall back to remote OpenAI image APIs when an OpenAI API key is present, which may send prompts and reference images outside the local Codex path.

Mitigation: Require an explicit backend choice and disable automatic OpenAI fallback unless remote OpenAI use is intended and approved.

Risk: The generated HTTP server is intended for local use but keeps authentication optional and uses permissive CORS, which can expose generation and image-file routes if bound beyond loopback.

Mitigation: Bind only to loopback unless protected, and add authentication plus an origin allowlist before exposing the server to other hosts.

Risk: Generated and reference images may persist in output directories, and decoded image identifiers need strict validation before file serving.

Mitigation: Restrict served files to the intended output directory, validate image IDs before path resolution, and define cleanup and retention for generated and reference images.

## Reference(s):

- [HTTP Contract](references/http-contract.md)
- [ClawHub skill page](https://clawhub.ai/catrefuse/skills/codex-image-server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Node.js HTTP server code, route contracts, smoke-test commands, and validation guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
