## Description: <br>
Manage a shared Windows application registry and control which agents may run registered apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gregtysick](https://clawhub.ai/user/gregtysick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain a shared Windows application registry, configure per-agent launch policy, validate registry entries, and launch or stop registered applications through controlled registry lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored launch paths determine what future app-launch requests execute. <br>
Mitigation: Review every launch path before saving it and protect the registry file because future launches depend on its contents. <br>
Risk: Sensitive applications could be launched by unintended agents if policy settings are too broad. <br>
Mitigation: Use allowlist or off mode for sensitive apps and confirm policy changes before writing them. <br>
Risk: Malformed or incomplete registry entries can cause failed launches or unreliable stop behavior. <br>
Mitigation: Run registry validation, keep runtime executable and process-name metadata when known, and avoid guessing repairs without approval. <br>


## Reference(s): <br>
- [Application Manager on ClawHub](https://clawhub.ai/gregtysick/application-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with text menus, JSON registry examples, and Windows shell command shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Manages a human-readable JSON registry at ~/.openclaw/registries/application_registry.json and prompts for confirmation before registry changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
