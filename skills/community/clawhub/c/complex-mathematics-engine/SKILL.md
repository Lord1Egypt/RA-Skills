---
name: complex-mathematics-engine
description: "Complex Mathematics Engine: Execute mathematical expressions using SymPy (symbolic), NumPy (numerical), or SciPy (scientific). Supports arithmetic, calculus, linear algebra, statistics, and equation solving with automatic backend detection. Use when an agent needs complex mathematics engine, calculus, solve derivative, calculate integral, find limit of function, calculate, expression, engine hint through AgentPMT-hosted remote tool calls. Discovery terms: complex mathematics engine, calculus."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/complex-mathematics-engine
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/complex-mathematics-engine"}}
---
# Complex Mathematics Engine

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
A universal math engine that intelligently executes mathematical and scientific expressions. An agent can submit a single expression string to solve a wide range of problems without needing to select a specific engine, ranging from simple arithmetic to advanced symbolic mathematics, numerical array operations, and scientific computing. It integrates three powerful computation backends: SymPy for symbolic mathematics including differentiation, integration, limits, series expansions, equation solving, and algebraic simplification; NumPy for numerical operations on arrays and matrices including linear algebra, element-wise operations, and statistical aggregations; and SciPy for scientific computing including probability distributions, optimization, curve fitting, special functions, and numerical integration. The engine automatically detects the appropriate back end based on expression syntax, or users can specify a preferred engine explicitly. Expressions support intuitive syntax including Unicode math symbols like π, ∞, and √ which are automatically converted, as well as caret notation for exponentiation. Symbolic results preserve variables and can be further manipulated, while numerical results are returned as JSON-serializable values with full precision. Built-in security validation prevents code injection while allowing access to a comprehensive library of mathematical functions. Results include execution timing, the engine used, and metadata about the computation including detected variables for symbolic expressions.

## Product Instructions
### Complex Mathematics Engine (009) - Instructions

#### Overview
Evaluate mathematical expressions using three powerful computation engines:
- **SymPy** — Symbolic math (calculus, algebra, equation solving)
- **NumPy** — Numerical computation (arrays, linear algebra, statistics)
- **SciPy** — Scientific computing (statistics distributions, optimization, special functions)

#### Action: `calculate`

##### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `expression` | string | Yes | Mathematical expression to compute. Max 50,000 characters. |
| `engine_hint` | string | No | Force a specific engine: `auto` (default), `sympy`, `numpy`, `scipy`. |

##### Engine Auto-Detection
When `engine_hint` is `auto` (default), the engine is chosen based on the expression:
- **SciPy** — Expressions containing `scipy.`, `stats.`, `optimize.`, `special.`, `interpolate.`, `integrate.`, `curve_fit`, `least_squares`
- **NumPy** — Expressions containing `np.`, `numpy.`, `array`, `zeros`, `ones`, `eye`, `linspace`, `arange`, `mean`, `std`, `dot`, `linalg.`
- **SymPy** — Expressions containing `diff`, `integrate`, `limit`, `solve`, `simplify`, `expand`, `factor` (and is the default fallback)

##### Supported Syntax

###### SymPy Examples
- `diff(x**2, x)` — Differentiate x² with respect to x
- `integrate(sin(x), x)` — Indefinite integral of sin(x)
- `solve(x**2 - 4, x)` — Solve x² - 4 = 0
- `limit(sin(x)/x, x, 0)` — Evaluate limit as x approaches 0
- `simplify((x**2 - 1)/(x - 1))` — Simplify expression
- `expand((x + 1)**3)` — Expand polynomial
- `factor(x**2 - 4)` — Factor polynomial

###### NumPy Examples
- `np.mean([1, 2, 3, 4, 5])` — Calculate mean
- `np.std([1, 2, 3])` — Standard deviation
- `np.dot([1, 2], [3, 4])` — Dot product
- `np.linalg.det(array([[1, 2], [3, 4]]))` — Matrix determinant
- `np.linspace(0, 10, 5)` — Generate evenly spaced values

###### SciPy Examples
- `stats.norm.cdf(0)` — Standard normal CDF at 0
- `stats.norm.pdf(0, loc=0, scale=1)` — Normal PDF
- `special.gamma(5)` — Gamma function
- `stats.t.ppf(0.975, df=10)` — t-distribution critical value

##### Unicode Support
The following Unicode symbols are automatically converted:
- `π` → `pi`, `∞` → `oo`, `√` → `sqrt`, `∂` → `diff`, `∫` → `integrate`
- `^` is converted to `**` for exponentiation

##### Security
Expressions are sandboxed. The following are blocked:
- `import`, `exec`, `eval`, `compile`, `open` statements
- Access to `os`, `sys`, `subprocess`, `pathlib`, `shutil`
- Dunder attributes (`__`)
- Semicolons and newlines (no multi-statement expressions)
- Only whitelisted functions and namespaces are permitted

##### Response Fields
- `expression` — The original expression submitted
- `engine_used` — Which engine processed the expression (`sympy`, `numpy`, or `scipy`)
- `execution_time_seconds` — How long the computation took
- `result` — The computed result (JSON-serializable)
- `result_str` — String representation of the result
- `metadata` — Additional info (result_type, variables if symbolic)

## When To Use
- Use this skill for `Complex Mathematics Engine` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: complex mathematics engine, calculus, solve derivative, calculate integral, find limit of function, calculate, expression, engine hint.
- Supported action names: `calculate`.

## Use Cases
- Calculus
- Solve Derivative
- Calculate Integral
- Find Limit of Function
- Algebra
- Solve Equation for Variable
- Simplify Polynomial
- Factor Expression
- Expand Formula
- Linear Algebra
- Matrix Multiplication
- Invert Matrix
- Solve Linear System
- Calculate Determinant
- Find Eigenvalues
- Statistics

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `calculate` (action slug: `calculate`): Evaluate a mathematical expression using SymPy (symbolic), NumPy (numerical/arrays), or SciPy (statistics/optimization). Supports calculus, linear algebra, statistics, and more. Price: `5` credits. Parameters: `engine_hint`, `expression`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "complex-mathematics-engine"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "complex-mathematics-engine"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "complex-mathematics-engine"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "complex-mathematics-engine"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "complex-mathematics-engine"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "complex-mathematics-engine"
  }
}
```

## Call This Tool
Product slug: `complex-mathematics-engine`

Marketplace page: https://www.agentpmt.com/marketplace/complex-mathematics-engine

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
    "name": "Complex-Mathematics-Engine",
    "arguments": {
      "action": "calculate",
      "engine_hint": "auto",
      "expression": "example expression"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "complex-mathematics-engine",
  "parameters": {
    "action": "calculate",
    "engine_hint": "auto",
    "expression": "example expression"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `calculate` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/complex-mathematics-engine
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
