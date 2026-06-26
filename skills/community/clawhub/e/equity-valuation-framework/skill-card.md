## Description: <br>
Provides a decision-grade equity valuation playbook and report standard for multiples analysis, DCF, quality assessment, scenarios, margin of safety, and structured investment risk review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndtchan](https://clawhub.ai/user/ndtchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, investors, and finance-focused agents use this skill to turn already-provided financial, market, peer, macro, and news inputs into a structured equity valuation memo. It is intended for decision support with explicit assumptions, confidence levels, data gaps, scenario ranges, and risk monitoring triggers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Equity valuation outputs could be mistaken for personalized investment advice. <br>
Mitigation: Treat outputs as research support, preserve the skill's educational disclaimer, and require a qualified human review before acting on investment conclusions. <br>
Risk: Incomplete, stale, or inconsistent financial inputs can produce misleading fair-value ranges. <br>
Mitigation: Run the required data quality gate, disclose missing inputs early, downgrade confidence when gaps are material, and avoid precise fair-value claims when data quality is low. <br>
Risk: Portfolio or proprietary investment details may be sensitive when shared in an agent session. <br>
Mitigation: Share only data that the user is comfortable using in the session and avoid unnecessary confidential portfolio details. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ndtchan/equity-valuation-framework) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with tables, scenario analysis, sensitivity discussion, risk register, confidence rating, and disclaimer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires already-provided financial and market inputs; does not fetch data directly.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
