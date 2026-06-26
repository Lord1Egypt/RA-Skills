## Description: <br>
Lightweight Garmin Connect skill that uses the clawhealth Python package to sync health data into local SQLite and expose JSON-friendly commands for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ernestyu](https://clawhub.ai/user/ernestyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to connect Garmin Connect account data to local SQLite storage and expose health, sleep, activity, HRV, training, and body-composition data as JSON-friendly agent commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Garmin credentials, session tokens, raw health payloads, and a local health database. <br>
Mitigation: Use the password-file setup with restrictive permissions and keep .env files, password files, session tokens, raw payloads, and the local database out of Git, shared folders, and untrusted backups. <br>
Risk: The skill depends on an external clawhealth CLI package path that the security evidence flags for careful review. <br>
Mitigation: Install only if the clawhealth package and maintainer are trusted, prefer a version-pinned and reviewed dependency path, and verify which clawhealth executable will run. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ernestyu/clawhealth-garmin) <br>
- [ClawHealth project homepage](https://github.com/ernestyu/clawhealth) <br>
- [Skill README](artifact/README.md) <br>
- [Skill specification](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON command results and Markdown setup guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include locally stored Garmin Connect health data surfaced through the clawhealth CLI.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata, SKILL.md frontmatter, manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
