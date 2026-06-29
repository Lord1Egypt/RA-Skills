# Complex Mathematics Engine Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `complex-mathematics-engine`

x402 availability: not enabled for this product.

## `calculate`

Action slug: `calculate`

Price: `5` credits

Evaluate a mathematical expression using SymPy (symbolic), NumPy (numerical/arrays), or SciPy (statistics/optimization). Supports calculus, linear algebra, statistics, and more.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `engine_hint` | `string` | no | Force a specific computation engine. 'auto' (default) automatically detects the best engine based on the expression. |
| `expression` | `string` | yes | Mathematical expression to compute. Supports SymPy, NumPy, and SciPy syntax. Examples: diff(x**2, x), np.mean([1,2,3]), stats.norm.cdf(0), solve(x**2 - 4, x). Max 50000 characters. |

Sample parameters:

```json
{
  "engine_hint": "auto",
  "expression": "example expression"
}
```

Generated JSON parameter schema:

```json
{
  "engine_hint": {
    "default": "auto",
    "description": "Force a specific computation engine. 'auto' (default) automatically detects the best engine based on the expression.",
    "enum": [
      "auto",
      "sympy",
      "numpy",
      "scipy"
    ],
    "required": false,
    "type": "string"
  },
  "expression": {
    "description": "Mathematical expression to compute. Supports SymPy, NumPy, and SciPy syntax. Examples: diff(x**2, x), np.mean([1,2,3]), stats.norm.cdf(0), solve(x**2 - 4, x). Max 50000 characters.",
    "required": true,
    "type": "string"
  }
}
```
