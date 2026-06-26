# Execution Queue Protocol

## Structure

Maintain only these lanes:

- **Current** — the single active execution item
- **Next** — the next item to start immediately after current
- **Blocked** — items that cannot move right now
- **Done** — completed items only

## Rules

### Todo / Current / Next
- keep them short
- keep them actionable
- break larger items into small execution steps
- do not mix done work back into todo

### Silent execution
- prefer doing over narrating
- do not spam routine progress notes
- surface only blockers, approvals, or meaningful shipped milestones

### Blocked
For a blocked item:
1. write one-line blocker note
2. move it to blocked
3. continue the next item immediately

### Done
Move work into done only when:
- files changed, or
- behavior changed, or
- a meaningful commit exists

## Promotion rule

When a lesson repeats:
- do not leave it trapped in one-off chat memory
- promote it into a durable rule, skill, reference, or project document

## Project-making / planner layer

For active projects, keep these artifacts aligned:
- README for quick entry
- SRS for formal product truth
- execution queue for active movement

Before deep implementation, clarify:
- purpose
- user
- sections/pages/flows
- ownership boundaries
- next execution order

## Ekalavya spirit

- keep learning even when conditions are imperfect
- practice in small steps until skill becomes stable
- rely on disciplined repetition, not only bursts of enthusiasm
- adapt under blockers instead of stopping entirely

## Preferred progress format

- **Done:** what finished
- **Current:** what is being executed now
- **Next:** what will happen right after
- **Blocker:** only if real

## Reset condition

If the work feels muddy or repetitive, rebuild the queue before continuing.
