## Description: <br>
Axiomata Skill Forge helps agents create, evaluate, improve, and prepare skills for ClawHub publication using standardized documentation, scripts, tests, and quality gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to bootstrap new skills, evaluate existing skills against quality thresholds, and prepare validated skill packages for publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives broad guidance for publishing and mutating skill files. <br>
Mitigation: Review generated or modified skills before publication, run security scans, and avoid applying changes outside the intended skill directory. <br>
Risk: Publication workflows can require a ClawHub token. <br>
Mitigation: Keep CLAWHUB_TOKEN out of prompts, logs, generated skill files, and committed artifacts. <br>
Risk: Included tests and examples reference hard-coded local skill directories and cleanup behavior. <br>
Mitigation: Run tests only in disposable or isolated skill directories until paths and cleanup boundaries are adapted for the local environment. <br>
Risk: Cluster-specific loyalty and alignment requirements may not fit general users. <br>
Mitigation: Remove or replace cluster-specific governance language before using generated skills outside that operating context. <br>


## Reference(s): <br>
- [Axiomata Skill Forge on ClawHub](https://clawhub.ai/kofna3369/axiomata-skill-forge) <br>
- [ClawHub](https://clawhub.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file creation, skill evaluation, and publication steps; review generated skills before publishing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact changelog; frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
