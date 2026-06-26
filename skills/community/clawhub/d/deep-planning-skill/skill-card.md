## Description: <br>
Deep Planning Skill helps agents plan complex architecture, algorithm, system-design, logic, and research tasks by comparing a baseline plan with domain-shifted alternatives and producing a self-contained execution blueprint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobertneek](https://clawhub.ai/user/bobertneek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, researchers, and agent operators use this skill when ordinary linear planning is likely to miss constraints or produce brittle designs. It guides an agent through baseline planning, structural abstraction, isolated domain questioning, comparison, hardening, and final blueprint generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Complex planning runs may add latency and token cost because the skill can ask the agent to use an isolated subagent. <br>
Mitigation: Use the skill for complex, novel, or high-risk planning tasks rather than routine bug fixes, simple refactors, factual lookup, or straightforward implementation. <br>
Risk: The planning benefit depends on keeping the Domain Questioner isolated from source-domain context. <br>
Mitigation: Provide the Domain Questioner only the selected domain, the domain-native problem statement, and its role payload; avoid repo access, source terminology, file paths, and project context unless external reference is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bobertneek/deep-planning-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown execution blueprint with structured sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include milestones, validation checks, recovery steps, progress logs, decision logs, and a final receipt.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
