---
name: ecommerce-aftersales-reply
description: Generate reusable, policy-aligned customer service replies for e-commerce aftersales scenarios. Use when support staff need fast, compliant Chinese responses for (1) return/exchange requests, (2) logistics exception inquiries such as delayed delivery, no tracking updates, lost parcels, wrong routing, or failed delivery, and (3) aftersales compensation negotiation. Reuse this skill across repeated customer conversations to keep tone, structure, empathy, and brand-service standards consistent while adapting to the specific case details.
---

# Ecommerce Aftersales Reply

## Overview

Generate standardized Chinese aftersales reply drafts for frontline e-commerce service agents. Keep responses polite, efficient, empathetic, boundary-aware, and suitable for repeated use across high-frequency customer support conversations.

## Core Objective

Produce a customer-facing reply that:

- acknowledges the customer's issue clearly
- communicates the handling result or next step directly
- stays within brand-service norms and does not overpromise
- protects the brand from ambiguous commitments, policy leakage, or emotional escalation
- remains easy for a human agent to send with minimal edits

## Input Handling

Before drafting, identify the following from the request if available:

- scenario type: return/exchange, logistics exception, or compensation negotiation
- customer concern and emotional state
- order stage and current status
- platform/policy constraints explicitly provided by the caller
- what has already been offered or rejected
- desired tone, if specified

If information is incomplete, do not invent operational facts. Draft a safe response that explains the current known position and asks for only the minimum missing information needed to proceed.

## Output Rules

Always output in simplified Chinese unless the caller explicitly asks otherwise.

Structure each reply in this order when suitable:

1. empathy/acknowledgment
2. issue confirmation
3. current handling decision, explanation, or next step
4. customer action guidance if needed
5. closing reassurance

Keep the message concise and directly sendable. Prefer natural paragraphs or short bullet-style lines when clarity improves readability.

## Brand-Service Standards

Follow these standards in every response:

- polite, calm, and respectful
- empathetic but not overly emotional
- firm when policy boundaries are involved
- no blame toward customer, warehouse, courier, or platform
- no absolute promises unless explicitly provided in the input
- no compensation commitment, refund timing commitment, or liability admission unless explicitly authorized in the input
- avoid internal jargon, process codes, or back-office language
- avoid saying the issue is “definitely” caused by any party unless confirmed in the input
- when rejecting a request, explain the basis tactfully and provide the next feasible option

## Scenario Workflow

### 1. Return or Exchange Request

For return/exchange cases:

- confirm the request type: return, exchange, refund-only, or return-and-refund
- restate the applicable condition if provided, such as unopened item, quality issue, wrong item, size mismatch, or exceeded period
- clearly state whether the request can proceed now, needs verification, or falls outside the stated rule
- if materials are needed, request them politely and specifically, such as photos, video, package label, or order number
- if the request is declined, provide a soft but clear explanation and a fallback path when available

Preferred reply emphasis:

- fairness
- clarity on next steps
- reduced back-and-forth

### 2. Logistics Exception Inquiry

For logistics exception cases:

- acknowledge the inconvenience first
- summarize the visible logistics issue, such as no update for several days, delivery delay, abnormal routing, failed delivery, damaged parcel, or possible loss
- explain the immediate action already taken or to be taken, such as urging the courier, checking with the warehouse, opening investigation, or asking the customer to verify contact details
- if there is no confirmed outcome yet, say so plainly and set expectation carefully without guaranteeing an exact result unless provided in the input
- when appropriate, instruct the customer on what to monitor next

Preferred reply emphasis:

- reassurance without overcommitting
- ownership of follow-up
- practical next step

### 3. Aftersales Compensation Negotiation

For compensation discussions:

- first recognize the customer's dissatisfaction or loss perception
- separate empathy from commitment: be understanding without immediately promising compensation
- if a compensation range, cap, or approved option is provided, stay strictly within that scope
- present the offered option clearly, including whether it is refund, partial refund, coupon, points, replacement support, or another approved remedy
- if the customer requests more than the authorized scope, respond firmly but politely, explain that the current solution is already the available support within the present case, and guide them to choose whether to accept or provide additional evidence for reassessment if allowed

Preferred reply emphasis:

- empathy with boundaries
- transparent offer wording
- de-escalation

## Response Modes

Choose the best mode based on the caller's need:

### A. Direct Send Mode

Use when enough facts are provided. Output only the final customer-facing reply.

### B. Multi-Option Mode

Use when the caller wants alternatives. Provide 3 versions:

- standard/professional
- warm/comforting
- firm/boundary-setting

Keep all versions compliant with the same facts.

### C. Fill-in Template Mode

Use when case details are incomplete but a reusable template is still useful. Provide a ready-to-edit response with clearly marked placeholders such as:

- [订单号]
- [问题描述]
- [处理方案]
- [需补充材料]
- [时效说明]

## Writing Guidance

Prefer these writing moves:

- “非常理解您当前的着急/困扰” over exaggerated apologies
- “这边先为您核实/处理/跟进” when action is still in progress
- “根据当前订单情况” when referring to known facts
- “在核实到更多结果后会第一时间同步您” only when follow-up is actually intended by the caller's scenario
- “目前可为您申请/提供的方案是” for compensation or policy-bounded offers

Avoid these writing moves:

- empty repetition of apologies
- vague promises like “一定马上解决” without basis
- internal phrasing like “系统显示异常件已逆向拦截” unless rewritten into customer-friendly language
- adversarial wording like “这不是我们的责任”
- mechanical, legalistic rejection phrasing unless the caller explicitly wants a tougher tone

## Output Quality Check

Before finalizing, ensure the draft:

- matches one of the three supported scenarios
- does not fabricate policy or timeline details
- includes a clear next step or outcome
- sounds like a real customer-service message, not analysis
- can be sent directly by a human agent with little or no revision

## Default Output Format

When the caller does not specify format, return:

- 场景判断：<one short phrase>
- 建议回复：
  <final Chinese reply>

If the caller explicitly asks for “only reply text”, output only the customer-facing reply.
