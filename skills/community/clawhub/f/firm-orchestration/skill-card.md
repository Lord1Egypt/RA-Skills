## Description: <br>
Pyramid multi-agent orchestration for OpenClaw routes objectives from a CEO agent through department, service, and employee sessions, then collects, validates, merges, and returns the final deliverable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use this skill to coordinate multi-agent OpenClaw work by delegating objectives across department-style sessions and merging returned outputs into a final deliverable. It is suited for structured implementation, audit, planning, and release workflows that need parallel task execution with documented convergence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Multi-agent fan-out can propagate broad objectives or sensitive context across spawned sessions. <br>
Mitigation: Keep objectives and constraints scoped, avoid secrets in delegated task text, and monitor spawned sessions on larger runs. <br>
Risk: Generated commits, draft PRs, reports, or recommendations may be incomplete or unsuitable for direct production use. <br>
Mitigation: Review all commits, draft PRs, and final deliverables before use or merge, and keep engineering PRs in review until validated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/firm-orchestration) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or task deliverables according to delivery_format, including a run summary and human-validation disclaimer.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate multiple OpenClaw sessions, accept partial results after a deadline, and require human review before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
