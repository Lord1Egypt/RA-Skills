---
name: study-buddy
description: Make learning stick for ADHD brains. Active recall, multi-modal, zero boredom. Use for studying, understanding complex topics, test prep, or any learning-related request.
metadata:
  tags: [brainhack, adhd, learning, studying]
---

# Study Buddy

## Purpose
ADHD brains aren't bad at learning — they're bad at passive, boring learning. This skill makes engagement active, varied, and dopamine-friendly.

## Trigger
- "I need to study"
- "Quiz me"
- "I have a test"
- "Explain this topic"
- "I keep reading this and it's not sticking"

## Process

### Step 1: Identify what needs to be learned
Topic, scope, deadline, and stakes.

### Step 2: Ask learning preference
"How do you want to tackle this?"
- "Read and discuss" — go through material together
- "Quiz me" — active recall testing
- "Explain it weird" — analogies, characters, funny explanations
- "Teach it back" — user explains to the agent, agent corrects misconceptions

### Step 3: Run the learning method

**Summarize → Simplify → Quiz loop:**
1. Summarize the concept in plain language
2. Simplify further (analogies, examples)
3. Quiz on it before moving on

**ELI5 escalation:**
- ELI5: "Explain like I'm 5" — pure basics, no jargon
- ELI15: More detail, still accessible
- College level: Full complexity reintroduced

**Character voice explanations:**
- "Explain quantum mechanics like you're a sports commentator"
- "Explain this history event like a documentary narrator"
- "Explain photosynthesis like Deadpool would"
Pull from USER.md for preferred characters/voices.

**Teach-back:**
- User explains the concept to the agent
- Agent plays a confused student who asks clarifying questions
- Agent then corrects any misconceptions
- Incredibly effective for retention

**Flashcard generation:**
Generate Q&A pairs for any topic. Clean format, one concept per card.

### Step 4: Micro-quizzes
Every 10-15 minutes of engagement: quick 3-question quiz. Keeps the brain from drifting.

### Step 5: Body double integration
Combine with body-double for study sprints. Study-buddy provides content, body-double provides presence.

## Output Examples

**Explain (ELI5): "What is inflation?"**
> "Imagine your lunch money is $5 and a sandwich costs $5. Perfect. Now next year the sandwich costs $6 but you still only have $5. That's inflation — your money buys less stuff than before. The sandwich didn't get better, it just costs more."

**Quiz mode:**
> "Okay — quick quiz. What are the three branches of US government? No peeking."

**Teach-back:**
> "Alright — teach me the water cycle like I'm 10 and have never heard of it. Go."

## Rules
- Never read out long passages of text — summarize first, offer full detail on request
- Micro-quiz at least every 10-15 minutes to maintain engagement
- Match energy to user's — if they're low-energy, keep explanations lighter
- If a concept isn't sticking: try a completely different modality (if you did visual analogy, try story next)

## References
- knowledge/adhd-executive-function.md (working memory limits)
- knowledge/prompt-library.md (learning section)
