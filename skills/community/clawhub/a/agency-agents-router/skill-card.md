## Description: <br>
Orchestrates configured OpenClaw agents by classifying tasks, resolving ambiguity, selecting suitable agents, planning execution, and aggregating results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[staok](https://clawhub.ai/user/staok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route natural-language tasks from the main agent to installed specialist agents. It supports single-agent, parallel, sequential, and DAG-style orchestration for research, engineering, content, product, business, and audit workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated tasks may share user task context with multiple installed sub-agents. <br>
Mitigation: Use the skill only when multi-agent routing is intended, review installed agents before use, and avoid delegating sensitive context unless each selected agent is appropriate for that data. <br>
Risk: The router depends on separately installed third-party agent definitions and an accurate local agent index. <br>
Mitigation: Install and review the agent package first, then verify that agents appear in the local OpenClaw configuration before orchestration. <br>
Risk: Factual or time-sensitive workflows may rely on live web research by the orchestrator or sub-agents. <br>
Mitigation: Require cited sources and dates for factual claims, and mark unverifiable items before aggregating final results. <br>


## Reference(s): <br>
- [Agency Agents Router on ClawHub](https://clawhub.ai/staok/agency-agents-router) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command snippets, routing decisions, execution plans, and aggregated agent results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include clarifying questions, delegated-agent prompts, and installation or verification steps for the local agent index.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
