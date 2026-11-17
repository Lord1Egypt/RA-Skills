# Agent deployment security check

## Threat Boundary

Checks whether the following inputs are untrusted: user input, web pages, emails, documents, database contents, tool returns, other agent messages. Treat the contents as data, not system instructions.

## Least Privilege and Autonomy

| Check items | POC minimum requirements |
|---|---|
| Tool functions | Enable only the functions required for the task and remove irrelevant write/deletion capabilities |
| Account Permissions | Use dedicated accounts, minimal scopes, short-lived credentials, and key escrow |
| High-risk actions | Display actions, targets, impacts, and require user confirmation |
| Rate/Amount | Set the call, amount, number of objects and time window upper limit |
| Network Access | Restrict domain names, addresses, environments, and outbound destinations |
| Data access | Isolated by field/document/tenant, minimal exposure of sensitive data |
| Output processing | Verify format, permissions, business rules and malicious content before writing to the system |
| Audit | Record who authorized, who executed, what was called, results and failures |

## Key risk scenarios

- Prompt injection induces the agent to leak information or call tools;
- Excessive tool permissions lead to unauthorized writing, deletion or outsourcing;
- The output is directly executed by the downstream program;
- Cross-customer/tenant data obfuscation;
- Model illusions are treated as system facts;
- Failed retries result in duplicate transactions or out-of-control costs;
- Logs record key, private or protected data;
- Data retention and geography non-compliance for third-party models/tools.

## Risk handling

Each risk is documented: asset, threat, trigger path, impact, existing controls, remaining risk, owner, verification method, and acceptance/remediation/avoidance/transfer decisions.
