## Description: <br>
问道云企业信息查询工具，支持通过问道云 API 查询企业基本信息、经营信息、财务信息、舆情信息、企业各类风险指标等功能，当用户需要查询企业相关信息时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rose-develop](https://clawhub.ai/user/rose-develop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business analysts use this skill to look up WenDaoYun company intelligence after selecting a specific company from search results. It helps retrieve company operating, financial, public opinion, legal risk, credit, customer, supplier, hiring, and risk-index information through the WenDaoYun API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided WenDaoYun API key. <br>
Mitigation: Treat WENDAOYUN_API_KEY as a secret, configure it only in trusted environments, and rotate it if exposure is suspected. <br>
Risk: Company names and lookup queries are sent to WenDaoYun. <br>
Mitigation: Use the skill only when WenDaoYun company intelligence lookups are intended and approved. <br>
Risk: Returned company intelligence may include legal, personal, or contact details. <br>
Mitigation: Avoid storing or sharing returned details unless there is a lawful business reason. <br>


## Reference(s): <br>
- [WenDaoYun Open Platform](https://open.wintaocloud.com/home) <br>
- [WenDaoYun API Invoke Base URL](https://h5.wintaocloud.com/prod-api/api/invoke) <br>
- [fuzzy-search-org - 企业模糊搜索](references/fuzzy-search-org.md) <br>
- [get-abnormal - 经营异常](references/get-abnormal.md) <br>
- [get-bankruptcy-regroup - 破产重整信息](references/get-bankruptcy-regroup.md) <br>
- [get-bond-info - 债券信息](references/get-bond-info.md) <br>
- [get-case-filing - 立案信息](references/get-case-filing.md) <br>
- [get-cases-terminated - 终本案件信息](references/get-cases-terminated.md) <br>
- [get-clear-info - 清算信息](references/get-clear-info.md) <br>
- [get-consumption-limits - 限制高消费信息](references/get-consumption-limits.md) <br>
- [get-customer - 客户查询信息](references/get-customer.md) <br>
- [get-deliver-notice - 送达公告信息](references/get-deliver-notice.md) <br>
- [get-dishonest-debtors - 失信被执行信息](references/get-dishonest-debtors.md) <br>
- [get-employment-detail - 企业招聘信息详情](references/get-employment-detail.md) <br>
- [get-employment-info - 企业招聘信息](references/get-employment-info.md) <br>
- [get-environmental-penalties - 环保处罚](references/get-environmental-penalties.md) <br>
- [get-equity-pledge - 股权质押](references/get-equity-pledge.md) <br>
- [get-execute-info - 被执行信息（强制执行）](references/get-execute-info.md) <br>
- [get-exit-ban - 限制出境信息](references/get-exit-ban.md) <br>
- [get-gua-info - 担保信息](references/get-gua-info.md) <br>
- [get-import-export-credit - 海关进出口信用信息](references/get-import-export-credit.md) <br>
- [get-inq-eval - 询价评估信息](references/get-inq-eval.md) <br>
- [get-judicial-notice - 法院公告信息](references/get-judicial-notice.md) <br>
- [get-judicial-sale - 司法拍卖信息](references/get-judicial-sale.md) <br>
- [get-labour-arb - 劳动仲裁送达报告](references/get-labour-arb.md) <br>
- [get-land-mortgage - 土地抵押](references/get-land-mortgage.md) <br>
- [get-open-court-arb - 开庭公告（劳动仲裁）](references/get-open-court-arb.md) <br>
- [get-open-court - 开庭公告（司法）](references/get-open-court.md) <br>
- [get-pre-mediate - 诉前调解信息](references/get-pre-mediate.md) <br>
- [get-public-inform - 公示催告](references/get-public-inform.md) <br>
- [get-punishments - 行政处罚](references/get-punishments.md) <br>
- [get-risk-index - 企业风险指数](references/get-risk-index.md) <br>
- [get-risk - 企业风险信息](references/get-risk.md) <br>
- [get-share-blocking - 股权冻结信息](references/get-share-blocking.md) <br>
- [get-simple-cancel - 简易注销](references/get-simple-cancel.md) <br>
- [get-supplier - 供应商查询](references/get-supplier.md) <br>
- [get-tax-notice - 欠税公告](references/get-tax-notice.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown responses with API lookup results and inline shell configuration commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the WENDAOYUN_API_KEY environment variable and sends company lookup queries to WenDaoYun.] <br>

## Skill Version(s): <br>
1.2.28 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
