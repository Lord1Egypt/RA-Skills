## Description: <br>
本技能应在用户收到法院短信（文书送达、立案通知、开庭提醒等）时使用，自动提取案号、当事人、下载链接，下载文书并归档到对应案件目录。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cat-xierluo](https://clawhub.ai/user/cat-xierluo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Legal practitioners and legal support staff use this skill to process Chinese court SMS notices, extract case and service-link details, download served documents, and archive them into the relevant case folder. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Court SMS messages, delivery links, downloaded documents, and archive JSON records may contain client-confidential legal data. <br>
Mitigation: Use only in a trusted workspace with client-confidential data controls, and remove bundled examples or retained raw SMS/API records that are not strictly needed. <br>
Risk: Reusable delivery URLs, credentials, or verification codes could allow unintended access to court documents. <br>
Mitigation: Confirm senders and links manually, avoid storing reusable delivery URLs or verification secrets, and rotate or delete any exposed credentials promptly. <br>
Risk: Automated browser or API download flows may fetch and store sensitive court records with limited user review. <br>
Mitigation: Review the workflow before installation, restrict execution to intended case workspaces, and verify archived files before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cat-xierluo/court-sms) <br>
- [Project homepage](https://github.com/cat-xierluo/legal-skills) <br>
- [Attribution](references/ATTRIBUTION.md) <br>
- [SMS pattern rules](references/sms-patterns.json) <br>
- [Archive format](references/archive-format.md) <br>
- [Report format](references/report-format.md) <br>
- [FachuanHybridSystem reference project](https://github.com/Lawyer-ray/FachuanHybridSystem) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown reports with shell commands, downloaded PDFs, and JSON archive records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create case folders, save court-document PDFs, and write internal archive JSON records.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter, CHANGELOG, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
