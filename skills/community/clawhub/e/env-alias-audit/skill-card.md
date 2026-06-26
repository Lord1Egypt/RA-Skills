## Description: <br>
Audit .env alias groups for missing required config, conflicting values, and canonical-key drift before deploy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to audit .env-style configuration before deployment, checking required environment-variable groups, conflicting alias values, and canonical-key drift. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit output can reveal short secret values or fragments of longer secrets from .env files. <br>
Mitigation: Run the skill only in a trusted workspace and avoid sharing transcripts, logs, or reports that include audit output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/env-alias-audit) <br>
- [Publisher profile](https://clawhub.ai/user/daniellummis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and terminal output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled shell script prints per-group OK, WARN, and FAIL statuses, a summary, and nonzero exit status for strict failures.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
