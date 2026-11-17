## Description: <br>
Focus Flow Optimizer Free guides an agent to diagnose focus bottlenecks and maintain a local productivity system for energy management, time blocking, task prioritization, and reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill with a tool-capable agent to organize personal productivity in a local focus-flow workspace, diagnose bottlenecks, plan time blocks, prioritize daily and weekly work, and review progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create or update local Markdown files under ~/focus-flow, including profile.md entries about long-term preferences or personal constraints. <br>
Mitigation: Approve write operations only after reviewing the proposed changes, with extra scrutiny for profile.md updates. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/focus-flow-optimizer-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command snippets and local Markdown file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update purpose-related Markdown files under ~/focus-flow after user review and approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
