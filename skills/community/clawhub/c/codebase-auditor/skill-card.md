## Description: <br>
Scans a project directory and generates a JSON inventory of key configuration, credential, CI/CD, and database files for backup planning before deployment or migration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ink5725](https://clawhub.ai/user/ink5725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill before deployment, migration, or infrastructure changes to identify important project settings, credential-related filenames, and environment configuration that should be considered for backup planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated inventory can expose sensitive project structure through paths and filenames for environment, key, or service-account files. <br>
Mitigation: Keep the generated JSON private, restrict access to the output directory, and avoid sharing the inventory outside trusted backup or migration workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ink5725/codebase-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/ink5725) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Console text plus a JSON file inventory] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated inventory contains file paths, file types, importance levels, descriptions, project path, scan timestamp, and counts; it does not include file contents.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
