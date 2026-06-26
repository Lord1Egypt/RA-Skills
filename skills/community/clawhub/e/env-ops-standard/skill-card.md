## Description: <br>
Safe .env Manager helps agents perform key-first .env CRUD operations with secret-safe defaults for troubleshooting missing environment keys and configuration failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pioneer-weirdo](https://clawhub.ai/user/pioneer-weirdo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to list, check, add, update, remove, lint, and validate .env keys without exposing secret values. It is intended for troubleshooting missing keys, authentication failures, and configuration drift while keeping writes deliberate and auditable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally reads and modifies local .env files, so incorrect set or unset operations can disrupt application configuration. <br>
Mitigation: Start with key-only discovery and existence checks, approve write operations deliberately, use dry-run previews when uncertain, and run lint or doctor after changes. <br>
Risk: Secrets can be exposed if users paste real values into visible command examples, chat transcripts, or logs. <br>
Mitigation: Provide secret values through stdin or another secure channel, avoid printing raw values, and keep examples redacted. <br>
Risk: Timestamped backups may retain previous sensitive values after credential rotation. <br>
Mitigation: Use the configured backup retention controls and periodically prune backup files after rotating sensitive values. <br>


## Reference(s): <br>
- [ENV Key Naming & Comment Standard](references/env-key-standard.md) <br>
- [Example envsafe policy](references/policy.example.json) <br>
- [ClawHub release page](https://clawhub.ai/pioneer-weirdo/env-ops-standard) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Secret values are redacted by default; write operations should be followed by lint or doctor validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
