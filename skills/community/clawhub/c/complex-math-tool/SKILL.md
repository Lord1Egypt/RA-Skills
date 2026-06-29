---
name: complex-math-tool
description: "Complex Math Tool: Math calculations: percentages, ratios, rounding, random numbers, aggregates (sum, avg, min, max), GCD. Returns formatted and raw values. Use when an agent needs complex math tool, percentage calculation, percent of total, what percent is x of y, percentage of value, math average, numbers, math gcd through AgentPMT-hosted remote tool calls. Discovery terms: complex math tool, percentage calculation, percent of total, what percent is x of y, percentage of value, math average."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/complex-math-tool
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/complex-math-tool"}}
---
# Complex Math Tool

## Freshness
Last updated: `2026-06-23`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
A utility for common mathematical calculations frequently needed in business, finance, data analysis, and everyday applications. It provides comprehensive percentage operations including calculating what percent one value is of another, finding a percentage of a given number, and determining percent increase or decrease between two values for tracking growth or decline metrics. Ratio calculation simplifies proportions between multiple numbers by finding the greatest common divisor and reducing to the smallest whole number representation. Number rounding supports configurable decimal precision from 0 to 10 places for formatting financial figures, measurements, and display values. Random number generation produces both floating-point values with specified decimal precision and integers within defined minimum and maximum bounds for sampling, testing, and simulation purposes. Aggregate functions operate on arrays of numbers to calculate sums, arithmetic averages, and identify minimum and maximum values with their array positions. The greatest common divisor function finds the largest integer that evenly divides all numbers in a set, useful for simplifying fractions and ratio calculations. All operations return formatted strings alongside raw values for immediate display or further computation.

## Product Instructions
### Complex Math Tool - Instructions

#### Overview
The Complex Math Tool provides a comprehensive set of mathematical operations including percentage calculations, number rounding, random number generation, aggregate operations (sum, average, min, max), ratio simplification, and greatest common divisor computation.

#### Actions

##### math-percent-calculate
Calculate what percentage one value is of a total.

**Required fields:**
- `numbers` (array): Exactly 2 numbers — [value, total]

**Example:**
```json
{
  "action": "math-percent-calculate",
  "numbers": [25, 200]
}
```
Returns: "25 is 12.5% of 200"

---

##### math-percentage-of
Calculate X% of a given value.

**Required fields:**
- `percent` (number): The percentage to apply (e.g., 25 for 25%)
- `value` (number): The base value

**Example:**
```json
{
  "action": "math-percentage-of",
  "percent": 15,
  "value": 200
}
```
Returns: "15% of 200 = 30"

---

##### math-percent-increase
Calculate the percent increase from an original value to a new value.

**Required fields:**
- `numbers` (array): Exactly 2 numbers — [original, new]

**Example:**
```json
{
  "action": "math-percent-increase",
  "numbers": [100, 150]
}
```
Returns: "100 to 150 is a 50% increase"

---

##### math-percent-decrease
Calculate the percent decrease from an original value to a new value.

**Required fields:**
- `numbers` (array): Exactly 2 numbers — [original, new]

**Example:**
```json
{
  "action": "math-percent-decrease",
  "numbers": [200, 150]
}
```
Returns: "200 to 150 is a 25% decrease"

---

##### math-ratio-calculate
Simplify the ratio between two or more numbers.

**Required fields:**
- `numbers` (array): 2 or more numbers

**Example:**
```json
{
  "action": "math-ratio-calculate",
  "numbers": [10, 25, 50]
}
```
Returns: Simplified ratio "2:5:10"

---

##### math-round-number
Round a number to a specified number of decimal places.

**Required fields:**
- `value` (number): The number to round

**Optional fields:**
- `decimals` (integer, 0-10): Decimal places. Default: 2

**Example:**
```json
{
  "action": "math-round-number",
  "value": 3.14159,
  "decimals": 3
}
```
Returns: 3.142

---

##### math-random-number
Generate a random floating-point number within a range.

**Required fields:**
- `min_value` (number): Minimum value (inclusive)
- `max_value` (number): Maximum value (must be greater than min_value)

**Optional fields:**
- `decimals` (integer, 0-10): Decimal places for the result. Default: 2

**Example:**
```json
{
  "action": "math-random-number",
  "min_value": 1.0,
  "max_value": 100.0,
  "decimals": 4
}
```
Returns: A random float between 1.0 and 100.0 with 4 decimal places

---

##### math-random-integer
Generate a random integer within a range (inclusive on both ends).

**Required fields:**
- `min_value` (number): Minimum integer value (inclusive)
- `max_value` (number): Maximum integer value (inclusive, must be greater than min_value)

**Example:**
```json
{
  "action": "math-random-integer",
  "min_value": 1,
  "max_value": 100
}
```
Returns: A random integer between 1 and 100

---

##### math-sum
Calculate the sum of an array of numbers.

**Required fields:**
- `numbers` (array): 1 or more numbers

**Example:**
```json
{
  "action": "math-sum",
  "numbers": [10, 20, 30, 40, 50]
}
```
Returns: 150

---

##### math-average
Calculate the arithmetic mean of an array of numbers.

**Required fields:**
- `numbers` (array): 1 or more numbers

**Example:**
```json
{
  "action": "math-average",
  "numbers": [85, 90, 78, 92, 88]
}
```
Returns: 86.6

---

##### math-min
Find the minimum (smallest) value in an array of numbers.

**Required fields:**
- `numbers` (array): 1 or more numbers

**Example:**
```json
{
  "action": "math-min",
  "numbers": [45, 12, 67, 3, 89]
}
```
Returns: 3 (at index 3)

---

##### math-max
Find the maximum (largest) value in an array of numbers.

**Required fields:**
- `numbers` (array): 1 or more numbers

**Example:**
```json
{
  "action": "math-max",
  "numbers": [45, 12, 67, 3, 89]
}
```
Returns: 89 (at index 4)

---

##### math-gcd
Calculate the greatest common divisor (GCD) of an array of integers.

**Required fields:**
- `numbers` (array): 1 or more integers (decimal values are converted to integers)

**Example:**
```json
{
  "action": "math-gcd",
  "numbers": [48, 36, 24]
}
```
Returns: GCD is 12

---

#### Common Workflows

##### Price discount calculation
1. Use `math-percentage-of` to calculate the discount amount (e.g., 20% of $150)
2. Use `math-sum` with a negative discount to get the final price

##### Comparing performance metrics
1. Use `math-percent-increase` or `math-percent-decrease` to compare two periods
2. Use `math-average` to find the mean across multiple data points

##### Statistical summary of a dataset
1. Use `math-sum` for the total
2. Use `math-average` for the mean
3. Use `math-min` and `math-max` for the range

##### Random selection
1. Use `math-random-integer` for picking random IDs or indices
2. Use `math-random-number` for generating random decimal values (e.g., test data)

#### Important Notes
- Division by zero is handled gracefully with descriptive error messages (e.g., percent-calculate with total=0)
- The `numbers` array order matters for percentage and ratio operations — check each action's description for the expected order
- GCD values are converted to integers before calculation
- Random number generation requires min_value to be strictly less than max_value
- All results include a human-readable `formatted` or `calculation` string for easy display

## When To Use
- Use this skill for `Complex Math Tool` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: complex math tool, percentage calculation, percent of total, what percent is x of y, percentage of value, math average, numbers, math gcd.
- Supported action names: `math-average`, `math-gcd`, `math-max`, `math-min`, `math-percent-calculate`, `math-percent-decrease`, `math-percent-increase`, `math-percentage-of`, `math-random-integer`, `math-random-number`, `math-ratio-calculate`, `math-round-number`, `math-sum`.

## Use Cases
- Percentage calculation
- percent of total
- what percent is X of Y
- percentage of value
- calculate X percent of Y
- percent increase calculation
- growth rate calculation
- percent decrease calculation
- decline rate calculation
- year over year change
- price change percentage
- ratio calculation
- ratio simplification
- proportion calculation
- aspect ratio
- recipe ratio scaling

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `13`.
x402 availability: not enabled for this product.

- `math-average` (action slug: `math-average`): Calculate the arithmetic mean (average) of an array of numbers. Price: `5` credits. Parameters: `numbers`.
- `math-gcd` (action slug: `math-gcd`): Calculate the greatest common divisor (GCD) of an array of integers. Price: `5` credits. Parameters: `numbers`.
- `math-max` (action slug: `math-max`): Find the maximum (largest) value in an array of numbers. Price: `5` credits. Parameters: `numbers`.
- `math-min` (action slug: `math-min`): Find the minimum (smallest) value in an array of numbers. Price: `5` credits. Parameters: `numbers`.
- `math-percent-calculate` (action slug: `math-percent-calculate`): Calculate what percentage one value is of a total. Provide two numbers: [value, total]. Returns the percentage with formatted output. Price: `5` credits. Parameters: `numbers`.
- `math-percent-decrease` (action slug: `math-percent-decrease`): Calculate the percent decrease from an original value to a new value. Provide two numbers: [original, new]. Price: `5` credits. Parameters: `numbers`.
- `math-percent-increase` (action slug: `math-percent-increase`): Calculate the percent increase from an original value to a new value. Provide two numbers: [original, new]. Price: `5` credits. Parameters: `numbers`.
- `math-percentage-of` (action slug: `math-percentage-of`): Calculate X% of a given value. For example, calculate 15% of 200. Returns the computed result. Price: `5` credits. Parameters: `percent`, `value`.
- `math-random-integer` (action slug: `math-random-integer`): Generate a random integer within a specified range (inclusive on both ends). Price: `5` credits. Parameters: `max_value`, `min_value`.
- `math-random-number` (action slug: `math-random-number`): Generate a random floating-point number within a specified range, rounded to a given number of decimal places. Price: `5` credits. Parameters: `decimals`, `max_value`, `min_value`.
- `math-ratio-calculate` (action slug: `math-ratio-calculate`): Calculate and simplify the ratio between two or more numbers. Returns the simplified ratio. Price: `5` credits. Parameters: `numbers`.
- `math-round-number` (action slug: `math-round-number`): Round a number to a specified number of decimal places. Price: `5` credits. Parameters: `decimals`, `value`.
- `math-sum` (action slug: `math-sum`): Calculate the sum of an array of numbers. Price: `5` credits. Parameters: `numbers`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "complex-math-tool"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "complex-math-tool"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "complex-math-tool"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "complex-math-tool"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "complex-math-tool"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "complex-math-tool"
  }
}
```

## Call This Tool
Product slug: `complex-math-tool`

Marketplace page: https://www.agentpmt.com/marketplace/complex-math-tool

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Complex-Math-Tool",
    "arguments": {
      "action": "math-average",
      "numbers": [
        1
      ]
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "complex-math-tool",
  "parameters": {
    "action": "math-average",
    "numbers": [
      1
    ]
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `math-average` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/complex-math-tool
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
