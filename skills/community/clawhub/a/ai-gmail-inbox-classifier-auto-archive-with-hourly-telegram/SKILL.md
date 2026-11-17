---
name: ai-gmail-inbox-classifier-auto-archive-with-hourly-telegram
description: "AI Gmail Inbox Classifier & Auto-Archive with Hourly Telegram Alerts: Automatically organize and clean up your Gmail inbox every hour, hands-free. This AI email automation reads each new message, classifies it into one of eleven of your own Gmail labels (across the \"00 Automated\", \"00 Human\", and \"00 Bookkeeping\" label groups), applies the right label, and archives it out of your inbox — so you reach inbox zero without lifting a finger. The moment a message is tagged Important, you get an insta."
version: 1.0.4
homepage: https://www.agentpmt.com/agent-workflow-skills/ai-gmail-inbox-classifier-auto-archive-with-hourly-telegram-alerts
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/agent-workflow-skills/ai-gmail-inbox-classifier-auto-archive-with-hourly-telegram-alerts"}}
---
# AI Gmail Inbox Classifier & Auto-Archive with Hourly Telegram Alerts

## Freshness
Last updated: `2026-08-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Workflow Does
Automatically organize and clean up your Gmail inbox every hour, hands-free. This AI email automation reads each new message, classifies it into one of eleven of your own Gmail labels (across the "00 Automated", "00 Human", and "00 Bookkeeping" label groups), applies the right label, and archives it out of your inbox — so you reach inbox zero without lifting a finger. The moment a message is tagged Important, you get an instant Telegram alert with a direct link to that email, so urgent messages never slip through. Ideal for busy professionals and teams who want smart email sorting, automated inbox triage, and real-time Telegram notifications for the emails that actually matter.

## Required Setup
- AgentPMT overview: `../what-is-agentpmt`.
- Account MCP/REST setup: `../agentpmt-account-mcp-rest-api-setup`.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

## Workflow Session Management
Call `AgentPMT-Workflow-Skills` with `start_workflow` before the first step and `end_workflow` after the final step.

```json
{"action":"start_workflow","skill_id":"ai-gmail-inbox-classifier-auto-archive-with-hourly-telegram-alerts"}
```

```json
{"action":"end_workflow","skill_id":"ai-gmail-inbox-classifier-auto-archive-with-hourly-telegram-alerts","rating":5,"comment":"completed"}
```

## Workflow Process
1. Fetch All Inbox Messages
   - Tool product: Gmail - All Email Actions.
   - Tool skill: `../gmail-all-email-actions`.
   - ClawHub page: https://clawhub.ai/agentpmt/gmail-all-email-actions.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill gmail-all-email-actions`.
   - Marketplace: https://www.agentpmt.com/marketplace/gmail-all-email-actions.
   - Tool instructions: Fetch all messages currently in the Gmail INBOX. Return the full list including message IDs, sender, subject, snippet, and any existing labels.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
2. For Each Email in Inbox
   - Iterate over the configured collection, then continue through the connected workflow path.
3. Get Full Email Details
   - Tool product: Gmail - All Email Actions.
   - Tool skill: `../gmail-all-email-actions`.
   - ClawHub page: https://clawhub.ai/agentpmt/gmail-all-email-actions.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill gmail-all-email-actions`.
   - Marketplace: https://www.agentpmt.com/marketplace/gmail-all-email-actions.
   - Tool instructions: Fetch the full details of the current email using email.id as the message ID. Extract and note: the sender email address, sender display name, subject, body content, threadId, and how many messages are in this thread. If the thread has multiple messages, this email is part of an ongoing conversation.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
4. Determine if Sender is Individual Human
   - Prompt: Determine whether the email sender is an individual human (a real person you might have a conversation with) versus an automated/system/company sender.
5. Is Sender an Individual Human?
   - Evaluate the configured branch options and follow the matching workflow path.
6. Check If User Previously Emailed This Person
   - Tool product: Gmail - All Email Actions.
   - Tool skill: `../gmail-all-email-actions`.
   - ClawHub page: https://clawhub.ai/agentpmt/gmail-all-email-actions.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill gmail-all-email-actions`.
   - Marketplace: https://www.agentpmt.com/marketplace/gmail-all-email-actions.
   - Tool instructions: Search for messages the USER previously SENT to this sender. Use the search query: to:{sender_email_address} (this only finds outbound messages from the user to this person). Do NOT include from:{sender} in the query -- we only care about messages the user initiated. If results are found, it means the user has previously emailed this person, confirming a real two-way relationship. Also check the current email threadId: if the thread contains multiple messages, note that the email is part of an ongoing conversation. Return: prior_correspondence_found (true/false), in_multi_message_thread (true/false).
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
7. Skip Prior Correspondence (Automated Sender)
   - Prompt: Provide a default result indicating no prior correspondence check was performed because the sender is automated.
8. Merge Correspondence Paths
   - Merge completed incoming workflow paths before continuing.
9. Classify Email Into Label
   - Prompt: Classify the email into exactly ONE of the eleven defined Gmail labels using priority-ordered rules, incorporating sender type and prior correspondence data.
10. Apply Gmail Label to Email
   - Tool product: Gmail - All Email Actions.
   - Tool skill: `../gmail-all-email-actions`.
   - ClawHub page: https://clawhub.ai/agentpmt/gmail-all-email-actions.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill gmail-all-email-actions`.
   - Marketplace: https://www.agentpmt.com/marketplace/gmail-all-email-actions.
   - Tool instructions: Apply the label returned by the classify-email prompt to the current email.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
11. Archive Email (Remove from Inbox)
   - Tool product: Gmail - All Email Actions.
   - Tool skill: `../gmail-all-email-actions`.
   - ClawHub page: https://clawhub.ai/agentpmt/gmail-all-email-actions.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill gmail-all-email-actions`.
   - Marketplace: https://www.agentpmt.com/marketplace/gmail-all-email-actions.
   - Tool instructions: Archive the current email by removing the INBOX label.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
12. Is Label Important?
   - Evaluate the configured branch options and follow the matching workflow path.
13. Build Gmail Direct Link
   - Prompt: Build the direct Gmail deep link: https://mail.google.com/mail/u/0/#all/{messageId}. Output JSON with 'gmail_link' and 'subject'.
14. Send Telegram Important Alert
   - Tool product: Telegram Instant Messenger.
   - Tool skill: `../telegram-instant-messenger`.
   - ClawHub page: https://clawhub.ai/agentpmt/telegram-instant-messenger.
   - skills.sh install: `npx skills add AgentPMT/agent-skills --skill telegram-instant-messenger`.
   - Marketplace: https://www.agentpmt.com/marketplace/telegram-instant-messenger.
   - Tool instructions: Send a Telegram message alerting the user to an important email.
   - Default parameters are configured on this workflow node; use the linked tool skill for schema details.
15. Hourly Run Summary
   - Prompt: Summarize the completed hourly Gmail inbox processing run. Report: total emails processed, how many were assigned to each of the eleven labels, how many Telegram notifications were sent, and confirm all emails archived.

## Tool Skill Links
- Gmail - All Email Actions: `../gmail-all-email-actions`; ClawHub https://clawhub.ai/agentpmt/gmail-all-email-actions; skills.sh `npx skills add AgentPMT/agent-skills --skill gmail-all-email-actions`; marketplace https://www.agentpmt.com/marketplace/gmail-all-email-actions
- Telegram Instant Messenger: `../telegram-instant-messenger`; ClawHub https://clawhub.ai/agentpmt/telegram-instant-messenger; skills.sh `npx skills add AgentPMT/agent-skills --skill telegram-instant-messenger`; marketplace https://www.agentpmt.com/marketplace/telegram-instant-messenger

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Workflow page: https://www.agentpmt.com/agent-workflow-skills/ai-gmail-inbox-classifier-auto-archive-with-hourly-telegram-alerts
- AgentPMT workflows: https://www.agentpmt.com/agent-workflow-skills
