## Description: <br>
Query project MySQL databases with automatic SSH tunnel setup and teardown for configured database targets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zenixp](https://clawhub.ai/user/zenixp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to list configured MySQL databases and run SQL queries against selected database environments, including databases reachable only through SSH tunnels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run SQL against configured databases using credential-backed access. <br>
Mitigation: Use read-only or least-privilege database users by default and manually review any non-SELECT query before execution. <br>
Risk: Database and SSH credentials may be exposed or misapplied if production and test configurations are mixed. <br>
Mitigation: Keep production and test credentials clearly separated, prefer environment variables for passwords, and prefer SSH keys for tunnel authentication. <br>
Risk: Broad or ambiguous database matching can target the wrong database. <br>
Mitigation: Use exact database names in configuration and query commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zenixp/db-query) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Installation Guide](artifact/scripts/INSTALL.md) <br>
- [Example Configuration](artifact/scripts/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and command-line text output from MySQL queries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local Python, mysql, and optional SSH commands against user-configured database targets.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
