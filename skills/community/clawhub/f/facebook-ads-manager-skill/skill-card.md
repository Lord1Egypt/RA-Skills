## Description: <br>
Orquestra planejamento, operacao e otimizacao de campanhas Meta Ads usando MCP tools com seguranca de escrita, cobertura completa de endpoints e carregamento progressivo de contexto. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamneves](https://clawhub.ai/user/williamneves) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External marketers, media buyers, and agents use this skill to plan, launch, diagnose, optimize, and operate Meta Ads campaigns through MCP tools with explicit controls for write actions, budgets, audiences, and rollback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide powerful Meta Ads write actions, including creates, updates, deletes, budget changes, and audience uploads. <br>
Mitigation: Use least-privilege Meta/MCP access, verify the ad account ID, create new campaigns, ad sets, and ads in PAUSED status, and require explicit approval for writes, deletes, budget changes, and audience uploads. <br>
Risk: Budget or targeting changes can create financial loss or delivery instability if applied too aggressively. <br>
Mitigation: Collect baseline insights, make incremental monitored changes, document expected impact, and define rollback conditions before execution. <br>
Risk: CRM audience uploads can involve personal data and consent obligations. <br>
Mitigation: Confirm user consent before uploading CRM data to Meta and delimit the audience scope and purpose before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/williamneves/facebook-ads-manager-skill) <br>
- [Project Homepage](https://github.com/williamneves/facebook-ads-manager-skill) <br>
- [Tools Index](artifact/references/tools-index.md) <br>
- [Safety Policy](artifact/references/safety-policy.md) <br>
- [Targeting Reference](artifact/references/targeting-reference.md) <br>
- [Diagnostics Reference](artifact/references/diagnostics-reference.md) <br>
- [Scaling Rules](artifact/references/scaling-rules.md) <br>
- [Creative Frameworks](artifact/references/creative-frameworks.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with exact MCP tool names, parameters, operational plans, action summaries, IDs, risk notes, and rollback steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill routes context progressively through workflow, checklist, and reference files to avoid loading unnecessary material.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and CHANGELOG; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
