## Description: <br>
Runs a script-backed AI C-Suite strategic debate for SaaS teams, producing structured debate rounds, a Chief-of-Staff brief, and a CEO decision with action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Founders, operators, and SaaS teams use this skill to structure strategic decisions on product, engineering, pricing, go-to-market, hiring, operations, or competitive response. It turns a decision topic and company context into a role-based executive debate, CEO brief, and action-oriented decision record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated strategy recommendations can be incomplete or unsuitable for a specific business context. <br>
Mitigation: Review the CEO decision, tradeoffs, confidence, reversibility, and review trigger before acting on the output. <br>
Risk: The company YAML and generated markdown may contain sensitive business information. <br>
Mitigation: Review or replace the sample company config, avoid putting secrets into YAML or generated markdown, and choose output paths carefully in shared workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clarezoe/ai-csuite) <br>
- [README.md](README.md) <br>
- [AI C-Suite Framework PRD](ai-csuite-framework-prd.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown decision artifact with local Python command workflow and YAML company context] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a company context file and writes decision output to a local markdown file.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
