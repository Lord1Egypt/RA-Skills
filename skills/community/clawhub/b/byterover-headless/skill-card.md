## Description: <br>
Query and curate a ByteRover knowledge base using the ByteRover CLI for retrieval, context curation, and context tree syncing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byteroverinc](https://clawhub.ai/user/byteroverinc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to operate ByteRover in headless workflows: authenticate, initialize a project, query stored knowledge, curate new context, and push or pull context tree changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Curated or synced context may include secrets, credentials, private keys, confidential files, or other sensitive project details. <br>
Mitigation: Review content before curate, push, or pull operations and exclude sensitive material unless it is intended to be stored in ByteRover. <br>
Risk: The skill depends on the third-party @byterover/cli package and a ByteRover API key. <br>
Mitigation: Install only when ByteRover and the CLI package are trusted, and use a dedicated, revocable API key. <br>
Risk: Push and pull commands can sync project context to or from ByteRover cloud storage. <br>
Mitigation: Require explicit user approval before push or pull operations, especially in automated or headless workflows. <br>


## Reference(s): <br>
- [ByteRover API key settings](https://app.byterover.dev/settings/keys) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends headless ByteRover CLI usage with machine-parseable JSON responses.] <br>

## Skill Version(s): <br>
1.6.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
