## Description: <br>
Orchestrates the continuous learning of new skills from arXiv papers by fetching papers, extracting code or skills, testing them, and solidifying validated work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run a learning cycle that finds new arXiv papers, extracts candidate skills, runs generated tests, and records validated skill work in the workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute generated smoke-test shell commands. <br>
Mitigation: Require manual approval and review of any generated smoke-test command before execution. <br>
Risk: The skill can persist generated skill work and learned-paper records in the workspace. <br>
Mitigation: Review generated skills before committing or enabling automatic hourly runs. <br>
Risk: The workflow depends on sibling arxiv-paper-reviews and arxiv-skill-extractor modules. <br>
Mitigation: Review and pin those sibling modules before using this skill in an automated workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanng-ide/arxiv-skill-learning) <br>
- [Publisher profile](https://clawhub.ai/user/wanng-ide) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON status with generated skill files and smoke-test command execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write learned-paper records and generated skill artifacts in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
