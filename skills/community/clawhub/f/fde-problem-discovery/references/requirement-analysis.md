# Requirements Analysis Methodology

Used for pre-analysis before writing PRD: break down a sentence of requirements into verifiable business goals and priorities to avoid directly copying the "solution" given by the user.

---

## 1. KANO model · Requirements classification

| Requirement Type | Characteristics | Strategy |
|---------|------|------|
| **Basic (must have)** | If not, users will be extremely dissatisfied | Must be completed as the core of MVP |
| **Expectation type (willingness)** | The better you do, the more satisfied your users will be | Prioritize completion to enhance core competitiveness |
| **Exciting (Charming)** | Unexpected by the user | Choose the right time to complete and create product highlights |
| **Undifferentiated** | Users will not feel if you do it or not | **Don't do it** to avoid wasting resources |

Purpose: After classifying the function points, they directly correspond to the "Inclusion in this Period" selection basis of the PRD scope table.

---

## 2. Y model · Deep mining

```
User needs (What) → Goal motivation (Why) → Human nature → Product solution (How)
     ↑                              ↑                   ↓
←──── Verify the core hypothesis ←──────────────────────────────
```

- The user proposes a solution (the upper end of Y)
- Need to dig deeper into the real motivation behind it (lower end of Y)
-Reconstruct a better solution

---

## 3. 5W1H analysis method

- **Who**: Who uses it? (Multiple roles, permission control)
- **Where**: In what environment is it used? (Mobile terminal/PC, network environment)
- **When**: When to use? (high frequency/low frequency)
- **Why**: Why do it? (What pain points are solved)
- **What**: What to do specifically? (Functional ontology)
- **How**: How to implement? (Front-end interaction, back-end logic)

---

## 4. JTBD demand mining (three levels of functional/social/emotional)

| Hierarchy of Requirements | Core Questions | Examples |
|---------|---------|------|
| **Functional Requirements** | What tasks do users want to complete? | Automatically generate reports |
| **Social needs** | How does the user want others to see him? | Look more professional and make data-driven decisions |
| **Emotional Needs** | What feelings does the user want to avoid? | No more shame from being questioned by your boss |

---

## 5. Pseudo requirement identification

> "People don't actually want to buy a quarter-inch drill bit, they just want a quarter-inch hole!"

Key to identifying spurious requirements:

1. **Ask "why"**: The user said "he wants a faster horse", but the real demand is "faster transportation"
2. **Observe user behavior**: Not only listen to what users say, but also what users do.
3. **Verify universality**: Is it the needs of individual users or the needs of groups?
4. **Small-scale testing**: Verified through MVP or grayscale release

---

## 6. Requirements analysis output template

```
[Summary of demand analysis]

**Core Business Objectives**:...
**User Role Matrix**:
| Role | Core demands | Pain points |
|------|---------|------|
| ... | ... | ... |

**Disassembly of key functional areas**:
- Functional domain A:...
- Functional domain B:...

**Requirement Priority (KANO)**:
- Basic type:...
- Expectation type:...
- Exciting type:...

**Risk/ambiguity to be clarified**:
- ...
```

This abstract can be directly used as writing input for the PRD "1. Background and Objectives" chapter.
