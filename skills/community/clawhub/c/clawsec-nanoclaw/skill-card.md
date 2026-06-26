## Description: <br>
ClawSec for NanoClaw helps agents check installed skills against security advisories, verify skill package signatures, and monitor protected NanoClaw files for unauthorized changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
NanoClaw operators and agents use this skill before installing skills and during audits to identify known vulnerabilities, refresh a signed advisory cache, verify package signatures, and check protected files for drift. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can automatically restore or approve protected NanoClaw files, and the security evidence says this authority needs Review. <br>
Mitigation: Restrict integrity tools to trusted or admin agents, review guardian/policy.json before enabling them, run checks with autoRestore=false first, and require human approval for baseline changes. <br>
Risk: Installing the full skill enables host-side integrity enforcement, not only advisory checks. <br>
Mitigation: Install it only when host-side enforcement is intended, and preserve backups of the soul-guardian state, audit log, patches, and quarantine files before relying on restore behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-nanoclaw) <br>
- [ClawSec advisory feed](https://clawsec.prompt.security/advisories/feed.json) <br>
- [Installation Guide](INSTALL.md) <br>
- [File Integrity Monitoring](docs/INTEGRITY.md) <br>
- [Skill Package Signing and Verification](docs/SKILL_SIGNING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with TypeScript examples, shell commands, and JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing MCP tools return advisory, signature, integrity, and audit status data; integrity operations can request host-side file checks or restores.] <br>

## Skill Version(s): <br>
0.0.10 (source: SKILL.md frontmatter, CHANGELOG, skill.json, server release evidence; released 2026-06-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
