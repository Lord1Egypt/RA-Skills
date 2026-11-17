## Description:

Validates OpenClaw configuration patches or openclaw.json files locally against a JSON Schema and reports specific field-level errors before configuration changes are submitted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to preflight OpenClaw configuration patches or full openclaw.json files before applying changes. It helps surface concrete schema or field-format errors instead of vague validation failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation may be incomplete when jsonschema is unavailable or no live or cached schema can be loaded.

Mitigation: Install jsonschema, refresh the schema cache before important configuration changes, and treat fallback checks as basic validation only.

Risk: The helper invokes the local OpenClaw CLI to fetch schema data and caches that schema under the user's home directory.

Mitigation: Run it only in a trusted OpenClaw environment and review local cache location and permissions if configuration data is sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/halfmoon82/skills/config-preflight-validator)
- [SKILL.md](artifact/SKILL.md)
- [config-preflight-validator.py](artifact/scripts/config-preflight-validator.py)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Plain text and terminal output with validation errors or pass/fail status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cache schema data under the user's OpenClaw workspace and may fall back to limited built-in checks when jsonschema or schema data is unavailable.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
