## Description: <br>
Indestructible audit logs for agent actions, stored in TiDB Zero. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilyjazz](https://clawhub.ai/user/lilyjazz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use Black Box to log and retrieve agent actions, errors, and reasoning traces in a TiDB-backed cloud database for audit and debugging workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent action, error, and possible reasoning content may be sent to a TiDB-backed cloud database. <br>
Mitigation: Prefer least-privilege user-provided TiDB credentials and avoid logging secrets, private prompts, or sensitive data. <br>
Risk: The database connection string is cached in ~/.openclaw_black_box_dsn. <br>
Mitigation: Protect or remove the cached DSN file and rotate database credentials if it may have been exposed. <br>
Risk: The skill describes audit logs as indestructible, but the security evidence says durability and compliance guarantees are overstated. <br>
Mitigation: Do not rely on this as tamper-proof or permanent compliance evidence without additional retention, access-control, and integrity controls. <br>


## Reference(s): <br>
- [ClawHub black-box release](https://clawhub.ai/lilyjazz/black-box) <br>
- [TiDB Zero provisioning endpoint](https://zero.tidbapi.com/v1alpha1/instances) <br>


## Skill Output: <br>
**Output Type(s):** [json, shell commands, configuration] <br>
**Output Format:** [JSON status responses and log records from command-line execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, curl, pymysql, and TiDB connection settings or the skill's auto-provisioning fallback.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
