## Description: <br>
Provides compliant summaries of Aliyun public product specifications, pricing, billing trends, and service announcements without performing account operations or handling sensitive data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codenova58](https://clawhub.ai/user/codenova58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and cloud operators use this skill to summarize Aliyun public pages and logged-in console views for product specs, pricing, billing overviews, and service announcements. It is intended for non-sensitive summary work, not account changes, access bypass, paid service actions, or credential handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user could expose Aliyun credentials, account IDs, billing details, or other sensitive console data while requesting summaries. <br>
Mitigation: Keep credentials and sensitive identifiers out of prompts and outputs, redact account-specific values, and summarize only non-sensitive visible information. <br>
Risk: Console automation could be mistaken for permission to perform account-changing or paid service actions. <br>
Mitigation: Use the skill for summaries only; do not make API calls, bypass access controls, or perform account operations through this skill. <br>
Risk: Repeated page access could conflict with Aliyun platform limits or account policies. <br>
Mitigation: Apply rate limits, respect platform access restrictions, and stop if Aliyun presents throttling or access warnings. <br>


## Reference(s): <br>
- [Aliyun Homepage](https://www.aliyun.com/) <br>
- [Aliyun Console](https://home.console.aliyun.com/) <br>
- [Aliyun Documentation Center](https://help.aliyun.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/codenova58/aliyun) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or concise text summaries with source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No account operations, API calls, credential collection, or sensitive-data storage.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
