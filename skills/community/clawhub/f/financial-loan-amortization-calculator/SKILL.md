---
name: financial-loan-amortization-calculator
description: "Financial Loan Amortization Calculator: Use this tool for any loan math or mortgage calculation. Use when an agent needs financial loan amortization calculator, financial loan calculator, mortgage payment planning, auto loan payment estimation, amortization schedule download, debt payoff acceleration analysis, affordability analysis, annual income through AgentPMT-hosted remote tool calls. Discovery terms: financial loan amortization calculator, financial loan calculator."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/financial-loan-calculator
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/financial-loan-calculator"}}
---
# Financial Loan Amortization Calculator

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Full-featured financial loan calculator supporting 11 operations: payment calculation, principal estimation, term calculation, simple and compound interest, amortization schedules with CSV export, side-by-side loan comparison, DTI-based affordability analysis, refinance break-even evaluation, payoff acceleration modeling with extra and lump-sum payments, and APR-to-effective-rate conversion. Handles mortgages, auto loans, personal loans, and investment growth scenarios with configurable compounding, payment frequencies, interest-only periods, and balloon terms.

## Product Instructions
### Financial Loan Calculator - Tool Instructions

#### Overview
Comprehensive financial loan calculator supporting mortgage, auto, and personal loan calculations. Provides 11 actions covering payment computation, principal calculation, term determination, simple and compound interest, full amortization schedules with CSV export, multi-scenario loan comparison, home affordability analysis, refinance break-even analysis, payoff acceleration modeling, and interest rate conversion. All calculations support configurable payment and compounding frequencies, interest-only periods, balloon payments, and extra payments.

---

#### Actions

##### calculate_payment
Compute the periodic payment for an amortizing loan. Supports interest-only periods and balloon payments.

**Required Parameters:**
- `action` (string): `"calculate_payment"`
- `principal` (number, >0): Loan principal amount
- `annual_rate` (number, 0-100): Nominal annual interest rate in percent
- `years` (number, >0): Loan term in years

**Optional Parameters:**
- `payments_per_year` (integer, default: 12, range: 1-365): Payment frequency per year
- `compounding_per_year` (integer, default: 12, range: 1-365): Compounding frequency per year
- `future_value` (number, default: 0): Target future value after final payment
- `balloon_payment` (number, default: 0): Balloon amount due at maturity
- `interest_only_periods` (integer, default: 0): Number of interest-only payment periods at the start

**Example:**
```json
{
  "action": "calculate_payment",
  "principal": 350000,
  "annual_rate": 6.25,
  "years": 30,
  "payments_per_year": 12,
  "compounding_per_year": 12
}
```

**Response fields:** `payment_per_period`, `interest_only_payment_per_period`, `periodic_rate_percent`, `total_periods`, `amortizing_periods`

---

##### calculate_loan_principal
Calculate the maximum loan principal supported by a given payment amount.

**Required Parameters:**
- `action` (string): `"calculate_loan_principal"`
- `payment_amount` (number, >0): Periodic payment amount
- `annual_rate` (number, 0-100): Nominal annual interest rate in percent
- `years` (number, >0) or `target_periods` (integer, >=1): Loan term (one or both required)

**Optional Parameters:**
- `payments_per_year` (integer, default: 12)
- `compounding_per_year` (integer, default: 12)
- `future_value` (number, default: 0)
- `balloon_payment` (number, default: 0)

**Example:**
```json
{
  "action": "calculate_loan_principal",
  "payment_amount": 2200,
  "annual_rate": 6.1,
  "years": 30
}
```

**Response fields:** `max_principal`, `periods`, `periodic_rate_percent`

---

##### calculate_term
Calculate the number of periods required to pay off a loan given principal, rate, and payment.

**Required Parameters:**
- `action` (string): `"calculate_term"`
- `principal` (number, >0): Loan principal
- `annual_rate` (number, 0-100): Nominal annual rate in percent
- `payment_amount` (number, >0): Periodic payment amount

**Optional Parameters:**
- `payments_per_year` (integer, default: 12)
- `compounding_per_year` (integer, default: 12)

**Example:**
```json
{
  "action": "calculate_term",
  "principal": 42000,
  "annual_rate": 7.9,
  "payment_amount": 850
}
```

**Response fields:** `required_periods`, `required_years`, `periodic_rate_percent`

Note: Returns an error if the payment amount is too low to amortize the loan (i.e., less than or equal to the interest-only payment).

---

##### simple_interest
Calculate simple (non-compounded) interest totals.

**Required Parameters:**
- `action` (string): `"simple_interest"`
- `principal` (number, >0): Principal amount
- `annual_rate` (number, 0-100): Annual interest rate in percent
- `years` (number, >0): Duration in years

**Example:**
```json
{
  "action": "simple_interest",
  "principal": 10000,
  "annual_rate": 5,
  "years": 3
}
```

**Response fields:** `principal`, `interest`, `total_amount`, `annual_rate_percent`, `years`

---

##### compound_interest
Calculate compound interest growth, optionally with periodic contributions.

**Required Parameters:**
- `action` (string): `"compound_interest"`
- `principal` (number, >0): Initial principal amount
- `annual_rate` (number, 0-100): Annual interest rate in percent
- `years` (number, >0): Investment duration in years

**Optional Parameters:**
- `compounding_per_year` (integer, default: 12): Compounding frequency
- `periodic_contribution` (number, default: 0): Amount added each contribution period
- `contribution_frequency_per_year` (integer, default: 12, range: 1-365): How often contributions are made
- `contribution_timing` (string, default: `"end"`): `"end"` or `"beginning"` of each period

**Example:**
```json
{
  "action": "compound_interest",
  "principal": 15000,
  "annual_rate": 7,
  "years": 10,
  "compounding_per_year": 12,
  "periodic_contribution": 300,
  "contribution_frequency_per_year": 12,
  "contribution_timing": "end"
}
```

**Response fields:** `future_value`, `principal_growth_component`, `contribution_growth_component`, `total_contributions`, `interest_earned`, `effective_annual_rate_percent`, `contribution_rate_percent`

---

##### amortization_schedule
Build a full amortization table with support for extra payments and optional CSV file export.

**Required Parameters:**
- `action` (string): `"amortization_schedule"`
- `principal` (number, >0): Loan principal
- `annual_rate` (number, 0-100): Nominal annual rate in percent
- `years` (number, >0): Loan term in years

**Optional Parameters:**
- `payments_per_year` (integer, default: 12)
- `compounding_per_year` (integer, default: 12)
- `future_value` (number, default: 0)
- `balloon_payment` (number, default: 0)
- `interest_only_periods` (integer, default: 0)
- `extra_payment` (number, default: 0): Recurring extra principal each period
- `extra_payment_start_period` (integer, default: 1): Period to begin recurring extra payments
- `one_time_extra_payments` (array): List of one-time extra payments, each with `period` (integer, >=1) and `amount` (number, >0)
- `start_date` (string): Schedule start date in `YYYY-MM-DD` format; adds date column to each row
- `return_schedule` (boolean, default: true): Include schedule rows in response
- `max_schedule_rows` (integer, default: 5000, range: 1-50000): Maximum rows to return
- `store_schedule_file` (boolean, default: false): Upload schedule as CSV to cloud storage
- `expiration_days` (integer, default: 7, range: 1-7): Cloud file expiration in days

**Example:**
```json
{
  "action": "amortization_schedule",
  "principal": 280000,
  "annual_rate": 6.4,
  "years": 30,
  "extra_payment": 200,
  "store_schedule_file": true,
  "expiration_days": 7
}
```

**Response fields:** `summary` (object with principal, rates, periods, payment, totals, paid_off_early flag), `schedule` (array of period rows with payment/principal/interest/extra_payment/balance/cumulative fields), `schedule_truncated` (boolean). When `store_schedule_file` is true: `schedule_file` with `file_id`, `signed_url`, `expiration_date`, `size_bytes`.

Each schedule row contains: `period`, `date` (if start_date provided), `payment`, `principal`, `interest`, `extra_payment`, `balance`, `cumulative_interest`, `cumulative_paid`.

---

##### compare_loans
Compare multiple loan scenarios side-by-side and rank by a selected metric.

**Required Parameters:**
- `action` (string): `"compare_loans"`
- `compare_scenarios` (array, minimum 2 items): Each scenario object requires:
  - `name` (string): Scenario label
  - `principal` (number, >0): Loan principal
  - `annual_rate` (number, 0-100): Annual rate in percent
  - `years` (number, >0): Term in years

**Optional per-scenario fields:** `payments_per_year` (default: 12), `compounding_per_year` (default: 12), `extra_payment` (default: 0), `balloon_payment` (default: 0), `interest_only_periods` (default: 0)

**Optional Parameters:**
- `comparison_metric` (string, default: `"lowest_total_cost"`): Ranking method. One of: `"lowest_payment"`, `"lowest_interest"`, `"lowest_total_cost"`

**Example:**
```json
{
  "action": "compare_loans",
  "comparison_metric": "lowest_total_cost",
  "compare_scenarios": [
    {"name": "30Y Fixed", "principal": 320000, "annual_rate": 6.5, "years": 30},
    {"name": "15Y Fixed", "principal": 320000, "annual_rate": 5.8, "years": 15}
  ]
}
```

**Response fields:** `comparison_metric`, `ranked_scenarios` (array sorted by metric, each with name/principal/annual_rate_percent/years/payment_per_period/total_interest/total_paid/actual_periods), `best_scenario`

---

##### affordability_analysis
Estimate affordable monthly payment, maximum loan principal, and maximum home price based on income and debts.

**Required Parameters:**
- `action` (string): `"affordability_analysis"`
- `annual_income` (number, >0): Gross annual income
- `annual_rate` (number, 0-100): Expected mortgage rate in percent
- `years` (number, >0): Loan term in years

**Optional Parameters:**
- `monthly_debts` (number, default: 0): Recurring monthly debt obligations
- `monthly_expenses` (number, default: 0): Additional recurring monthly expenses
- `front_end_ratio` (number, default: 0.28, range: 0-1): Maximum housing expense ratio
- `back_end_ratio` (number, default: 0.36, range: 0-1): Maximum total debt ratio
- `property_tax_monthly` (number, default: 0)
- `insurance_monthly` (number, default: 0)
- `hoa_monthly` (number, default: 0)
- `down_payment` (number, default: 0): Down payment amount (added to max principal for max home price)
- `payments_per_year` (integer, default: 12)
- `compounding_per_year` (integer, default: 12)

**Example:**
```json
{
  "action": "affordability_analysis",
  "annual_income": 145000,
  "monthly_debts": 850,
  "annual_rate": 6.2,
  "years": 30,
  "down_payment": 60000
}
```

**Response fields:** `monthly_income`, `front_end_limit`, `back_end_limit`, `gross_housing_budget`, `net_housing_budget_for_pi`, `max_loan_principal`, `max_home_price_with_down_payment`, `assumptions`

Note: Returns an error if deductions (taxes, insurance, HOA, expenses) exceed the available housing budget.

---

##### refinance_break_even
Estimate payment savings, break-even period, and net lifetime benefit of refinancing.

**Required Parameters:**
- `action` (string): `"refinance_break_even"`
- `current_balance` (number, >0): Current remaining loan balance
- `current_rate` (number, 0-100): Current annual rate in percent
- `current_remaining_term_months` (integer, >=1): Remaining months on current loan
- `new_rate` (number, 0-100): New annual rate in percent
- `new_term_months` (integer, >=1): New loan term in months
- `closing_costs` (number, >=0): Refinance closing costs

**Optional Parameters:**
- `current_payment` (number, >0): Current monthly payment. If omitted, calculated automatically from balance/rate/term.

**Example:**
```json
{
  "action": "refinance_break_even",
  "current_balance": 295000,
  "current_rate": 7.1,
  "current_remaining_term_months": 312,
  "new_rate": 6.1,
  "new_term_months": 360,
  "closing_costs": 5500
}
```

**Response fields:** `current_payment`, `new_payment`, `monthly_savings`, `closing_costs`, `break_even_months`, `current_remaining_interest`, `new_total_interest`, `interest_savings`, `lifetime_net_benefit_after_costs`, `recommendation` (`"favorable"` or `"not_favorable"`)

The recommendation is `"favorable"` when break-even occurs within the remaining term and the lifetime net benefit is positive.

---

##### payoff_acceleration
Model interest and term savings from recurring and one-time extra payments by comparing baseline vs accelerated scenarios.

**Required Parameters:**
- `action` (string): `"payoff_acceleration"`
- `principal` (number, >0): Loan principal
- `annual_rate` (number, 0-100): Nominal annual rate in percent
- `years` (number, >0): Original loan term in years

**Optional Parameters:**
- `payments_per_year` (integer, default: 12)
- `compounding_per_year` (integer, default: 12)
- `extra_payment` (number, default: 0): Recurring extra principal each period
- `extra_payment_start_period` (integer, default: 1): Period to begin extra payments
- `one_time_extra_payments` (array): One-time extra payments, each with `period` and `amount`
- `future_value` (number, default: 0)
- `balloon_payment` (number, default: 0)
- `interest_only_periods` (integer, default: 0)
- `start_date` (string): Optional start date in `YYYY-MM-DD`

**Example:**
```json
{
  "action": "payoff_acceleration",
  "principal": 250000,
  "annual_rate": 6.0,
  "years": 30,
  "extra_payment": 300,
  "one_time_extra_payments": [{"period": 24, "amount": 5000}]
}
```

**Response fields:** `baseline` (summary without extra payments), `accelerated` (summary with extra payments), `periods_saved`, `years_saved`, `interest_saved`

---

##### rate_conversion
Convert a nominal annual percentage rate (APR) into effective annual and payment-period rates.

**Required Parameters:**
- `action` (string): `"rate_conversion"`
- `annual_rate` (number, 0-100): Nominal annual rate in percent

**Optional Parameters:**
- `compounding_per_year` (integer, default: 12): Compounding frequency
- `payments_per_year` (integer, default: 12): Payment frequency

**Example:**
```json
{
  "action": "rate_conversion",
  "annual_rate": 8.0,
  "compounding_per_year": 12,
  "payments_per_year": 26
}
```

**Response fields:** `nominal_annual_rate_percent`, `effective_annual_rate_percent`, `payment_period_rate_percent`, `daily_effective_rate_percent`, `assumptions`

---

#### Workflows

1. **Home Purchase Planning** - Use `affordability_analysis` to determine budget, then `calculate_payment` to see exact payments, then `amortization_schedule` with `store_schedule_file: true` for a downloadable payment plan.
2. **Loan Comparison Shopping** - Use `compare_loans` with multiple scenarios (e.g., 15Y vs 30Y, different rates) ranked by `lowest_total_cost` or `lowest_payment`.
3. **Refinance Decision** - Use `refinance_break_even` to see if refinancing makes sense, check `recommendation` field and `break_even_months`.
4. **Early Payoff Strategy** - Use `payoff_acceleration` to model the impact of extra payments on term and interest savings.
5. **Investment Growth Projection** - Use `compound_interest` with `periodic_contribution` to project savings/investment growth over time.
6. **Rate Analysis** - Use `rate_conversion` to compare APR vs effective rates across different compounding frequencies.

---

#### Notes

- All monetary results are rounded to 2 decimal places. Rate percentages are rounded to 6 decimal places.
- The `interest_only_periods` value must be less than the total number of payment periods.
- When `compounding_per_year` differs from `payments_per_year`, the tool correctly converts the nominal rate to the appropriate periodic rate using the effective rate method.
- Amortization schedules can be very large. Use `max_schedule_rows` to cap output size (default 5000, max 50000). If truncated, `schedule_truncated` is true.
- Set `return_schedule: false` to get only the summary without period-by-period rows.
- CSV file uploads via `store_schedule_file` expire in 1-7 days (configurable via `expiration_days`).
- The `calculate_term` action will error if the payment is too low to amortize the loan (payment <= interest-only amount).
- For `refinance_break_even`, if `current_payment` is not provided, it is automatically calculated from the current balance, rate, and remaining term.
- The `compare_loans` action requires at least 2 scenarios.
- All date fields use `YYYY-MM-DD` format. Invalid formats return a validation error.

## When To Use
- Use this skill for `Financial Loan Amortization Calculator` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: financial loan amortization calculator, financial loan calculator, mortgage payment planning, auto loan payment estimation, amortization schedule download, debt payoff acceleration analysis, affordability analysis, annual income.
- Supported action names: `affordability_analysis`, `amortization_schedule`, `calculate_loan_principal`, `calculate_payment`, `calculate_term`, `compare_loans`, `compound_interest`, `payoff_acceleration`, `rate_conversion`, `refinance_break_even`, `simple_interest`.

## Use Cases
- Mortgage payment planning
- Auto loan payment estimation
- Amortization schedule download
- Debt payoff acceleration analysis
- Refinance break-even evaluation
- Simple and compound interest projection
- Debt-to-income affordability checks
- Balloon payment scenario modeling
- Interest-only period planning
- Loan comparison analysis

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `11`.
x402 availability: not enabled for this product.

- `affordability_analysis` (action slug: `affordability-analysis`): Estimate affordable monthly payment, maximum loan principal, and maximum home price based on income, debts, and DTI ratios. Price: `5` credits. Parameters: `annual_income`, `annual_rate`, `back_end_ratio`, `compounding_per_year`, `down_payment`, `front_end_ratio`, `hoa_monthly`, `insurance_monthly`, plus 5 more.
- `amortization_schedule` (action slug: `amortization-schedule`): Build a full amortization table with support for extra payments, one-time lump sums, interest-only periods, balloon payments, and optional CSV file export to cloud storage. Price: `5` credits. Parameters: `annual_rate`, `balloon_payment`, `compounding_per_year`, `expiration_days`, `extra_payment`, `extra_payment_start_period`, `future_value`, `interest_only_periods`, plus 8 more.
- `calculate_loan_principal` (action slug: `calculate-loan-principal`): Calculate the maximum loan principal supported by a given periodic payment amount. Price: `5` credits. Parameters: `annual_rate`, `balloon_payment`, `compounding_per_year`, `future_value`, `payment_amount`, `payments_per_year`, `target_periods`, `years`.
- `calculate_payment` (action slug: `calculate-payment`): Compute the periodic payment for an amortizing loan. Supports interest-only periods, balloon payments, and configurable payment/compounding frequencies. Price: `5` credits. Parameters: `annual_rate`, `balloon_payment`, `compounding_per_year`, `future_value`, `interest_only_periods`, `payments_per_year`, `principal`, `years`.
- `calculate_term` (action slug: `calculate-term`): Calculate the number of periods and years required to pay off a loan given principal, rate, and payment amount. Price: `5` credits. Parameters: `annual_rate`, `compounding_per_year`, `payment_amount`, `payments_per_year`, `principal`.
- `compare_loans` (action slug: `compare-loans`): Compare multiple loan scenarios side-by-side and rank by selected metric (lowest payment, lowest interest, or lowest total cost). Price: `5` credits. Parameters: `compare_scenarios`, `comparison_metric`.
- `compound_interest` (action slug: `compound-interest`): Calculate compound interest growth over time, optionally with periodic contributions. Supports configurable compounding frequency and contribution timing. Price: `5` credits. Parameters: `annual_rate`, `compounding_per_year`, `contribution_frequency_per_year`, `contribution_timing`, `periodic_contribution`, `principal`, `years`.
- `payoff_acceleration` (action slug: `payoff-acceleration`): Model interest and term savings from recurring and one-time extra payments by comparing baseline vs accelerated payoff scenarios. Price: `5` credits. Parameters: `annual_rate`, `balloon_payment`, `compounding_per_year`, `extra_payment`, `extra_payment_start_period`, `future_value`, `interest_only_periods`, `one_time_extra_payments`, plus 4 more.
- `rate_conversion` (action slug: `rate-conversion`): Convert a nominal annual percentage rate (APR) into effective annual, payment-period, and daily effective rates. Price: `5` credits. Parameters: `annual_rate`, `compounding_per_year`, `payments_per_year`.
- `refinance_break_even` (action slug: `refinance-break-even`): Estimate payment savings, break-even period, and net lifetime benefit of refinancing a loan. Price: `5` credits. Parameters: `closing_costs`, `current_balance`, `current_payment`, `current_rate`, `current_remaining_term_months`, `new_rate`, `new_term_months`.
- `simple_interest` (action slug: `simple-interest`): Calculate simple (non-compounded) interest totals for a given principal, rate, and duration. Price: `5` credits. Parameters: `annual_rate`, `principal`, `years`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "financial-loan-calculator"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "financial-loan-calculator"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "financial-loan-calculator"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "financial-loan-calculator"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "financial-loan-calculator"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "financial-loan-calculator"
  }
}
```

## Call This Tool
Product slug: `financial-loan-calculator`

Marketplace page: https://www.agentpmt.com/marketplace/financial-loan-calculator

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
    "name": "Financial-Loan-Amortization-Calculator",
    "arguments": {
      "action": "affordability_analysis",
      "annual_income": 0,
      "annual_rate": 0,
      "back_end_ratio": 0.36,
      "compounding_per_year": 12,
      "down_payment": 0,
      "front_end_ratio": 0.28,
      "hoa_monthly": 0,
      "insurance_monthly": 0
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "financial-loan-calculator",
  "parameters": {
    "action": "affordability_analysis",
    "annual_income": 0,
    "annual_rate": 0,
    "back_end_ratio": 0.36,
    "compounding_per_year": 12,
    "down_payment": 0,
    "front_end_ratio": 0.28,
    "hoa_monthly": 0,
    "insurance_monthly": 0
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `affordability_analysis` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/financial-loan-calculator
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
