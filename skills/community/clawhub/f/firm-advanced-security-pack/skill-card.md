## Description: <br>
Advanced security audit pack covering secrets lifecycle, path canonicalization, exec plan freeze, hook routing, config includes, prototype pollution, safeBins profiles, and group policy defaults. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security engineers use this skill to audit OpenClaw configuration files for high-severity and critical security issues across secrets handling, path handling, execution approvals, hooks, includes, prototype pollution, safeBins profiles, and group policy defaults. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on mcp-openclaw-extensions for its actual security checks, so the effective behavior is controlled by that extension. <br>
Mitigation: Verify the extension source, version, and permissions before running the audit commands. <br>
Risk: Audit commands inspect OpenClaw configuration files that may contain sensitive operational details. <br>
Mitigation: Run the checks only on configuration files you intend to inspect and avoid sharing scan inputs or results outside the authorized review context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/romainsantoli-web/firm-advanced-security-pack) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline OpenClaw audit commands and configuration file parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only security audit workflow that depends on mcp-openclaw-extensions >= 3.0.0.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
