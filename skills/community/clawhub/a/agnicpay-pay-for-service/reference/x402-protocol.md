# x402 Protocol Reference

## Arguments & Options

| Option                  | Description                                        |
| ----------------------- | -------------------------------------------------- |
| `<url>`                 | Full URL of the x402-enabled API endpoint          |
| `-X, --method <method>` | HTTP method (default: GET)                         |
| `-d, --data <json>`     | Request body as JSON string                        |
| `-q, --query <params>`  | Query parameters as JSON string                    |
| `-h, --headers <json>`  | Custom HTTP headers as JSON string                 |
| `--max-amount <amount>` | Max payment in USDC atomic units (1000000 = $1.00) |
| `--correlation-id <id>` | Group related operations                           |
| `--json`                | Output as JSON                                     |

## USDC Amounts

x402 uses USDC atomic units (6 decimals):

| Atomic Units | USD   |
| ------------ | ----- |
| 1000000      | $1.00 |
| 100000       | $0.10 |
| 50000        | $0.05 |
| 10000        | $0.01 |

## Input Validation

Before constructing the command, validate all user-provided values:

- **url**: Must be a valid HTTPS URL (`^https://[^\s;|&]+$`). Reject URLs containing spaces, semicolons, pipes, or backticks.
- **method**: Must be one of GET, POST, PUT, DELETE, PATCH (case-insensitive).
- **data**: Must be valid JSON. Parse it first; reject if parsing fails.
- **max-amount**: Must be a positive integer (`^\d+$`).

Do not pass unvalidated user input into the command.
