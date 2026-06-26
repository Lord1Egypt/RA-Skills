## Description: <br>
Structured web research framework for agents that plan searches, evaluate sources, synthesize findings into briefs, maintain a research library, and monitor evolving topics. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[Clawdssen](https://clawhub.ai/user/Clawdssen) <br>

### License/Terms of Use: <br>
CC-BY-NC-4.0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to turn web search into structured research workflows for market research, competitor analysis, topic deep dives, and recurring monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can maintain persistent notes in a local research folder. <br>
Mitigation: Use the research folder intentionally, avoid confidential topics in shared or indexed workspaces, and review stored briefs before relying on them. <br>
Risk: Topic monitoring can repeatedly collect or update research over time. <br>
Mitigation: Keep monitoring disabled unless intentionally configured and review monitor outputs before acting on them. <br>
Risk: Generated research briefs may contain incorrect, stale, or misleading conclusions. <br>
Mitigation: Review generated briefs and cited sources before using findings for decisions. <br>


## Reference(s): <br>
- [Advanced Patterns](references/advanced-patterns.md) <br>
- [Research Assistant on ClawHub](https://clawhub.ai/Clawdssen/agentledger-research-assistant) <br>
- [The Agent Ledger](https://theagentledger.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown research briefs, monitoring notes, templates, and setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local research library files when the user configures the workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
