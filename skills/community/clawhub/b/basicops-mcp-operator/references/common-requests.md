# Common BasicOps requests

Use this reference to map natural-language requests to likely BasicOps operations.

## Task updates

User request:
- "assign this to Amanda"
Likely action:
- resolve user -> update current task assignee

User request:
- "mark this complete"
Likely action:
- update current task status to Complete

User request:
- "rename this to onboarding rollout"
Likely action:
- update current task or project title

User request:
- "make this high priority"
Likely action:
- update current task priority to High

## Summaries and rewrites

User request:
- "summarize this thread"
Likely action:
- read current message or task thread -> produce concise summary

User request:
- "rewrite the description based on the discussion"
Likely action:
- read local context -> update description with concise, grounded content

## Subtasks and planning

User request:
- "break this into subtasks"
Likely action:
- inspect current parent task -> create a modest subtask set

User request:
- "turn this plan into a checklist"
Likely action:
- derive checklist items from the current discussion or description

## Reviews and collaboration

User request:
- "request review from Kai"
Likely action:
- resolve reviewer -> request review on the current task

User request:
- "post this update to the task"
Likely action:
- create a message on the current task or reply in thread

## Related work

User request:
- "find related tasks"
Likely action:
- inspect same-project tasks or closely related objects -> summarize likely matches

## When to ask a clarifying question

Ask one short question when:
- multiple people match the requested assignee or reviewer
- the target object is unclear
- the user says "update this" but the intended field is unclear
- the request could affect multiple projects or tasks

Good examples:
- "Which field do you want updated?"
- "Do you mean the current task or the whole project?"
- "Which Amanda should I assign it to?"
