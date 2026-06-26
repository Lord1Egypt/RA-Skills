## Description: <br>
Distributes ecommerce advertising budget across channels and campaigns based on ROAS targets, funnel stage, seasonality, and current performance data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ecommerce sellers, growth marketers, agencies, and brand teams use this skill to turn fixed monthly or quarterly ad budgets into channel, campaign, funnel-stage, and seasonal allocation plans with triggers for reallocating spend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may include confidential campaign exports, margin data, or customer-level metrics while preparing an allocation plan. <br>
Mitigation: Use aggregated channel metrics when possible and avoid pasting confidential or customer-level data into the agent session unless that use is acceptable for the organization. <br>
Risk: Allocation recommendations depend on the freshness and quality of spend, revenue, ROAS, audience, and seasonality inputs. <br>
Mitigation: Confirm the input checklist before planning and label thin, stale, or missing data as low confidence in the final allocation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leooooooow/aes-ad-budget-allocator) <br>
- [Input Checklist for Budget Allocation](references/input-checklist.md) <br>
- [Modeling Marginal ROAS](references/marginal-roas-model.md) <br>
- [Seasonality Playbook](references/seasonality-playbook.md) <br>
- [Ad Budget Allocation Output Template](references/output-template.md) <br>
- [Allocation Quality Checklist](assets/quality-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown allocation plan with tables, assumptions, triggers, and review checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only skill; no scripts, credential handling, or hidden execution behavior found in security evidence.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
