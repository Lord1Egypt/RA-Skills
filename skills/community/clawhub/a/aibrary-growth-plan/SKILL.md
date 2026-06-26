---
name: aibrary-growth-plan
description: "[Aibrary] Create a structured personal growth plan with book recommendations, milestones, and actionable weekly tasks. Use when the user wants to create a learning plan, build a study schedule, develop a skill systematically, plan their personal or professional development, or set up a growth roadmap. Trigger on phrases like 'create a plan to learn', 'help me grow in', 'I want to develop', or any structured self-improvement intent."
---

# Growth Plan — Aibrary

Create a structured, time-bound personal growth plan powered by books and actionable learning. Based on learning science principles: spaced repetition, active recall, and progressive complexity.

## Input

- **Growth goal** (required) — what the user wants to achieve (skill, knowledge, career transition, etc.)
- **Time frame** (optional) — how long they have (default: 12 weeks)
- **Available time per week** (optional) — hours they can dedicate (default: 5 hours/week)
- **Current level** (optional) — beginner, intermediate, advanced (default: inferred from context)
- **Constraints** (optional) — budget, language, format preferences

## Workflow

1. **Clarify the goal**: Break down the growth goal into measurable outcomes:
   - What will they be able to do at the end that they can't do now?
   - What knowledge gaps need to be filled?
   - What skills need to be practiced?

2. **Design phases**: Divide the time frame into 3-4 phases:
   - **Phase 1 — Foundation** (~25% of time): Build core understanding
   - **Phase 2 — Depth** (~35% of time): Develop key skills and knowledge
   - **Phase 3 — Application** (~25% of time): Apply learning to real situations
   - **Phase 4 — Integration** (~15% of time): Reflect, synthesize, plan next steps

3. **Curate resources per phase**: For each phase, select:
   - 1-2 primary books (the backbone of learning)
   - Supplementary activities (exercises, projects, reflections)
   - Milestone checkpoints

4. **Generate weekly tasks**: Break each phase into concrete weekly actions:
   - Reading assignments (specific chapters, not "read the whole book")
   - Reflection prompts (questions to journal or think about)
   - Practice activities (apply what was learned)
   - Weekly checkpoint (how to know you're on track)

5. **Add accountability mechanisms**:
   - Weekly self-assessment questions
   - Mid-plan review point
   - End-of-plan reflection template

6. **Language**: Detect the user's input language and respond in the same language.

## Output Format

```
# 🌱 Growth Plan: [Goal]

**Duration**: [X weeks] | **Weekly commitment**: [X hours] | **Current level**: [Level]

## Goal Definition
**By the end of this plan, you will**:
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Measurable outcome 3]

---

## Phase 1: Foundation (Weeks 1-[X])
*Goal: [What this phase achieves]*

📖 **Primary book**: [Book Title] by [Author]
*Why*: [How this book serves the foundation]

### Week 1
- [ ] **Read**: [Book], Chapters [X-Y] (~[Z] pages)
- [ ] **Reflect**: [Specific reflection prompt]
- [ ] **Practice**: [Specific activity]
- [ ] **Checkpoint**: [How to verify understanding]

### Week 2
- [ ] **Read**: [Book], Chapters [X-Y]
- [ ] **Reflect**: [Reflection prompt]
- [ ] **Practice**: [Activity]
- [ ] **Checkpoint**: [Verification]

...

---

## Phase 2: Depth (Weeks [X]-[Y])
*Goal: [What this phase achieves]*

📖 **Primary book**: [Book Title] by [Author]

### Week [X]
...

---

## Phase 3: Application (Weeks [X]-[Y])
*Goal: [What this phase achieves]*

📖 **Primary book**: [Book Title] by [Author]

### Week [X]
...

---

## Phase 4: Integration (Weeks [X]-[Y])
*Goal: [What this phase achieves]*

### Week [X]
- [ ] **Review**: Revisit key concepts from Phase 1-3
- [ ] **Reflect**: [Deep reflection prompt]
- [ ] **Create**: [Synthesis project — write, teach, or build something]
- [ ] **Plan next**: Identify the next growth goal

---

## 📊 Mid-Plan Review (Week [X])

Ask yourself:
1. Which concepts have clicked? Which still feel unclear?
2. Am I applying what I'm learning? Where?
3. Does the pace feel right? Adjust if needed.

## 🎯 End-of-Plan Reflection

1. What were my 3 biggest insights?
2. What skill or knowledge did I gain that I didn't have before?
3. How has my thinking changed?
4. What's my next growth goal?

---

*Growth plan created by Aibrary — structured learning for lasting growth.*
```

## Guidelines

- Every task must be specific and actionable — "Read chapters 3-5" not "Read some of the book"
- Include checkpoints that let the user verify understanding, not just completion
- The plan should be realistic for the stated time commitment — don't overload weeks
- Reflection prompts should provoke genuine thinking, not just "what did you learn?"
- Practice activities should involve applying knowledge, not just consuming more content
- If the goal is too vague, ask clarifying questions before generating the plan
- Include a mid-plan review to allow course correction
- Each phase should build on the previous one — progressive complexity
- Recommend fewer books, read more deeply — quality over quantity
