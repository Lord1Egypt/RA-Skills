## Description: <br>
Internationalization audit pack for scanning locale files and detecting missing translation keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and localization teams use this skill to audit JSON and YAML locale files for missing keys, inconsistent structures, and untranslated strings before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the required mcp-openclaw-extensions package. <br>
Mitigation: Install only if you trust that package and its OpenClaw tool behavior. <br>
Risk: An overly broad config_path could cause the audit to inspect unintended repository or locale files. <br>
Mitigation: Point config_path only at the repository or locale directories intended for the i18n audit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/firm-i18n-audit-pack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain-text audit findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a config_path parameter to select the repository or locale configuration to audit.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
