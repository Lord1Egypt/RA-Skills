---
name: "fake-math-proof-audit"
description: "Audit mathematical proofs or proof-like arguments for Korpi's 63 fake proof methods and explain exact proof defects."
---

# Fake Math Proof Audit

Use this skill to audit mathematical proofs and proof-like technical arguments against Korpi's 63 fake proof methods. This skill is intentionally narrower than `bullshit-argument-audit`: stay close to the numbered Korpi methods and explain the mathematical proof defect.

## Required Reference

Read `references/korpi-63-methods.md` whenever the user asks for a full taxonomy pass, names one of the fake proof methods, asks "which method is this?", or provides a proof longer than a few paragraphs.

## Core Workflow

1. Identify the mathematical claim being proved.
2. Extract the stated assumptions, definitions, lemmas, transformations, diagrams, examples, citations, and conclusion.
3. Check whether each step follows from earlier steps, definitions, accepted theorems, or a valid inference rule.
4. Match suspicious moves to the closest Korpi method number and name. Prefer the exact numbered label when it fits.
5. Explain the defect in proof terms: missing lemma, unjustified quantifier leap, circularity, invalid generalization, undefined term, semantic shift, non sequitur, unverifiable citation, appeal to authority, or proof of a different statement.
6. Separate style from substance. A terse proof is not fake if the omitted step is genuinely standard for the audience; a long formal-looking proof is fake if the inference chain fails.
7. Offer a repair path: the exact missing statement, lemma, condition, counterexample check, citation, definition, or proof strategy needed.

## Output Format

Use this format by default:

```markdown
**Verdict**
Short reliability judgment: valid, likely valid but underspecified, incomplete, invalid, or not a proof.

**Detected Fake Proof Methods**
- **#N - Method Name** at step/location: evidence. Why this is not a proof. Repair: what would be needed.

**Proof Gap Map**
- Claim: ...
- Given assumptions: ...
- Missing or invalid step: ...
- Minimum repair: ...
```

For a short proof, give the top 1-3 methods. For a long proof or paper, group repeated instances and keep representative examples.

## Calibration

- Do not force a Korpi label when the proof is simply wrong in an ordinary way; explain the ordinary defect and say no special Korpi method is needed.
- Do not call something plagiarism, deception, or ghost reference unless the evidence supports that stronger label.
- Treat examples and pictures as explanatory aids, not defects, when a real general argument accompanies them.
- Treat authority and citations as supporting context only; a proof still needs a valid inference chain unless the task is explicitly literature review.
- For formal math, be careful with quantifiers. Many fake methods hide in moves from "some" to "all," finite to infinite, generic examples to universal claims, or changed definitions.
- For lecture notes and homework, tolerate standard omissions only when the omitted theorem is obvious for the course level. Otherwise flag as #45 Proof by Omission.

## Relationship To Broad Argument Audits

Use this skill for math proofs and proof-like technical derivations. Use `bullshit-argument-audit` for general essays, debates, podcasts, political claims, business claims, or non-mathematical rhetoric. If the user asks to apply the 63 fake methods metaphorically to non-math text, use this skill but state that the mapping is metaphorical.
