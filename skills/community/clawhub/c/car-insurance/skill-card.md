## Description:

Guides Korean users through car tax, used-car pricing, auto-insurance estimates, claims, mandatory insurance, maintenance costs, and traffic fine questions with source-tiered Markdown responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sw326](https://clawhub.ai/user/sw326)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer Korea-focused automotive and auto-insurance questions, including car tax estimates, used-car checks, insurance quote context, claim steps, required coverage, maintenance costs, and traffic fines.

### Deployment Geography for Use:

South Korea

## Known Risks and Mitigations:

Risk: Insurance estimates, vehicle-history checks, and accident guidance may involve sensitive personal, vehicle, or incident details.

Mitigation: Ask only for the minimum details needed, avoid unnecessary age, plate, VIN-like, accident, or vehicle-history identifiers, and confirm before searches use those details.

Risk: Car tax, insurance premium, traffic fine, and claim guidance can become inaccurate when legal rates, public disclosures, or insurer criteria change.

Mitigation: Use the skill's official source tiers and disclaimers, refresh current rules or market data before giving estimates, and frame outputs as informational rather than legal or binding insurance advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sw326/skills/car-insurance)
- [Intent router](references/intent_router.md)
- [Output templates](references/output_templates.md)
- [Source tiers](references/source_tiers.md)
- [Playbook](playbook.md)
- [Korean National Law Information Center - Local Tax Act](https://www.law.go.kr/법령/지방세법)
- [Encar](https://www.encar.com)
- [KB Chachacha](https://www.kbchachacha.com)
- [Insurance Damoa](https://www.e-insmarket.or.kr)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Analysis, Shell commands]

**Output Format:** [Markdown with tables, checklists, source notes, and occasional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flash responses are always produced; deep-dive responses are used on request or for claim, maintenance, used-car, and insurance comparison intents.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
