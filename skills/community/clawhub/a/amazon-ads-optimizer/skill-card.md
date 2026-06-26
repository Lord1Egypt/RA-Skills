## Description: <br>
Amazon Ads Optimizer helps Amazon sellers evaluate advertising performance, apply bid guardrails, plan flywheel-based keyword bidding, generate negative-keyword recommendations, and draft short video ad scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Amazon marketplace sellers and advertising operators use this skill to turn product, lifecycle stage, ACoS limits, campaign data, and organic ranking signals into profit-focused bid, budget, keyword, and video ad recommendations. It is intended as advisory planning support and does not apply campaign changes automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bid, pause, budget, or negative-keyword recommendations could reduce sales or waste spend if applied without review. <br>
Mitigation: Review recommendations in Amazon Ads against current margins, campaign data, inventory, seasonality, and business goals before applying them. <br>
Risk: Calculator results depend on user-supplied revenue, cost, conversion, and campaign inputs. <br>
Mitigation: Verify calculator inputs against current margin and campaign records, then treat outputs as planning guidance rather than automatic decisions. <br>


## Reference(s): <br>
- [Flywheel Bid Strategy and Guardrail Framework](artifact/references/bid-strategies.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/amazon-ads-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown recommendations with optional plain-text or JSON calculator output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include ACoS, ROAS, CPC, profit-margin, bid-guardrail, keyword, budget, execution-plan, and video-script recommendations based on user-provided inputs.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
