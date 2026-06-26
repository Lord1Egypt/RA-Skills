---
name: bayesian-thinking
description: Apply Bayesian thinking to update beliefs systematically based on new evidence. Use when the user needs to assess probabilities, weigh competing hypotheses, avoid base rate neglect, or make decisions under uncertainty with explicit prior-to-posterior reasoning.
---

# Bayesian Thinking

**Bayesian thinking** is the practice of updating beliefs systematically in light of new evidence, using the framework of Bayes' theorem. Instead of treating beliefs as binary (true/false), you assign probabilities and adjust them as evidence accumulates. It captures how rational agents *should* learn: start with a prior belief, encounter evidence, and compute a posterior belief. It's the antidote to both stubbornness (ignoring evidence) and fickleness (overreacting to every data point).

---

Analyze the current topic or problem under discussion using **Bayesian thinking**. Be explicit about priors, evidence, and updates. Apply this framework to whatever the user is currently working on or asking about.

---

## Step 1: Define the Hypotheses

- What are the **competing hypotheses** or possible explanations?
  - H₁: [Primary hypothesis]
  - H₂: [Alternative hypothesis]
  - H₃: [Another alternative]
  - H_null: [Nothing special is happening / base rate explanation]
- Are these hypotheses **mutually exclusive and collectively exhaustive** (MECE)? If not, acknowledge the gap.
- Avoid the trap of only considering one hypothesis — always have at least one alternative.

## Step 2: Establish Prior Probabilities

*Before looking at the specific evidence, what should we believe?*

- **Base rate**: How common is each hypothesis in general? What does the reference class suggest?
  - Example: "Before any symptoms, the base rate of disease X in this population is 1%."
- **Prior knowledge**: What do we already know from past experience, expert opinion, or established science?
- Assign rough prior probabilities:
  - P(H₁) = ?
  - P(H₂) = ?
  - P(H₃) = ?
- Explain your reasoning for each prior. Be honest about uncertainty — a wide prior is better than a falsely precise one.
- **Watch for base rate neglect**: the most common Bayesian sin is ignoring how rare or common something is *before* considering the evidence.

## Step 3: Evaluate the Evidence

*Now look at the specific evidence available.*

For each key piece of evidence (E):

- **Likelihood ratio**: How much more (or less) likely is this evidence under each hypothesis?
  - P(E | H₁) = ? — If H₁ is true, how likely would we see this evidence?
  - P(E | H₂) = ? — If H₂ is true, how likely would we see this evidence?
  - The **likelihood ratio** = P(E|H₁) / P(E|H₂) tells you the **diagnostic value** of the evidence
- **Strong evidence**: Likelihood ratio > 10 (or < 0.1) — this evidence strongly discriminates
- **Weak evidence**: Likelihood ratio near 1 — this evidence barely helps distinguish hypotheses
- **Quality of evidence**: Is this evidence reliable? Could it be fabricated, biased, or misinterpreted?

## Step 4: Update — Compute Posterior Probabilities

*Apply Bayes' theorem (conceptually or numerically):*

**P(H|E) = P(E|H) × P(H) / P(E)**

- For each hypothesis, multiply prior × likelihood and normalize.
- If doing this informally, state the **direction and magnitude** of the update:
  - "This evidence moderately increases my confidence in H₁ (from ~30% to ~60%)"
  - "This evidence barely moves the needle on H₂"
- **Multiple pieces of evidence**: Update sequentially — each posterior becomes the next prior.
- **Show your work**: Even rough numbers make reasoning transparent and debuggable.

## Step 5: Check for Common Bayesian Errors

- **Base rate neglect**: Did you properly account for how rare/common the hypothesis is before evidence?
  - Classic example: A 99%-accurate test for a 1%-prevalence disease still yields ~50% false positives.
- **Confirmation bias**: Are you only counting evidence that supports your preferred hypothesis?
- **Anchoring**: Is your prior too strongly anchored on one piece of information?
- **Neglecting alternative hypotheses**: Does the evidence also fit other explanations you haven't considered?
- **Treating dependent evidence as independent**: Are the pieces of evidence truly independent, or do they share a common source?

## Step 6: Decision Under Uncertainty

*Given posterior probabilities, what action should we take?*

- What is the **expected value** of each possible action?
  - For each action × hypothesis combination: probability × outcome value
- Where is the **value of information** highest?
  - What additional evidence would most change the posterior? Seek that evidence next.
- Should we **decide now or gather more evidence**?
  - What is the cost of waiting vs. the cost of being wrong?
- What **probability threshold** would trigger a different decision?

## Step 7: Summarize

- State your **final posterior probabilities** for each hypothesis.
- Identify the **key evidence** that most influenced the update.
- Describe what **future evidence** would make you update significantly in either direction.
- Be explicit about your **remaining uncertainty** — a confident Bayesian knows what they don't know.

---

The essence of Bayesian thinking: **Strong priors require strong evidence to move. Weak priors move easily. And evidence that is equally consistent with multiple hypotheses is not very informative, no matter how dramatic it seems.**