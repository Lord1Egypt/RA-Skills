# Permission Errors

Read this file only when a task operation fails because the app identity appears to lack task access.

## Primary Error

- `1470403`: the app identity does not have permission to read or edit the task

## Interpret It Carefully

This usually means the fixed app identity is not authorized for that task, even if the task exists.

Possible reasons:

- the app did not create the task
- the app is not a task assignee or creator
- the task is not reachable through another permission path such as task hierarchy or a shared container

## Response Pattern

1. Do not retry blindly.
2. Explain that the failure is a task-permission issue, not just a transient API error.
3. Suggest checking whether the task was created by or shared with the app identity.

## Other Common Error Family

- `1470400`: the request shape or task state is invalid

Treat this as a payload or state-transition problem, not an authorization problem.
