---
name: calculator
description: This skill should be used when the user asks to "calculate", "compute", "do math", mentions arithmetic operations like "add", "subtract", "multiply", "divide", or asks questions like "what is 1+1". Provides basic arithmetic calculation capabilities.
version: 1.0.0
---

# Calculator Skill

A simple calculator skill that performs basic arithmetic operations.

## When This Skill Applies

This skill activates when the user's request involves:
- Basic arithmetic calculations (addition, subtraction, multiplication, division)
- Math expressions evaluation
- Number computation requests

## Instructions

When this skill is activated:

1. Parse the mathematical expression from the user's request
2. Perform the calculation step by step
3. Return the result clearly

## Supported Operations

| Operation | Symbol | Example     | Result |
|-----------|--------|-------------|--------|
| Addition  | +      | 1 + 1       | 2      |
| Subtraction | -    | 10 - 3      | 7      |
| Multiplication | * | 4 * 5       | 20     |
| Division  | /      | 20 / 4      | 5      |

## Example

**User**: What is 1 + 1?

**Steps**:
1. Parse expression: `1 + 1`
2. Perform addition: `1 + 1 = 2`
3. Return result: **2**

## Rules

- Always show the calculation process
- For division, check for division by zero and warn the user
- Support chained operations (e.g., `1 + 2 * 3`)
- Follow standard mathematical order of operations (PEMDAS)
- Return results with appropriate precision (avoid unnecessary decimal places)
