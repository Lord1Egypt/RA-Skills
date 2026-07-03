## Description: <br>
AgentPMT Workflow Creator helps agents build, validate, publish, remix, and manage reusable multi-step AgentPMT workflow DAGs that orchestrate tools, prompts, loops, branches, and human notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
For agents that need to design or maintain AgentPMT-hosted workflow skills, including drafting workflow graphs, validating node and edge structures, publishing versioned snapshots, remixing public workflows, and managing showcase examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow publishing, draft deletion, and marketplace updates can change or remove user-visible AgentPMT assets. <br>
Mitigation: Validate workflow graphs before create, update, or publish actions; confirm destructive draft deletions and publishing intent before making changes. <br>
Risk: AgentPMT workflow prompts and attached context can transfer sensitive, secret, or regulated data to the remote workflow platform. <br>
Mitigation: Use a scoped AgentPMT token and keep secrets or regulated data out of prompts and attached context unless the user has a clear, authorized reason. <br>
Risk: Invented or stale tool identifiers can produce invalid workflows or connect the wrong marketplace tool. <br>
Mitigation: Call get_instructions and fetch_tools before authoring tool nodes, and use validate before persisting graph changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/agentpmt-workflow-creator) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/agentpmt-workflow-creator) <br>
- [AgentPMT publisher profile](https://clawhub.ai/user/agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [AgentPMT workflow plans, JSON-style action payloads, DAG node and edge definitions, validation requests, and publishing metadata.] <br>
**Output Parameters:** [Actions include get_instructions, fetch_tools, search_public, validate, create_new, fetch_existing, update_existing, publish, remix, delete, add_showcase_example, remove_showcase_example, fetch_industry_tags, attach_context, and detach_context; key parameters include workflow nodes, edges, tool product IDs, prompt definitions, branch options, context document IDs, skill IDs, visibility, industry tags, and showcase examples.] <br>
**Other Properties Related to Output:** [The skill uses AgentPMT-hosted remote tool calls and expects agents to fetch real tool identifiers, validate graph structure before persistence, avoid graph cycles, and use for_each nodes for iteration.] <br>

## Skill Version(s): <br>
1.0.1 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
