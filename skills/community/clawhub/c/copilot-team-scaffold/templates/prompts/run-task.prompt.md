---
description: "Execute a task from tasks.md by task ID (e.g. T-008). Auto-selects the correct Agent, checks dependencies, and runs the task."
agent: "agent"
argument-hint: "Task ID, e.g. T-008"
---
Execute the following task from the project task list.

## Steps

1. Read the task list: [tasks.md](.spec-flow/active/{{PROJECT_SLUG}}/tasks.md)
2. Find the task matching `{{ input }}` — extract its description, dependencies, status, complexity, and assigned Agent
3. **Dependency check**: If any dependency task is not ✅ Done, stop and report which are blocking
4. **Read module AGENTS.md**: Read the `AGENTS.md` file(s) for the target module(s) this task will touch
5. **Execute**: Implement the task following the constraints in the root [AGENTS.md](AGENTS.md) and the module AGENTS.md
6. **Test**: If the task's test mode is TDD or 边写边测, write/update tests as part of execution
7. **Verify**: Run the relevant test suite and confirm passing
8. **Report**: Summarize what was done, files changed, and any follow-up needed
