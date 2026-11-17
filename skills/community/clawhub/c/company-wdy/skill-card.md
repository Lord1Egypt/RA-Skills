## Description:

Uses the WenDaoYun API to search companies and retrieve basic, operational, financial, public-opinion, and risk information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rose-develop](https://clawhub.ai/user/rose-develop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query WenDaoYun for company search results and selected company-detail datasets after confirming the target company.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose authentication error details when WenDaoYun API calls fail.

Mitigation: Configure the API key outside chat, avoid pasting secrets into conversations, treat authentication errors as sensitive, and rotate any leaked key.

Risk: The skill depends on WenDaoYun as a third-party commercial API and may return third-party company-risk data.

Mitigation: Install only when the deployment is comfortable using WenDaoYun and has reviewed data-use, privacy, and vendor requirements.

Risk: When no API key is configured, the skill presents setup and promotional onboarding text.

Mitigation: Review the no-key response before deployment and adjust surrounding user guidance if promotional setup text is not appropriate.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/rose-develop/skills/company-wdy)
- [WenDaoYun API key setup](https://open.wendaoyun.com/home)
- [WenDaoYun API base endpoint](https://h5.wintaocloud.com/prod-api/api/invoke)
- [fuzzy-search-org - company fuzzy search](references/fuzzy-search-org.md)
- [get-risk - company risk information](references/get-risk.md)
- [get-punishments - administrative penalties](references/get-punishments.md)
- [get-execute-info - enforcement information](references/get-execute-info.md)
- [get-judge-doc - judgment documents](references/get-judge-doc.md)
- [get-open-court - court hearing notices](references/get-open-court.md)
- [get-dishonest-debtors - dishonest debtor records](references/get-dishonest-debtors.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration guidance]

**Output Format:** [Markdown text with API request guidance and company information summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WENDAOYUN_API_KEY; API responses may include company, legal, financial, public-opinion, and risk records.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
