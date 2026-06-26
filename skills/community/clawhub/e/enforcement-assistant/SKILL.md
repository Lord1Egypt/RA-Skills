---
name: enforcement-assistant
description: Assist with civil enforcement application (执行申请) preparation and process guidance after obtaining a court judgment. Provides procedural guidance only.
version: 1.0.0
tags: legal, enforcement, china, civil-law, court
---

# Enforcement Application Assistant

## Overview

This skill helps users prepare civil enforcement applications (民事执行申请) and navigate the enforcement process after obtaining a court judgment or arbitration award. It guides users through the required documents, procedures, and timelines for applying to the court for compulsory enforcement.

**⚠️ Important Disclaimer**: This tool provides procedural guidance only. It does not constitute legal advice, nor does it guarantee enforcement success. Enforcement outcomes depend on the debtor's assets and other factors. Always consult a qualified attorney for complex enforcement matters.

## Usage Scenarios

### Scenario 1: Prepare an enforcement application for a loan judgment
**User input:** "判决下来了，对方就是不还钱，5万借款判决已经生效了，怎么申请执行？"
**Expected output:** Generate a complete enforcement application framework with applicant/defendant information, basis for enforcement (court name, case number, judgment date), specific enforcement request (amount owed + interest), facts and reasons summary, and attachments checklist (judgment copy, proof of effectiveness, applicant ID). Include guidance on which court to file with and the 2-year deadline.

### Scenario 2: Judgment debtor has no discoverable assets
**User input:** "申请执行了，但法官说查不到对方名下有财产，我该怎么办？"
**Expected output:** Explain asset investigation limitations and proactive steps the applicant can take: provide asset leads (bank accounts, properties, vehicles, equity), request credit惩戒 (restrict debtor from high-consumption activities and travel), apply for inclusion in the dishonesty list (失信被执行人), monitor for future asset discovery, and consider settlement negotiations or debtor bankruptcy as alternatives.

### Scenario 3: Enforcement for an arbitration award
**User input:** "仲裁裁决已经下来了，对方公司不履行，怎么申请法院强制执行？"
**Expected output:** Generate an enforcement application tailored for an arbitration award. Note that arbitration awards require court confirmation before enforcement (unlike court judgments), and the competent court is the intermediate court at the debtor's location or asset location. Include the required documents (original arbitration award, service certificate, arbitration agreement). Explain the timeline differences between judgment enforcement and award enforcement.
### Scenario 4: 前同事借了3万不还怎么办
**User input:** "前同事去年借了3万一直不还，微信聊天记录和转账记录都有，我想到法院申请强制执行怎么办？"
**Expected output:** 先说明强制执行的前提条件：必须先有生效判决/调解书/仲裁裁决/公证债权文书。建议用户先去法院起诉（小额诉讼程序，标的3万适用）。指导收集证据（聊天记录、转账凭证、催收记录），起草起诉状（模板可在中国裁判文书网参考），计算诉讼费（约500元）。执行阶段提供查询被执行人财产的方法：不动产、银行账户、微信/支付宝余额等。

## When to Use This Skill

- After obtaining a court judgment that needs enforcement
- Preparing an enforcement application (执行申请书)
- Understanding the enforcement process and timeline
- Gathering required documents for enforcement
- Learning about enforcement measures and options
- Understanding enforcement limitations

## Limitations

- Provides **procedural guidance only**, not legal strategy
- Cannot guarantee successful enforcement
- Does not assess debtor's assets or enforceability
- Not a substitute for professional legal representation
- Enforcement rules may vary by jurisdiction

## When Enforcement is Available

### Judgments/Awards Eligible for Enforcement

| Document Type | When Enforceable |
|--------------|------------------|
| Civil judgment (民事判决) | After生效 (takes effect) |
| Civil mediation (民事调解书) | After生效 |
| Payment order (支付令) | 15 days after送达 if no objection |
| Arbitration award (仲裁裁决) | After作出 |
| Notarized debt instrument (公证债权文书) | Directly enforceable |

### Timing Requirements

- **Application period**: Within **2 years** from the last day of the履行期限
- **Calculation**: From the date specified in the judgment for履行义务
- **Extension**: May apply for extension under special circumstances

**⚠️ Important**: Missing the 2-year deadline may result in losing the right to enforce.

## Required Documents

### 1. Enforcement Application (执行申请书)

**Required content**:
- Applicant and被执行人 information
- Basis for enforcement (judgment/arbitration details)
- Enforcement request (specific relief sought)
- Facts and reasons
- Attachments list

### 2. Supporting Documents

| Document | Purpose | Notes |
|----------|---------|-------|
| Original judgment/mediation document | Proof of enforceable right | Certified copy acceptable |
| Proof of生效 | Confirm document is final | 生效证明 |
| Applicant ID | Identity verification | Copy |
| 被执行人 Information | Locate debtor | Address, contact, assets |
| Power of attorney (if applicable) | Authorization | Notarized if needed |

### 3. Asset Information (if available)

- Bank accounts
- Real estate
- Vehicles
- Equity/interests
- Other assets

## Workflow

1. **Verify judgment status** — Confirm judgment is final and生效
2. **Check deadline** — Ensure within 2-year limitation period
3. **Gather documents** — Collect all required materials
4. **Draft application** — Prepare enforcement application
5. **File with court** — Submit to competent enforcement court
6. **Follow up** — Track case progress and provide asset线索

## Choosing the Right Court

### Competent Court

Enforcement applications should be filed with:
- **First-instance court** (一审法院) that issued the judgment, OR
- **Court at被执行人's location** (被执行人住所地法院), OR
- **Court where被执行人's property is located** (财产所在地法院)

### Jurisdiction Considerations

- Convenience for execution
- Location of debtor's assets
- Court's enforcement capacity

## Enforcement Measures

### Available Measures

| Measure | Description | When Used |
|---------|-------------|-----------|
| Property inquiry |查询被执行人财产 | Initial investigation |
| Bank account freeze |冻结银行账户 | Upon finding accounts |
| Asset seizure |查封、扣押财产 | Tangible assets found |
| Real estate auction |拍卖房产 | Real estate available |
| Vehicle detention |扣押车辆 | Vehicles found |
| Equity freeze |冻结股权 | Corporate interests |
| Income garnishment |扣留提取收入 | Salary/business income |
| Restrictions |限制高消费、出境 | Non-cooperative debtors |
| Credit reporting |纳入失信名单 | 失信被执行人 |
| Criminal liability |拒不执行判决罪 | Serious violations |

### Enforcement Costs

- **Application fee**: No fee for enforcement applications
- **Actual costs**: Applicant may need to advance for certain measures
- **Cost recovery**: Deducted from执行款

## Application Content Structure

### Standard Enforcement Application

```
执行申请书

申请人：[姓名/名称]
地址：[详细地址]
联系方式：[电话/邮箱]

被执行人：[姓名/名称]
地址：[详细地址]
联系方式：[如有]

申请事项：
1. 请求强制执行[法院名称][案号]民事判决书/调解书
2. 请求执行标的：[具体金额或行为]
3. [其他请求]

事实与理由：
[简述案件经过、判决内容、履行期限、被执行人未履行情况等]

此致
[执行法院名称]

申请人：[签名/盖章]
日期：[年月日]

附件：
1. 判决书/调解书复印件
2. 生效证明
3. 申请人身份证明
4. [其他材料]
```

## Usage

### Basic Request
```
"帮我写执行申请书"
"怎么申请强制执行"
"判决下来对方不履行怎么办"
```

### With Context
```
"民间借贷判决执行"
"仲裁裁决申请执行"
"对方欠钱不还申请执行"
```

### Process Questions
```
"申请执行需要什么材料"
"执行期限是多久"
"执行不到钱怎么办"
```

## Output Format

The skill provides:
- **Application template** tailored to case type
- **Document checklist** for required materials
- **Process guidance** on filing and follow-up
- **Timeline expectations** for typical cases
- **Next steps** recommendations

## Common Challenges

### 1. Cannot Locate Debtor
- Provide known addresses
- Provide contact information
- Provide workplace information
- Consider hiring investigators

### 2. No Discoverable Assets
- Provide asset线索
- Monitor for future assets
- Consider settlement negotiations
- Apply for debtor bankruptcy (if applicable)

### 3. Enforcement Resistance
- Report to court
- Apply for信用惩戒
- Consider criminal prosecution for拒执罪
- Seek legal assistance

## Enforcement Timeline

| Stage | Typical Duration | Notes |
|-------|-----------------|-------|
| Filing to acceptance | 7 days | Court reviews application |
| Case assignment | 7-15 days | Assigned to执行法官 |
| Initial investigation | 30 days | Asset inquiry |
| Execution measures | Variable | Depends on assets found |
| Case conclusion | Variable | Settlement or termination |

## References

For detailed guidance and templates:
- [references/enforcement-process.md](references/enforcement-process.md) — Complete enforcement procedure guide
- [references/application-templates.md](references/application-templates.md) — Application document templates
- [references/asset-inquiry.md](references/asset-inquiry.md) — Asset investigation guidance

## Important Reminders

- **Time Limit**: 2-year deadline is strict
- **Asset线索**: Provide as much information as possible
- **Cooperation**: Cooperate with court investigations
- **Patience**: Enforcement can take time
- **Costs**: No application fee, but may have other costs
- **Settlement**: Consider settlement at any stage

## Privacy Note

Case information is processed for guidance only. No data is stored or transmitted to third parties.

## Disclaimer

Enforcement success depends on many factors including debtor's assets, cooperation, and court resources. This tool provides general guidance only and cannot guarantee specific outcomes. Consult an attorney for enforcement strategy and complex situations.
