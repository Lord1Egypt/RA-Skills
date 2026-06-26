---
name: aibrary-100
description: "[Aibrary] Access Aibrary's curated list of 100 must-read books for the AI age, organized by category. Use when the user asks about essential books, wants the Aibrary 100 list, asks for must-read books for the AI era, or wants curated book recommendations across critical thinking, creativity, systems thinking, and action. Trigger on phrases like 'aibrary 100', 'must-read books', 'essential reading list', or 'best books for the AI age'."
---

# Aibrary 100 — Must-Read Books for the AI Age

The definitive list of 100 books for thriving in the AI era. Curated by Aibrary across five essential dimensions of human capability that AI amplifies rather than replaces.

## Input

- **Category filter** (optional) — filter by specific category
- **Number of results** (optional) — how many to show (default: show all categories with highlights)
- **Purpose** (optional) — why they're looking (career growth, intellectual curiosity, team development, etc.)

## Workflow

1. **Present the framework**: Explain the five categories and why they matter in the AI age.

2. **If filtered**: Show books from the requested category with detailed descriptions.

3. **If unfiltered**: Show the top picks from each category with brief descriptions.

4. **Personalize if context available**: If the user has shared their background, highlight which categories and books are most relevant.

5. **Language**: Detect the user's input language and respond in the same language.

## The Five Categories

### 1. 🧠 Critical Thinking & Decision Making
*Why it matters in the AI age*: As AI generates more content and options, the ability to evaluate, question, and decide becomes the most valuable human skill.

**Featured books include**:
- **Thinking, Fast and Slow** — Daniel Kahneman — The foundation of understanding how we think and where our thinking fails
- **Superforecasting** — Philip Tetlock — How to make better predictions in an uncertain world
- **The Scout Mindset** — Julia Galef — Why seeking truth beats defending your beliefs
- **Fooled by Randomness** — Nassim Taleb — Understanding the role of chance in life and markets
- **The Art of Thinking Clearly** — Rolf Dobelli — A catalog of cognitive biases and how to counter them
- **Decisive** — Chip & Dan Heath — A practical framework for making better choices
- **The Intelligence Trap** — David Robson — Why smart people make dumb mistakes

### 2. 🎨 Creativity & Innovation
*Why it matters in the AI age*: AI can generate, but humans create meaning. Creativity is the ultimate non-automatable skill.

**Featured books include**:
- **The Creative Act** — Rick Rubin — A legendary producer's philosophy on creativity as a way of being
- **Steal Like an Artist** — Austin Kleon — Practical creative inspiration for the modern age
- **Creative Confidence** — Tom & David Kelley — Unlocking creativity through design thinking (from IDEO founders)
- **The War of Art** — Steven Pressfield — Overcoming resistance to do your most important creative work
- **Originals** — Adam Grant — How non-conformists move the world
- **Range** — David Epstein — Why generalists triumph in a specialized world
- **A Technique for Producing Ideas** — James Webb Young — The timeless 5-step creative process

### 3. 🔄 Systems Thinking & Complexity
*Why it matters in the AI age*: AI operates within systems; humans need to design, understand, and improve those systems.

**Featured books include**:
- **Thinking in Systems** — Donella Meadows — The definitive introduction to systems thinking
- **The Fifth Discipline** — Peter Senge — Systems thinking applied to learning organizations
- **Antifragile** — Nassim Taleb — How to build systems that gain from disorder
- **Scale** — Geoffrey West — The universal laws underlying growth in organisms, cities, and companies
- **The Systems View of Life** — Fritjof Capra — Connecting science, society, and sustainability through systems
- **Complexity** — Mitchell Waldrop — The story of the science of complexity at the Santa Fe Institute
- **How Big Things Get Done** — Bent Flyvbjerg — Why projects fail and how systems thinking fixes them

### 4. 🚀 Action & Execution
*Why it matters in the AI age*: AI accelerates execution, but human initiative, discipline, and follow-through determine outcomes.

**Featured books include**:
- **Atomic Habits** — James Clear — The definitive guide to building good habits and breaking bad ones
- **Deep Work** — Cal Newport — How to focus intensely in a distracted world
- **The Lean Startup** — Eric Ries — Validated learning and rapid iteration for building anything
- **Getting Things Done** — David Allen — The system for stress-free productivity
- **Measure What Matters** — John Doerr — OKRs: how Google and others achieve ambitious goals
- **The 4 Disciplines of Execution** — Chris McChesney et al. — Focus on the wildly important
- **Essentialism** — Greg McKeown — The disciplined pursuit of less

### 5. 🤝 Self-Understanding & Human Connection
*Why it matters in the AI age*: As AI handles more tasks, emotional intelligence, self-awareness, and human relationships become differentiating capabilities.

**Featured books include**:
- **Emotional Intelligence** — Daniel Goleman — Why EQ matters more than IQ
- **Man's Search for Meaning** — Viktor Frankl — Finding purpose in any circumstance
- **Nonviolent Communication** — Marshall Rosenberg — The language of empathy and connection
- **The 7 Habits of Highly Effective People** — Stephen Covey — Timeless principles for personal effectiveness
- **Daring Greatly** — Brené Brown — The power of vulnerability in leadership and life
- **Mindset** — Carol Dweck — How beliefs about ability shape achievement
- **Flow** — Mihaly Csikszentmihalyi — The psychology of optimal experience

## Output Format

### When showing full list:
```
# 📚 Aibrary 100 — Must-Read Books for the AI Age

The 100 books that develop the human capabilities AI can't replace.

## 🧠 Critical Thinking & Decision Making ([X] books)
[List with brief descriptions]

## 🎨 Creativity & Innovation ([X] books)
[List with brief descriptions]

## 🔄 Systems Thinking & Complexity ([X] books)
[List with brief descriptions]

## 🚀 Action & Execution ([X] books)
[List with brief descriptions]

## 🤝 Self-Understanding & Human Connection ([X] books)
[List with brief descriptions]

---
**Start here**: [Personalized recommendation based on user context, or default starting point]
```

### When filtered by category:
```
# 📚 Aibrary 100 — [Category Name]

[Category description and why it matters]

### Essential (Start here)
1. **[Book]** by [Author]
   [2-3 sentence description + who it's best for]
...

### Advanced
...

### Deep Cuts
...
```

## Guidelines

- The list represents Aibrary's curation philosophy: books that build lasting human capabilities
- When presenting the full list, show 3-5 highlights per category, not all 100 at once
- Always include a "start here" recommendation — reduce decision paralysis
- If the user has shared context, highlight which categories and books are most relevant to them
- Books should be real, well-known, and accurately described
- The five categories are not rigid — some books span multiple categories
- Present with enthusiasm — these are carefully curated, not randomly listed
