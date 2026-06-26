## Description: <br>
Process code review feedback critically by checking correctness before acting, pushing back on incorrect suggestions, and avoiding performative agreement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill when responding to PR or MR review comments, triaging reviewer suggestions, deciding when to implement changes, and drafting evidence-based pushback or clarification requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to inspect PR review threads or reply through GitHub tooling in repositories where that access may not be authorized. <br>
Mitigation: Use it only in projects where repository and GitHub review access are permitted, and review proposed replies or changes before posting or resolving conversations. <br>
Risk: Incorrect triage may dismiss valid review feedback or accept a flawed suggestion. <br>
Mitigation: Require evidence such as code references, test output, documentation, or reproduction steps before accepting or declining feedback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iliaal/compound-eng-receiving-code-review) <br>
- [Headless Mode](references/headless-mode.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with structured triage text and inline shell commands when GitHub PR replies are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Headless mode can return AUTO-FIX, AUTO-DECLINE, ESCALATE, and PRIOR FEEDBACK triage sections.] <br>

## Skill Version(s): <br>
4.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
