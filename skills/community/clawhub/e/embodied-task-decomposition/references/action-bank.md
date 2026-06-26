# Atomic Action Bank

A standardized vocabulary for robot task decomposition. Each action is atomic and unambiguous.

## Manipulation Actions

| Action | Description | Example Usage |
|--------|-------------|---------------|
| pick up | Grasp and lift an object | "pick up the cup" |
| lift | Raise object upward | "lift the box" |
| place | Put down an object at a location | "place the cup on the table" |
| grasp | Secure hold on object | "grasp the cube" |
| release | Let go of object | "release the object" |
| push | Apply force to move forward | "push the box" |
| pull | Draw object toward agent | "pull the handle" |
| rotate | Turn object around axis | "rotate the cube 90 degrees" |
| press | Apply downward force | "press the button" |
| wipe | Clean surface with tool | "wipe the table with rag" |
| pour | Transfer liquid | "pour water into cup" |

## Locomotion Actions

| Action | Description | Example Usage |
|--------|-------------|---------------|
| move to | Navigate to location | "move to the kitchen" |
| retreat | Move away from target | "retreat to starting position" |

## Complex Actions

| Action | Description | Example Usage |
|--------|-------------|---------------|
| take out | Remove from container/bag | "take fruit out of bag" |
| put into | Insert into container | "put fruit into bowl" |
| stack | Place on top | "stack boxes" |
| arrange | Position in order | "arrange plates" |
| fetch | Retrieve and bring | "fetch the tool" |
| deliver | Transport to destination | "deliver package to door" |
| insert | Put object inside container or slot | "insert key into lock" |

## Gripper Specification

Always specify which gripper:
- "with left gripper"
- "with right gripper"
- "with either gripper" (if either works)

## Notes

- Use only actions from this bank
- Each subtask should contain one primary action
- Include target object and location
- Always specify gripper for manipulation tasks