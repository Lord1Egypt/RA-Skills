# Complexity Assessor

Determines appropriate response depth. Triggers only when the user explicitly asks for depth or a detailed breakdown, never on generic words like "analyze", "compare", "explain", or "help me" alone.

## Role

- Assess query complexity
- Recommend response depth
- Prevent over/under-engineering

## Trigger Keywords

weigh trade-offs, compare options, how detailed, decision depth, how complex is this

## Output

```
Complexity Assessor:
Level: [1-Lookup | 2-Clarify | 3-Explain | 4-Analyze | 5-Deliberate | 6-Research]
Format: [one-liner | prose | steps | table]
Depth: [brief | moderate | thorough]
```
