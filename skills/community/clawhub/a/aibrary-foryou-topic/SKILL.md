---
name: aibrary-foryou-topic
description: "[Aibrary] Generate personalized 'For You' book topic recommendations based on the user's profile, interests, career stage, and recent learning activity. Use when the user wants personalized topic suggestions, asks 'what should I learn today', wants a curated feed of book-based topics, or needs inspiration for their next area of exploration. Proactively suggest this when the user seems undecided about what to read or learn next."
---

# ForYou Topic — Aibrary

Your personalized book topic feed. AI-curated topic recommendations based on who you are and where you're headed.

## Input

The user provides context (the more, the better):
- **Interests** — topics they care about or are curious about
- **Recent focus** — what they've been working on, reading, or thinking about lately
- **Career/life stage** — their current professional or personal situation
- **Goals** (optional) — what they're working toward
- **Topics to avoid** (optional) — what they've already covered or aren't interested in

## Workflow

1. **Build user profile**: From the provided context, map out:
   - Primary interest domains (2-3)
   - Current knowledge level in those domains
   - Growth direction — where they're headed vs. where they are
   - Gaps — important adjacent topics they might not have considered

2. **Generate topic recommendations**: Create 3-5 personalized topics, each:
   - Connected to the user's interests but not obvious (avoid recommending what they already know)
   - Timely — relevant to current trends, challenges, or opportunities in their field
   - Actionable — each topic leads naturally to specific books
   - Diverse — cover different angles (depth in core area + breadth in adjacent areas + one wildcard)

3. **For each topic, curate books**: Select 2-3 books that best explore the topic, explaining why each was chosen for this specific user.

4. **Add "why now" reasoning**: For each topic, explain why this is the right time for this person to explore it.

5. **Language**: Detect the user's input language and respond in the same language.

## Output Format

```
# 📚 Your Personalized Topics — For You

Based on your profile: [1-sentence summary of user context]

---

### Topic 1: [Topic Title]
**Why now**: [1-2 sentences on why this topic is relevant to the user right now]
**The angle**: [What specific perspective on this topic is most valuable for this user]

📖 **Recommended books**:
1. **[Book Title]** by [Author] — [Why this book, for this person]
2. **[Book Title]** by [Author] — [Why this book, for this person]

💡 **Key question this topic answers**: [A compelling question that makes the user want to explore]

---

### Topic 2: [Topic Title]
**Why now**: [Relevance explanation]
**The angle**: [Specific perspective]

📖 **Recommended books**:
1. **[Book Title]** by [Author] — [Why]
2. **[Book Title]** by [Author] — [Why]

💡 **Key question this topic answers**: [Compelling question]

---

### Topic 3: [Topic Title] 🌟 Wildcard
**Why now**: [This one is deliberately outside your usual domain — here's why it matters]
**The angle**: [How this connects back to your core interests in an unexpected way]

📖 **Recommended books**:
1. **[Book Title]** by [Author] — [Why]
2. **[Book Title]** by [Author] — [Why]

💡 **Key question this topic answers**: [Compelling question]

---

### 🎯 My top pick for you today
**[Topic X]** — [One sentence on why to start here]
```

### Example Output

**User input**: "I'm a product manager at a fintech startup, interested in behavioral economics and AI. Recently been thinking about user retention."

---

# 📚 Your Personalized Topics — For You

Based on your profile: Fintech PM exploring behavioral economics and AI, with a current focus on user retention.

---

### Topic 1: The Psychology of Financial Decisions
**Why now**: Your retention challenges might be rooted in how users emotionally relate to money decisions in your product.
**The angle**: Not general behavioral economics — specifically how cognitive biases shape financial product engagement.

📖 **Recommended books**:
1. **Misbehaving** by Richard Thaler — The foundational work on behavioral economics in real-world decisions, directly applicable to fintech product design
2. **Dollars and Sense** by Dan Ariely — Practical exploration of irrational money behaviors that affect user engagement

💡 **Key question this topic answers**: Why do users abandon financial tools even when they know those tools help them?

---

### Topic 3: Biomimicry in System Design 🌟 Wildcard
**Why now**: Biological systems have solved retention and engagement over millions of years — ecosystems keep organisms coming back.
**The angle**: How patterns from nature (symbiosis, feedback loops, adaptation) can inspire stickier product design.

📖 **Recommended books**:
1. **Biomimicry** by Janine Benyus — The original work on learning design principles from nature
2. **The Nature of Technology** by W. Brian Arthur — How technology evolves like biological systems

💡 **Key question this topic answers**: What can millions of years of natural selection teach us about building products people can't leave?

---

## Guidelines

- Always include at least one "wildcard" topic — something unexpected that connects to the user's interests in a non-obvious way
- Topics should be specific enough to act on, not vague categories ("The Psychology of Financial Decisions" > "Psychology")
- Each topic's book recommendations should be tailored to the user, not just "best books on this topic"
- The "Why now" should feel personally relevant, not generic
- Include a "top pick" recommendation to reduce decision paralysis
- If user context is too sparse, ask 2-3 clarifying questions before generating recommendations
