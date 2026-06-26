## Description: <br>
Qualify trade show leads from badge scans, booth notes, or voice memos into scored CRM-ready cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weilun88313](https://clawhub.ai/user/weilun88313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Exhibitor sales and marketing teams use this skill during or shortly after trade shows to convert badge scans, booth notes, and voice memos into conservative lead qualification cards for follow-up and CRM handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lead inputs can contain personal data from badges, business cards, emails, and booth notes. <br>
Mitigation: Only process data the user is authorized to use, minimize contact details, and confirm applicable privacy and marketing rules before follow-up or CRM use. <br>
Risk: Badge-only or ambiguous notes can be mistaken for stronger buying intent than the evidence supports. <br>
Mitigation: Keep unknown fields explicit, avoid fabricating needs or urgency, and review the generated tier before using it for sales follow-up. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/weilun88313/badge-qualifier) <br>
- [Artifact README](README.md) <br>
- [MEDICA booth lead example](examples/medica-booth-lead.md) <br>
- [Skill homepage declared in artifact](https://github.com/LensmorOfficial/trade-show-skills/tree/main/badge-qualifier) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown lead qualification cards with optional batch summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Hot/Warm/Cold lead tiers, contact fields, qualification rationale, recommended next step, unknowns, and a required footer.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
