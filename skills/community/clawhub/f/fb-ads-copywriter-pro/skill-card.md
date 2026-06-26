## Description: <br>
Generates Cantonese Facebook ad copy variants with A/B testing suggestions, audience analysis, and campaign guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chungvic](https://clawhub.ai/user/chungvic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, agencies, and operators use this skill to turn product details or client questionnaire inputs into Facebook ad copy, A/B test plans, audience segments, and campaign recommendations. <br>

### Deployment Geography for Use: <br>
Global; examples and defaults are oriented toward Hong Kong Cantonese marketing copy. <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports an embedded fallback GLM API key. <br>
Mitigation: Use a user-provided GLM_API_KEY, remove reliance on any bundled fallback key, and rotate any exposed credential before production use. <br>
Risk: Business, questionnaire, or customer content may be sent to external GLM, email, or Telegram services. <br>
Mitigation: Avoid confidential client data unless approved for those providers, and document consent and data-flow expectations before use. <br>
Risk: Optional Resend and Telegram delivery can send generated material to unintended recipients. <br>
Mitigation: Enable delivery integrations only after confirming recipient addresses, chat IDs, and client consent. <br>
Risk: The security guidance recommends clearer dependency and privacy controls. <br>
Mitigation: Prefer a release with pinned dependencies and explicit privacy notices, or review and pin dependencies before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chungvic/fb-ads-copywriter-pro) <br>
- [API documentation](references/api-docs.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON delivery package with ad copy, test recommendations, audience analysis, and campaign guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate six ad variants, A/B test combinations, audience segments, budget guidance, and optional email or Telegram delivery.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
