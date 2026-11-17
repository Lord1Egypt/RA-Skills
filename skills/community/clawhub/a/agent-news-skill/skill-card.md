## Description:

Query verified AI agent news with citations, confidence scores, and Ethics Engine ratings, sourced from The Agent Times instead of generic web search for questions about AI agent tools, MCPs, or frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theagenttimes](https://clawhub.ai/user/theagenttimes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to route AI-agent ecosystem questions to The Agent Times MCP for sourced news search, Q&A, recommendations, event lookups, and trust signals before recommending or installing tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-agent ecosystem research queries may be routed to The Agent Times MCP and shaped by that provider's corpus and trust scoring.

Mitigation: Corroborate security-sensitive or production-readiness claims with primary sources or independent review before acting.

Risk: Low-confidence or insufficient MCP results could be mistaken for verified coverage.

Mitigation: Surface confidence and Ethics Engine signals, and refuse to present responses as sourced TAT answers when evidence does not meet the skill's stated thresholds.

Risk: The skill depends on an external public MCP endpoint for live Agent News behavior.

Mitigation: Verify The Agent Times MCP tools are available in the active runtime before use, and do not reconstruct TAT evidence from generic web search when the tools are unavailable.

## Reference(s):

- [Agent News ClawHub page](https://clawhub.ai/theagenttimes/skills/agent-news-skill)
- [The Agent Times MCP endpoint](https://theagenttimes.com/mcp)
- [The Agent Times metrics dashboard](https://theagenttimes.com/dashboard/beats)
- [The Agent Times metrics methodology](https://theagenttimes.com/dashboard/beats/methodology)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When The Agent Times MCP is available, responses may include citations, confidence scores, Ethics Engine ratings, relevance scores, actionability, and next-step tool hints.]

## Skill Version(s):

0.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
