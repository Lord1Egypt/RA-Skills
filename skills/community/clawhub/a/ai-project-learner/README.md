# AI Project Learner

An [OpenClaw](https://openclaw.org) skill that generates concept dependency graphs for users building projects with AI.

## What it does

- Analyzes your AI project description
- Identifies 8-20 concepts you need to learn
- Maps prerequisite dependencies between concepts
- Adapts difficulty to project complexity (beginner/intermediate/advanced)
- Provides a recommended learning order

## Install

```bash
clawhub install ai-project-learner
```

## Pricing

**$0.01 USDT** per call via [SkillPay.me](https://skillpay.me) (95% to author, 5% platform fee).

## How it works

1. Agent reads `SKILL.md` for concept graph generation instructions
2. Worker charges billing via SkillPay
3. Agent analyzes the project and builds a concept dependency graph
4. Returns structured JSON with concepts, prerequisites, and learning order

## Example output

```json
{
  "project": "RAG chatbot for internal docs",
  "complexity": "intermediate",
  "domain": "nlp",
  "concepts": [
    {
      "id": "llm-basics",
      "name": "Large Language Models",
      "description": "Neural networks trained on vast text data that can generate and understand language.",
      "difficulty": 1,
      "prerequisites": []
    },
    {
      "id": "embeddings",
      "name": "Text Embeddings",
      "description": "Converting text into numerical vectors that capture semantic meaning.",
      "difficulty": 2,
      "prerequisites": ["llm-basics"]
    },
    {
      "id": "vector-db",
      "name": "Vector Databases",
      "description": "Specialized databases for storing and querying embedding vectors at scale.",
      "difficulty": 3,
      "prerequisites": ["embeddings"]
    }
  ],
  "learning_order": ["llm-basics", "embeddings", "vector-db"],
  "estimated_hours": 15
}
```

## Tech Stack

TypeScript | Cloudflare Workers | SkillPay.me | ClawHub

## License

Private. All rights reserved.
