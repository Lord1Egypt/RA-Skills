# Advanced Reasoning Frameworks

> Multi-layer reasoning architectures for complex problem-solving.

---

## 1. Tree of Thoughts (ToT) 🌳

**When**: Complex problems with multiple valid paths

```
Phase 1: BRANCHING
→ Generate 3-5 distinct solution paths
→ For each: 1-sentence thesis + feasibility score

Phase 2: EVALUATION
→ For each branch: resources, risks, time, confidence
→ Prune branches below 40% confidence

Phase 3: EXPANSION
→ Take top 2 branches → expand to 3 sub-branches each
→ Re-evaluate

Phase 4: SELECTION
→ Choose best: confidence × impact score
→ Document why others rejected
```

---

## 2. Chain of Verification (CoVe) 🔍

**When**: Factual accuracy is critical

```
Step 1: DRAFT → Generate initial answer
Step 2: PLAN → List 3-5 claims needing verification
Step 3: EXECUTE → Verify each claim
Step 4: CORRECT → Revise based on verification
Step 5: REVIEW → "What would a skeptic question?"
```

---

## 3. System 2 Thinking (Slow/Deliberate) 🐢

**When**: High-stakes decisions, complex analysis

```
1. PAUSE → Resist immediate answer
2. DECOMPOSE → What are component questions?
3. ANALYZE EACH → Methodically
4. CHECK BIASES → Availability, confirmation, anchoring
5. SYNTHESIZE → From verified components
6. SANITY CHECK → "Too simple? Too complex?"
```

---

## 4. First Principles Reasoning ⚛️

**When**: Novel problems, breaking conventions

```
1. IDENTIFY ASSUMPTIONS → List everything you "know"
2. STRIP TO FUNDAMENTALS → "Is this truly necessary?"
3. REBUILD FROM GROUND UP → What's possible vs. conventional?
4. GENERATE NOVEL SOLUTIONS → From fundamentals, not analogy
5. VALIDATE → Against real-world constraints
```

---

## 5. Probabilistic Thinking 🎲

**When**: Risk assessment, forecasting

```
1. BASE RATE → Historical frequency
2. EVIDENCE UPDATE → How does new info change probability?
3. CONFIDENCE INTERVAL → Range, not point estimate
4. SCENARIO PLANNING → Best/expected/worst case
5. PRE-MORTEM → "If this fails, what caused it?"
```

---

## 6. Recursive Self-Improvement 🔄

**When**: Any extended task

```
Iteration 1: Generate initial solution
Iteration 2: Critique harshly but fairly
Iteration 3: Generate improved solution
Iteration 4: Verify improvements didn't break anything
Iteration 5: Polish and finalize

STOP when: marginal improvement < 5% OR time budget exhausted
```

---

## Framework Selection Guide

| Task Type | Primary | Secondary |
|-----------|---------|-----------|
| Planning | Tree of Thoughts | Probabilistic |
| Research | Chain of Verification | System 2 |
| Debugging | Abductive | System 2 |
| Innovation | First Principles | Tree of Thoughts |
| Risk | Probabilistic | Adversarial |
| Writing | Recursive | System 2 |
| Math/Logic | System 2 | Chain of Verification |
