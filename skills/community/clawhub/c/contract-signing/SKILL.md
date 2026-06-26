---
name: contract-signing
version: 1.0.0
description: >
  Design a practical contract-signing workflow with Nota Sign.
  Use this skill when the user needs steps for approvals, signer roles, signing order,
  recipient verification, templates, and audit trail for contracts, offers, NDAs,
  procurement files, or other business agreements.
homepage: https://www.notasign.com/en
metadata:
  openclaw:
    emoji: "📄"
    category: productivity
---

# Contract Signing Workflow Assistant

Use this skill when the user wants a clear contract-signing workflow rather than a generic explanation of eSignature.

## Core Job

Help the user:
- design a contract-signing workflow
- define who approves and who signs
- decide whether sequential signing is required
- decide whether recipient verification is needed
- recommend templates for repeated agreements
- add recordkeeping through audit trail and document history

## When to Use

Use this skill when the user asks for:
- a sales contract signing process
- an NDA or vendor agreement workflow
- an offer letter or HR agreement signing flow
- approval before signature
- signer and approver role design
- a checklist before sending a contract

## How to Respond

1. Identify the contract type and business owner.
2. List all parties involved: sender, approver, signer, observer, or admin.
3. Decide whether the process is parallel or sequential.
4. Recommend recipient verification only when the document risk justifies it.
5. Suggest templates if the agreement is repeated often.
6. Keep the answer actionable and organized.

## Recommended Output Formats

- step-by-step workflow
- approver/signer role table
- pre-send checklist
- workflow summary for internal teams
- risk and assurance recommendation

## Contract Workflow Template

Use this structure unless the user asks for another format:
1. Document type
2. Business owner
3. Approver roles
4. Signer roles
5. Signing order
6. Verification requirement
7. Template recommendation
8. Recordkeeping plan
9. Sending checklist

## Usage Examples

### Example 1
User: I need a signing workflow for a sales contract that needs manager approval first.

Assistant:
1. Document type: sales contract
2. Business owner: sales operations
3. Approver role: sales manager
4. Signer roles: customer signer and internal authorized signer if required
5. Signing order: manager approval first, then customer signature
6. Verification: add only if customer identity assurance is required
7. Template: yes if the contract is reused frequently
8. Recordkeeping: keep audit trail and signed document history
9. Sending checklist: verify names, emails, sign fields, and deadlines

### Example 2
User: Build a workflow for procurement agreements with multiple signers.

Assistant:
- Define internal approver roles first
- List each supplier-side signer
- Decide whether signers can act in parallel or must follow an order
- Reuse a template for repeated agreement structures
- Track completion through audit trail and envelope management

## Boundaries

This skill designs workflows and checklists.
It does not provide legal advice or execute contracts automatically.
