# Expert Insist 🧠

> Stop your AI from being a yes-man. Make it think independently.

A prompt-engineering skill that forces AI agents to go through **3 rounds of internal validation** before giving any advice. Prevents sycophant behavior — where AI just agrees with whatever you say.

## The Problem

You ask your AI agent for advice. It gives you an answer. You push back. It immediately flips — with zero re-derivation. The advice becomes worthless because it's just a mirror of whatever you last said.

```
You: "I think I should do X"
AI: "Great idea! X is the way to go."
You: "Actually, maybe Y is better"
AI: "You're right, Y is definitely better!"
```

This is **sycophant behavior**. The AI has no backbone. This is dangerous when you're using AI for real decisions.

## How It Works

### Three-Round Validation

**Round 1: Initial Analysis**
- Form your own conclusion + reasoning chain + key assumptions

**Round 2: Self-Challenge**
- "What if my #1 assumption is wrong?"
- "What's the strongest case for the opposite?"
- "Am I just agreeing with the user?"

**Round 3: Resolve** *(only if Rounds 1 & 2 disagree)*
- Deeper reasoning → final stance
- If still divergent → present both views with reasoning

### The Key Rule

> "Being corrected isn't embarrassing. Changing your mind isn't embarrassing. But changing your mind without re-deriving your logic — that's embarrassing."

When a user corrects the AI, it doesn't just flip. It:
1. Asks clarifying questions if the new information is unclear
2. Re-runs its entire reasoning chain
3. Arrives at an independent conclusion — not just echoing the user

### In Practice

```
You: "I think I should invest in X"
AI: "I analyzed X independently. My take: Y is better because [reasoning].
     Key assumption: [X]. If that's wrong, my conclusion changes."

You: "But X has advantage Z"
AI: "You're right about Z. But that changes my analysis because...
     I still lean Y, but now for a different reason: [new reasoning]."
```

## Auto-Trigger

The skill activates **automatically** when the user asks opinion-based questions — no manual invocation needed.

**Triggers on:** "what should I do", "which is better", "analyze this", "pros and cons", "recommend", "evaluate", strategy/planning questions, user corrections requiring revised advice.

**Skips:** pure factual answers, task execution, formatting, code writing.

## Installation

### For OpenClaw

```bash
mkdir -p skills/expert-insist
# Copy SKILL.md to skills/expert-insist/SKILL.md
```

The skill auto-triggers on opinion-based queries. No configuration needed.

### For Other AI Frameworks

Copy the methodology from `SKILL.md` into your system prompt or agent instructions. It's a pure prompt pattern — no API keys, no dependencies.

## What It IS

- A pure prompt pattern — no API keys, no dependencies, no vendor lock-in
- Framework-agnostic — works with any LLM, any agent framework
- MIT licensed

## What It is NOT

- Not a fine-tuned model
- Not a wrapper library
- Not a SaaS product

It's a methodology you drop into your system prompt. 15 minutes to integrate, immediate behavior change.

## Why This Matters

The biggest problem with AI right now isn't capability — it's sycophancy. Models are trained to be helpful, which too often means being agreeable. But useful advice requires disagreement. You don't need an AI that says "you're right." You need one that says "here's why I think you're wrong."

## Contributing

We're especially interested in:
- Real-world use cases and edge cases
- Translations (currently EN + CN)
- Integration guides for other frameworks (LangChain, CrewAI, AutoGen, etc.)

## License

MIT
