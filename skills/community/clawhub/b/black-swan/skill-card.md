## Description: <br>
Black Swan helps agents audit strategies, portfolios, and retrospective narratives for fat-tail exposure, hidden Gaussian assumptions, and tail-survival design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and decision-makers use this skill to stress-test plans, portfolios, and postmortems where rare high-impact events, fat tails, or hindsight narratives may distort risk judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated stress-test guidance can be over-trusted as prediction or financial advice. <br>
Mitigation: Use the output as an audit aid, review conclusions with qualified judgment, and avoid relying on it to predict specific tail events. <br>
Risk: Applying the skill to private plans, portfolios, or incidents may expose sensitive context to the agent runtime. <br>
Mitigation: Review the visible instructions before use and avoid granting access to private files, credentials, or administrative actions unless the environment is approved for that data. <br>


## Reference(s): <br>
- [Black Swan source bibliography](artifact/references/sources.md) <br>
- [Long-Term Capital Management collapse example](artifact/examples/long-term-capital-management-collapse-1998.md) <br>
- [Black Swan on ClawHub](https://clawhub.ai/deciqai/skills/black-swan) <br>
- [deciqAI](https://deciqai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit with headings, lists, and step-by-step coaching questions when appropriate.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May stop at explicit wait points during novice coaching; does not require tools, MCP servers, credentials, or shell commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
