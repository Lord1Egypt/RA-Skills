---
name: ai-project-learner
description: Generate a concept dependency graph for AI projects. Identifies what you need to learn, in what order, adapted to project complexity.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - SKILLPAY_API_KEY
    emoji: "🧠"
---

# AI Project Learner

Generate a concept dependency graph for users building projects with AI. Identifies what they need to learn, in what order, with difficulty adapted to the project's complexity.

## How to Use This Skill

### Step 1: Charge billing

POST to the skill endpoint to authorize payment:

```
POST https://ai-project-learner.swmengappdev.workers.dev/charge
Content-Type: application/json

{"user_id": "<user_id>"}
```

If successful, you'll receive `{"success": true}`.
If payment fails, you'll receive a `payment_url` to share with the user.

### Step 2: Analyze the project

From the user's project description, determine:

**Complexity level:**
- **beginner** — Uses a single API or library, straightforward pipeline (e.g., "chatbot using OpenAI API", "sentiment classifier with HuggingFace")
- **intermediate** — Combines multiple AI techniques, has data pipeline or custom logic (e.g., "RAG chatbot with custom embeddings", "multi-agent workflow")
- **advanced** — Involves fine-tuning, custom model architectures, or production-scale systems (e.g., "fine-tuned LLM for legal documents", "real-time ML pipeline with feature store")

**Domain:**
Classify into one of: `nlp`, `cv` (computer vision), `agents`, `data`, `multimodal`, `generative`, `mlops`, `other`

### Step 3: Build the concept dependency graph

Generate **8-20 concepts** (scale with complexity: beginner ~8, intermediate ~12-15, advanced ~15-20).

For each concept, provide:
- **id** — kebab-case identifier (e.g., `text-embeddings`)
- **name** — Human-readable name (e.g., "Text Embeddings")
- **description** — 1-2 sentence explanation of what it is and why it matters for this project
- **difficulty** — Integer 1-5 (1=fundamental, 5=advanced)
- **prerequisites** — Array of concept `id`s that should be understood first

**Rules for building the graph:**
- Every concept's prerequisites must reference other concepts in the graph
- Concepts with no prerequisites are entry points (difficulty 1-2)
- No circular dependencies
- Order concepts so prerequisites always appear before dependents
- Descriptions should be practical ("what it is + why you need it for this project"), not academic
- Difficulty should be calibrated to the project: a beginner project should have mostly difficulty 1-3 concepts, an advanced project can have difficulty 4-5 concepts

**Concept categories to consider (pick relevant ones):**
- Foundations: LLMs, APIs, prompting, tokens, context windows
- Data: embeddings, vector databases, chunking, preprocessing
- Architecture: RAG, agents, chains, tool use, memory, planning
- Training: fine-tuning, RLHF, LoRA, evaluation, datasets
- Production: deployment, monitoring, caching, rate limiting, cost optimization
- Safety: guardrails, content filtering, hallucination detection, red teaming

### Step 4: Compute learning order

Produce a topologically sorted `learning_order` array of concept `id`s. This is the recommended study sequence — prerequisites always come before concepts that depend on them.

### Step 5: Estimate total learning time

Estimate `estimated_hours` as a total for all concepts. Use these rough heuristics:
- Difficulty 1 concept: ~1 hour
- Difficulty 2 concept: ~1.5 hours
- Difficulty 3 concept: ~2.5 hours
- Difficulty 4 concept: ~4 hours
- Difficulty 5 concept: ~6 hours

### Output Format

Return the result as JSON:

```json
{
  "project": "<user's project description>",
  "complexity": "beginner|intermediate|advanced",
  "domain": "nlp|cv|agents|data|multimodal|generative|mlops|other",
  "concepts": [
    {
      "id": "llm-basics",
      "name": "Large Language Models",
      "description": "Neural networks trained on vast text data that can generate and understand language. The foundation of your chatbot project.",
      "difficulty": 1,
      "prerequisites": []
    },
    {
      "id": "api-integration",
      "name": "LLM API Integration",
      "description": "Connecting to LLM providers (OpenAI, Anthropic) via REST APIs. How you'll send prompts and receive responses.",
      "difficulty": 1,
      "prerequisites": ["llm-basics"]
    }
  ],
  "learning_order": ["llm-basics", "api-integration"],
  "estimated_hours": 15
}
```

## Pricing
$0.01 USDT per call via SkillPay.me
