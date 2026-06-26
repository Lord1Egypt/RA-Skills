## Description: <br>
Chinese-language skill for querying class-action settlement opportunities across the United States, Canada, the United Kingdom, and Australia, with no-proof claims highlighted. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adsorgcn](https://clawhub.ai/user/adsorgcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking users ask an agent for current class-action settlement listings, country-specific cases, no-proof claims, and application guidance. The skill helps users understand eligibility and find claim links while reminding them to apply only for claims they genuinely qualify for. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts an external API to retrieve settlement data and presents external claim links. <br>
Mitigation: Review and approve the api.ilang.ai data access before use, and verify claim details on official settlement sites before submitting any application. <br>
Risk: Users may misunderstand settlement eligibility or attempt claims they do not qualify for. <br>
Mitigation: Use the skill's eligibility warnings and apply only to claims where the user genuinely meets the stated requirements. <br>
Risk: Setup guidance may involve DeepSeek or platform API keys outside the skill itself. <br>
Mitigation: Keep API keys private, avoid sharing them in chats or screenshots, and rotate any key that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adsorgcn/freemoney) <br>
- [I-Lang Homepage](https://ilang.ai) <br>
- [Claims API Status](https://api.ilang.ai/claims/api/stats) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese Markdown summaries, tables, and step-by-step claim guidance with external claim links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only GET requests to api.ilang.ai after user activation; no code or persistent local files are produced.] <br>

## Skill Version(s): <br>
1.3.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
