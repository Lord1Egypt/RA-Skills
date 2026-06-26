# BasicOps workflow patterns

Use this reference when deciding how much context to gather before acting.

## Principle

Gather enough context to act safely, but no more.

## Fast path

Use the fast path for simple, explicit mutations on a clear current object.

Examples:
- assign this to Amanda
- mark this complete
- rename this to Q3 launch plan
- set priority high

Pattern:
1. identify the current object
2. resolve the target person or field value if needed
3. perform the update
4. return or post a short summary

## Full-context path

Use the fuller path when the request depends on interpretation, thread history, or nearby work.

Examples:
- summarize this thread
- rewrite this task description based on the discussion
- find related work
- explain what is blocked
- create subtasks from the plan above

Pattern:
1. read the current task, project, note, or thread
2. inspect nearby context only when it materially helps
3. complete the requested action or produce the summary
4. keep the result concise

## Local-first scope

Prefer the current object first.

- Stay on the current task unless the user asks for related tasks or project-wide context.
- Stay in the current thread unless replying there is impossible.
- Stay in the current project unless the request clearly calls for broader inspection.

## After-write summary

After a successful write, say exactly what changed.

Examples:
- "Assigned the task to Amanda."
- "Set status to Complete and posted a follow-up note."
- "Created 4 subtasks under the parent task."

## Avoid over-reading

Do not fetch broad project history or large message sets for a trivial mutation. The skill should feel responsive and deliberate, not nosy.
