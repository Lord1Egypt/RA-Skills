---
name: Document Signature Packet Builder
version: 1.0.0
tags: [document-signing, signature-workflow, e-signature, packet-assembly]
---
# Document Signature Packet Builder

## Purpose

Turn a set of document-signing instructions into a practical sign-here and logistics checklist. The goal is to help the user avoid missed signatures, dates, initials, attachments, identity items, witnesses, notarization steps, copies, and submission details.

This skill is not legal advice. It does not interpret clauses, explain legal consequences, decide whether the user should sign, or confirm that a signature packet is legally valid.

## When to Use

Use this when the user needs to prepare documents such as:

- Application forms
- Agency or school forms
- Real estate or rental packets
- Employment, benefits, onboarding, or HR packets
- Bank, insurance, tax, or benefits forms
- Consent, authorization, or release forms
- Any packet with signature, date, initial, witness, notary, attachment, or submission requirements

## Required Inputs

Ask for the minimum needed to make a reliable logistics checklist.

- Document names or a list of forms in the packet
- Issuer or receiving organization
- Deadline and submission method
- Known instructions from the issuer
- Pages or sections that require signatures, dates, initials, witnesses, notarization, seals, photos, copies, or attachments
- Whether the user is signing alone or with other parties
- Whether original documents, copies, wet ink, electronic signature, or notarization are required
- Identification, payment, appointment, mailing, upload, or delivery requirements
- Any unclear instructions the user wants to track for confirmation

## Operating Rules

- Give sign-here and logistics support only.
- Do not interpret legal meaning, rights, obligations, penalties, waivers, or enforceability.
- Do not advise the user whether to sign.
- Do not infer hidden requirements from a document type. Use only the user's instructions and clearly marked common logistics reminders.
- Tell the user to confirm rules with the issuer when anything is unclear.
- If notarization, witnesses, certified copies, translations, guardianship, power of attorney, court, immigration, tax, medical, financial, employment, or real estate matters are involved, recommend confirmation with the issuer or a qualified professional.
- Mark every uncertain item as "confirm with issuer".
- Respect privacy. Do not ask for full identity numbers or sensitive document contents unless necessary for the checklist, and prefer redacted descriptions.

## Workflow

1. Inventory every document in the packet.
2. Identify each visible signature, date, initial, witness, notary, attachment, copy, payment, and submission requirement from the provided instructions.
3. Group actions by signer and by document.
4. Add logistics items for identity, appointment timing, copies, delivery method, deadline, and proof of submission.
5. Create a confirmation list for unclear or issuer-specific rules.
6. Provide a final packet assembly order.

## Output Format

Return the result in this structure:

### Packet Summary

- Issuer or recipient:
- Packet purpose:
- Deadline:
- Submission method:
- Signers:
- Known issuer instructions:

### Sign-Here Checklist

For each document, list:

- Document name:
- Signature required:
- Date required:
- Initials required:
- Witness required:
- Notary required:
- Attachments required:
- Copies required:
- Notes to confirm:

### Logistics Checklist

- Identification:
- Appointment or notary timing:
- Ink or electronic format:
- Original versus copy handling:
- Payment or fee:
- Mailing, upload, drop-off, or delivery details:
- Proof of submission:
- Backup copy plan:

### Questions to Confirm With Issuer

List every unclear signing rule, format requirement, attachment requirement, deadline issue, or submission detail.

### Packet Assembly Order

Give a simple order for signing, attaching, copying, and submitting the packet.

### Boundary Note

Include this note:

"This is a sign-here and logistics checklist only. It does not interpret the document, provide legal advice, or confirm validity. Confirm signing rules and submission requirements with the issuer or a qualified professional before relying on the packet."

## Example Prompts

Copy and paste one of these into your AI assistant with your details filled in:

1. **Benefits enrollment packet:** "I have an employee benefits enrollment packet with 4 forms: health insurance election, dependent verification, beneficiary designation, and direct deposit authorization. The HR deadline is Friday. Each form has different signature requirements — some need witness signatures and one needs notarization. Walk me through a sign-here checklist so I don't miss anything."

2. **Real estate closing docs:** "I'm closing on a house next Tuesday and the title company sent a packet with 12 documents. Several need notarized signatures, some need initials on every page, and two need my spouse's signature too. I also need to bring two forms of ID and a cashier's check. Build me a logistics checklist and packet assembly order."

3. **School enrollment forms:** "My child's school enrollment packet has a registration form, medical authorization, photo release, emergency contact card, and free/reduced lunch application. Each has different signature and date spots. Some need a doctor's signature on the medical form. The deadline is August 1. Create a checklist with what to sign, what to attach, and what to confirm with the school."


## Usage Scenarios

### Scenario 1

**User Input:** "Build a packet for a home purchase: purchase agreement, lead disclosure, title affidavit. Buyer signs first, then seller."

**Expected Output:** Packet manifest with document order, signer slots per doc, required notation fields (initials on each page, date, witness line) flagged.

### Scenario 2

**User Input:** "I need to send this packet to 3 signers. Generate separate envelopes for each with their pages only."

**Expected Output:** Three sub-packets extracted: Buyer envelope (all pages), Seller envelope (seller-signature pages only), Notary envelope (notarization pages).

### Scenario 3

**User Input:** "Audit the completed packet. Are there any missing initials or unsigned pages?"

**Expected Output:** Completeness report: lists every required signature/initial field vs. actuals. Flags 2 missing initials on page 7 and 1 unsigned witness line on page 12.


### Scenario 4: 合同签约材料包整理
**User input:** "签房租/工作/合伙合同需要准备一堆材料，每次东找西找。有没有一个万能材料清单模板？"
**Expected output:** 常见签约材料包模板——租房类：身份证复印件（正反面同页）+ 收入证明/银行流水（最近3个月）+ 工作证明/工牌复印件 + 紧急联系人信息 + 押金转账截图；工作类（入职）：身份证复印件 + 学历学位证书复印件 + 离职证明原件 + 银行卡复印件 + 1寸照片电子版；合伙类：身份证 + 征信报告（中国人民银行征信中心）+ 出资证明 + 合伙人协议草稿。建议把所有常用材料的扫描件存到一个加密的云文件夹（百度网盘/阿里云盘），需要时直接打印或发PDF。

## Quality Bar

A good output is concrete, cautious, and easy to follow during a signing appointment. It prevents missed logistics without pretending to interpret the document.
