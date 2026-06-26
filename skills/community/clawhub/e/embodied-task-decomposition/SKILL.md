---
name: embodied-task-decomposition
description: |
  Decompose complex physical tasks into atomic subtasks for robot execution.
  Use when user provides: (1) An image showing a physical scene (indoor/outdoor), and (2) A natural language task instruction.
  Triggers on phrases like "decompose this task", "break down this task", "split this task into subtasks", "task instruction", 
  or any request to turn a high-level instruction into step-by-step robot actions.
  Also triggers when user provides image + task text together.
---

# Embodied Task Decomposition

This skill decomposes high-level natural language instructions into atomic subtasks that a robot can execute.

## When to Use

- User provides an image AND a task instruction
- User asks to "decompose", "break down", or "split" a task
- User wants step-by-step actions for robot execution

## Input Format

1. **Image**: Photo of the physical scene (any environment: kitchen, office, outdoor, etc.)
2. **Task Instruction**: Natural language description of what to accomplish

Example:
```
Task Instruction: take toasted bread from bread machine on white table place on plate
Image: [image path or description]
```

## Output Format

Numbered list of subtasks, each following format:
```
{action} {target} {location/optional prepositional phrase} with {left/right/either} gripper
```

## Process

1. **Analyze the image** - Identify objects, surfaces, locations, tools visible
2. **Understand the task** - What is the goal? What needs to be moved/ manipulated?
3. **Break into atomic actions** - Each subtask = one action from the action bank
4. **Specify gripper** - Always indicate left, right or either gripper

## Action Bank

Refer to [action-bank.md](action-bank.md) for the complete list of allowed actions. All subtasks MUST use actions from this bank.

## Examples

See [examples.md](examples.md) for detailed decomposition examples across different domains.

## Important Notes

- Use ONLY actions from the action bank
- Each subtask = one primary action
- Always specify gripper (left/right/either)
- Include target object and location
- Keep subtasks atomic and sequential
- Consider object state changes (e.g., "open bag" before "take fruit")

## Updating the Action Bank

The agent MAY add new actions to the action bank when needed. To add a new action:

1. **Check for duplicates** - Search existing actions for similar functionality
2. **Verify functional difference** - New action must serve a distinct purpose
3. **Add with documentation** - Include description and example usage

### Duplicate Check Criteria

A new action is considered a duplicate if it:
- Has the same name as an existing action
- Describes the same physical movement (e.g., "lift" vs "raise")
- Can be used interchangeably with an existing action in all contexts

### Adding a New Action

When adding to [action-bank.md](action-bank.md), follow this format:

```markdown
| action_name | Description | Example Usage |
|-------------|-------------|---------------|
| new_action | What it does | "new_action the object"
```

Example of adding "insert" (different from "place" - "place" = put on surface, "insert" = put into container):

```markdown
| insert | Put object inside a container or slot | "insert the key into the lock"
```