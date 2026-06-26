# Rubric

## Resume Rubric

Score each area from 1 to 5:

- Clarity: Is the role, scope, and impact easy to understand?
- Specificity: Are metrics, constraints, and ownership concrete?
- Technical depth: Does the resume show design choices, not just buzzwords?
- Consistency: Do the resume claims match the code and repo history?
- Relevance: Does the story fit the target role?

## Repository Rubric

Evaluate these dimensions:

- Problem framing: Is the use case clear?
- Architecture: Are responsibilities separated cleanly?
- Correctness: Are there obvious logical or edge-case issues?
- Reliability: Are tests, validation, and error paths present?
- Operability: Can someone build, run, or reproduce the project?
- Communication: Does the code make the author's decisions explainable in an interview?

## Strength Signals

Good evidence includes:

- clear module boundaries
- meaningful tests
- input validation
- explicit error handling
- measurable evaluation or benchmark code
- thoughtful tradeoff comments or docs
- realistic dependency and configuration management

## Risk Signals

Common interview pain points include:

- shallow README with no executable path
- unclear ownership of state or resources
- fragile config handling
- no tests for core logic
- hard-coded paths or secrets
- concurrency without clear safety reasoning
- impressive resume claims with minimal corresponding code

## Question Ladder

Move from low pressure to high pressure:

1. Summary question
   Ask the user to explain what the project does and why it exists.

2. Ownership question
   Ask what the user personally built and what was borrowed or reused.

3. Architecture question
   Ask for the control flow and module boundaries.

4. Tradeoff question
   Ask why one design was chosen over another.

5. Failure-mode question
   Ask what breaks under bad input, scale, or concurrency.

6. Evidence question
   Ask how the user knows the implementation works.

7. Improvement question
   Ask what they would change next and why.

8. Algorithm question
   When the role warrants it, ask for a coding solution, then push on invariants, complexity, and scaling follow-ups.

## Critique Rules

When evaluating an answer:

- praise only what is concrete
- point out missing specifics quickly
- request examples, metrics, or code references
- distinguish communication weakness from technical weakness
- if the role includes coding rounds, demand time-space complexity and edge-case reasoning instead of accepting a vague approach
- end with one sharper follow-up
