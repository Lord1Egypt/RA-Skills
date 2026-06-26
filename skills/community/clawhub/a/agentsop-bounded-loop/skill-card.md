## Description: <br>
Universal discipline for any LM-driven loop: agent retries, plan-act-observe flows, multi-agent handoffs, optimizer passes, and test-fix cycles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentsope](https://clawhub.ai/user/agentsope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, review, and repair cyclic LM-agent workflows so retries, handoffs, tool loops, and test-fix cycles terminate with explicit counters, progress checks, budgets, and escalation paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Framework examples may be applied without adapting shared loop state, human escalation, or timeout budgets to the user's application. <br>
Mitigation: Review the proposed loop bounds, escalation branch, and timeout or token budgets against the target workflow before deployment. <br>
Risk: The skill provides guidance for control flow patterns but does not validate the user's implementation. <br>
Mitigation: Add tests that inject permanent failures and assert termination, stagnation handling, and final-state preservation. <br>


## Reference(s): <br>
- [R1 Source Evidence](references/R1-source-evidence.md) <br>
- [R2 Cross-Framework Comparison](references/R2-cross-framework.md) <br>
- [LangGraph GRAPH_RECURSION_LIMIT](https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT) <br>
- [LangGraph issue #6731](https://github.com/langchain-ai/langgraph/issues/6731) <br>
- [CrewAI issue #330](https://github.com/crewAIInc/crewAI/issues/330) <br>
- [Delegation ping-pong in CrewAI](https://azguards.com/technical/the-delegation-ping-pong-breaking-infinite-handoff-loops-in-crewai-hierarchical-topologies/) <br>
- [LangGraph FAQs and Gotchas](https://sumanmichael.github.io/langgraph-cheatsheet/cheatsheet/faqs-gotchas/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and framework-specific recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation guidance only; it does not execute tools or change runtime state by itself.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
