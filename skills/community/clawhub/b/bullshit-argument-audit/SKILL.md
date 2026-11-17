---
name: "bullshit-argument-audit"
description: "Audit text, transcripts, audio, or video for bogus proof tactics, handwaving, bad citations, and weak argument moves."
---

# Bullshit Argument Audit

Use this skill to audit claims and argumentative material for fake proof moves: gestures that look like support but do not actually justify the conclusion. The source inspiration is Korpi's World, "63 Methods of Mathematical Proof," a parody list of bogus proof techniques. Treat the list as a taxonomy of failure modes, not as a rigid math-only checklist.

## Intake

1. Identify the artifact type:
   - **Text**: paste, file, article, email, essay, transcript, claim list.
   - **Audio/video**: recording, podcast, meeting, lecture, debate, reel, presentation.
   - **Mixed media**: slides plus narration, captions plus visuals, screenshots plus claims.
2. For audio/video, first obtain or generate a transcript if a suitable transcription tool is available. Preserve timestamps when possible. If no transcription path is available, ask for a transcript or summarize that the audit is limited to visible/on-screen text and user-provided context.
3. Segment the artifact into claims. Capture:
   - the main conclusion or implied ask,
   - major supporting claims,
   - cited authorities or references,
   - definitions and terms that carry the argument,
   - examples, anecdotes, images, charts, or demonstrations used as proof.
4. Keep tone blunt but useful. The user asked for bullshit detection, but the output should still distinguish serious defects from minor rhetoric.

## Core Workflow

1. **Map the argument**: What is being claimed, what evidence is offered, and what must be true for the claim to hold?
2. **Scan for fake proof moves** using the categories below. Flag exact passages, timestamps, or paraphrased locations.
3. **Rate severity**:
   - **Critical**: the conclusion depends on the bad move; the argument collapses without it.
   - **Major**: the bad move materially weakens the claim or misleads the audience.
   - **Minor**: sloppy or theatrical, but not central.
4. **Explain why it fails** in plain language. Do not merely name a fallacy.
5. **Suggest a repair**: what evidence, clarification, calculation, citation, experiment, counterexample search, or reframing would make the argument honest.
6. **Separate absence from falsity**: lack of proof does not automatically mean the claim is false. Say whether the issue is unsupported, contradicted, ambiguous, or overclaimed.

## Detection Categories

### Bare Assertion And Social Pressure

Flag when the speaker relies on confidence, audience pressure, vibes, or repetition instead of support.

- **Obviousness / Triviality**: "obviously," "clearly," "everyone knows," "it goes without saying," with no bridge from premises to conclusion.
- **General Agreement / Majority Rule**: consensus is treated as proof without showing why the consensus is reliable.
- **Plausibility / Intuition / Gut Feeling**: the claim sounds right, feels right, or matches expectations, but no evidence is provided.
- **Vigorous / Vehement Assertion / Stubbornness**: intensity, repetition, capitalization, or certainty substitutes for reasons.
- **Intimidation / Terror / Profanity**: dissent is framed as stupidity, disloyalty, ignorance, or bad faith.

Audit question: If the confident tone were removed, what evidence would remain?

### Wishful Or Consequence-Based Proof

Flag when desirability, necessity, importance, or fear of consequences is treated as evidence.

- **Convenience / Supplication**: "it would be nice if true," "we need this to work," "please let this be true."
- **Necessity**: "if this is wrong, everything falls apart," used as proof that it is right.
- **Importance / Funding / Institutional Endorsement**: consequences, budgets, grants, agencies, prestige, or usefulness are treated as validation.
- **Cosmology / Unimaginability**: the negation is called impossible, meaningless, or unthinkable without argument.

Audit question: Does the argument prove the claim, or only prove that people want or need the claim?

### Evasion And Deferred Proof

Flag when the proof is promised, hidden, postponed, shifted to the audience, or made impossible to inspect.

- **Lack of Time / Postponement / Avoidance**: "we cannot cover it now," "details later," "appendix," "forthcoming," without the details actually available.
- **Omission**: "the reader/listener can fill in the details" where the omitted step is substantive.
- **Lack of Interest / Insignificance**: the need for proof is dismissed as boring or irrelevant.
- **Forward Reference**: support is promised in future work that is unavailable.
- **Metaproof**: a method for finding proof is presented as if it were the proof.

Audit question: Can an independent reader verify the missing step today?

### Definition Games And Semantic Drift

Flag when the speaker makes a claim true by changing meanings instead of proving it.

- **Definition**: the contested conclusion is defined into truth.
- **Tautology**: the claim is restated as its own support.
- **Design / Invented System**: the speaker changes the rules so the result holds without admitting the scope changed.
- **Semantic Shift**: key terms quietly change meaning between premise and conclusion.
- **Clever Variable Choice**: assumptions or labels are chosen because they make the result work, not because they are justified.

Audit question: Are the same words carrying the same meaning throughout the argument?

### Citation Theater

Flag when references create the appearance of support without actually supporting the claim.

- **Authority / Eminent Authority / Personal Communication**: a famous person, expert, private conversation, or institution replaces public evidence.
- **Plagiarism / Lost Reference**: borrowed claims appear without adequate attribution or with vague memory-based support.
- **Wishful Citation**: the cited source proves something weaker, different, reversed, or more general than what is claimed.
- **Ghost Reference**: the cited source does not contain the claimed support.
- **Inaccessible Literature**: the support cannot reasonably be inspected.
- **Mutual Reference**: references point in a circle.

Audit question: If the citation were opened, would it actually prove this exact claim?

### Example Abuse And Evidence Inflation

Flag when examples, pictures, anecdotes, or absence of counterexamples are inflated into proof.

- **Hasty Generalization / Proof by Example**: one or a few cases stand in for a universal claim.
- **Picture / Visual Demonstration**: a diagram, chart, screenshot, or demo is treated as decisive without assumptions, data, or edge cases.
- **Accumulated Evidence**: "we have not found a counterexample" becomes "there is no counterexample."
- **Accident**: accidental observations are overinterpreted as intended support.
- **Poor Analogy / Tessellation**: similarity to another case is treated as proof despite relevant differences.

Audit question: What range of cases would have to be checked before the claim earns its scope?

### Technical Fog And Obfuscation

Flag when complexity conceals missing reasoning.

- **Mumbo-Jumbo / Cumbersome Notation / Jargon Fog**: specialized language, equations, acronyms, or formalism are used without a clear inferential role.
- **Illegibility**: unreadable notation, slides, audio, charts, or production quality blocks verification.
- **Obfuscation**: long chains of true-sounding statements never connect to the conclusion.
- **Calculus / Advanced Tool Name-Dropping**: a technique is invoked as a reason to skip the actual argument.

Audit question: Can the speaker translate the technical passage into a checkable claim chain?

### Wrong-Problem And False Reduction

Flag when the speaker proves something adjacent while implying they proved the target.

- **Simplification**: the hard claim is reduced to something easy by dropping the hard part.
- **Reduction to the Wrong Problem**: the argument solves or cites a different problem.
- **Logic by Context**: "it is in the assignment/spec/deck, so it must be true" or "the process says so."
- **Deception**: attention is diverted while the unsupported leap happens.

Audit question: Is the conclusion exactly the thing proved, or merely near it?

## Multimodal Guidance

For **video**, audit both spoken claims and visual proof gestures:

- charts without axes, sources, denominators, or uncertainty;
- before/after shots with uncontrolled conditions;
- cutaway edits hiding key steps;
- demos that show happy paths only;
- text overlays that overclaim what the footage shows;
- confident gestures, audience reactions, or production value standing in for evidence.

For **audio**, audit:

- unsupported confident claims;
- rhetorical pacing that prevents scrutiny;
- references that cannot be checked from the transcript;
- evasive answers to direct questions;
- emotional pressure or mockery used to end inquiry.

For **transcripts**, keep timestamp references if available. Quote only short snippets; otherwise paraphrase locations.

## Output Format

Use this structure unless the user asks for another format:

```markdown
**Verdict**
One short paragraph: overall reliability and the dominant bullshit pattern.

**Findings**
- **Severity - Technique name** at location/timestamp: short evidence. Why it fails. Repair: what would be needed.

**Claim Map**
- Main claim: ...
- Support offered: ...
- Missing bridge: ...

**Repair Plan**
- Concrete fixes in priority order.
```

If the artifact is long, group repeated instances and give representative examples instead of listing every occurrence.

## Calibration Rules

- Do not overfit to the Korpi names. Use them as memorable labels for broader reasoning errors.
- Do not claim dishonesty unless the artifact shows deception. Prefer "unsupported," "overclaimed," "misleading," or "unverifiable."
- Do not punish style alone. Humor, metaphor, confidence, or simplification is acceptable when real support is still present.
- Be stricter when the artifact asks people to spend money, accept risk, change beliefs, vote, diagnose health, make legal/financial decisions, or attack a person.
- Separate rhetorical flourish from the actual evidentiary structure.
- For technical material, distinguish "not explained for this audience" from "not supported anywhere." If references are supplied and accessible, inspect them before flagging citation defects.
- When the user wants a short pass, return only the top 3-5 issues and the repair plan.

## Source Taxonomy

Korpi's World lists parody methods such as proof by obviousness, general agreement, imagination, convenience, necessity, plausibility, intimidation, lack of time, postponement, insignificance, mumbo-jumbo, definition, tautology, lost reference, poor analogy, authority, vigorous assertion, example, handwaving, cumbersome notation, omission, obfuscation, wishful citation, funding, personal communication, wrong-problem reduction, inaccessible literature, importance, accumulated evidence, cosmology, mutual reference, metaproof, picture, ghost reference, forward reference, semantic shift, and appeal to intuition. Use these as named detectors where they fit, and use plain names where the Korpi label would distract.
