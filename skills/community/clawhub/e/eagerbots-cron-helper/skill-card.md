## Description: <br>
Explain, generate, and validate cron expressions, convert between plain English schedules and cron syntax, and show next run times. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josephflu](https://clawhub.ai/user/josephflu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and automation authors use this skill to understand existing cron expressions, generate schedules from natural language, validate cron syntax, and preview upcoming run times. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to run a local Python helper through uv, and first use may download Python dependencies. <br>
Mitigation: Review the command before execution and run it only in a trusted workspace where local helper execution and dependency installation are acceptable. <br>
Risk: Six-field cron support should be verified because the security guidance notes that included documentation and validation logic are mostly 5-field oriented. <br>
Mitigation: Validate 6-field expressions with the target scheduler before relying on generated schedules in production. <br>


## Reference(s): <br>
- [Cron Syntax Quick Reference](references/cron-syntax.md) <br>
- [OpenClaw Cron Documentation](https://docs.openclaw.com/cron) <br>
- [Publisher Repository Homepage](https://github.com/josephflu/clawhub-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized console output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke a local Python helper through uv; next-run previews are time-dependent.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
