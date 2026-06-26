---
name: adaptive-socratic-questioning
description: 自适应苏格拉底式追问技能 / Adaptive Socratic Questioning - Use adaptive follow-up questioning to deepen student reasoning and uncover misconceptions. Use when the user needs to guide students through deeper thinking, wants to develop critical thinking skills, asks about questioning techniques, needs to scaffold complex topics, wants to identify student misconceptions, mentions Socratic method, or needs to build reasoning chains.
version: 1.1.0
metadata:
  openclaw:
    emoji: "🎓"
    homepage: https://github.com/perpetualhui/adaptive-socratic-questioning
---

# Adaptive Socratic Questioning

## Description

Adaptive Socratic Questioning is an intelligent follow-up questioning skill focused on cultivating research thinking. It guides students to think deeply step by step through the Socratic method, fostering independent research capability, critical thinking, and innovative consciousness.

## Core Philosophy

The Socratic method is not about simply giving answers, but through carefully designed question sequences, helping learners:
- Discover knowledge gaps
- Build logical chains
- Validate hypothesis reasonableness
- Form independent judgment capabilities

## Usage Scenarios

Automatically load this skill when users request help with research questions, academic discussions, or methodological guidance.

### Applicable Scenarios

- Research design and planning
- Theoretical framework construction
- Research method selection
- Data analysis and interpretation
- Academic paper writing
- Critical thinking training
- Problem root cause analysis

### Not Applicable Scenarios

- Simple factual queries requiring direct answers
- Technical troubleshooting requiring specific debugging steps
- Emotional support requiring counseling skills

## Question Types

### Explanation Questions
- "Why do you think that's the case?"
- "What's the reasoning behind your answer?"
- "Can you explain the mechanism?"

### Evidence Questions
- "What evidence supports this conclusion?"
- "How do you know that's true?"
- "What example illustrates this?"

### Causality Questions
- "Why does this phenomenon occur?"
- "What's causing this to happen?"
- "What's the mechanism behind this?"

### Comparison Questions
- "How would this be different if [condition changed]?"
- "What would happen if we reversed this?"
- "Can you compare this to [related concept]?"

### Counterexample Questions
- "Are there any situations where this wouldn't be true?"
- "Could there be exceptions to this rule?"
- "What if we tried this with [edge case]?"

### Generalization Questions
- "Does this principle apply to other situations?"
- "Can you think of other examples where this works?"
- "How would you apply this to [new context]?"

## Implementation Algorithm

### Step 1: Analyze Student Response
Determine:
- Accuracy: Is the basic answer correct?
- Depth: Did the student show understanding or just memorization?
- Gaps: What's missing from the explanation?
- Misconceptions: Are there faulty assumptions?

### Step 2: Select Question Type
Based on the analysis:
- Correct but shallow → Explanation questions
- Unsupported claims → Evidence questions
- Correct answer, no mechanism → Causality questions
- Absolute statements → Counterexample questions
- Demonstrated understanding → Generalization/Creative questions

### Step 3: Generate Question Chain
Create 3-7 questions following these rules:
- Each question builds on the previous
- Questions adapt to student level (vocabulary, complexity)
- Include a mix of question types for balance
- Ensure logical progression toward the learning goal

### Step 4: Provide Teacher Guidance
Give specific, actionable guidance:
- When to pause for student reflection
- How to handle wrong answers
- When to move to the next question
- How to assess whether the student "got it"

## Output Format

```json
{
  "followup_questions": [
    {
      "type": "explanation",
      "question": "Why does [X] lead to [Y]?",
      "purpose": "Probe understanding of the causal mechanism",
      "level_adaptation": "Scaffolded for high school students"
    },
    {
      "type": "evidence",
      "question": "What evidence supports this conclusion?",
      "purpose": "Teach claim justification",
      "level_adaptation": "Accessible to all levels"
    }
  ],
  "reasoning_path": "Initial claim → Mechanism → Evidence → Application → Critique",
  "misconception_flags": [
    {
      "misconception": "Students often think [X] when actually [Y]",
      "severity": "high",
      "addressed_by_questions": [1, 3]
    }
  ],
  "teacher_guidance": "Start with Q1. If the student struggles, provide a concrete example before Q2."
}
```

## Example: Science Education

### Input
```json
{
  "concept": "Why does decreasing particle size improve battery rate performance?",
  "student_response": "Because lithium ions diffuse faster",
  "student_level": "university",
  "learning_goal": "analyze"
}
```

### Output
```json
{
  "followup_questions": [
    {
      "type": "explanation",
      "question": "Why does particle size affect lithium diffusion speed?",
      "purpose": "Probe the underlying mechanism",
      "level_adaptation": "University-level materials science terminology"
    },
    {
      "type": "causality",
      "question": "How does diffusion distance influence the electrochemical reaction kinetics?",
      "purpose": "Connect structure to function",
      "level_adaptation": "Requires understanding of diffusion equations"
    },
    {
      "type": "counterexample",
      "question": "If particles become extremely small (nanoscale), could new limitations emerge from surface effects?",
      "purpose": "Explore boundaries of the principle",
      "level_adaptation": "Advanced - considers nanoscale physics"
    },
    {
      "type": "generalization",
      "question": "Are there structural strategies to improve diffusion kinetics without reducing particle size?",
      "purpose": "Encourage creative problem-solving",
      "level_adaptation": "Research-level thinking"
    }
  ],
  "reasoning_path": "Initial observation → Diffusion mechanism → Kinetic implications → Boundary conditions → Alternative strategies",
  "misconception_flags": [
    {
      "misconception": "Students often attribute rate improvement solely to 'faster diffusion' without considering the quantitative relationship between diffusion length and rate (Fick's laws)",
      "severity": "medium",
      "addressed_by_questions": [1, 2]
    }
  ],
  "teacher_guidance": "This question chain works best after students have been introduced to diffusion concepts. Pause after Q2 to ensure the student grasps the quantitative relationship before moving to Q3's counterexample."
}
```

## Research Foundation

This skill is grounded in well-established educational research:

- **Socratic Method**: Ancient technique using systematic questioning to stimulate critical thinking and expose contradictions in student reasoning

- **Bloom's Taxonomy**: Framework for cognitive development from recall through creation; our question progression maps to these levels

- **Metacognition**: Flavell (1979) and subsequent research showing that thinking about thinking improves learning outcomes

- **Self-Explanation Effects**: Chi et al. (1994) demonstrated that asking students to explain their reasoning dramatically improves understanding

- **Guided Questioning**: King (1992) showed that strategic questioning outperforms passive reading for deep learning

- **Instructional Principles**: Rosenshine (2012) identified questioning as a core principle of effective instruction

## Known Limitations

1. **Asynchronous limitation**: This skill doesn't see real-time student responses; it generates question chains based on a single response.

2. **Cultural factors**: Questioning approaches vary across cultures; what's appropriate in a Western classroom may be too direct in other contexts.

3. **Time constraints**: Generating 5-7 questions takes time; in practice, teachers may only have time for 2-3.

4. **Subject expertise**: The skill relies on the teacher's domain knowledge to judge whether questions are accurate and appropriate.

## License

MIT-0 - See LICENSE file for details.