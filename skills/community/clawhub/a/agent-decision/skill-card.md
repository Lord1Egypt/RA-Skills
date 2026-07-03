## Description: <br>
Agent开发决策辅助系统 analyzes an AI agent product idea across technical selection, competition, market outlook, industry fit, feasibility, stability, cost, and promotion strategy, then generates an interactive HTML feasibility decision report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and founders use this skill to evaluate AI agent product ideas before implementation. It helps compare LLM and agent framework options, assess market and competitive context, estimate costs, identify stability risks, and produce a decision report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation phrases may cause the skill to run for requests that only loosely match agent feasibility analysis. <br>
Mitigation: Narrow trigger wording and require confirmation before performing web research or file-writing actions. <br>
Risk: Generated active HTML may include untrusted report content. <br>
Mitigation: Open generated reports only from trusted inputs, HTML-escape report content, and review files before sharing or hosting them. <br>
Risk: Report output paths could be directed outside the intended workspace. <br>
Mitigation: Constrain output paths to a safe workspace and review the destination before writing the HTML report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/agent-decision) <br>
- [Project homepage](https://github.com/bettermen/agent-decision) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated interactive HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports include active HTML and Canvas-based visualization; Python is required for the report generator.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
