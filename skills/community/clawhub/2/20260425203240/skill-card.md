## Description: <br>
OUA (OpenClaw Unified Assessment) v2.0 is an engineering-focused AI evaluation framework that combines 8 OIT capability dimensions and 5 LLI delivery dimensions across 104 Normal, Hard, and Extreme test questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rafeyu8899](https://clawhub.ai/user/rafeyu8899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, evaluators, and AI teams use this skill to run structured capability, engineering reliability, tool-use accuracy, satisfaction, and self-correction assessments for AI agents or models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes adversarial benchmark prompts and red-team style examples intended for evaluation. <br>
Mitigation: Use the prompts only in authorized testing and avoid pasting them into unrelated systems. <br>
Risk: The skill includes a local scoring script that generates reports from benchmark results. <br>
Mitigation: Review the script before running it and execute it only in an appropriate local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rafeyu8899/20260425203240) <br>
- [test-bank-v2.md](artifact/references/test-bank-v2.md) <br>
- [test-bank.md](artifact/references/test-bank.md) <br>
- [OUA v2.0 upgrade plan](artifact/OUA-v2.0-upgrade-plan.md) <br>
- [OUA v2.0 weight revision](artifact/OUA-v2.0-weight-revision.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with scoring instructions, test prompts, JSON inputs, shell commands, and generated HTML or JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces benchmark scoring reports and improvement guidance from structured test results.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
