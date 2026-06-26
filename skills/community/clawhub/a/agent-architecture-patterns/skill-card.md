## Description: <br>
AI Agent architecture patterns library with 10 patterns for single and multi-agent systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banxian87](https://clawhub.ai/user/banxian87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as reference material for selecting and implementing single-agent and multi-agent architecture patterns, including ReAct, Reflection, Plan-and-Solve, Tree of Thoughts, Manager-Worker, Peer-to-Peer, Hierarchical, Market-Based, and Pipeline designs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes executable examples and agent/tool patterns that the security scan marked for review before installation. <br>
Mitigation: Install it as reference material, review copied code, and run local security checks before adapting examples into production systems. <br>
Risk: Some examples use unsafe dynamic evaluation for calculator-style behavior. <br>
Mitigation: Replace eval-style calculation with a safe math parser or a constrained, reviewed calculation service. <br>
Risk: Model-selected tool calls and file access patterns may be under-scoped if copied directly. <br>
Mitigation: Add approval gates, policy checks, and path allowlists before enabling tool calls or filesystem access. <br>
Risk: Prompts, code, credentials, or personal data could be exposed if examples are connected to external LLM or search services without review. <br>
Mitigation: Avoid sending confidential data to external services unless approved by the deployment owner and covered by data-handling controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/banxian87/agent-architecture-patterns) <br>
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629) <br>
- [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.11366) <br>
- [Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091) <br>
- [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601) <br>
- [CrewAI](https://github.com/joaomdmoura/crewAI) <br>
- [AutoGen](https://github.com/microsoft/autogen) <br>
- [LangChain](https://github.com/langchain-ai/langchain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes architecture pattern descriptions, implementation examples, and test or run commands; copied code should be reviewed and hardened before use.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
