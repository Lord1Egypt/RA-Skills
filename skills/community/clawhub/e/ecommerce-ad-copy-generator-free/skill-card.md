## Description: <br>
Free basic version of ecommerce ad copy generator. Generates 3 ad copies from product info, and reserves premium upgrade hooks for 10-copy batch generation and A/B variants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wingogx](https://clawhub.ai/user/wingogx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External ecommerce sellers and marketing operators use this skill to generate three short ad copy variants for Facebook, Google, and TikTok from product names, selling points, and target audiences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may follow a premium payment link without confirming that the domain and publisher are expected. <br>
Mitigation: Verify the payment domain and publisher before following premium links. <br>
Risk: Future billing integration could expose or misuse SkillPay credentials if configured casually. <br>
Mitigation: Keep SkillPay API keys in environment variables and do not enable charge endpoints unless the billing flow is clearly documented and explicitly approved. <br>


## Reference(s): <br>
- [SkillPay API Contract](references/skillpay-api-contract.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wingogx/ecommerce-ad-copy-generator-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON containing generated ad copy objects and upgrade guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces three free ad copy variants; premium tier requests return upgrade guidance rather than automatic charging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
