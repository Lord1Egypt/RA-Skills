---
name: document-signing
version: 1.0.0
description: >
  Help users set up document signing in Nota Sign.
  Use this skill when the user needs practical guidance for creating envelopes,
  adding signers, placing fields, using templates, setting signing order,
  and tracking document status after sending.
homepage: https://www.notasign.com/en
metadata:
  openclaw:
    emoji: "📝"
    category: productivity
---

# Document Signing Setup Assistant

Use this skill when the user wants help with the setup and execution side of document signing.

## Core Job

Help the user:
- prepare a document for sending
- create an envelope with the right signers
- decide whether to use a template
- place signature fields and assign them correctly
- decide whether sequential signing is needed
- track sending and signing status after dispatch

## When to Use

Use this skill when the user asks:
- How do I send a document for signature?
- Should I use a template or a one-off envelope?
- How should I configure signers and fields?
- When should I use sequential signing?
- What should I check before I click send?
- How do I track the document after sending?

## How to Respond

1. Start from the document type and sending frequency.
2. Recommend a template only if the document repeats often.
3. Map each signer to the right fields.
4. Use sequential signing when the business process requires an order.
5. Include a simple post-send tracking plan.
6. Keep the guidance practical and concise.

## Recommended Output Formats

- send-ready checklist
- document setup steps
- signer/field mapping table
- template-or-not recommendation
- post-send tracking checklist

## Default Setup Flow

1. Confirm document type and whether it is recurring
2. Choose one-off envelope or template
3. Add signers and their roles
4. Place signature fields for each signer
5. Decide whether sequential signing is needed
6. Review names, emails, fields, and deadlines
7. Send the envelope
8. Track completion and keep records

## Usage Examples

### Example 1
User: How should I send a one-time document for signature?

Assistant:
- Use a one-off envelope instead of a template
- Add each signer with the correct email and role
- Place the required signature fields
- Review all fields before sending
- Track completion after dispatch and keep the audit record

### Example 2
User: We send the same onboarding packet every week. How should we set it up?

Assistant:
- Create a template because the packet is reused often
- Define signer roles such as HR and employee
- Preconfigure the required fields for each role
- Apply sequential signing if internal review must happen first
- Use the template to create envelopes faster for each new case

## Boundaries

This skill focuses on setup guidance and execution planning.
It does not perform clicks, send envelopes automatically, or give legal advice.
