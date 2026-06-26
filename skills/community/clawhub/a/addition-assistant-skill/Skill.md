---
name: Addition Assistant
description: Calculate addition expressions from user input, including integers, decimals, and negative numbers, and return concise step-by-step results.
---

## Overview
Use this skill when the user asks for addition calculations.

## When to Use
- User asks to add two or more numbers.
- User inputs expressions like `3 + 5`, `1.2 + 3.4 + 5`, `-2 + 9`.

## Scope
- Supported: addition only.
- Not supported: subtraction, multiplication, division, equations, symbolic algebra.

## Input Handling
- Accept numbers separated by `+`, spaces, commas, or Chinese wording (for example: `加`).
- Normalize full-width symbols to half-width symbols before parsing.

## Workflow
1. Extract all numeric values from user input.
2. Verify at least two valid numbers are present.
3. Compute the sum.
4. Return:
   - Parsed numbers
   - Expression
   - Final result

## Output Format
Always return:
1. Expression used
2. Result
3. Optional one-line check

Example:
- Expression: `1.2 + 3.4 + 5`
- Result: `9.6`

## Safety and Accuracy Rules
- Do not invent missing numbers.
- If input is ambiguous, ask user to rewrite in explicit form.
- Preserve decimal precision as entered when reasonable.
