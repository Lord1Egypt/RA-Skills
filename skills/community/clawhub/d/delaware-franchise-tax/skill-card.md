## Description: <br>
Guides users through Delaware annual franchise tax calculations, eCorp portal filing steps, payment handoff, receipt saving, and reminders for C-Corps and LLCs/LPs/GPs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External founders, operators, and their agents use this skill to calculate Delaware franchise tax, prepare annual report inputs, follow official eCorp filing steps, and preserve confirmation records. <br>

### Deployment Geography for Use: <br>
United States (Delaware) <br>

## Known Risks and Mitigations: <br>
Risk: Automation may affect a live government filing portal, including CAPTCHA handling and portal navigation. <br>
Mitigation: Use the skill primarily as a checklist and filing guide; keep CAPTCHA solving, final review, submission, and payment manual. <br>
Risk: The workflow can involve sensitive credentials, banking details, credit card details, and payment decisions. <br>
Mitigation: Do not ask the agent to collect or enter payment details; the user should enter card or ACH information directly and confirm the final filing. <br>
Risk: Optional banking or cloud-storage connectors could expose more account or document access than the task requires. <br>
Mitigation: Avoid connecting broad banking or cloud-storage access unless strictly needed, and use the narrowest available permissions. <br>
Risk: Incorrect entity data, asset figures, or share counts can produce an inaccurate tax estimate or filing. <br>
Mitigation: Verify calculations against Delaware official sources and user records before filing; consult a tax professional for entity-specific advice. <br>


## Reference(s): <br>
- [Tax Calculation Reference](reference/tax-calculation.md) <br>
- [Filing Instructions](reference/filing-instructions.md) <br>
- [Delaware Franchise Tax FAQ](reference/faq.md) <br>
- [Delaware eCorp Portal Playwright Notes](reference/ecorp-portal-playwright-notes.md) <br>
- [Connectors](CONNECTORS.md) <br>
- [Delaware Division of Corporations Pay Taxes](https://corp.delaware.gov/paytaxes/) <br>
- [Delaware Franchise Tax Calculator](https://corp.delaware.gov/frtaxcalc/) <br>
- [Delaware eCorp Filing Portal](https://icis.corp.delaware.gov/ecorp/logintax.aspx) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with calculation tables and occasional shell or Playwright snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided entity, stock, asset, officer/director, registered-agent, and payment-related information; payment details remain user-entered.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
