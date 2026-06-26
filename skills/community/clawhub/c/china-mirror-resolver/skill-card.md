## Description: <br>
Self-healing China mirror source resolver that helps agents discover, validate, and configure domestic package, registry, and repository mirrors for developer tools in mainland China. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[The-Ladder-of-Rrogress](https://clawhub.ai/user/The-Ladder-of-Rrogress) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers working in mainland China use this skill to diagnose slow or failed developer-tool downloads, test available mirror sources, and apply validated package-manager, registry, or repository configuration changes. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change package-manager, Docker, operating-system package, and language-tool source configuration. <br>
Mitigation: Require a preview of the exact tool, mirror URL, config file, backup path, commands, and rollback steps before applying any fix; manually approve sudo or administrator changes. <br>
Risk: Search-discovered or untrusted mirrors can be unavailable, misleading, or malicious. <br>
Mitigation: Prefer well-known HTTPS institutional mirrors, validate every candidate before use, and avoid unknown personal servers or unverifiable mirror lists. <br>
Risk: Some package-manager options, such as pip trusted-host, can weaken certificate verification for a selected host. <br>
Mitigation: Use trusted-host only for known institutional mirrors when necessary, and prefer mirrors with valid HTTPS certificates that do not require certificate-verification bypasses. <br>


## Reference(s): <br>
- [Configuration Templates](references/config-templates.md) <br>
- [Mirror Validation Script](scripts/validate.sh) <br>
- [ClawHub Skill Page](https://clawhub.ai/The-Ladder-of-Rrogress/china-mirror-resolver) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed mirror URLs, config file paths, backup steps, validation results, and rollback steps before persistent changes are applied.] <br>

## Skill Version(s): <br>
2.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
