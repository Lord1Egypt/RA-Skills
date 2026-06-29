# Financial Loan Amortization Calculator Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `financial-loan-calculator`

x402 availability: not enabled for this product.

## `affordability_analysis`

Action slug: `affordability-analysis`

Price: `5` credits

Estimate affordable monthly payment, maximum loan principal, and maximum home price based on income, debts, and DTI ratios.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `annual_income` | `number` | yes | Gross annual income |
| `annual_rate` | `number` | yes | Expected mortgage rate in percent |
| `back_end_ratio` | `number` | no | Maximum total debt ratio to gross income |
| `compounding_per_year` | `integer` | no | Compounding frequency per year |
| `down_payment` | `number` | no | Down payment amount (added to max principal for max home price) |
| `front_end_ratio` | `number` | no | Maximum housing expense ratio to gross income |
| `hoa_monthly` | `number` | no | Estimated monthly HOA fees |
| `insurance_monthly` | `number` | no | Estimated monthly insurance |
| `monthly_debts` | `number` | no | Recurring monthly debt obligations |
| `monthly_expenses` | `number` | no | Additional recurring monthly expenses |
| `payments_per_year` | `integer` | no | Payment frequency per year |
| `property_tax_monthly` | `number` | no | Estimated monthly property tax |
| `years` | `number` | yes | Loan term in years |

Sample parameters:

```json
{
  "annual_income": 0,
  "annual_rate": 0,
  "back_end_ratio": 0.36,
  "compounding_per_year": 12,
  "down_payment": 0,
  "front_end_ratio": 0.28,
  "hoa_monthly": 0,
  "insurance_monthly": 0
}
```

Generated JSON parameter schema:

```json
{
  "annual_income": {
    "description": "Gross annual income",
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "annual_rate": {
    "description": "Expected mortgage rate in percent",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "back_end_ratio": {
    "default": 0.36,
    "description": "Maximum total debt ratio to gross income",
    "maximum": 1,
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "compounding_per_year": {
    "default": 12,
    "description": "Compounding frequency per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "down_payment": {
    "default": 0,
    "description": "Down payment amount (added to max principal for max home price)",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "front_end_ratio": {
    "default": 0.28,
    "description": "Maximum housing expense ratio to gross income",
    "maximum": 1,
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "hoa_monthly": {
    "default": 0,
    "description": "Estimated monthly HOA fees",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "insurance_monthly": {
    "default": 0,
    "description": "Estimated monthly insurance",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "monthly_debts": {
    "default": 0,
    "description": "Recurring monthly debt obligations",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "monthly_expenses": {
    "default": 0,
    "description": "Additional recurring monthly expenses",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "payments_per_year": {
    "default": 12,
    "description": "Payment frequency per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "property_tax_monthly": {
    "default": 0,
    "description": "Estimated monthly property tax",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "years": {
    "description": "Loan term in years",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  }
}
```

## `amortization_schedule`

Action slug: `amortization-schedule`

Price: `5` credits

Build a full amortization table with support for extra payments, one-time lump sums, interest-only periods, balloon payments, and optional CSV file export to cloud storage.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `annual_rate` | `number` | yes | Nominal annual interest rate in percent |
| `balloon_payment` | `number` | no | Balloon due at maturity |
| `compounding_per_year` | `integer` | no | Compounding frequency per year |
| `expiration_days` | `integer` | no | Cloud file expiration in days |
| `extra_payment` | `number` | no | Recurring extra principal each period |
| `extra_payment_start_period` | `integer` | no | Period to begin recurring extra payments |
| `future_value` | `number` | no | Target future value |
| `interest_only_periods` | `integer` | no | Interest-only period count |
| `max_schedule_rows` | `integer` | no | Maximum amortization rows to return |
| `one_time_extra_payments` | `array` | no | List of one-time extra principal payments |
| `payments_per_year` | `integer` | no | Payment frequency per year |
| `principal` | `number` | yes | Loan principal |
| `return_schedule` | `boolean` | no | Include schedule rows in response |
| `start_date` | `string` | no | Schedule start date in YYYY-MM-DD format; adds date column to each row |
| `store_schedule_file` | `boolean` | no | Upload schedule as CSV to cloud storage and return file metadata |
| `years` | `number` | yes | Loan term in years |

Sample parameters:

```json
{
  "annual_rate": 0,
  "balloon_payment": 0,
  "compounding_per_year": 12,
  "expiration_days": 7,
  "extra_payment": 0,
  "extra_payment_start_period": 1,
  "future_value": 0,
  "interest_only_periods": 0
}
```

Generated JSON parameter schema:

```json
{
  "annual_rate": {
    "description": "Nominal annual interest rate in percent",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "balloon_payment": {
    "default": 0,
    "description": "Balloon due at maturity",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "compounding_per_year": {
    "default": 12,
    "description": "Compounding frequency per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "expiration_days": {
    "default": 7,
    "description": "Cloud file expiration in days",
    "maximum": 7,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "extra_payment": {
    "default": 0,
    "description": "Recurring extra principal each period",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "extra_payment_start_period": {
    "default": 1,
    "description": "Period to begin recurring extra payments",
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "future_value": {
    "default": 0,
    "description": "Target future value",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "interest_only_periods": {
    "default": 0,
    "description": "Interest-only period count",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "max_schedule_rows": {
    "default": 5000,
    "description": "Maximum amortization rows to return",
    "maximum": 50000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "one_time_extra_payments": {
    "description": "List of one-time extra principal payments",
    "items": {
      "properties": {
        "amount": {
          "description": "Extra principal payment amount",
          "minimum": 0,
          "required": true,
          "type": "number"
        },
        "period": {
          "description": "Payment period index (1-based)",
          "minimum": 1,
          "required": true,
          "type": "integer"
        }
      },
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "payments_per_year": {
    "default": 12,
    "description": "Payment frequency per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "principal": {
    "description": "Loan principal",
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "return_schedule": {
    "default": true,
    "description": "Include schedule rows in response",
    "required": false,
    "type": "boolean"
  },
  "start_date": {
    "description": "Schedule start date in YYYY-MM-DD format; adds date column to each row",
    "required": false,
    "type": "string"
  },
  "store_schedule_file": {
    "default": false,
    "description": "Upload schedule as CSV to cloud storage and return file metadata",
    "required": false,
    "type": "boolean"
  },
  "years": {
    "description": "Loan term in years",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  }
}
```

## `calculate_loan_principal`

Action slug: `calculate-loan-principal`

Price: `5` credits

Calculate the maximum loan principal supported by a given periodic payment amount.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `annual_rate` | `number` | yes | Nominal annual interest rate in percent |
| `balloon_payment` | `number` | no | Balloon due at maturity |
| `compounding_per_year` | `integer` | no | Compounding frequency per year |
| `future_value` | `number` | no | Target future value |
| `payment_amount` | `number` | yes | Periodic payment amount |
| `payments_per_year` | `integer` | no | Payment frequency per year |
| `target_periods` | `integer` | no | Target number of payment periods (alternative to years) |
| `years` | `number` | no | Loan term in years (provide years or target_periods or both) |

Sample parameters:

```json
{
  "annual_rate": 0,
  "balloon_payment": 0,
  "compounding_per_year": 12,
  "future_value": 0,
  "payment_amount": 0,
  "payments_per_year": 12,
  "target_periods": 1,
  "years": 0
}
```

Generated JSON parameter schema:

```json
{
  "annual_rate": {
    "description": "Nominal annual interest rate in percent",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "balloon_payment": {
    "default": 0,
    "description": "Balloon due at maturity",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "compounding_per_year": {
    "default": 12,
    "description": "Compounding frequency per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "future_value": {
    "default": 0,
    "description": "Target future value",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "payment_amount": {
    "description": "Periodic payment amount",
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "payments_per_year": {
    "default": 12,
    "description": "Payment frequency per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "target_periods": {
    "description": "Target number of payment periods (alternative to years)",
    "maximum": 12000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "years": {
    "description": "Loan term in years (provide years or target_periods or both)",
    "maximum": 100,
    "minimum": 0,
    "required": false,
    "type": "number"
  }
}
```

## `calculate_payment`

Action slug: `calculate-payment`

Price: `5` credits

Compute the periodic payment for an amortizing loan. Supports interest-only periods, balloon payments, and configurable payment/compounding frequencies.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `annual_rate` | `number` | yes | Nominal annual interest rate in percent |
| `balloon_payment` | `number` | no | Balloon amount due at maturity |
| `compounding_per_year` | `integer` | no | Compounding frequency per year |
| `future_value` | `number` | no | Target future value after final payment |
| `interest_only_periods` | `integer` | no | Number of interest-only payment periods at the start |
| `payments_per_year` | `integer` | no | Payment frequency per year |
| `principal` | `number` | yes | Loan principal amount |
| `years` | `number` | yes | Loan term in years |

Sample parameters:

```json
{
  "annual_rate": 0,
  "balloon_payment": 0,
  "compounding_per_year": 12,
  "future_value": 0,
  "interest_only_periods": 0,
  "payments_per_year": 12,
  "principal": 0,
  "years": 0
}
```

Generated JSON parameter schema:

```json
{
  "annual_rate": {
    "description": "Nominal annual interest rate in percent",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "balloon_payment": {
    "default": 0,
    "description": "Balloon amount due at maturity",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "compounding_per_year": {
    "default": 12,
    "description": "Compounding frequency per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "future_value": {
    "default": 0,
    "description": "Target future value after final payment",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "interest_only_periods": {
    "default": 0,
    "description": "Number of interest-only payment periods at the start",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "payments_per_year": {
    "default": 12,
    "description": "Payment frequency per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "principal": {
    "description": "Loan principal amount",
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "years": {
    "description": "Loan term in years",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  }
}
```

## `calculate_term`

Action slug: `calculate-term`

Price: `5` credits

Calculate the number of periods and years required to pay off a loan given principal, rate, and payment amount.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `annual_rate` | `number` | yes | Nominal annual interest rate in percent |
| `compounding_per_year` | `integer` | no | Compounding frequency per year |
| `payment_amount` | `number` | yes | Periodic payment amount |
| `payments_per_year` | `integer` | no | Payment frequency per year |
| `principal` | `number` | yes | Loan principal |

Sample parameters:

```json
{
  "annual_rate": 0,
  "compounding_per_year": 12,
  "payment_amount": 0,
  "payments_per_year": 12,
  "principal": 0
}
```

Generated JSON parameter schema:

```json
{
  "annual_rate": {
    "description": "Nominal annual interest rate in percent",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "compounding_per_year": {
    "default": 12,
    "description": "Compounding frequency per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "payment_amount": {
    "description": "Periodic payment amount",
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "payments_per_year": {
    "default": 12,
    "description": "Payment frequency per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "principal": {
    "description": "Loan principal",
    "minimum": 0,
    "required": true,
    "type": "number"
  }
}
```

## `compare_loans`

Action slug: `compare-loans`

Price: `5` credits

Compare multiple loan scenarios side-by-side and rank by selected metric (lowest payment, lowest interest, or lowest total cost).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `compare_scenarios` | `array` | yes | Loan scenarios to compare (minimum 2 required) |
| `comparison_metric` | `string` | no | How to rank scenarios |

Sample parameters:

```json
{
  "compare_scenarios": [
    {
      "annual_rate": 0,
      "balloon_payment": 0,
      "compounding_per_year": 12,
      "extra_payment": 0,
      "interest_only_periods": 0,
      "name": "example name",
      "payments_per_year": 12,
      "principal": 0
    }
  ],
  "comparison_metric": "lowest_total_cost"
}
```

Generated JSON parameter schema:

```json
{
  "compare_scenarios": {
    "description": "Loan scenarios to compare (minimum 2 required)",
    "items": {
      "properties": {
        "annual_rate": {
          "description": "Annual rate in percent",
          "maximum": 100,
          "minimum": 0,
          "required": true,
          "type": "number"
        },
        "balloon_payment": {
          "default": 0,
          "description": "Balloon due at maturity",
          "minimum": 0,
          "required": false,
          "type": "number"
        },
        "compounding_per_year": {
          "default": 12,
          "description": "Compounding per year",
          "maximum": 365,
          "minimum": 1,
          "required": false,
          "type": "integer"
        },
        "extra_payment": {
          "default": 0,
          "description": "Recurring extra principal per payment",
          "minimum": 0,
          "required": false,
          "type": "number"
        },
        "interest_only_periods": {
          "default": 0,
          "description": "Interest-only period count",
          "minimum": 0,
          "required": false,
          "type": "integer"
        },
        "name": {
          "description": "Scenario label",
          "required": true,
          "type": "string"
        },
        "payments_per_year": {
          "default": 12,
          "description": "Payments per year",
          "maximum": 365,
          "minimum": 1,
          "required": false,
          "type": "integer"
        },
        "principal": {
          "description": "Loan principal",
          "minimum": 0,
          "required": true,
          "type": "number"
        },
        "years": {
          "description": "Term in years",
          "maximum": 100,
          "minimum": 0,
          "required": true,
          "type": "number"
        }
      },
      "type": "object"
    },
    "required": true,
    "type": "array"
  },
  "comparison_metric": {
    "default": "lowest_total_cost",
    "description": "How to rank scenarios",
    "enum": [
      "lowest_payment",
      "lowest_interest",
      "lowest_total_cost"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `compound_interest`

Action slug: `compound-interest`

Price: `5` credits

Calculate compound interest growth over time, optionally with periodic contributions. Supports configurable compounding frequency and contribution timing.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `annual_rate` | `number` | yes | Annual interest rate in percent |
| `compounding_per_year` | `integer` | no | Compounding frequency per year |
| `contribution_frequency_per_year` | `integer` | no | How often contributions are made per year |
| `contribution_timing` | `string` | no | Whether contribution is made at period end or beginning |
| `periodic_contribution` | `number` | no | Amount added each contribution period |
| `principal` | `number` | yes | Initial principal amount |
| `years` | `number` | yes | Investment duration in years |

Sample parameters:

```json
{
  "annual_rate": 0,
  "compounding_per_year": 12,
  "contribution_frequency_per_year": 12,
  "contribution_timing": "end",
  "periodic_contribution": 0,
  "principal": 0,
  "years": 0
}
```

Generated JSON parameter schema:

```json
{
  "annual_rate": {
    "description": "Annual interest rate in percent",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "compounding_per_year": {
    "default": 12,
    "description": "Compounding frequency per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "contribution_frequency_per_year": {
    "default": 12,
    "description": "How often contributions are made per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "contribution_timing": {
    "default": "end",
    "description": "Whether contribution is made at period end or beginning",
    "enum": [
      "end",
      "beginning"
    ],
    "required": false,
    "type": "string"
  },
  "periodic_contribution": {
    "default": 0,
    "description": "Amount added each contribution period",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "principal": {
    "description": "Initial principal amount",
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "years": {
    "description": "Investment duration in years",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  }
}
```

## `payoff_acceleration`

Action slug: `payoff-acceleration`

Price: `5` credits

Model interest and term savings from recurring and one-time extra payments by comparing baseline vs accelerated payoff scenarios.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `annual_rate` | `number` | yes | Nominal annual interest rate in percent |
| `balloon_payment` | `number` | no | Balloon due at maturity |
| `compounding_per_year` | `integer` | no | Compounding frequency per year |
| `extra_payment` | `number` | no | Recurring extra principal each period |
| `extra_payment_start_period` | `integer` | no | Period to begin recurring extra payments |
| `future_value` | `number` | no | Target future value |
| `interest_only_periods` | `integer` | no | Interest-only period count |
| `one_time_extra_payments` | `array` | no | One-time extra payments |
| `payments_per_year` | `integer` | no | Payment frequency per year |
| `principal` | `number` | yes | Loan principal |
| `start_date` | `string` | no | Optional start date in YYYY-MM-DD format |
| `years` | `number` | yes | Original loan term in years |

Sample parameters:

```json
{
  "annual_rate": 0,
  "balloon_payment": 0,
  "compounding_per_year": 12,
  "extra_payment": 0,
  "extra_payment_start_period": 1,
  "future_value": 0,
  "interest_only_periods": 0,
  "one_time_extra_payments": [
    {
      "amount": 0,
      "period": 1
    }
  ]
}
```

Generated JSON parameter schema:

```json
{
  "annual_rate": {
    "description": "Nominal annual interest rate in percent",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "balloon_payment": {
    "default": 0,
    "description": "Balloon due at maturity",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "compounding_per_year": {
    "default": 12,
    "description": "Compounding frequency per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "extra_payment": {
    "default": 0,
    "description": "Recurring extra principal each period",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "extra_payment_start_period": {
    "default": 1,
    "description": "Period to begin recurring extra payments",
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "future_value": {
    "default": 0,
    "description": "Target future value",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "interest_only_periods": {
    "default": 0,
    "description": "Interest-only period count",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "one_time_extra_payments": {
    "description": "One-time extra payments",
    "items": {
      "properties": {
        "amount": {
          "description": "Extra principal payment amount",
          "minimum": 0,
          "required": true,
          "type": "number"
        },
        "period": {
          "description": "Payment period index (1-based)",
          "minimum": 1,
          "required": true,
          "type": "integer"
        }
      },
      "type": "object"
    },
    "required": false,
    "type": "array"
  },
  "payments_per_year": {
    "default": 12,
    "description": "Payment frequency per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "principal": {
    "description": "Loan principal",
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "start_date": {
    "description": "Optional start date in YYYY-MM-DD format",
    "required": false,
    "type": "string"
  },
  "years": {
    "description": "Original loan term in years",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  }
}
```

## `rate_conversion`

Action slug: `rate-conversion`

Price: `5` credits

Convert a nominal annual percentage rate (APR) into effective annual, payment-period, and daily effective rates.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `annual_rate` | `number` | yes | Nominal annual interest rate in percent |
| `compounding_per_year` | `integer` | no | Compounding frequency per year |
| `payments_per_year` | `integer` | no | Payment frequency per year |

Sample parameters:

```json
{
  "annual_rate": 0,
  "compounding_per_year": 12,
  "payments_per_year": 12
}
```

Generated JSON parameter schema:

```json
{
  "annual_rate": {
    "description": "Nominal annual interest rate in percent",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "compounding_per_year": {
    "default": 12,
    "description": "Compounding frequency per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "payments_per_year": {
    "default": 12,
    "description": "Payment frequency per year",
    "maximum": 365,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `refinance_break_even`

Action slug: `refinance-break-even`

Price: `5` credits

Estimate payment savings, break-even period, and net lifetime benefit of refinancing a loan.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `closing_costs` | `number` | yes | Refinance closing costs |
| `current_balance` | `number` | yes | Current remaining loan balance |
| `current_payment` | `number` | no | Current monthly payment (if omitted, calculated automatically from balance/rate/term) |
| `current_rate` | `number` | yes | Current annual interest rate in percent |
| `current_remaining_term_months` | `integer` | yes | Remaining months on current loan |
| `new_rate` | `number` | yes | New annual interest rate in percent |
| `new_term_months` | `integer` | yes | New loan term in months |

Sample parameters:

```json
{
  "closing_costs": 0,
  "current_balance": 0,
  "current_payment": 0,
  "current_rate": 0,
  "current_remaining_term_months": 1,
  "new_rate": 0,
  "new_term_months": 1
}
```

Generated JSON parameter schema:

```json
{
  "closing_costs": {
    "description": "Refinance closing costs",
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "current_balance": {
    "description": "Current remaining loan balance",
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "current_payment": {
    "description": "Current monthly payment (if omitted, calculated automatically from balance/rate/term)",
    "minimum": 0,
    "required": false,
    "type": "number"
  },
  "current_rate": {
    "description": "Current annual interest rate in percent",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "current_remaining_term_months": {
    "description": "Remaining months on current loan",
    "maximum": 1200,
    "minimum": 1,
    "required": true,
    "type": "integer"
  },
  "new_rate": {
    "description": "New annual interest rate in percent",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "new_term_months": {
    "description": "New loan term in months",
    "maximum": 1200,
    "minimum": 1,
    "required": true,
    "type": "integer"
  }
}
```

## `simple_interest`

Action slug: `simple-interest`

Price: `5` credits

Calculate simple (non-compounded) interest totals for a given principal, rate, and duration.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `annual_rate` | `number` | yes | Annual interest rate in percent |
| `principal` | `number` | yes | Principal amount |
| `years` | `number` | yes | Duration in years |

Sample parameters:

```json
{
  "annual_rate": 0,
  "principal": 0,
  "years": 0
}
```

Generated JSON parameter schema:

```json
{
  "annual_rate": {
    "description": "Annual interest rate in percent",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "principal": {
    "description": "Principal amount",
    "minimum": 0,
    "required": true,
    "type": "number"
  },
  "years": {
    "description": "Duration in years",
    "maximum": 100,
    "minimum": 0,
    "required": true,
    "type": "number"
  }
}
```
