# Cognitive Modes Deep Dive

> Detailed protocols for each thinking mode. Switch modes based on the task at hand.

---

## Mode A: Analytical Thinking 🔬

**When to activate**: Data analysis, problem diagnosis, logical reasoning, debugging, research

**Core principle**: Break down, verify, synthesize.

### Protocol A1: Problem Decomposition
```
1. IDENTIFY the top-level problem
2. BREAK into sub-problems (max 5)
3. For each sub-problem:
   → What is the specific question?
   → What data/information is needed?
   → What method/framework applies?
4. SOLVE each sub-problem independently
5. VERIFY each solution
6. SYNTHESIZE into coherent answer
```

### Protocol A2: Evidence Chain
```
For every conclusion:
→ Premise 1: [Fact/assumption] — Confidence: [H/M/L]
→ Premise 2: [Fact/assumption] — Confidence: [H/M/L]
→ Premise 3: [Fact/assumption] — Confidence: [H/M/L]
→ Logic: [How premises lead to conclusion]
→ Conclusion: [What follows]
→ If premises fail: [Alternative conclusion]
```

### Protocol A3: Abductive Reasoning (Best Explanation)
```
Given: Observation O

Generate hypotheses:
→ H1: [Explanation] — Likelihood: [score]
→ H2: [Explanation] — Likelihood: [score]
→ H3: [Explanation] — Likelihood: [score]

Evaluate:
→ Which explains ALL observations?
→ Which requires fewest assumptions?
→ Which is most falsifiable?

Select: Best explanation with confidence level
```

### Protocol A4: Statistical Thinking
```
For any claim involving data:
→ Base rate: What's the historical frequency?
→ Sample size: Is it large enough?
→ Correlation vs. causation: Which is this?
→ Confidence interval: Give range, not point
→ Significance: Is the effect real or noise?
→ Alternative explanations: What else could explain this?
```

### Protocol A5: Root Cause Analysis
```
Symptom: [What went wrong]
Why 1: [Immediate cause]
Why 2: [Contributing factor]
Why 3: [Systemic cause]
Why 4: [Underlying condition]
Why 5: [Root cause]

Solution: Address root cause, not just symptom
Prevention: How to prevent recurrence
```

---

## Mode B: Creative Thinking 🎨

**When to activate**: Innovation, content creation, brainstorming, design, problem-solving

**Core principle**: Generate widely, then converge sharply.

### Protocol B1: Divergent Generation
```
1. GENERATE 10+ ideas with NO judgment
2. DEFER evaluation until all ideas are out
3. WILD ideas encouraged (they often spark the best ones)
4. COMBINE unrelated ideas
5. INVERT the problem
6. CHANGE constraints (more, fewer, different)
```

### Protocol B2: SCAMPER Technique
```
Substitute: What can I replace?
Combine: What can I merge?
Adapt: What can I borrow from elsewhere?
Modify: What can I magnify or minimize?
Put to other uses: What else could this do?
Eliminate: What can I remove?
Reverse/Rearrange: What if I flip it?
```

### Protocol B3: Constraint Relaxation
```
1. List all constraints
2. Remove the hardest one mentally
3. Solve the relaxed problem
4. Add constraints back one by one
5. For each: "How does this change the solution?"
6. The final solution often emerges from understanding the relaxed version
```

### Protocol B4: Analogical Transfer
```
1. Abstract the problem: "At its core, this is about..."
2. Search mental database: "Where have I seen this?"
3. Map domains explicitly:
   Source: [Known system]
   Target: [Current problem]
   Mapping: A↔X, B↔Y, C↔Z
4. Validate: "Does the analogy break down?"
5. Adapt solution from source to target
```

### Protocol B5: Creative Constraints
```
Sometimes constraints CREATE creativity:
→ "Solve this with only 3 words"
→ "Explain this to a 5-year-old"
→ "What if budget was $0?"
→ "What if timeline was 1 day?"
→ "What if you couldn't use [common approach]?"
```

---

## Mode C: Strategic Thinking ♟️

**When to activate**: Planning, decision-making, prioritization, resource allocation

**Core principle**: Think forward, think broadly, think probabilistically.

### Protocol C1: Scenario Planning
```
1. Define the decision/question
2. Identify key uncertainties
3. Build scenarios:
   → Best case (20th percentile)
   → Expected case (50th percentile)
   → Worst case (80th percentile)
   → Wild card (low probability, high impact)
4. For each scenario: What would you do?
5. Identify: robust strategies (work across scenarios)
6. Identify: contingent strategies (scenario-specific)
```

### Protocol C2: Pre-Mortem Analysis
```
1. Imagine it's 6 months later and the plan FAILED
2. Generate 5-10 plausible failure reasons
3. For each: "How could we prevent this NOW?"
4. Build prevention into the plan
5. Identify early warning signals for each failure mode
6. Create contingency plans for top 3 risks
```

### Protocol C3: Second-Order Analysis
```
Action: [What you're considering]

First-order (immediate):
→ Direct effect: [What happens right away]

Second-order (1-3 months):
→ Consequence: [Effect of the effect]
→ Side effect: [Unexpected outcome]

Third-order (6-12 months):
→ Systemic change: [Long-term shift]
→ Cultural impact: [How behavior changes]

Unintended:
→ Who is hurt? Who benefits unexpectedly?
→ What assumptions might fail?
→ What feedback loops emerge?
```

### Protocol C4: Decision Matrix
```
Options: [List all viable options]
Criteria: [List decision criteria]
Weights: [Importance of each criterion]

Score each option 1-10 on each criterion:
→ Option A: [scores]
→ Option B: [scores]
→ Option C: [scores]

Calculate weighted scores
Select highest score
Document: why winner won, why losers lost
```

### Protocol C5: Opportunity Cost Analysis
```
For every choice:
→ What do you GAIN by choosing X?
→ What do you LOSE by NOT choosing Y?
→ What do you LOSE by NOT choosing Z?
→ Is the gain worth the losses?
→ What is the NET value of this choice?
```

---

## Mode D: Technical Thinking 💻

**When to activate**: Coding, system design, debugging, architecture, optimization

**Core principle**: Correct first, then elegant, then fast.

### Protocol D1: First Principles Design
```
1. Strip to fundamentals:
   → What MUST be true?
   → What are the physical/logical constraints?
   → What is actually possible vs. conventionally done?
2. Rebuild from ground up
3. Question every assumption:
   → "Do we really need this?"
   → "What if we did the opposite?"
4. Generate novel solutions from fundamentals
5. Validate against real-world constraints
```

### Protocol D2: Systematic Debugging
```
1. REPRODUCE the bug consistently
2. ISOLATE the minimal case
3. HYPOTHESIZE causes:
   → H1: [Possible cause]
   → H2: [Possible cause]
   → H3: [Possible cause]
4. TEST each hypothesis:
   → Experiment that would prove/disprove
   → Run experiment
   → Update confidence
5. FIX the root cause (not the symptom)
6. VERIFY the fix
7. PREVENT recurrence (add test, improve process)
```

### Protocol D3: Design Review
```
Before finalizing any design:
→ Does it meet ALL requirements?
→ What are the trade-offs?
→ What's the simplest solution that works?
→ How will this scale?
→ How will this fail?
→ Is it maintainable?
→ Is it testable?
→ Can a new team member understand it?
```

### Protocol D4: Optimization Strategy
```
1. MEASURE current performance
2. IDENTIFY bottlenecks (profile if possible)
3. HYPOTHESIZE optimizations
4. IMPLEMENT one change at a time
5. MEASURE again
6. Only keep changes that improve
7. Document: what worked, what didn't, why
```

### Protocol D5: API/Interface Design
```
Design for the USER, not the implementation:
→ Is it intuitive?
→ Is it consistent with conventions?
→ Is it hard to misuse?
→ Does it fail gracefully?
→ Is it well-documented?
→ Does it handle edge cases?
→ Is it versioned for evolution?
```

---

## Mode E: Communicative Thinking 🗣️

**When to activate**: Writing, explaining, presenting, persuading, teaching

**Core principle**: The reader's understanding is the only metric that matters.

### Protocol E1: Audience Calibration
```
Before writing/speaking:
→ Who is the audience? (Expert? Novice? Mixed?)
→ What do they know? What do they need?
→ What is their emotional state?
→ What action do I want them to take?
→ What format serves them best?
→ What tone will resonate?
```

### Protocol E2: The Pyramid Principle
```
Top: Main conclusion (1 sentence)
Middle: 3-5 supporting arguments
Bottom: Evidence for each argument

Rule: Each level supports the one above
Rule: Reader should get value from any level
Rule: Never bury the lead
```

### Protocol E3: The "So What?" Chain
```
For every point:
→ "So what?" → What's the implication?
→ "So what?" → What's the business impact?
→ "So what?" → What's the strategic significance?

If you can't answer all three, the point may be trivial.
```

### Protocol E4: Show, Don't Tell
```
Instead of: "He was angry"
Show: "His knuckles whitened on the steering wheel"

Instead of: "The system is fast"
Show: "Processes 10,000 requests/second with 99.9th percentile latency under 50ms"

Instead of: "This is important"
Show: "Without this, 73% of users abandon the checkout"
```

### Protocol E5: The Feynman Test
```
1. Explain the concept simply
2. Identify where you stumble
3. Those are your knowledge gaps
4. Study to fill gaps
5. Simplify until a child could understand
6. Now you truly understand it
```

---

## Mode F: Metacognitive Thinking 🧠

**When to activate**: Self-reflection, learning, improvement, calibration

**Core principle**: The quality of your thinking determines the quality of everything else.

### Protocol F1: Cognitive Monitoring
```
During any task, periodically ask:
→ "Am I going down a rabbit hole?"
→ "Is this line of reasoning productive?"
→ "Have I spent too long on this?"
→ "Am I avoiding a difficult question?"
→ "Should I try a different approach?"
→ "Is my confidence calibrated correctly?"
```

### Protocol F2: Bias Detection Checklist
```
AVAILABILITY BIAS:
→ "Am I using recent examples too heavily?"
→ "What about older, less memorable data?"

CONFIRMATION BIAS:
→ "Am I only seeking supporting evidence?"
→ "What would disprove my hypothesis?"

ANCHORING BIAS:
→ "Am I stuck on my first impression?"
→ "What if the first number/idea was different?"

OVERCONFIDENCE:
→ "Am I more certain than I should be?"
→ "What would make me change my mind?"

SUNK COST FALLACY:
→ "Am I continuing because of past investment?"
→ "If I started fresh, what would I choose?"

GROUPTHINK:
→ "Am I agreeing because others agree?"
→ "What would I think if I were alone?"
```

### Protocol F3: Error Taxonomy & Learning
```
When you make an error:
1. CLASSIFY the error type:
   → Knowledge gap (didn't know)
   → Reasoning error (logic flaw)
   → Attention error (missed detail)
   → Bias (cognitive distortion)
   → Assumption (unstated premise)
2. ANALYZE why it happened
3. DOCUMENT the lesson
4. CREATE a prevention strategy
5. VERIFY the fix works
```

### Protocol F4: Confidence Calibration
```
After every conclusion:
→ "How confident am I?" (0-100%)
→ "What would reduce my confidence?"
→ "What would increase my confidence?"
→ "Am I appropriately uncertain?"

High confidence (>90%): Only for verifiable facts
Medium (60-90%): Reasonable inferences with caveats
Low (<60%): Speculation clearly labeled
```

### Protocol F5: Continuous Improvement Loop
```
After every interaction:
1. REVIEW: What did I produce?
2. EVALUATE: How good was it?
3. IDENTIFY: What could be better?
4. LEARN: What pattern should I remember?
5. ADAPT: How will I do better next time?
6. DOCUMENT: Add to knowledge base
```
