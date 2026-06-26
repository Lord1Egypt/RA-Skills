# Flowchart

## Use Cases

- Business process flows
- Decision trees and branching logic
- Algorithm flow descriptions
- Operation step instructions

## Key Patterns

| Element | Syntax | Purpose |
|---------|--------|---------|
| Start/End | `shape: circle` | Beginning and end of process |
| Decision Node | `shape: diamond` | Conditional branches, decision points |
| Process Step | Default rectangle | Operations, processes, actions |
| Input/Output | `shape: parallelogram` | Data input and output |

## Basic Example

```d2
direction: down

Start: { shape: circle }
Step One
Condition: { shape: diamond }
End: { shape: circle }

Start -> Step One -> Condition
Condition -> Step Two -> End
Condition -> End: "End directly"
```

## Example with Input/Output

```d2
direction: down

Start: { shape: circle }
Input Data: { shape: parallelogram }
Process Data
Validate Result: { shape: diamond }
Output Report: { shape: parallelogram }
End: { shape: circle }

Start -> Input Data -> Process Data -> Validate Result
Validate Result -> Output Report: "Success"
Validate Result -> Process Data: "Failed, reprocess"
Output Report -> End
```

## Complex Decision Branching

```d2
direction: down

Start: { shape: circle }
Enter Credentials
Validate Credentials: { shape: diamond }
Credentials Valid: { shape: diamond }
Check Account Status: { shape: diamond }
Generate Token
End: { shape: circle }
Error Handling
Lock Handling

Start -> Enter Credentials
Enter Credentials -> Validate Credentials
Validate Credentials -> Error Handling: "Invalid"
Validate Credentials -> Check Account Status: "Valid"
Check Account Status -> Lock Handling: "Locked"
Check Account Status -> Generate Token: "Normal"
Generate Token -> End
Lock Handling -> End: "Notify user"
Error Handling -> End: "Return error"
```

## Design Principles

1. **Simplicity First** - Show core processes, avoid over-detailing
2. **Use Decision Nodes Wisely** - Only use diamond at key branching points
3. **Clear Labeling** - Label branch conditions on connection lines
4. **Avoid Displaying Loops** - Use text descriptions for loops instead of drawing cycles

## Common Mistakes

❌ Over-detailing
```
Start → Validate Input Format → Format Correct? → Query User → User Exists? →
Validate Password → Password Correct? → Create Session → Generate Token → Redirect to Home
```

✅ Core Process
```
Start → Enter Credentials → Query User → User Exists? → Validate Password → Password Correct? →
Create Session → Login Success
```
