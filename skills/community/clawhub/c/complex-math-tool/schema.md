# Complex Math Tool Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `complex-math-tool`

x402 availability: not enabled for this product.

## `math-average`

Action slug: `math-average`

Price: `5` credits

Calculate the arithmetic mean (average) of an array of numbers.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `numbers` | `array` | yes | Array of 1 or more numbers to average. Example: [10, 20, 30]. |

Sample parameters:

```json
{
  "numbers": [
    1
  ]
}
```

Generated JSON parameter schema:

```json
{
  "numbers": {
    "description": "Array of 1 or more numbers to average. Example: [10, 20, 30].",
    "items": {
      "type": "number"
    },
    "required": true,
    "type": "array"
  }
}
```

## `math-gcd`

Action slug: `math-gcd`

Price: `5` credits

Calculate the greatest common divisor (GCD) of an array of integers.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `numbers` | `array` | yes | Array of 1 or more integers. Values are converted to integers before calculation. |

Sample parameters:

```json
{
  "numbers": [
    1
  ]
}
```

Generated JSON parameter schema:

```json
{
  "numbers": {
    "description": "Array of 1 or more integers. Values are converted to integers before calculation.",
    "items": {
      "type": "number"
    },
    "required": true,
    "type": "array"
  }
}
```

## `math-max`

Action slug: `math-max`

Price: `5` credits

Find the maximum (largest) value in an array of numbers.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `numbers` | `array` | yes | Array of 1 or more numbers. Returns the largest value and its index. |

Sample parameters:

```json
{
  "numbers": [
    1
  ]
}
```

Generated JSON parameter schema:

```json
{
  "numbers": {
    "description": "Array of 1 or more numbers. Returns the largest value and its index.",
    "items": {
      "type": "number"
    },
    "required": true,
    "type": "array"
  }
}
```

## `math-min`

Action slug: `math-min`

Price: `5` credits

Find the minimum (smallest) value in an array of numbers.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `numbers` | `array` | yes | Array of 1 or more numbers. Returns the smallest value and its index. |

Sample parameters:

```json
{
  "numbers": [
    1
  ]
}
```

Generated JSON parameter schema:

```json
{
  "numbers": {
    "description": "Array of 1 or more numbers. Returns the smallest value and its index.",
    "items": {
      "type": "number"
    },
    "required": true,
    "type": "array"
  }
}
```

## `math-percent-calculate`

Action slug: `math-percent-calculate`

Price: `5` credits

Calculate what percentage one value is of a total. Provide two numbers: [value, total]. Returns the percentage with formatted output.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `numbers` | `array` | yes | Array of exactly 2 numbers: [value, total]. Example: [25, 200] calculates what percent 25 is of 200. |

Sample parameters:

```json
{
  "numbers": [
    1
  ]
}
```

Generated JSON parameter schema:

```json
{
  "numbers": {
    "description": "Array of exactly 2 numbers: [value, total]. Example: [25, 200] calculates what percent 25 is of 200.",
    "items": {
      "type": "number"
    },
    "required": true,
    "type": "array"
  }
}
```

## `math-percent-decrease`

Action slug: `math-percent-decrease`

Price: `5` credits

Calculate the percent decrease from an original value to a new value. Provide two numbers: [original, new].

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `numbers` | `array` | yes | Array of exactly 2 numbers: [original, new]. Example: [200, 150] calculates percent decrease from 200 to 150. |

Sample parameters:

```json
{
  "numbers": [
    1
  ]
}
```

Generated JSON parameter schema:

```json
{
  "numbers": {
    "description": "Array of exactly 2 numbers: [original, new]. Example: [200, 150] calculates percent decrease from 200 to 150.",
    "items": {
      "type": "number"
    },
    "required": true,
    "type": "array"
  }
}
```

## `math-percent-increase`

Action slug: `math-percent-increase`

Price: `5` credits

Calculate the percent increase from an original value to a new value. Provide two numbers: [original, new].

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `numbers` | `array` | yes | Array of exactly 2 numbers: [original, new]. Example: [100, 150] calculates percent increase from 100 to 150. |

Sample parameters:

```json
{
  "numbers": [
    1
  ]
}
```

Generated JSON parameter schema:

```json
{
  "numbers": {
    "description": "Array of exactly 2 numbers: [original, new]. Example: [100, 150] calculates percent increase from 100 to 150.",
    "items": {
      "type": "number"
    },
    "required": true,
    "type": "array"
  }
}
```

## `math-percentage-of`

Action slug: `math-percentage-of`

Price: `5` credits

Calculate X% of a given value. For example, calculate 15% of 200. Returns the computed result.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `percent` | `number` | yes | The percentage to apply (e.g., 25 for 25%). |
| `value` | `number` | yes | The value to calculate the percentage of. |

Sample parameters:

```json
{
  "percent": 1,
  "value": 1
}
```

Generated JSON parameter schema:

```json
{
  "percent": {
    "description": "The percentage to apply (e.g., 25 for 25%).",
    "required": true,
    "type": "number"
  },
  "value": {
    "description": "The value to calculate the percentage of.",
    "required": true,
    "type": "number"
  }
}
```

## `math-random-integer`

Action slug: `math-random-integer`

Price: `5` credits

Generate a random integer within a specified range (inclusive on both ends).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `max_value` | `number` | yes | Maximum integer value (inclusive). Must be greater than min_value. |
| `min_value` | `number` | yes | Minimum integer value (inclusive). |

Sample parameters:

```json
{
  "max_value": 1,
  "min_value": 1
}
```

Generated JSON parameter schema:

```json
{
  "max_value": {
    "description": "Maximum integer value (inclusive). Must be greater than min_value.",
    "required": true,
    "type": "number"
  },
  "min_value": {
    "description": "Minimum integer value (inclusive).",
    "required": true,
    "type": "number"
  }
}
```

## `math-random-number`

Action slug: `math-random-number`

Price: `5` credits

Generate a random floating-point number within a specified range, rounded to a given number of decimal places.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `decimals` | `integer` | no | Number of decimal places for the result (0-10). Default: 2. |
| `max_value` | `number` | yes | Maximum value for the random number (exclusive). Must be greater than min_value. |
| `min_value` | `number` | yes | Minimum value for the random number (inclusive). |

Sample parameters:

```json
{
  "decimals": 2,
  "max_value": 1,
  "min_value": 1
}
```

Generated JSON parameter schema:

```json
{
  "decimals": {
    "default": 2,
    "description": "Number of decimal places for the result (0-10). Default: 2.",
    "maximum": 10,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "max_value": {
    "description": "Maximum value for the random number (exclusive). Must be greater than min_value.",
    "required": true,
    "type": "number"
  },
  "min_value": {
    "description": "Minimum value for the random number (inclusive).",
    "required": true,
    "type": "number"
  }
}
```

## `math-ratio-calculate`

Action slug: `math-ratio-calculate`

Price: `5` credits

Calculate and simplify the ratio between two or more numbers. Returns the simplified ratio.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `numbers` | `array` | yes | Array of 2 or more numbers to calculate the ratio for. Example: [10, 25, 50]. |

Sample parameters:

```json
{
  "numbers": [
    1
  ]
}
```

Generated JSON parameter schema:

```json
{
  "numbers": {
    "description": "Array of 2 or more numbers to calculate the ratio for. Example: [10, 25, 50].",
    "items": {
      "type": "number"
    },
    "required": true,
    "type": "array"
  }
}
```

## `math-round-number`

Action slug: `math-round-number`

Price: `5` credits

Round a number to a specified number of decimal places.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `decimals` | `integer` | no | Number of decimal places (0-10). Default: 2. |
| `value` | `number` | yes | The number to round. |

Sample parameters:

```json
{
  "decimals": 2,
  "value": 1
}
```

Generated JSON parameter schema:

```json
{
  "decimals": {
    "default": 2,
    "description": "Number of decimal places (0-10). Default: 2.",
    "maximum": 10,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "value": {
    "description": "The number to round.",
    "required": true,
    "type": "number"
  }
}
```

## `math-sum`

Action slug: `math-sum`

Price: `5` credits

Calculate the sum of an array of numbers.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `numbers` | `array` | yes | Array of 1 or more numbers to sum. Example: [10, 20, 30]. |

Sample parameters:

```json
{
  "numbers": [
    1
  ]
}
```

Generated JSON parameter schema:

```json
{
  "numbers": {
    "description": "Array of 1 or more numbers to sum. Example: [10, 20, 30].",
    "items": {
      "type": "number"
    },
    "required": true,
    "type": "array"
  }
}
```
