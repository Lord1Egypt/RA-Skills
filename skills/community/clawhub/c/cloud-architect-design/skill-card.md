## Description: <br>
Cloud Architect Design helps agents produce enterprise cloud architecture guidance for multi-cloud strategy, migration planning, FinOps optimization, compliance architecture, and disaster recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, and enterprise teams use this skill to draft cloud architecture plans, migration roadmaps, cost optimization recommendations, compliance-oriented designs, and disaster recovery options across AWS, Azure, and GCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent toward shell execution or live cloud account operations. <br>
Mitigation: Install only after review, use read-only and least-privilege cloud roles by default, and require manual approval before Terraform or cloud CLI commands affect live accounts. <br>
Risk: The skill discusses real cloud credentials and deployment workflows without clear built-in safety limits. <br>
Mitigation: Keep credentials scoped to the intended task, avoid broad administrative roles, and review generated deployment or querying steps before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cloud-architect-design) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown with structured examples and optional JSON-style result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include architecture diagrams in text form, migration plans, cost estimates, compliance checklists, and command-oriented cloud operations guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
