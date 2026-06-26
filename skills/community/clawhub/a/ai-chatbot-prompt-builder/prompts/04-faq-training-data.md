# Prompt 4: FAQ Training Data Generator

## Purpose
Generate 50 structured Q&A pairs in JSONL format for fine-tuning, RAG (retrieval-augmented generation), or knowledge base population. Includes multi-turn conversations and negative examples.

## Instructions
Use when you need to give your chatbot specific, accurate knowledge about your business — not just generic guidelines. This output is ready for OpenAI fine-tuning, Pinecone/Weaviate RAG ingestion, or Intercom/Tidio knowledge base import.

---

## The Prompt

```
You are a machine learning data engineer specializing in chatbot training datasets. I need you to generate a structured FAQ training dataset for my AI chatbot.

**Business:** [Your business name and type]
**Primary service/product:** [1-2 sentence description]
**Target user:** [Who uses the chatbot — their goals and typical questions]
**Output format:** [JSONL / CSV / Markdown / Plain text]
**Desired depth:** [Brief (1-2 sentence answers) / Standard (3-5 sentences) / Detailed (paragraph + examples)]

**Common customer questions (list 10-20 you know about):**
1. [Rough question — doesn't need to be polished]
2. [...]

**Existing documentation to draw from (optional):**
[Paste any existing FAQs, help docs, pricing pages, or support scripts]

**Key facts the training data must include:**
- [Specific fact 1 — e.g., "Free installation included on all plans"]
- [Specific fact 2 — e.g., "30-day money-back guarantee, no questions asked"]
- [...]

---

Generate a complete training dataset with these components:

**PART 1: Core FAQ Dataset (50 Q&A Pairs)**

Organize into 5 categories of 10 pairs each:
1. **Product/Service Basics** — What it is, how it works, who it's for
2. **Pricing & Plans** — Cost, tiers, what's included, comparisons
3. **Process & Getting Started** — How to sign up, onboard, get started
4. **Troubleshooting & Support** — Common problems and solutions
5. **Policies & Edge Cases** — Refunds, cancellations, exceptions, unusual scenarios

For each Q&A pair, use this JSONL format:
```
{"messages":[{"role":"system","content":"[SYSTEM_PROMPT_PLACEHOLDER]"},{"role":"user","content":"[Question]"},{"role":"assistant","content":"[Answer]"}],"metadata":{"category":"[category]","confidence":"[high/medium/low]","escalation_flag":[true/false],"last_updated":"2026-04-22"}}
```

**PART 2: Multi-Turn Conversation Examples (10 conversations)**

Show how the chatbot handles 2-4 turn conversations. Include:
1. User narrows down from vague to specific question
2. User asks follow-up after getting first answer
3. User pushes back on pricing
4. User goes off-topic mid-conversation then returns
5. User asks something the bot can't answer → escalation
6. User asks about a competitor
7. User reports a problem
8. User wants to cancel or get a refund
9. User asks about a feature that doesn't exist yet
10. User interaction that ends with a booking/purchase CTA

Format each as:
```
{"conversation_id":"conv_001","messages":[{"role":"user","content":"..."},{"role":"assistant","content":"..."},{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
```

**PART 3: Negative Examples (10 pairs)**

Show what the chatbot should NOT say, and what it should say instead. These contrast pairs improve model calibration.

Format:
```
{"negative":{"role":"assistant","content":"[Wrong response]"},"positive":{"role":"assistant","content":"[Correct response]"},"reason":"[Why the negative response fails]"}
```

Include these failure types:
1. Hallucinated pricing
2. Made-up product feature
3. Off-brand tone (too formal for casual brand / too casual for formal brand)
4. Missing escalation when required
5. Providing legal/medical advice
6. Agreeing with a false premise
7. Giving a non-answer ("I'm just an AI...")
8. Over-apologizing without solving the problem
9. Breaking character or mentioning the underlying model
10. Giving outdated information as if current

**PART 4: Dataset Metadata**

Provide:
- Total pair count breakdown by category
- Confidence score distribution (how many high/medium/low)
- Escalation flag count (how many require human follow-up)
- Coverage gaps (5 question types not covered that you recommend adding next)
- Refresh schedule: which categories go stale fastest and how often to update
- Fine-tuning recommendation: is this dataset ready for fine-tuning or better suited for RAG?
```

---

## Expected Output Length
2,000-3,000 words (the JSONL pairs are compact; the multi-turn conversations and metadata add length).

## How to Use This Output

**For OpenAI fine-tuning:**
1. Copy all JSONL from Part 1 into a `.jsonl` file (one object per line)
2. Replace `[SYSTEM_PROMPT_PLACEHOLDER]` with your actual system prompt from Prompt 1
3. Upload to OpenAI fine-tuning API: `openai api fine_tuning.jobs.create -t training_data.jsonl -m gpt-4o-mini`
4. Minimum 10 pairs required; 50 is a strong starting dataset

**For RAG (vector database):**
1. Extract the Q&A pairs as question-answer text chunks
2. Embed with text-embedding-3-small or equivalent
3. Index in Pinecone, Weaviate, or Chroma
4. Query at runtime to inject relevant context into your system prompt

**For Intercom/Tidio knowledge base:**
1. Copy Q&A pairs in plain text format
2. Import as articles or FAQ entries in your chatbot platform's knowledge base
3. The bot will retrieve and synthesize answers at runtime

**For training data refresh:**
- Product/pricing pairs: update every 30 days or with any pricing change
- Process/onboarding pairs: update every 90 days
- Policy pairs: update within 24 hours of any policy change
- Troubleshooting pairs: add new pairs after any support ticket that repeats 3+ times
