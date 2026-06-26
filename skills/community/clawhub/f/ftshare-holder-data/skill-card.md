## Description: <br>
Queries A-share shareholder, shareholder-count, share-change, and equity-pledge data from market.ft.tech for individual stocks or market-wide pledge summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shawn92](https://clawhub.ai/user/Shawn92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve A-share top-holder, floating-holder, shareholder-count, shareholder-change, and equity-pledge data for stock analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs bundled Python scripts and sends requested stock symbols to market.ft.tech. <br>
Mitigation: Install only if this network request pattern is acceptable for the deployment environment. <br>
Risk: Returned financial data may be incomplete, delayed, or unsuitable as investment advice. <br>
Mitigation: Treat results as informational and verify material decisions against authoritative financial sources. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Shawn92/ftshare-holder-data) <br>
- [market.ft.tech API host](https://market.ft.tech) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON data returned by Python command-line helpers, usually summarized by the agent as text or tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only market data queries; stock-code requests are sent to market.ft.tech.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
