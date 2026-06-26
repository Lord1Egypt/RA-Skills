# Throughline Patterns

Use this file when `outline/chapter_briefs.jsonl` is hard to convert into one lead block.

## Field-to-move mapping

### `throughline`

Use it to answer:
- what shared question this chapter is really asking
- why the H3 subsections belong together

Good transformation:
- convert a topic list into one comparison problem

Example transformation:
- weak input: `state management`, `deliberation`, `feedback loops`
- stronger throughline: `The chapter compares how systems preserve decision quality once intermediate state, delayed feedback, and multi-step control must all be managed together.`

### `key_contrasts`

Use it to choose 2-3 recurring contrasts that can appear in the lead.

Good contrasts are:
- comparative
- reusable across several H3 subsections
- readable as prose rather than labels

Prefer:
- `fixed structure versus runtime adaptation`
- `richer state versus easier verification`
- `local gains versus transfer under tighter constraints`

Avoid:
- copied slash lists
- internal planner labels
- contrast inventories longer than the lead can hold naturally

### `lead_paragraph_plan`

Use it to decide progression.

Good use:
- interpret the plan as movement in the argument, not as a miniature table of contents

Example:
- weak use: `first cover setup, then methods, then evaluation`
- stronger use: `move from the source of the bottleneck to the design choices it induces, then to the conditions under which those choices remain comparable`

## Compression rule

If a brief contains many bullets, compress them into:
- one chapter-level question
- two or three recurring contrasts
- one progression sentence if needed

If the brief cannot be compressed that way, the lead should stay conservative and avoid over-claiming coherence.
