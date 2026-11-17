## Description: <br>
Cron Mate Free helps agents draft, explain, and validate five-field cron expressions, including common Chinese natural-language scheduling phrases and template lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and automation teams use this skill to draft new cron schedules, translate existing five-field cron expressions into Chinese explanations, validate basic syntax, and find common scheduling templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive schedule details may be processed by the surrounding agent or LLM despite examples that describe local Python execution. <br>
Mitigation: Avoid entering sensitive schedules until the publisher clarifies the processing model; use non-sensitive examples or run local validation code directly where possible. <br>
Risk: The helper covers basic five-field cron syntax and does not support advanced cron features such as L, W, #, seconds, years, or time-zone conversion. <br>
Mitigation: Review generated expressions against the target scheduler's documentation and test them before using them for production jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cron-mate-free) <br>
- [Detailed cron helper reference](artifact/references/detail.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, inline cron expressions, validation results, and Chinese schedule descriptions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on standard five-field cron expressions and local Python standard-library examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release version and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
