## Description: <br>
CoolSkill Builder helps agents turn repositories, API documentation, natural-language requirements, or code snippets into standardized zero-dependency skill modules with manifests, tests, registry metadata, and security checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fredtai](https://clawhub.ai/user/fredtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to generate portable skill packages from source material, including skill.yaml, impl.py, test.py, and manifest.json outputs. It is intended for workflows that need local registry versioning, cross-agent tool compatibility, and security validation before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create local registry files and generated artifacts with broad activation behavior. <br>
Mitigation: Review generated files, manifests, and registry changes before registering or publishing them. <br>
Risk: The skill can push generated content to GitHub when GITHUB_TOKEN and GITHUB_REPO are configured. <br>
Mitigation: Keep those environment variables unset unless remote sync is intended, and verify the target repository before enabling sync. <br>
Risk: The artifact includes an HTTP invocation example that may be unsafe outside trusted local networks. <br>
Mitigation: Use the HTTP example only in trusted environments and add authentication, authorization, and network controls before exposing it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fredtai/coolskill-builder) <br>
- [ZeroSkill-Forge specification](artifact/references/spec.md) <br>
- [File template specification](artifact/references/file-templates.md) <br>
- [Security rules](artifact/references/security-rules.md) <br>
- [Registry format](artifact/references/registry-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown report with embedded YAML, Python, JSON, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces generated skill files, security scan results, test summaries, registry paths, and optional publishing guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
