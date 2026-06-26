## Description: <br>
Daily-updated intelligence on what's happening across 16 areas of AI, exposed through 12 MCP tools that let an agent query signals, trends, blockers, predictions, alerts, and wiki content from public Eigen Terminal data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawkatdidar](https://clawhub.ai/user/shawkatdidar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and AI-focused teams use this skill to let an agent pull current AI landscape intelligence and summarize only the signals relevant to the user's work. It supports daily briefs, topic deep dives, cause-and-effect analysis, trend review, blocker review, speed metrics, predictions, search, page reads, product updates, and breaking-update checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public AI intelligence over the network from terminal.clawlab.dev. <br>
Mitigation: Install only in environments where a Node MCP server making read-only requests to that domain is acceptable. <br>
Risk: The skill asks the agent to use local project or conversation context to decide which intelligence is relevant. <br>
Mitigation: Ask the agent before it inspects local context, and review generated briefs for relevance and disclosure before sharing. <br>
Risk: The current JavaScript artifact may need a packaging or syntax fix before it runs correctly. <br>
Mitigation: Smoke test the MCP server after installation before relying on it in a production workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shawkatdidar/eigen-ai-terminal) <br>
- [Eigen AI Terminal public homepage](https://terminal.clawlab.dev) <br>
- [Eigen AI Terminal public data endpoint](https://terminal.clawlab.dev/data) <br>
- [Eigen AI Terminal public wiki endpoint](https://terminal.clawlab.dev/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted text returned from MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are synthesized from public Eigen Terminal data; the agent is instructed to avoid supplementing tool responses with training knowledge.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
