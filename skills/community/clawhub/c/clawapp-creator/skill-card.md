## Description: <br>
Builds or adapts static front-end apps and mini-games for Nima Tech Space by helping create manifests, package compliant zips, preview, validate, and upload when requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NimaChu](https://clawhub.ai/user/NimaChu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw/Codex users use this skill to create or retrofit static front-end apps and mini-games for CLAWSPACE publishing, including optional platform LLM integration, package validation, and upload workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish apps using saved CLAWSPACE account credentials. <br>
Mitigation: Install only when publishing authority is acceptable, prefer macOS Keychain over plaintext config storage, and require explicit final confirmation before upload. <br>
Risk: A broad publish request may lead to an unintended upload or overwrite. <br>
Mitigation: Run the account-check and dry-run steps before publishing, and confirm account, slug, package path, and overwrite status before upload. <br>
Risk: Stored credentials may be exposed if plaintext config storage is used. <br>
Mitigation: Use Keychain storage where available and restrict plaintext upload configuration file permissions when a config fallback is necessary. <br>


## Reference(s): <br>
- [Platform Contract](artifact/references/platform-contract.md) <br>
- [Model API](artifact/references/model-api.md) <br>
- [First Batch Templates](artifact/docs/first-batch-templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/NimaChu/clawapp-creator) <br>
- [Nima Tech Space](https://www.nima-tech.space) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated project, manifest, configuration, and package files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local static app packages and publishing commands; upload workflows should require explicit final confirmation.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
