# Change Policy
#tags: skills review

Classify every proposed edit after the line is frozen.

## bugfix
- fixes a proven contradiction, broken validation rule, or failing required scenario
- may be applied to the frozen line

## clarification
- improves wording, formatting, or reference synchronization without changing runtime behavior
- may be applied to the frozen line

## structural
- changes runtime order, required fields, validation semantics, mode behavior, or consultant roles
- also includes self-review stance changes that materially alter self-position pressure, consultant challenge shaping, or synthesis decision pressure even when no fourth public stage is added
- must go to backlog unless a required scenario test proves the current line is insufficient

## experimental
- optional future capability, optimization, or convenience idea
- must go to backlog for the next planned release

## Current-line rule
Only `bugfix` and `clarification` changes belong in the frozen line by default.
Do not treat “this could be even better” as enough reason to modify the current reference line.
Do treat self-evolution doctrine upgrades as candidate-line work when they materially alter self-review behavior.
