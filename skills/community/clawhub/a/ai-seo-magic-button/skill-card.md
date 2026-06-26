## Description: <br>
AI SEO Magic Button audits a provided site for AEO/GEO readiness and produces a ready-to-run AI-SEO plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[automatelab](https://clawhub.ai/user/automatelab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and site operators use this skill to audit sites they own or are authorized to scan, identify AEO/GEO and citation gaps, and produce a prioritized plan for follow-up agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill crawls a target site and processes page content through SEO and citation helper engines. <br>
Mitigation: Run it only on sites you own or are authorized to scan, and avoid private or regulated content unless approved. <br>
Risk: The generated plan may contain inaccurate or unsuitable SEO recommendations. <br>
Mitigation: Review plan.json and plan.md before executing changes, starting with critical and high-priority items. <br>
Risk: The workflow spawns helper engines and writes local audit plan files. <br>
Mitigation: Run it in a trusted workspace and inspect generated files before using them for downstream edits. <br>


## Reference(s): <br>
- [AI SEO Magic Button on ClawHub](https://clawhub.ai/automatelab/ai-seo-magic-button) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance plus local plan.json and plan.md files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an actionable plan rather than applying direct site edits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
