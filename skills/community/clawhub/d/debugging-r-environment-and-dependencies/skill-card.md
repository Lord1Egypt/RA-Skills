## Description: <br>
Diagnose and fix R environment issues, including package installation failures, dependency conflicts, system library problems, renv errors, and Bioconductor version mismatches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JackKuo666](https://clawhub.ai/user/JackKuo666) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and data scientists use this skill to diagnose and repair R project environments, package installation failures, dependency conflicts, system library issues, renv problems, and Bioconductor mismatches so scripts can run reproducibly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested fixes can change system packages, R libraries, project lockfiles, PATH settings, permissions, or project environments. <br>
Mitigation: Review and explicitly approve privileged commands, package reinstalls, renv restore or update actions, lockfile rebuilds, library cleanup, and PATH or permission changes before execution. <br>
Risk: Environment repair steps may overwrite or replace reproducibility artifacts such as renv.lock or project library state. <br>
Mitigation: Back up important project files, especially renv.lock and project-specific configuration, before applying repair steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JackKuo666/debugging-r-environment-and-dependencies) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell, R, and configuration commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OS-specific package-manager commands, R package installation commands, renv repair steps, and verification checks.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
