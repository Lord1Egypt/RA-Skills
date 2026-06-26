## Description: <br>
Your AI Founder Partner for building and scaling startups -- diagnose your stage, run hypothesis experiments, make pricing decisions, design growth loops, and ship weekly execution reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neiljo-gy](https://clawhub.ai/user/neiljo-gy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External founders and startup teams use this founder persona pack to diagnose stage and bottlenecks, design 7-day experiments, make pricing and growth decisions, and produce weekly continue/stop/pivot reviews with human approval gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad command, file, network, social, onchain, and purchase-related authority that is not tightly scoped to its stated workflows. <br>
Mitigation: Install and run it only in an agent runtime where Bash, curl/WebFetch, file writes, openclaw commands, onchain actions, and purchase-related actions require explicit human approval and tight scoping. <br>
Risk: Founder guidance may affect financing, equity, legal, employment, budget, brand, or other irreversible business decisions. <br>
Mitigation: Keep human approval gates for financing, equity, legal, hiring or firing, high-risk budget, brand, and irreversible external commitments. <br>
Risk: Optional community integrations may expand behavior beyond the core skill package. <br>
Mitigation: Keep optional integrations disabled until each integration is separately vetted and approved for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/neiljo-gy/entrepreneur-skill) <br>
- [stage-diagnosis](references/stage-diagnosis.md) <br>
- [hypothesis-lab](references/hypothesis-lab.md) <br>
- [pricing-decision](references/pricing-decision.md) <br>
- [growth-loop-design](references/growth-loop-design.md) <br>
- [weekly-founder-review](references/weekly-founder-review.md) <br>
- [agent-org-governance](references/agent-org-governance.md) <br>
- [metrics-baseline](references/metrics-baseline.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown guidance and reports, with optional JSON metric inputs and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The weekly review script reads structured JSON metrics and writes a Markdown report.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
