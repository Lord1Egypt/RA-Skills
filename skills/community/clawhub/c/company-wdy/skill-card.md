## Description: <br>
Queries WenDaoYun company records through the WenDaoYun API, including basic company information, business information, financial information, public opinion information, and risk indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rose-develop](https://clawhub.ai/user/rose-develop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search for a company, confirm the intended company, and then retrieve WenDaoYun legal, financial, operational, public opinion, or risk details for that confirmed company. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company names or keywords entered by the user are sent to the WenDaoYun API. <br>
Mitigation: Install and use the skill only when sending those company queries to WenDaoYun is acceptable. <br>
Risk: The WenDaoYun API key is sensitive and can authorize API usage if exposed. <br>
Mitigation: Store the key in WENDAOYUN_API_KEY, keep it private, and revoke it through WenDaoYun if it is exposed. <br>
Risk: Detailed legal, financial, or risk data could be requested for the wrong company when search results are ambiguous. <br>
Mitigation: Require user confirmation of the selected company before making any detailed information request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rose-develop/skills/company-wdy) <br>
- [WenDaoYun open platform](https://open.wintaocloud.com/home) <br>
- [WenDaoYun API invoke endpoint](https://h5.wintaocloud.com/prod-api/api/invoke) <br>
- [fuzzy-search-org - company fuzzy search](artifact/references/fuzzy-search-org.md) <br>
- [get-risk - company risk information](artifact/references/get-risk.md) <br>
- [get-execute-info - execution information](artifact/references/get-execute-info.md) <br>
- [get-dishonest-debtors - dishonest debtor information](artifact/references/get-dishonest-debtors.md) <br>
- [get-judge-doc - judgment documents](artifact/references/get-judge-doc.md) <br>
- [get-case-filing - case filing information](artifact/references/get-case-filing.md) <br>
- [get-punishments - administrative penalties](artifact/references/get-punishments.md) <br>
- [get-tax-notice - tax arrears notices](artifact/references/get-tax-notice.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown text with API request guidance and structured company search or detail results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WENDAOYUN_API_KEY; sends company names or keywords to WenDaoYun and requires user confirmation before detailed queries.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
