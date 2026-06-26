## Description: <br>
A Chinese-language finance and tax calculation skill that helps users estimate tax-inclusive product pricing and overall tax burden, including VAT, combined VAT/surtax/stamp/income tax, and annual tax-burden scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect required Chinese tax-calculation inputs, call 1688 finance-tax tools, and return user-facing Chinese markdown with a tax disclaimer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tax-calculation inputs, signed request metadata, and minimal usage reporting are sent to the 1688 skills gateway. <br>
Mitigation: Install only when that data flow is acceptable, and review gateway-related configuration before running or configuring the skill. <br>
Risk: The skill requires FINANCE_TAX_API_KEY and can write the key to local OpenClaw configuration or a local OpenClaw gateway. <br>
Mitigation: Use a dedicated key, avoid placing unrelated secrets in the skill directory .env or OpenClaw config, and review OPENCLAW_GATEWAY_URL before configuration. <br>
Risk: Tax estimates may be incomplete or unsuitable as final tax advice. <br>
Mitigation: Preserve the skill's required disclaimer and have users confirm results against tax authorities or qualified tax practice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-finance-tax) <br>
- [Tax calculation workflow](artifact/references/tax-calculation.md) <br>
- [Field mapping reference](artifact/references/reference.md) <br>
- [Common rules](artifact/references/common/common-rules.md) <br>
- [Common error handling](artifact/references/common/error-handling.md) <br>
- [1688 VAT calculator](https://work.1688.com/?_path_=sellerPro/zijinguanli/taxrouter&_hex_pageKey=calculatorOnlyVat&_hex_tracelog=openSkills) <br>
- [1688 combined tax calculator](https://work.1688.com/?_path_=sellerPro/zijinguanli/taxrouter&_hex_pageKey=calculatorQuadTax&_hex_tracelog=openSkills) <br>
- [1688 overall tax-burden calculator](https://work.1688.com/?_path_=sellerPro/zijinguanli/taxrouter&_hex_pageKey=calculatorOverallTax&_hex_tracelog=openSkills) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON containing success, markdown, and data fields; user-facing content is returned as Chinese markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each user-facing tax calculation response includes a disclaimer; command output should display the markdown field before any agent analysis.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact constants state 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
