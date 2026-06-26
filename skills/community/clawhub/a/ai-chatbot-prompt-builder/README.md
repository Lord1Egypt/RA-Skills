# AI Chatbot Prompt & Persona Builder

**Build production-ready AI chatbot system prompts, personas, guardrails, and training data — no prompt engineering experience required.**

## The Problem

Every business wants an AI chatbot in 2026. Most fail within 90 days. Not because the technology doesn't work — because the prompts were bad. Generic system prompts produce generic responses. No guardrails means the bot says things it shouldn't. No persona means it sounds like every other chatbot. No training data means it hallucinates answers to basic questions.

This skill fixes all four failure points in one workflow.

## What You Get

**4 production-ready outputs:**

1. **System Prompt** — complete 500-800 word system prompt with role, knowledge base, behavioral rules, response format guidance, escalation triggers, and 3 sample response templates. Copy-paste into any AI platform: ChatGPT, Claude, Gemini, Intercom, Tidio, Crisp, or custom API.

2. **Persona & Brand Voice** — chatbot character sheet with name, archetype, backstory, 10 signature phrases, 10 anti-patterns, platform adaptation notes, and 5 sample exchanges showing the persona in action.

3. **Guardrails & Edge Cases** — master guardrails document (10-15 rules), topic boundary matrix, 5 off-topic deflection scripts, sensitive question handling playbook (pricing, complaints, legal threats, mental health signals), jailbreak resistance instructions, and escalation trigger matrix (12 scenarios).

4. **FAQ Training Data (50 pairs)** — JSONL format ready for OpenAI fine-tuning or RAG ingestion. Includes 10 multi-turn conversation examples, negative training pairs, metadata tags, and a refresh schedule recommendation.

## Who This Is For

- SaaS companies deploying support or onboarding bots
- E-commerce stores adding AI to product discovery and checkout
- Service businesses (HVAC, legal, medical, real estate) automating pre-sales Q&A
- Coaches and consultants deflecting intake and FAQ with AI
- Agencies building client chatbots repeatedly
- Internal tools teams (HR bots, IT help desks, knowledge base assistants)

## Example

**Business:** NightGuard Security (Las Vegas, $39/month residential monitoring)  
**Bot:** Ranger — former Las Vegas Metro officer, calm and reassuring, never pushy  
**Result:** System prompt + persona + 15-rule guardrails + 50 Q&A pairs in JSONL

Full example in `examples/nightguard-security-complete.md`

## Quick Start

1. Open Prompt 1 (`prompts/01-system-prompt-engineer.md`)
2. Fill in your business details (5 minutes)
3. Run the prompt in Claude or ChatGPT
4. Paste the output as your chatbot's system prompt
5. Use Prompts 2-4 to layer in persona, guardrails, and training data

## Pricing

- **Free:** Prompt 1 (System Prompt Engineer)
- **Full skill:** $29 one-time (all 4 prompts + example)
- **DFY:** $197/chatbot setup — Max builds it for you

## Platforms Supported

Works with any LLM or chatbot platform that accepts a system prompt:
- OpenAI (ChatGPT, GPT-4o, API)
- Anthropic (Claude)
- Google (Gemini)
- Intercom Fin
- Tidio, Crisp, Drift, Freshchat
- Custom API integrations
- Voiceflow, Botpress, ManyChat
