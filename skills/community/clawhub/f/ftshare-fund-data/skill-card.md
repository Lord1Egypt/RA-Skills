## Description: <br>
Provides A-share fund data from market.ft.tech, including fund basic information, NAV history, cumulative returns, fund overviews, and supported fund symbols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawn92](https://clawhub.ai/user/shawn92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up A-share fund details, NAV history, cumulative returns, fund overviews, and supported fund symbols, then present the returned data in concise tables or summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fund lookup parameters are sent to market.ft.tech. <br>
Mitigation: Use only fund identifiers and query parameters needed for the lookup; do not enter private, account, or unrelated personal information. <br>
Risk: The skill runs included Python scripts to retrieve fund data. <br>
Mitigation: Review and scan the artifact before deployment, and run it only in an environment where outbound access to market.ft.tech is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shawn92/ftshare-fund-data) <br>
- [market.ft.tech data service](https://market.ft.tech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [JSON from Python handlers, typically summarized by the agent as tables or concise text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fund lookup parameters include institution code, return period, page, and page size.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
