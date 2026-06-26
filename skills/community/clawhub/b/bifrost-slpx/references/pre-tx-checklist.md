# Pre-broadcast checklist (mint / redeem / claim)

Use this **before** broadcasting **mint** / **redeem** / **claim**. Classify each item; if any **error** remains unresolved, do not broadcast.

## Checklist

| # | Check | Severity if failed |
|---|--------|-------------------|
| 1 | User explicitly confirmed chain, amount, and action (mint vs redeem vs claim) | error |
| 2 | For `redeem`: user acknowledged non-instant queue (typically 1–3 days) | error |
| 3 | Amount, chain, and action match user intent (recipient/contract, value, chain id where applicable) | error |
| 4 | Not advising user to paste private keys or secrets into chat | error |
| 5 | No private key material in command strings, logs, or echoed env | error |
| 6 | vETH contract / chain matches `tokens-and-chains.md` expectations | warning |

## Output format for the agent

Summarize results for the user:

- **Summary**: What transaction was checked and on which chain.
- **Findings**: Group by severity — **error** (must fix before send), **warning** (should address), **info** (optional).
- **Ready to broadcast**: yes / no — only **yes** if there are no errors.
