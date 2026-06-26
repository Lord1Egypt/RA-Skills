# Prompt 1: System Prompt Engineer

## Purpose
Generate a complete, production-ready system prompt for an AI chatbot or assistant.

## Instructions
Copy the prompt below into Claude or ChatGPT. Fill in the bracketed sections with your information. The output is ready to paste as a system prompt in any AI platform.

---

## The Prompt

```
You are a world-class prompt engineer specializing in production AI chatbot deployments. I need you to write a complete system prompt for my AI assistant.

Here is my business information:

**Business Name:** [Your business name]
**Business Type:** [e.g., SaaS, e-commerce, law firm, HVAC company, coaching practice]
**Primary Use Case:** [Customer support / Pre-sales Q&A / User onboarding / Internal knowledge base / Appointment booking]
**Target User:** [Who chats with the bot — e.g., "homeowners in Las Vegas comparing security systems"]

**What the bot should ALWAYS do (list 5-10):**
1. [e.g., Greet users by name if provided]
2. [e.g., Ask one clarifying question before answering]
3. [e.g., End every response with a next-step suggestion]
4. [...]

**What the bot should NEVER do (list 5-10):**
1. [e.g., Quote specific pricing without noting it's subject to assessment]
2. [e.g., Discuss competitor products by name]
3. [e.g., Provide legal or medical advice]
4. [...]

**Key products/services and descriptions:**
- [Product/service name]: [1-2 sentence description, key features, price if applicable]
- [Product/service name]: [...]

**Policies the bot must know:**
- Refund policy: [...]
- Shipping/delivery: [...]
- Support hours: [...]
- Escalation path: [e.g., "Route to human via email at support@company.com or phone 702-555-0100"]

**Desired tone:** [Formal / Friendly / Professional / Casual / Empathetic / Authoritative]
**Bot's name (optional):** [Name or "generate a name"]

---

Now generate a complete system prompt with these sections:

1. **Role Definition** — Who the bot is, what it does, and what it does NOT do (2-3 sentences)
2. **Knowledge Base** — What the bot knows: products, policies, FAQs. Be specific with facts provided.
3. **Behavioral Rules** — 10-15 explicit DO/DON'T pairs with brief rationale
4. **Response Format** — Length guidance, structure (bullets vs prose), emoji policy, how to handle "I don't know"
5. **Escalation Triggers** — Exact phrases or scenarios that should route to a human (list 8-10)
6. **Persona Block** — Tone, voice, 3 phrases the bot uses consistently, 3 phrases it never uses
7. **Greeting Template** — The first message the bot sends when a conversation starts
8. **3 Sample Responses** — Show how the bot handles: (a) a common pre-sales question, (b) a complaint, (c) an out-of-scope request

Format the system prompt so I can copy it directly into the system prompt field of my AI platform. Use clear section headers.
```

---

## Expected Output Length
500-800 words for the system prompt itself, plus sample responses (additional 200-300 words).

## Platforms Where You Can Use This
- **OpenAI:** Paste into the "System" field in the API playground, or use as the system message in your API calls
- **Anthropic (Claude):** Paste into the system parameter in API calls, or use in Claude's "System prompt" field
- **Intercom Fin:** Paste into the AI persona configuration
- **Tidio / Crisp / Freshchat:** Use in the AI agent system instructions
- **Voiceflow:** Add as a "set AI model" block with system prompt
- **Custom API:** Include as the `system` role message in your messages array

## Tips
- Be specific about pricing — "our plans start at $39/month" is better than "we have competitive pricing"
- The escalation path is critical: the bot needs to know exactly where to send users it can't help
- The "NEVER do" list prevents 80% of chatbot failures — be honest about what your bot shouldn't handle
- Run the prompt through your chosen platform and test with 10 real customer questions before going live
