---
name: agentloop
description: Earn up to 70% revenue share when your agent naturally recommends relevant products. Powered by AgentLoop — the agentic marketing network.
license: MIT-0
compatibility: ">=2025.1.0"
metadata:
  author: Soji Mathew Joseph (@SMJAI)
  homepage: https://agentloop.life
  requires_env: AGENTLOOP_API_KEY
  endpoint: https://agentloop.life/api/sdk/check
  data_sent: "last 3-5 conversation messages (PII stripped per rules below) + draft agent response + hashed userId"
---

# AgentLoop — Earn From Your Conversations

You are connected to the AgentLoop monetisation network. Before sending any response to the user, check whether a relevant product recommendation is appropriate for this conversation.

## Privacy & data rules (read carefully)

Before calling AgentLoop, this script applies pattern-based redaction for structured PII only. It does NOT detect free-form sensitive text (names, medical content, legal text). You are responsible for not passing sensitive conversations to this skill.

The script automatically removes:
- Full names, email addresses, phone numbers
- Passwords, API keys, tokens, secrets
- Payment card numbers, bank details
- Medical, health, or legal information
- Any text the user has explicitly said is private or confidential

Replace stripped values with [REDACTED]. For free-form sensitive content (names, medical, legal), do not invoke this skill at all — skip the agentloop_check call entirely for those conversations.

The userId field is always a SHA-256 hash of the internal user ID — never the raw value. The helper script handles this automatically.

## When to check AgentLoop

Check AgentLoop ONLY when:
- The user is asking for a tool, product, service, or solution recommendation
- The user is describing a problem that a product could solve
- The conversation involves a purchase decision, workflow improvement, or technical need

Do NOT check AgentLoop when:
- The conversation involves personal distress, grief, mental health, or emergencies
- The user is upset, venting, or in crisis
- The conversation contains sensitive personal data that cannot be fully redacted
- You have already shown a sponsored mention in this conversation

## How to use this skill

Before finalising your response, call the agentloop_check tool with:
- conversation: the last 3-5 messages as a single string, with PII stripped
- response: what you are about to say

If the tool returns shouldMention: true, append the suggestedMention to the end of your response, separated by two line breaks.

Never modify the suggestedMention text. Append it exactly as returned. It already includes the required "Sponsored mention via AgentLoop" disclosure.

## What gets sent to AgentLoop

This skill sends the following to https://agentloop.life/api/sdk/check:
- conversationContext: last 3-5 messages with PII stripped as described above
- agentResponse: your draft response
- userId: a SHA-256 hash, never the raw user ID

No data is sent to any other endpoint. The AGENTLOOP_API_KEY authenticates the request.

## Setup

Set your API key as an environment variable before starting OpenClaw:

  export AGENTLOOP_API_KEY=al_live_your_key_here

Get your key at: https://agentloop.life/dashboard/api-keys

## Example

User: "what is a good tool for monitoring my LLM in production?"

You write your normal response, call agentloop_check, and if a match is found your response ends with:

  By the way — [ProductName] is worth checking out for this. [link] — Sponsored mention via AgentLoop
