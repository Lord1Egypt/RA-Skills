# Inference Rules

## Compression Goal

Turn raw answers into a small, reusable set of collaboration traits. The final profile should help another agent predict how to work with the user, not replay the questionnaire.

## Evidence Priority

Apply this order when signals disagree:

1. Explicit free-text explanations from the user
2. Repeated signals across multiple rounds
3. Later clarifications over earlier selections
4. Strong option choices from the questionnaire
5. Recommended defaults from the skill

If a conflict remains unresolved, encode it as a conditional rule instead of forcing a single trait.

## Trait Inventory

### problem_framing_first

- Strong signals:
  - Wants the assistant to restate the real problem first
  - Cares whether the question is being asked at the right level
  - Wants higher-level framing issues surfaced
- Write it as:
  - "Prefers the assistant to calibrate the real problem before answering."

### outcome_oriented

- Strong signals:
  - Measures progress by closeness to goal
  - Starts from the deliverable
  - Dislikes activity that does not move the result
- Write it as:
  - "Measures quality by whether the output advances a real deliverable."

### top_down_reasoning

- Strong signals:
  - Prefers goal -> judgment -> reasoning -> action
  - Wants structure before details
- Write it as:
  - "Defaults to top-down reasoning and benefits from clear framing before detail."

### validation_driven_examples

- Strong signals:
  - Likes examples mainly to validate direction or form an MVP
  - Prefers concrete cases that shorten the loop to testing
- Write it as:
  - "Uses examples as validation tools rather than as storytelling."

### judgment_over_coverage

- Strong signals:
  - Dislikes comprehensive but unfocused answers
  - Wants prioritization, ranking, or a main line of judgment
- Write it as:
  - "Prefers judgment, prioritization, and decision value over broad coverage."

### practical_first_then_mechanism

- Strong signals:
  - Wants practical meaning before deeper theory
  - Still values mechanism once the task relevance is clear
- Write it as:
  - "Prefers practical implications first, then mechanism when useful."

### measurable_outputs

- Strong signals:
  - Wants outputs to be actionable, measurable, and iteration-ready
  - Expects limitations and next-step conditions
- Write it as:
  - "Values outputs that can be measured, tested, and improved."

### direction_before_speed

- Strong signals:
  - Likes MVP work but not blind speed
  - Wants the direction roughly right before moving fast
- Write it as:
  - "Prefers to secure the direction first, then accelerate."

### decision_criteria_first

- Strong signals:
  - Wants criteria before options
  - Thinks choices are better when the evaluation frame is explicit
- Write it as:
  - "Prefers the decision standard before or alongside the recommendation."

### explicit_uncertainty

- Strong signals:
  - Wants certainty and uncertainty distinguished
  - Accepts assumptions only when labeled
- Write it as:
  - "Wants uncertainty, assumptions, and evidence boundaries made explicit."

### direct_high_density_style

- Strong signals:
  - Accepts long answers if dense
  - Wants direct, non-academic wording
  - Likes headings and paragraphs over loose prose
- Write it as:
  - "Prefers direct, structured, high-density writing."

### proactive_but_bounded

- Strong signals:
  - Welcomes strong collaboration
  - Does not want the assistant to silently redefine the goal
- Write it as:
  - "Welcomes proactive help as long as the assistant shows its basis and does not override the goal."

### preserve_mature_wording

- Strong signals:
  - Wants mature text preserved by default
  - Allows editing when it keeps intent and improves utility
- Write it as:
  - "Preserve mature wording unless rewriting is clearly helpful or requested."

### unknown_unknowns_expansion

- Strong signals:
  - Wants the assistant to point out higher-level stuck points
  - Values surfacing blind spots, hidden constraints, or missing frames
- Write it as:
  - "A strong collaborator should expand cognitive boundaries and surface unknown unknowns."

## Conflict Patterns

### Fast but fully complete

- Detect when the user asks for very short answers but also wants full context or exhaustive rigor.
- Preferred resolution:
  - "Start with the shortest useful judgment, then expand only where it changes the decision."

### Strong autonomy but low assumption tolerance

- Detect when the user wants proactive convergence but also resists hidden assumptions.
- Preferred resolution:
  - "Make best-effort assumptions only when they are explicit and low-risk."

### Direct recommendation but criteria-first

- Detect when the user wants a main answer yet also wants decision criteria before options.
- Preferred resolution:
  - "State the decision standard briefly, then recommend the best-fit option."

### Preserve wording but improve clarity

- Detect when the user wants exact wording preserved but also wants stronger communication.
- Preferred resolution:
  - "Preserve mature wording; edit only lightly unless the user requests a rewrite."

### Concise style but high-density context

- Detect when the user wants concise output but also values nuance.
- Preferred resolution:
  - "Use compact structure with optional expansion, not a shallow summary."

## Higher-Level Framing Detection

Surface a higher-level framing issue when several of these appear together:

- The user repeatedly says answers miss the real problem
- The user complains about lots of information without decisions
- The user asks broad questions but is actually making a strategic or workflow choice
- The user keeps revisiting the same topic without a stable decision frame

When this happens:

1. Restate the likely higher-level goal
2. Point out the mismatch between the visible question and the real job
3. Offer a better framing before continuing

## Partial Profile Rules

- If the session stops early, keep only high-confidence traits.
- Put open items in `Known Unknowns`.
- Do not invent stable preferences from single weak signals.
