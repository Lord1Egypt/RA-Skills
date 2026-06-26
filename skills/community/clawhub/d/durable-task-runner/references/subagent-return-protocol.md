# Subagent return protocol

Attribution note:
- This protocol is adapted from ideas in ClawHub `subagent-orchestrator`, especially its structured return headers and anti-drop controller philosophy.
- This version is simplified for durable-task-runner and should remain credited accordingly.

## Required headers

Every worker/subagent return should include:

- `tag:` `autopilot | done | idle | blocked | handoff | need_user`
- `task_id:` durable task id
- `line:` task line / branch name
- `node:` current node id
- `goal_status:` `partial | complete | waiting | blocked`
- `next_role:` next owner label such as `main`, `verify`, `research`, `worker`, `user`, `none`

Do not invent free-form alternatives for `goal_status`.

## Short body

After headers, keep the body short:

1. Goal
2. Completed
3. Changed artifacts/files
4. Current status
5. Next step
6. Risk

## Controller expectation

The orchestrator must not treat a finished round as a finished line.

If a worker returns `tag: autopilot`, the controller must do one of these before ending the turn:
- dispatch the next node
- explicitly mark the line `idle`
- explicitly mark the line `blocked`
- explicitly mark the line `need_user`
- explicitly mark the line `done`

Anything else is a dropped line.

## Delivery-proof rule

If a worker claims delivery on an external surface, require proof where applicable:
- target
- object/message id or equivalent
- human-checkable location description

Without proof, do not mark externally delivered work complete.
