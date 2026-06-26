# Pending Review Policy

Use pending review when safe automatic merge is not possible.

## Send to pending review when

1. One `user_id` matches multiple subjects
2. New evidence conflicts with an existing `union_id`
3. Important support fields strongly disagree
4. Critical identifiers are missing

## Review priority

1. `union_id`
2. `user_id`
3. `phone`
4. `name`
5. source reliability

## Outcomes

- `merged` — add to an existing subject
- `new_subject` — keep as a separate person
- `rejected` — invalid or untrusted input

## Principle

Prefer a slow review over a wrong merge.
