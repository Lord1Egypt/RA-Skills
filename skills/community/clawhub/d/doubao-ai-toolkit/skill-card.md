## Description:

Helps an agent use pinned local Doubao and Volcano Engine CLI tools for image, video, speech, chat, search, and embedding tasks after explicit user authorization and privacy checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocxf](https://clawhub.ai/user/cryptocxf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when a user explicitly chooses Doubao or Volcano Engine services and needs guided local CLI commands for multimodal generation, transcription, chat, search, or embeddings. The skill emphasizes credential handling, file authorization, URL review, callback review, and clear reporting of generated file paths and failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, search terms, URLs, text, images, audio, and video may be sent to Doubao, Volcano Engine, or related services.

Mitigation: Use the skill only after the user explicitly selects those services, explain what data will be sent, and require authorization before using local files, URLs, callbacks, or search queries.

Risk: ARK_API_KEY could be exposed if copied into chat, command arguments, logs, callback URLs, or generated files.

Mitigation: Keep ARK_API_KEY in the environment or a secret manager, never echo or validate the key value, and stop use if leakage is suspected.

Risk: Dependency upgrades could change CLI behavior or supply-chain exposure.

Mitigation: Install from the locked release artifact with npm ci, keep lifecycle scripts disabled, and review pinned dependencies before upgrades.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline bash command examples and generated file paths when commands are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Doubao or Volcano Engine credentials through ARK_API_KEY and uses pinned npm dependencies from the release artifact.]

## Skill Version(s):

1.0.1 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
