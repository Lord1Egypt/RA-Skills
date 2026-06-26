## Description: <br>
Creates, migrates, refactors, validates, and benchmarks skills for the alicloud-skills repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and maintainers of alicloud-skills use this skill to create new skills, adapt external skills, improve trigger descriptions, add smoke tests, and run validation or benchmark workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can terminate a process already listening on the eval viewer port. <br>
Mitigation: Review helper scripts before use, avoid running the eval viewer on a port used by other work, prefer static output or a free port, and control local execution. <br>
Risk: Benchmark and optimization workflows may send or log unpublished skill prompts, eval data, and model responses through Anthropic tooling. <br>
Mitigation: Treat --results-dir logs and Anthropic API calls as sensitive, avoid using confidential inputs unless approved, and review saved artifacts before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-skill-creator) <br>
- [Schemas reference](references/schemas.md) <br>
- [Sources reference](references/sources.md) <br>
- [Anthropic skill creator reference](https://github.com/anthropics/skills/tree/main/skills/skill-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update skill files, smoke tests, validation artifacts, benchmark outputs, and reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
